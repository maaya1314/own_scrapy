import pymongo
from scrapy.conf import settings

def get_loc_from_db(author_url):
    connection = pymongo.Connection(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
    collection = connection[settings['MONGODB_DB']]
    db = collection[settings['MONGODB_COLLECTION']]
    item = db.find_one({"author_url":author_url,"loc":{"$exists":True}, "loc":{"$ne":""}})
    if item:
        return item["loc"]
    return None

def topic_exists(title_url):
    connection = pymongo.Connection(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
    collection = connection[settings['MONGODB_DB']]
    db = collection[settings['MONGODB_COLLECTION']]
    item = db.find_one({"title_url":title_url})
    if item:
        return True
    return False
