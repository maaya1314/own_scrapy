# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy import log
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy.contrib.pipeline.images import ImagesPipeline
import hashlib
from scrapy.http import Request

class MyImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        url = request.url
        image_guid = hashlib.sha1(url).hexdigest()
        return 'full/%s/%s.jpg' % (image_guid[:2], image_guid)

    def thumb_path(self, request, thumb_id, response=None, info=None):
        url = request.url
        thumb_guid = hashlib.sha1(url).hexdigest()  # change to request.url after deprecation
        return 'thumbs/%s/%s/%s.jpg' % (thumb_id, thumb_guid[:2], thumb_guid)

class MongoDBPipeline(object):
    def __init__(self):
        connection = pymongo.Connection(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]
    def process_item(self, item, spider):
        try:
            self.collection.insert(dict(item))
        except Exception, e:
            log.msg(str(e), level=log.ERROR)
        return item

