import unittest
import mock
from extractor.crawlers.linkedin import LinkedInCrawler
from extractor.config import Config


class LinkedInCrawlerTest(unittest.TestCase):

    def setUp(self):
        self.conf = Config()

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

if __name__ == '__main__':
    unittest.main()
