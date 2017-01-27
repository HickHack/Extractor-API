import unittest
import mock
from extractor.crawlers.linkedin import LinkedInCrawler


class LinkedInCrawlerTest(unittest.TestCase):

    @mock.patch('extractor.crawlers.linkedin.os')
    @mock.patch('extractor.crawlers.linkedin.urllib')
    @mock.patch('extractor.crawlers.linkedin.cookielib')
    def test_configure_opener_file_not_exist(self, mock_cookielib,
                                             mock_urllib, mock_os):
        reference = LinkedInCrawler('', '')
        header = [
            ('User-agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; .NET CLR 1.1.4322)')
        ]

        mock_os.access.return_value = False

        reference.configure_opener()

        self.assertTrue(mock_urllib.request.build_opener.called)
        self.assertTrue(mock_urllib.request.HTTPRedirectHandler.called)
        self.assertTrue(mock_urllib.request.HTTPHandler.called)
        self.assertTrue(mock_urllib.request.HTTPSHandler.called)
        self.assertTrue(mock_urllib.request.HTTPCookieProcessor.called)
        self.assertTrue(mock_urllib.request.HTTPCookieProcessor.called)
        self.assertListEqual(mock_urllib.request.build_opener().addheaders, header)
        self.assertFalse(mock_cookielib.load.called)

    @mock.patch('extractor.crawlers.linkedin.os')
    @mock.patch('extractor.crawlers.linkedin.cookielib')
    def test_configure_opener_file_load(self, mock_cookielib, mock_os):
        reference = LinkedInCrawler('', '')

        mock_os.access.return_value = True

        reference.configure_opener()

        self.assertTrue(mock_os.access.called)
        self.assertTrue(mock_cookielib.MozillaCookieJar.called)

    @mock.patch('extractor.crawlers.linkedin.urllib')
    @mock.patch('extractor.crawlers.linkedin.time')
    def test_request_with_no_data_GET(self, mock_time, mock_urllib):
        reference = LinkedInCrawler('', '')

        reference.opener = mock_urllib.request.build_opener
        mock_urllib.request.build_opener.open.return_value = 'some response'

        response = reference.request('some url')

        mock_urllib.request.build_opener.open.assert_called_with('some url')
        self.assertTrue(mock_time.sleep.called)
        self.assertEqual(response, 'some response')
        self.assertEqual(1, reference.total_requests)

    @mock.patch('extractor.crawlers.linkedin.urllib')
    @mock.patch('extractor.crawlers.linkedin.time')
    def test_request_with_data_POST(self, mock_time, mock_urllib):
        reference = LinkedInCrawler('', '')

        reference.opener = mock_urllib.request.build_opener
        mock_urllib.request.build_opener.open.return_value = 'some response'

        response = reference.request('some url', 'some data')

        mock_urllib.request.build_opener.open.assert_called_with('some url', 'some data')
        self.assertTrue(mock_time.sleep.called)
        self.assertEqual(response, 'some response')
        self.assertEqual(1, reference.total_requests)

    @mock.patch('extractor.crawlers.linkedin.urllib')
    def test_request_with_data_POST(self, mock_urllib):
        reference = LinkedInCrawler('', '')

        reference.opener = mock_urllib.request.build_opener
        mock_urllib.request.build_opener.open.side_effects = Exception('Some Exception')

        reference.request('some url')

        mock_urllib.request.build_opener.open.assert_called_with('some url')
        self.assertRaises(Exception, 'Some Exception')


if __name__ == '__main__':
    unittest.main()
