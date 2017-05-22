# -*- coding: utf-8 -*-
import scrapy
from sites_spider.items import JianshuItem

import math


class JianshuSpider(scrapy.Spider):
    name = 'jianshu'
    allowed_domains = ['jianshu.com']

    def __init__(self, user_id=None, *args, **kwargs):
        super(JianshuSpider, self).__init__(*args, **kwargs)
        self.user_id = user_id
        self.page_base_url = 'http://www.jianshu.com/u/%s?order_by=shared_at&page='
        self.first_url = self.page_base_url % user_id + '1'
        # self.page_urls = []
        
    def start_requests(self):
        scrapy.Request(self.first_url, self.first_page_parse)

    def first_page_parse(self, response):
        # 获取总共的文章数
        post_num = int(response.selector.xpath('//div[contains(@class,"info")]//p/text()').extract()[2])
        # 计算页数(每页9篇文章)
        page_num = math.ceil(post_num/9)
        # 文章列表的URL
        page_urls = [self.page_base_url%self.user_id + str(page_id) for page_id in range(1, page_num+1)]
        self.log(page_urls)
        for page_url in page_urls:
            scrapy.Request(page_url, self.per_page_parse)

    def per_page_parse(self, response):
        post_urls = response.selector.xpath('//a[contains(@class,"title")]/@href').extract()
        self.log(post_urls)
        for post_url in post_urls:
            self.log(''+post_url)











