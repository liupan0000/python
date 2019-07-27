# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class DushuSpider(CrawlSpider):
    name = 'dushu'
    allowed_domains = ['www.dushu.com']
    start_urls = ['https://www.dushu.com/book/1158.html']

    rules = (
        # scrapy.Request(url, callback=self.parse)
        # 提取页码的链接, 作用就是获取到所有页面，进而提取到每一个界面的书籍的详情页链接
        Rule(LinkExtractor(allow=r'/book/1158_\d+.html'), follow=True),
        # 提取详情页链接
        Rule(LinkExtractor(allow=r'/book/\d+/'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        title = response.xpath("//h1/text()").extract_first()
        print(title)


    # def parse(self, response):
    #     # 设定一些其他页码的规则
    #     for page in page_list:
    #         # 请求每一个页面
    #         # 解析每一个页面的书籍（获取到名字、详情页链接等功能）
    #         for book_url in book_urls:
    #             # 请求每一本书的信息
    #             yield scrapy.Request(book_url, callback=self.parse_book)
    #
    #
    # def parse_book(self, response):
    #     # 解析每一本书的内容
    #     yield book_item