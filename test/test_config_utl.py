import os
import unittest
from pathlib import Path
from unittest import mock

from src import config_util


# TODO: pathの設定方法が複雑で実装のテストになっていない感もあるので検討、またwindows/mac環境に依存しないようにする
class ConfigUtilScript(unittest.TestCase):
    @mock.patch('src.config_util.to_resource_file_abs_path')
    def test_get_config_when_default_env_return_default_config(self, mock_path):
        mock_path.return_value = Path(os.path.join(os.path.dirname(__file__), 'resources', 'config.ini'))
        actual = config_util.get_config()
        self.assertEqual(['test'], (actual.sections()))
        self.assertEqual([('env', 'default')], (actual.items('test')))

    @mock.patch('src.config_util.to_resource_file_abs_path')
    def test_get_config_when_prod_env_return_prod_config(self, mock_path):
        try:
            os.environ['notification_bot_env'] = 'prod'
            mock_path.return_value = Path(os.path.join(os.path.dirname(__file__), 'resources', 'config_prod.ini'))
            actual = config_util.get_config()
            self.assertEqual(['test'], (actual.sections()))
            self.assertEqual([('env', 'prod')], (actual.items('test')))
        finally:
            if os.getenv('notification_bot_env'):
                del os.environ['notification_bot_env']

    @mock.patch('src.config_util.to_resource_file_abs_path')
    def test_get_config_when_file_not_found_return_raise(self, mock_path):
        mock_path.return_value = Path('not_exists_path')
        with self.assertRaises(FileNotFoundError):
            config_util.get_config()

    def test_to_resource_file_abs_path_when_file_name_return_abs_path(self):
        expected = Path(os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'src', 'resources', 'scraping_settings.json')))
        actual = config_util.to_resource_file_abs_path('scraping_settings.json')
        self.assertEqual(expected, actual)

    def test_to_resource_file_abs_path_when_not_exists_file_name_return_abs_path(self):
        expected = Path(os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'src', 'resources', 'not_exists_file')))
        actual = config_util.to_resource_file_abs_path('not_exists_file')
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
