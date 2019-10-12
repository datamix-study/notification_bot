import logging
import os
import time

from src import parser, config_util
from src.http_repository import AbstractHttpRepository
from src.scraping_setting_repository import AbstractScrapingSettingRepository


class ExecuteController:
    def __init__(self,
                 scraping_setting_repository: AbstractScrapingSettingRepository,
                 http_repository: AbstractHttpRepository):
        self._scraping_setting_repository = scraping_setting_repository
        self._http_repository = http_repository
        self._is_dry_run = (os.getenv('notification_bot_run') == 'dry_run')  # Trueならデータの更新やslack通知を行わない

    def run(self, sleep_sec=1):
        scraping_settings = self._scraping_setting_repository.get_settings()
        for setting in scraping_settings:
            logging.info('try {}'.format(setting.parser_name))
            time.sleep(sleep_sec)  # 負荷対策

            # 前回と今回でURL一覧に差異があるかを確認
            all_parse_results = self._fetch_parse_results(setting)
            if not all_parse_results:
                # エラーなり通知なりしたほうが良いかも？
                logging.warning('{} returns empty, may have failed to parse'.format(setting.parser_name))
            parse_result_urls = [result.url for result in all_parse_results]
            if set(parse_result_urls) == set(setting.last_article_urls):
                continue

            # 追加がある(通知対象)かを確認
            new_articles = [result for result in all_parse_results if (result.url not in setting.last_article_urls)]
            new_article_urls = [result.url for result in new_articles]
            if not new_article_urls:
                # 例えばmeetupは開催済みイベントは取得していないためlast_urlsにあってnew_urlsにない場合がある
                logging.info('{} found no new articles, but found removed past ones'.format(setting.parser_name))
                if not self._is_dry_run:
                    self._scraping_setting_repository.update_last_article_urls(setting.parser_name, parse_result_urls)
                continue

            # 通知の実行
            logging.info('{} found changes (count: {})'.format(setting.parser_name, len(new_article_urls)))
            _ = [logging.debug(article) for article in new_articles]  # debug code
            if not self._is_dry_run:
                self._notice(new_articles, setting.message_template)
                self._scraping_setting_repository.update_last_article_urls(setting.parser_name, parse_result_urls)

    def output_log_running_env(self) -> ():
        logging.info('[env: {}, is_dry_run: {}, scraping_setting_repository: {}, http_repository: {}]'.format(
            os.getenv('notification_bot_env'),
            self._is_dry_run,
            self._scraping_setting_repository.__class__.__name__,
            self._http_repository.__class__.__name__,
        ))

    def _fetch_parse_results(self, scraping_setting):
        parser_instance = parser.factory(scraping_setting.parser_name)
        response_text = self._http_repository.fetch_response_text(scraping_setting.access_url)
        return parser_instance.extract_article_urls(response_text)

    def _notice(self, new_results, message_template):
        for result in new_results:
            message = message_template.format(result.get_message_param_dict_with_url())
            post_url = config_util.get_config()['slack']['post_url']
            self._http_repository.post_slack(post_url, message)
