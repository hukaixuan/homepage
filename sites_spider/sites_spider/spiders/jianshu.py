# -*- coding: utf-8 -*-
import scrapy
from sites_spider.items import PostItem
from .util import post_urls_not_in_db, get_url_and_site_id

import math


class JianshuSpider(scrapy.Spider):
    name = 'jianshu'
    allowed_domains = ['jianshu.com']

    def __init__(self, user_id=None, *args, **kwargs):
        super(JianshuSpider, self).__init__(*args, **kwargs)
        self.user_id = user_id
        self.base_url = 'http://www.jianshu.com'
        self.url, self.site_id = get_url_and_site_id(user_id, self.base_url)
        # http://www.jianshu.com/u/77cd37f5fa75?order_by=shared_at&page=1
        self.page_base_url = self.url+'?page='
        self.first_url = self.page_base_url + '1'

    def start_requests(self):
        yield scrapy.Request(self.first_url, self.first_page_parse)

    def first_page_parse(self, response):
        # 获取总共的文章数
        post_num = int(response.selector.xpath('//div[contains(@class,"info")]//p/text()').extract()[2])
        # 计算页数(每页9篇文章)
        page_num = math.ceil(post_num/9)
        # 第一页的文章链接
        post_urls = response.selector.xpath('//a[contains(@class,"title")]/@href').extract()
        # 添加未爬取的文章的URL
        post_urls = [self.base_url+post_url for post_url in post_urls]
        for post_url in post_urls_not_in_db(post_urls):
            yield scrapy.Request(post_url, self.per_post_parse)
        # 文章列表的URL
        page_urls = [self.page_base_url + str(page_id) for page_id in range(1, page_num+1)]
        for page_url in page_urls:
            self.log('从%s爬取数据' %page_url)
            yield scrapy.Request(page_url, self.per_page_parse)

    def per_page_parse(self, response):
        post_urls = response.selector.xpath('//a[contains(@class,"title")]/@href').extract()
        post_urls = [self.base_url+post_url for post_url in post_urls]
        for post_url in post_urls_not_in_db(post_urls):
            yield scrapy.Request(post_url, self.per_post_parse)

    def per_post_parse(self, response):
        item = PostItem()
        item['site_id'] = self.site_id
        item['user_id'] = self.user_id
        item['title'] = response.selector.xpath('//h1[contains(@class, "title")]/text()').extract()[0]
        item['post_time'] = response.selector.xpath('//span[contains(@class, "publish-time")]/text()').extract()[0]
        item['content'] = response.selector.xpath('//div[contains(@class, "show-content")]').extract()[0]
        img_urls = response.selector.xpath('//div[contains(@class, "image-package")]/img/@src').extract()
        if img_urls:
            item['img'] = response.urljoin(img_urls[0])
        item['origin_url'] = response.url
        yield item











