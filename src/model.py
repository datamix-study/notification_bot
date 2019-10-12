import json
from typing import List


class ScrapingSetting:
    # last_urlsは冗長感(複数の過去のURLも保持)があるかもしれないが、最新URL1件のみを保持して処理をしていたときの不具合対応で今の形となった
    # -> 最新URLに変更があった場合や最新の記事がページ先頭にない場合に対応が難しかった
    def __init__(self, parser_name: str, access_url: str, last_article_urls: List[str], message_template: str):
        self.parser_name = parser_name
        self.access_url = access_url
        self.last_article_urls = last_article_urls
        self.message_template = message_template

    def __str__(self):
        return json.dumps(self.__dict__, ensure_ascii=False)

    def __eq__(self, other):
        if isinstance(other, ScrapingSetting):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        return not self.__eq__(other)


class ParseResult:
    def __init__(self, url: str, message_param_dict: dict):
        self.url = url
        self.message_param_dict = message_param_dict

    def get_message_param_dict_with_url(self) -> dict:
        all_dict = self.message_param_dict
        all_dict['url'] = self.url
        return all_dict

    def __str__(self) -> str:
        return json.dumps(self.__dict__, ensure_ascii=False)

    def __eq__(self, other):
        if isinstance(other, ParseResult):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        return not self.__eq__(other)
