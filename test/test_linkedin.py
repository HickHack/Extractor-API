import unittest
import mock
from bs4 import BeautifulSoup
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
    def test_request_failure_with_data_POST(self, mock_urllib):
        reference = LinkedInCrawler('', '')

        reference.opener = mock_urllib.request.build_opener
        mock_urllib.request.build_opener.open.side_effects = Exception('Some Exception')

        reference.request('some url')

        mock_urllib.request.build_opener.open.assert_called_with('some url')
        self.assertRaises(Exception, 'Some Exception')

    @mock.patch.object(LinkedInCrawler, 'request_html')
    def test_load_soup_valid_html(self, mock_load_html):
        reference = LinkedInCrawler('', '')
        mock_load_html.return_value = '<html><head><title>Test</title></head>'

        soup = reference.load_soup('some url', 'some data')

        mock_load_html.assert_called_with('some url', 'some data')
        self.assertIs(BeautifulSoup, type(soup))

    @mock.patch('http.client.HTTPResponse')
    @mock.patch.object(LinkedInCrawler, 'request')
    def test_request_json(self, mock_request, mock_response):
        reference = LinkedInCrawler('', '')

        mock_request.return_value = mock_response
        mock_response.read.return_value = b'{"key": 1024}'
        mock_response.info().get_content_charset.return_value = 'utf-8'

        json = reference.request_json('some url', 'some data')

        mock_request.assert_called_with('some url', 'some data')
        self.assertTrue(mock_response.read.called)
        self.assertDictEqual(json, {'key': 1024})

    @mock.patch('http.client.HTTPResponse')
    @mock.patch.object(LinkedInCrawler, 'request')
    def test_request_json_error(self, mock_request, mock_response):
        reference = LinkedInCrawler('', '')

        mock_request.return_value = mock_response
        mock_response.read.return_value = b'{key: 1024}'
        mock_response.info().get_content_charset.return_value = 'utf-8'

        json = reference.request_json('', '')

        self.assertDictEqual(json, {})
