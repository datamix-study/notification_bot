import json
from abc import ABCMeta, abstractmethod
from urllib.request import Request, urlopen


class AbstractHttpRepository(metaclass=ABCMeta):
    _STATUS_CODE_OK = 200

    @abstractmethod
    def fetch_response_text(self, scraping_url: str) -> str:
        raise NotImplementedError()

    @abstractmethod
    def post_slack(self, post_slack_url: str, post_message: str) -> str:
        raise NotImplementedError()


class HttpRepository(AbstractHttpRepository):
    def fetch_response_text(self, scraping_url: str) -> str:
        headers = {'User-Agent': 'Mozilla/5.0'}
        request = Request(scraping_url, method='GET', headers=headers)
        return self._fetch_response_text(request)

    def post_slack(self, post_slack_url: str, post_message: str) -> str:
        data = {'text': post_message}
        headers = {'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}
        request = Request(post_slack_url, method='POST', data=json.dumps(data).encode(), headers=headers)
        return self._fetch_response_text(request)

    def _fetch_response_text(self, request):
        with urlopen(request) as response:
            if response.getcode() != self._STATUS_CODE_OK:
                raise HttpRepositoryError('response status code is not ok [status_code: {}, url: {}]'
                                          .format(response.getcode(), request.full_url))
            encoding = response.info().get_content_charset(failobj='UTF-8')
            return response.read().decode(encoding=encoding)


class HttpRepositoryError(Exception):
    pass
