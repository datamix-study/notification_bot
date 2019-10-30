import json
from abc import ABCMeta, abstractmethod
from typing import List

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from src import config_util
from src.model import ScrapingSetting


class AbstractScrapingSettingRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_settings(self) -> List[ScrapingSetting]:
        raise NotImplementedError()

    @abstractmethod
    def update_last_article_urls(self, parser_name: str, new_article_urls: List[str]) -> ():
        raise NotImplementedError()


class JsonFileScrapingSettingRepository(AbstractScrapingSettingRepository):
    def get_settings(self) -> List[ScrapingSetting]:
        with self._get_json_abs_path().open(mode='r') as f:
            scraping_dict = json.load(f)

        return [self._create_settings(parser_name, setting_dict) for parser_name, setting_dict in scraping_dict.items()]

    def update_last_article_urls(self, parser_name: str, new_article_urls: List[str]) -> ():
        new_setting_dict = {}
        for setting in self.get_settings():
            if setting.parser_name == parser_name:
                setting.last_article_urls = new_article_urls
            new_setting_dict[setting.parser_name] = self._to_dict(setting)

        with self._get_json_abs_path().open(mode='w') as f:
            json.dump(new_setting_dict, f, indent=4, ensure_ascii=False)

    @staticmethod
    def _create_settings(parser_name, setting_dict):
        return ScrapingSetting(parser_name.strip(),
                               setting_dict['access_url'].strip(),
                               [s.strip() for s in setting_dict['last_article_urls']],
                               setting_dict['message_template'].strip())

    @staticmethod
    def _to_dict(setting):
        return {'access_url': setting.access_url,
                'last_article_urls': setting.last_article_urls,
                'message_template': setting.message_template}

    @staticmethod
    def _get_json_abs_path():
        abs_path = config_util.to_resource_file_abs_path('scraping_settings.json')
        if not abs_path.exists():
            raise FileNotFoundError('resource file does not exist: {}'.format(abs_path))
        return abs_path


class GoogleSheetsScrapingSettingRepository(AbstractScrapingSettingRepository):
    _COLUMN_PARSER_NAME = 'A'
    _COLUMN_ACCESS_URL = 'B'
    _COLUMN_LAST_ARTICLE_URLS_ = 'C'
    _COLUMN_MESSAGE_TEMPLATE = 'D'

    _ROW_FIRST_SETTING_VALUE = 2

    def get_settings(self) -> List[ScrapingSetting]:
        settings = []
        for row_number in range(self._ROW_FIRST_SETTING_VALUE, self._open_worksheet().row_count):
            if not self._read_cell(self._COLUMN_PARSER_NAME, row_number):
                break
            settings.append(self._create_settings(row_number))
        return settings

    def update_last_article_urls(self, parser_name: str, new_article_urls: List[str]) -> ():
        for row_number in range(self._ROW_FIRST_SETTING_VALUE, self._open_worksheet().row_count):
            if not self._read_cell(self._COLUMN_PARSER_NAME, row_number):
                raise ScrapingSettingRepositoryError('{} does not match in the parser_name column'.format(parser_name))

            if self._read_cell(self._COLUMN_PARSER_NAME, row_number) == parser_name:
                urls_str = ",".join(new_article_urls)
                self._open_worksheet().update_acell(self._COLUMN_LAST_ARTICLE_URLS_ + str(row_number), urls_str)
                break

    def _read_cell(self, column_label, row_number):
        return self._open_worksheet().acell(column_label + str(row_number)).value

    def _create_settings(self, row_number):
        urls_str = self._read_cell(self._COLUMN_LAST_ARTICLE_URLS_, row_number)
        urls = [url.strip() for url in urls_str.split(',') if url.strip()]
        return ScrapingSetting(self._read_cell(self._COLUMN_PARSER_NAME, row_number),
                               self._read_cell(self._COLUMN_ACCESS_URL, row_number),
                               urls,
                               self._read_cell(self._COLUMN_MESSAGE_TEMPLATE, row_number))

    @staticmethod
    def _open_worksheet():
        config = config_util.get_config()['google_sheets']
        scopes = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            config_util.to_resource_file_abs_path(config['key_json_file_name']), scopes)
        client = gspread.authorize(credentials)

        return client.open_by_key(config['spreadsheet_key']).worksheet(config['sheet_name'])


class ScrapingSettingRepositoryError(Exception):
    pass
