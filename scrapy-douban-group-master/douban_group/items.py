# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TumblrGirlsItem(scrapy.Item):
    _id = scrapy.Field()
    link_url = scrapy.Field()
    image_url = scrapy.Field()
    file_path = scrapy.Field()
    file_content = scrapy.Field()
    create_date = scrapy.Field()
    vote_count = scrapy.Field()

class DoubanGroupItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    title = scrapy.Field()
    title_url = scrapy.Field()
    author = scrapy.Field()
    author_url = scrapy.Field()
    comment_count = scrapy.Field()
    last_reply_time = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    loc = scrapy.Field()
