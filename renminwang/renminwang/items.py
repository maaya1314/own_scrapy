# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RenminwangItem(scrapy.Item):
    # 定义MySQL表名和MongoDB数据集合名
    collection = table = "images"  # 表名和集合名

    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()  # 标题
    link = scrapy.Field()  # 链接
    date = scrapy.Field()  # 发布时间
