import json
from abc import ABCMeta, abstractmethod
from typing import List

from bs4 import BeautifulSoup

from src.model import ParseResult


class AbstractParser(metaclass=ABCMeta):
    @abstractmethod
    def extract_article_urls(self, text: str) -> List[ParseResult]:
        raise NotImplementedError()


class DataMixInformationParser(AbstractParser):
    def extract_article_urls(self, text: str) -> List[ParseResult]:
        soup = BeautifulSoup(text, "html.parser")
        list_contents = soup.select('#wrapper > div.blogs.content_section.cf > div > div.inner > ul > li')

        results = []
        for content in list_contents:
            a_tag = content.select_one('h4 > a')
            if not a_tag:
                continue
            results.append(ParseResult(a_tag.attrs['href'], {'title': a_tag.text}))

        return results


class DataMixMediaParser(AbstractParser):
    def extract_article_urls(self, text: str) -> List[ParseResult]:
        soup = BeautifulSoup(text, "html.parser")
        list_contents = soup.select('#wrapper > div.media-area > div > div.inner > ul > li')

        results = []
        for content in list_contents:
            a_tag = content.select_one('h4 > a')
            if not a_tag:
                continue
            results.append(ParseResult(a_tag.attrs['href'], {'title': a_tag.text}))

        return results


class DataMixBlogParser(AbstractParser):
    def extract_article_urls(self, text: str) -> List[ParseResult]:
        soup = BeautifulSoup(text, "html.parser")
        article_div_contents = soup.select('#wrapper > div.blog-area > div > div.inner > ul > li')

        results = []
        for content in article_div_contents:
            a_tag = content.select_one('h3 > a')
            if not a_tag:
                continue
            results.append(ParseResult(a_tag.attrs['href'], {'title': a_tag.text}))

        return results


class MeetupApiParser(AbstractParser):
    def extract_article_urls(self, text: str) -> List[ParseResult]:
        if not text:
            return []
        response_objects = json.loads(text)
        return [ParseResult(result['link'], {'title': result['name']}) for result in response_objects]


class ParserError(Exception):
    pass


def factory(parser_name: str) -> AbstractParser:
    parsers = [cls for cls in AbstractParser.__subclasses__() if cls.__name__ == parser_name]
    if len(parsers) != 1:
        raise ParserError('parser is not single: [parser_name: {}, count: {}]'.format(parser_name, len(parsers)))
    return parsers[0]()
