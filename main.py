import logging
import os
import sys

from src import config_util
from src.controller import ExecuteController
from src.http_repository import HttpRepository
from src.scraping_setting_repository import GoogleSheetsScrapingSettingRepository, JsonFileScrapingSettingRepository


def _get_or_empty_string(string_list, index):
    if index + 1 <= len(string_list):
        return string_list[index]
    return ''


def main():
    try:
        # 環境設定
        if _get_or_empty_string(sys.argv, 1) in ['error']:  # TODO: エラーの検知・通知方法を検討する
            raise RuntimeError('no problem')
        elif _get_or_empty_string(sys.argv, 1) in ['p', 'prod']:
            env = 'prod'
            log_level = logging.INFO
            scraping_setting_repository = GoogleSheetsScrapingSettingRepository()
        elif _get_or_empty_string(sys.argv, 1) in ['d', 'dev']:
            env = 'dev'
            log_level = logging.INFO
            scraping_setting_repository = GoogleSheetsScrapingSettingRepository()
        else:
            env = 'local'
            log_level = logging.DEBUG
            scraping_setting_repository = JsonFileScrapingSettingRepository()

        os.environ['notification_bot_env'] = env
        os.environ['notification_bot_run'] = 'run' if _get_or_empty_string(sys.argv, 2) == 'run' else 'dry_run'
        logging.basicConfig(level=log_level, format='%(asctime)s %(levelname)s %(message)s')

        # 処理開始
        logging.info('start')
        execute_controller = ExecuteController(scraping_setting_repository, HttpRepository())
        execute_controller.output_log_running_env()

        execute_controller.run()
    except BaseException as ex:
        logging.exception('an error has occurred in notification_bot: %s', ex)
        # TODO: エラーの検知・通知方法を検討する
        HttpRepository().post_slack(config_util.get_config()['slack']['error_post_url'],
                                    'an error has occurred in notification_bot: {}'.format(str(ex)))

    logging.info('finish')


if __name__ == "__main__":
    main()
