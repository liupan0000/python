# -*- coding: utf-8 -*-
import scrapy


class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films']

    def parse(self, response):
       #  获得某一页的href链接
       movie_pages = response.xpath('//div[@class="movie-item"]/a/@href').extract()
       for page in movie_pages:
           yield response.follow(page,callback = self.parse_movie)
       #     最后一页的链接
       next_page = response.xpath('//ul[@class="list-pager"]/li[last()]/a/@href').get()
       if next_page:
           # response.follow可以使用相对地址，request需要提供完整的路径（带协议的路径）。
           # response.follow可以使用包含url的css选择器
           # response.follow可以使用标签
           yield response.follow(next_page,callback=self.parse)

    def parse_movie(self,response):
        container = response.xpath('//div[@class="movie-brief-container"]')
        movie = {}
        movie["name"] = container.xpath('./h3/text()').extract_first()
        movie["category"]=container.xpath('./ul/li[1]/text()').extract_first()
        movie['duration']=container.xpath('./ul/li[2]/text()').extract_first()
        movie['showtime']=container.xpath('./ul/li[3]/text()').extract_first()
        yield movie

        filename ='movie.txt'
        with open(filename,'a') as f:
            f.write('-'*60+'\n')
            for key,value in movie.items():
                f.write('%s:%s\n' %(key,value))
        # f.close()
        actor_pages = response.xpath('//div[@class="celebrity-group"][1]/ul/li/a/@href')
        yield from[response.follow(page,callback = self.parse_actor) for page in actor_pages]

    def parse_actor(self,response):
        actor={}
        short_info = response.xpath('//div[@class="shortInfo"]')
        actor['china-name']=short_info.xpath('./p[contains(@class,"china-name ")]/text()').get()
        actor['eng-name']=short_info.xpath('./p[contains(@class,"eng-name")]/text()').get()
        actor['profession']=short_info.xpath('./p[@class="property"]/span[@class="profession"]/text()').get()
        actor['birthday']=short_info.xpath('./p[@class="property]/span[@class="birthday"]/text()').get()
        yield actor




