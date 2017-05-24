# -*- coding: utf-8 -*-
import pymysql
import os
import time
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SitesSpiderPipeline(object):
    def process_item(self, item, spider):
        return item

def dbHandle():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password=os.environ.get('MYSQL_PWD'),
        db='homepage',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn

class PostPipline(object):
    def process_item(self,item,spider):
        dbObject = dbHandle()
        cursor = dbObject.cursor()
        sql = "INSERT INTO posts(user_id, site_id, title,content,post_time,origin_url,img,timestamp) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
        try:
            cursor.execute(sql,(item.get('user_id'),item.get('site_id'),item.get('title'),item.get('content').replace('<img src="//','<img src="http://'),item.get('post_time'),item.get('origin_url'), item.get('img'), int(time.time())))
            print('===============》插入《==================')
            cursor.connection.commit()
        except BaseException as e:
            print("错误在这里>>>>>>>>>>>>>",e,"<<<<<<<<<<<<<错误在这里")
            dbObject.rollback()
        return item



