# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json


class QuotesbotPipeline(object):

    def open_spider(self, spider):
        if spider.name == 'toscrape-xpath':
            self.file = open("rst.json", "w")

    def process_item(self, item, spider):
        # print(item)
        if spider.name == 'toscrape-xpath':
            item = dict(item)
            json_data = json.dumps(item, ensure_ascii=False) + ", \n"
            self.file.write(json_data)
        return item

    def close_spider(self, spider):
        if spider.name == 'toscrape-xpath':
            self.file.close()

