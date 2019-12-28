import os
import unittest
from pathlib import Path
from unittest import mock

from src.model import ScrapingSetting
from src.scraping_setting_repository import JsonFileScrapingSettingRepository, GoogleSheetsScrapingSettingRepository


class TestJsonFileScrapingSettingRepository(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.sut = JsonFileScrapingSettingRepository()
        self.patcher = mock.patch('src.scraping_setting_repository.config_util.to_resource_file_abs_path')
        self.mock_path = self.patcher.start()

    def tearDown(self):
        super().tearDown()
        self.patcher.stop()

    def test_get_settings_when_resource_then_settings(self):
        self.mock_path.return_value = Path(
            os.path.abspath(os.path.join(__file__, '..', 'resources', 'scraping_settings.json')))
        expected0 = ScrapingSetting('DataMixInformationParser',
                                    'https://datamix.co.jp/news/',
                                    ['https://datamix.co.jp/news/20191009/', 'https://datamix.co.jp/news/3551/'],
                                    1,
                                    'データミックスのお知らせが更新されました [{0[title]}] {0[url]}')
        actual = self.sut.get_settings()

        self.assertEqual(1, len(actual))
        self.assertEqual(expected0, actual[0])

    def test_get_settings_when_resource_not_found_then_raise(self):
        self.mock_path.return_value = Path('not_exists_path')
        with self.assertRaises(FileNotFoundError):
            self.sut.get_settings()

    def test_update_last_article_urls_when_resource_not_found_then_raise(self):
        self.mock_path.return_value = Path('not_exists_path')
        with self.assertRaises(FileNotFoundError):
            self.sut.get_settings()

    # TODO: `update_last_article_urls`メソッドのテスト作成


class TestGoogleSheetsScrapingSettingRepository(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.sut = GoogleSheetsScrapingSettingRepository()

    def tearDown(self):
        pass

    # TODO: テスト作成


if __name__ == '__main__':
    unittest.main()
