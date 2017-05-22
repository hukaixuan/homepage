# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SitesSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class JianshuItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    likes = scrapy.Field()
    post_time = scrapy.Field()