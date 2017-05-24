# -*- coding: utf-8 -*-
import scrapy
from .util import get_url_and_site_id, post_urls_not_in_db
from sites_spider.items import PostItem
import math


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['zhihu.com']
    # start_urls = ['http://zhihu.com/']

    def __init__(self, user_id=None, *args, **kwargs):
        super(ZhihuSpider, self).__init__(*args, **kwargs)
        self.user_id = user_id
        self.base_url = 'https://www.zhihu.com'
        self.url, self.site_id = get_url_and_site_id(user_id, self.base_url)
        # https://www.zhihu.com/people/kacey-17/answers?page=1
        self.page_base_url = self.url+'/answers?page='
        self.first_url = self.page_base_url + '1'

    def start_requests(self):
        yield scrapy.Request(self.first_url, self.first_page_parse)

    def first_page_parse(self, response):
        # 获取总共的回答数
        post_num = int(response.selector.xpath('//*[@id="ProfileMain"]/div[1]/ul/li[2]/a/span/text()').extract()[2])
        # 计算页数(每页20篇回答)
        page_num = math.ceil(post_num/20)
        # 第一页的回答链接
        post_urls = response.selector.xpath('//h2[contains(@class,"ContentItem-title")]/a/@href').extract()
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
        post_urls = response.selector.xpath('//h2[contains(@class,"ContentItem-title")]/a/@href').extract()
        post_urls = [self.base_url+post_url for post_url in post_urls]
        for post_url in post_urls_not_in_db(post_urls):
            yield scrapy.Request(post_url, self.per_post_parse)

    def per_post_parse(self, response):
        item = PostItem()
        item['site_id'] = self.site_id
        item['user_id'] = self.user_id
        item['title'] = response.selector.xpath('//h1[contains(@class, "QuestionHeader-title")]/text()').extract()[0]
        item['post_time'] = response.selector.xpath('//div[contains(@class, "ContentItem-time")]/text()').extract()[0][4:]
        item['content'] = response.selector.xpath('//span[contains(@class, "RichText CopyrightRichText-richText")]').extract()[0]
        item['img'] = None
        item['origin_url'] = response.url
        yield item



