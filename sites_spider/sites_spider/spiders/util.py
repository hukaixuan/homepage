# -*- coding: utf-8 -*-
import pymysql
import os

def post_urls_not_in_db(post_urls):
    print('=============>', post_urls)
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password=os.environ.get('MYSQL_PWD'),
                             db='homepage',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    try:
        # with connection.cursor() as cursor:
        #     # Create a new record
        #     sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)" 
        #     cursor.execute(sql, ('webmaster@python.org', 'very-secret'))
        #     # connection is not autocommit by default. So you must commit to save # your changes.
        # connection.commit()
        with connection.cursor() as cursor:
            # Read a single record
            post_urls_str = str(post_urls).replace('[','(').replace(']',')')
            sql = "SELECT `origin_url` FROM `posts` WHERE `origin_url` in %s" %post_urls_str
            cursor.execute(sql)
            results = cursor.fetchall()
            post_urls_in_db = [result['origin_url'] for result in results]
            print('in_db:====>',post_urls_in_db)
            res = [post_url for post_url in post_urls if post_url not in post_urls_in_db]
            print('not_in:====>', res)
    finally: 
        connection.close()
    return res

def get_url_and_site_id(user_id, base_url):
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password=os.environ.get('MYSQL_PWD'),
                             db='homepage',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # Read a single record
            base_url = base_url+'%'
            sql = "SELECT `url`,`id` FROM `sites` WHERE `user_id`=%s AND `url` LIKE %s" 
            cursor.execute(sql,(user_id, base_url))
            results = cursor.fetchone()
            print(results)
    finally: 
        connection.close()
    return results.get('url'), results.get('id')






