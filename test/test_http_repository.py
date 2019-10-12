import http.client
import unittest
from unittest import mock

from src.http_repository import HttpRepository, HttpRepositoryError


class TestHttpRepository(unittest.TestCase):
    TEST_URL = 'https://localhost.com'

    def setUp(self):
        super().setUp()
        self.sut = HttpRepository()
        self.patcher = mock.patch('src.http_repository.urlopen')
        self.mock_urlopen = self.patcher.start()

    def tearDown(self):
        super().tearDown()
        self.patcher.stop()

    def test_fetch_response_text_when_ok_then_return_text(self):
        self.mock_urlopen.return_value.__enter__.return_value.getcode.return_value = 200
        self.mock_urlopen.return_value.__enter__.return_value.info.return_value = http.client.HTTPMessage()
        self.mock_urlopen.return_value.__enter__.return_value.read.return_value = b'<!doctype html>'

        expected = '<!doctype html>'
        actual = self.sut.fetch_response_text(self.TEST_URL)
        self.assertEqual(expected, actual)
        self.assertEqual(1, self.mock_urlopen.call_count)

    def test_fetch_response_text_when_status500_then_raise(self):
        self.mock_urlopen.return_value.__enter__.return_value.getcode.return_value = 500

        with self.assertRaises(HttpRepositoryError):
            self.sut.fetch_response_text(self.TEST_URL)
        self.assertEqual(1, self.mock_urlopen.call_count)

    def test_post_slack_when_ok_then_return_text(self):
        self.mock_urlopen.return_value.__enter__.return_value.getcode.return_value = 200
        self.mock_urlopen.return_value.__enter__.return_value.info.return_value = http.client.HTTPMessage()
        self.mock_urlopen.return_value.__enter__.return_value.read.return_value = b'ok'

        expected = 'ok'
        actual = self.sut.post_slack(self.TEST_URL, 'message')
        self.assertEqual(expected, actual)
        self.assertEqual(1, self.mock_urlopen.call_count)

    def test_post_slack_when_status500_then_raise(self):
        self.mock_urlopen.return_value.__enter__.return_value.getcode.return_value = 500

        with self.assertRaises(HttpRepositoryError):
            self.sut.post_slack(self.TEST_URL, 'message')
        self.assertEqual(1, self.mock_urlopen.call_count)


if __name__ == '__main__':
    unittest.main()
