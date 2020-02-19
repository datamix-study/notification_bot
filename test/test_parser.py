import unittest
from typing import List

from src import parser
from src.model import ParseResult
from src.parser import DataMixInformationParser, AbstractParser, ParserError, DataMixBlogParser, MeetupApiParser, \
    DataMixMediaParser
from test import test_parser_helper


# TODO: expectedやassertの数が多く分かりにくいのでhelperに切り出す、list用のassertを利用するなどリファクタリングする
class TestParser(unittest.TestCase):
    pass


class TestDataMixInformationParser(TestParser):
    def setUp(self):
        super().setUp()
        self.sut = DataMixInformationParser()

    def tearDown(self):
        pass

    def test_extract_article_urls_when_parsable_source_then_parse_results(self):
        expected0 = ParseResult('https://datamix.co.jp/news/20191009/',
                                {'title': '2019年10月12日(土)の休講及び無料説明会中止のお知らせ'})
        expected1 = ParseResult('https://datamix.co.jp/news/3551/',
                                {'title': 'オデッセイコミュニケーションズ主催「第17回 オデッセイ ユニバーシティ」にて弊社代表が講演いたします'})
        expected2 = ParseResult('https://datamix.co.jp/news/20191002/', {
            'title': 'DX時代の企業の人財戦略セミナー「AIを活用した組織分析、データサイエンティスト育成の実践」を株式会社ネクストエデュケーションシンク様と共催いたします'})
        expected3 = ParseResult('https://datamix.co.jp/news/20190919/',
                                {'title': '「第8回日本HRチャレンジ大賞」においてイノベーション賞を受賞しました'})
        expected4 = ParseResult('https://datamix.co.jp/news/20190910/',
                                {'title': '「ネクスト・ザ・ファースト46  – 次代を担う市場の開拓者-」に掲載されました'})
        expected5 = ParseResult('https://datamix.co.jp/news/20190830/',
                                {'title': '【プレスリリース】 gacco® (ガッコ) セレクト有料講座に「データサイエンス スキル育成プログラム」を開講'})
        expected6 = ParseResult('https://datamix.co.jp/news/20190409/',
                                {'title': '【プレスリリース】ゴールデンウィーク中でデータ分析スキルを身につけるデータサイエンス研修を提供 ― 短期間でデータ分析、機械学習の基礎知識を習得 ―'})
        expected7 = ParseResult('https://datamix.co.jp/news/20190403/',
                                {'title': '【プレスリリース】「データサイエンティスト育成コース パートタイムプログラム」の開講を増設'})
        expected8 = ParseResult('https://datamix.co.jp/news/20190312/',
                                {'title': '【プレスリリース】データミックスがSpeeeと業務提携を実施　ノウハウを活かした独自のビジネストランスレーター育成研修制度を提供'})
        expected9 = ParseResult('https://datamix.co.jp/news/20190226/',
                                {
                                    'title': '【プレスリリース】国内のデータサイエンティスト育成スクールにおいて初の取組みとなる リアルな企業データを活用したデータ分析PoC『OpenPoC』の提供を開始'})

        actual = self.sut.extract_article_urls(test_parser_helper.DATAMIX_INFORMATION_SOURCE)
        self.assertEqual(10, len(actual))
        self.assertEqual(expected0, actual[0])
        self.assertEqual(expected1, actual[1])
        self.assertEqual(expected2, actual[2])
        self.assertEqual(expected3, actual[3])
        self.assertEqual(expected4, actual[4])
        self.assertEqual(expected5, actual[5])
        self.assertEqual(expected6, actual[6])
        self.assertEqual(expected7, actual[7])
        self.assertEqual(expected8, actual[8])
        self.assertEqual(expected9, actual[9])

    def test_extract_article_urls_when_empty_source_then_empty(self):
        actual = self.sut.extract_article_urls('')
        self.assertEqual(0, len(actual))


class TestDataMixMediaParser(TestParser):
    def setUp(self):
        super().setUp()
        self.sut = DataMixMediaParser()

    def tearDown(self):
        pass

    def test_extract_article_urls_when_parsable_source_then_parse_results(self):
        expected0 = ParseResult('https://datamix.co.jp/news/20190320/',
                                {'title': '【メディア掲載】フリーランスエンジニアNoteに弊社代表 堅田のインタビューが掲載されました'})
        expected1 = ParseResult(
            'https://datamix.co.jp/news/%e3%80%90%e3%83%a1%e3%83%87%e3%82%a3%e3%82%a2%e6%8e%b2%e8%bc%89%e3%80%91%e6%97%a5%e5%88%8a%e5%b7%a5%e6%a5%ad%e6%96%b0%e8%81%9e%e9%9b%bb%e5%ad%90%e7%89%88%e3%81%ab%e5%bc%8a%e7%a4%be%e5%a0%85%e7%94%b0/',
            {'title': '【メディア掲載】日刊工業新聞電子版に弊社堅田のインタビューが掲載されました'})
        expected2 = ParseResult(
            'https://datamix.co.jp/news/%e3%80%90%e3%83%a1%e3%83%87%e3%82%a3%e3%82%a2%e6%8e%b2%e8%bc%89%e3%80%91%e3%83%9e%e3%82%a4%e3%83%8a%e3%83%93%e3%83%8b%e3%83%a5%e3%83%bc%e3%82%b9%e3%81%ab%e5%bc%8a%e7%a4%be%e4%bb%a3%e8%a1%a8-%e5%a0%85/',
            {'title': '【メディア掲載】マイナビニュースに弊社代表 堅田のインタビューが掲載されました'})
        expected3 = ParseResult('https://datamix.co.jp/news/diamond_online/',
                                {'title': '【メディア掲載】Diamond onlineに弊社代表 堅田のインタビューが掲載されました'})
        expected4 = ParseResult(
            'https://datamix.co.jp/news/%e3%80%90%e3%83%a1%e3%83%87%e3%82%a3%e3%82%a2%e6%8e%b2%e8%bc%89%e3%80%91%e3%83%8f%e3%83%bc%e3%83%90%e3%83%bc%e3%83%bb%e3%83%93%e3%82%b8%e3%83%8d%e3%82%b9%e3%83%bb%e3%82%aa%e3%83%b3%e3%83%a9%e3%82%a4/',
            {'title': '【メディア掲載】ハーバー・ビジネス・オンラインに代表堅田のインタビュー記事が掲載されました。'})
        actual = self.sut.extract_article_urls(test_parser_helper.DATAMIX_MEDIA_SOURCE)
        self.assertEqual(5, len(actual))
        self.assertEqual(expected0, actual[0])
        self.assertEqual(expected1, actual[1])
        self.assertEqual(expected2, actual[2])
        self.assertEqual(expected3, actual[3])
        self.assertEqual(expected4, actual[4])

    def test_extract_article_urls_when_empty_source_then_empty(self):
        actual = self.sut.extract_article_urls('')
        self.assertEqual(0, len(actual))


class TestDataMixBlogParser(TestParser):
    def setUp(self):
        super().setUp()
        self.sut = DataMixBlogParser()

    def tearDown(self):
        pass

    def test_extract_article_urls_when_parsable_source_then_parse_results(self):
        expected0 = ParseResult('https://datamix.co.jp/interview-fujita-coo/',
                                {'title': '「データサイエンスはMBA以上の武器になる」- データミックスCOO藤田'})
        expected1 = ParseResult('https://datamix.co.jp/dtst_shimizu/',
                                {'title': '清水 嵩文_データサイエンティスト育成のフロンティア_インストラクター紹介'})
        expected2 = ParseResult('https://datamix.co.jp/blog-what-is-data-science/',
                                {'title': 'データサイエンス（Data Science）とは？'})
        expected3 = ParseResult('https://datamix.co.jp/blog-taiki-jidou/',
                                {'title': '保育園に入りやすい区はどこ？ 〜２３区別「待機児童の状況」の変化〜'})

        actual = self.sut.extract_article_urls(test_parser_helper.DATAMIX_BLOG_SOURCE)
        self.assertEqual(4, len(actual))
        self.assertEqual(expected0, actual[0])
        self.assertEqual(expected1, actual[1])
        self.assertEqual(expected2, actual[2])
        self.assertEqual(expected3, actual[3])

    def test_extract_article_urls_when_empty_source_then_empty(self):
        actual = self.sut.extract_article_urls('')
        self.assertEqual(0, len(actual))


class TestMeetupApiParser(TestParser):
    def setUp(self):
        super().setUp()
        self.sut = MeetupApiParser()

    def tearDown(self):
        pass

    def test_extract_article_urls_when_parsable_source_then_parse_results(self):
        actual = self.sut.extract_article_urls(test_parser_helper.MEETUP_API_SOURCE)
        expected0 = ParseResult('https://www.meetup.com/datamix/events/265234301/',
                                {'title': 'レコメンデーション論文を読む！データミックスゼミ第3回'})
        expected1 = ParseResult('https://www.meetup.com/datamix/events/265235011/',
                                {'title': '自然言語処理の論文を読む！データミックスゼミ第3回'})
        self.assertEqual(2, len(actual))
        self.assertEqual(expected0, actual[0])
        self.assertEqual(expected1, actual[1])

    def test_extract_article_urls_when_empty_source_then_empty(self):
        actual = self.sut.extract_article_urls('')
        self.assertEqual(0, len(actual))

    def test_extract_article_urls_when_empty_json_then_empty(self):
        actual = self.sut.extract_article_urls('{ }')
        self.assertEqual(0, len(actual))


class TestScript(TestParser):
    def test_factory_when_single_exists_name_then_instance(self):
        self.assertIsInstance(parser.factory('DataMixInformationParser'), DataMixInformationParser)

    def test_factory_when_not_exists_name_then_raise(self):
        with self.assertRaises(ParserError):
            parser.factory('not exists')

    def test_factory_when_multi_exists_name_then_raise(self):
        class __DuplicatedNameTestParser(AbstractParser):
            def extract_article_urls(self, text: str) -> List[ParseResult]:
                pass

        class __DuplicatedNameTestParser(AbstractParser):
            def extract_article_urls(self, text: str) -> List[ParseResult]:
                pass

        with self.assertRaises(ParserError):
            parser.factory('__DuplicatedNameTestParser')


if __name__ == '__main__':
    unittest.main()
