# -*- coding: utf-8 -*-
import scrapy
import json


class AjkSpider(scrapy.Spider):
    name = 'ajk'
    allowed_domains = ['www.baidu.com/']

    post_url = "https://fanyi.baidu.com/sug"

    # POST
    # 如何提交自定义请求的办法
    def start_requests(self):
        data = {
            "kw": "baby"
        }
        # yield关键字返回，因为此函数必须返回一个可迭代对象
        yield scrapy.FormRequest(url=self.post_url, formdata=data, callback=self.baidu_parse)

    # 返回一个request对象或者item， 也许要返回可迭代对象
    def baidu_parse(self, response):
        datas = json.loads(response.text)["data"]

        for data in datas:
            print(data)



        # # start_urls是一个初始url的列表，spider会分别对列表内部的所有url执行请求对象的封装
        # # 然后提交给引擎，引擎交给调度器
        # urls = ['https://www.baidu.com/s?wd=scrapy','https://www.baidu.com/s?wd=requests']
        #
        # # 默认隐藏的一个回调函数
        # # 提交请求的回调函数
        # # 封装每一个要提交的url， 并且绑定每一个url在得到响应之后的回调函数
        # def start_requests(self):
        #     for url in self.urls:
        #         # 请求对象如何封装
        #         yield scrapy.Request(url=url, callback=self.parse_dancer)
        #
        # # 回调函数，这个response对象就是下载器得到的对应url的响应对象
        # # 可以返回item， 也可以返回request
        # def parse_dancer(self, response):
        #     print(response.url)
