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


class PostItem(scrapy.Item):
    user_id = scrapy.Field()
    site_id = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    post_time = scrapy.Field()
    origin_url = scrapy.Field()
    img = scrapy.Field()






