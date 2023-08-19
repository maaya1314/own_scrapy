# Define here the models for your scraped items
# 定义需要爬取的字段信息
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    print("*********items")
    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()