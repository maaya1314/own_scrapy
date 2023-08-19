# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

import pymongo
import pymysql
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class RenminwangPipeline:
    def __init__(self):
        self.save_file = ["renshi", "fanfu", "all_net"]

    def open_spider(self, spider):
        if spider.name in self.save_file:
            self.file = open('renshi_info.json', 'w')

    def close_spider(self, spider):
        if spider.name in self.save_file:
            self.file.close()

    def process_item(self, item, spider):
        if spider.name in self.save_file:
            item = dict(item)
            # 将字典数据序列化
            json_data = json.dumps(item, ensure_ascii=False) + ',\n'  # , ensure_ascii=False
            self.file.write(json_data)
        return item


# 将图片信息保存到MongoDB数据库
class MongoPipeline:
    def __init__(self, mongo_uri, mongo_db):
        # 传入连接MongoDB数据库必要的信息
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        # 这个cls就是MongoPipeline本身，这里创建了MongoPipeline类的实例
        return cls(mongo_uri=crawler.settings.get("MONGO_URI"),
                   mongo_db=crawler.settings.get("MONGO_DB"))

    # 开启Spider时调用
    def open_spider(self, spider):
        # 连接MongoDB数据库
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    # 处理Item对象
    def process_item(self, item, spider):
        print(item)
        # 获取数据集的名字(本例是images)
        name = item.collection
        # 向images数据集插入文档
        self.db[name].insert_one(dict(item))
        return item

    def close_spider(self, spider):
        # 关闭MongoDB数据库
        self.client.close()


# 将图片信息保存到MySQL数据库中
class MysqlPipeline:
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

    @classmethod
    def from_crawler(cls, crawler):
        # 创建MysqlPipeline类的实例
        return cls(
            host=crawler.settings.get("MYSQL_HOST"),
            database=crawler.settings.get("MYSQL_DATABASE"),
            user=crawler.settings.get("MYSQL_USER"),
            password=crawler.settings.get("MYSQL_PASSWORD"),
            port=crawler.settings.get("MYSQL_PORT"),
        )

    def open_spider(self, spider):
        # 连接数据库
        print(1111)
        self.db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database,
                                  # 注意这里的编码有坑，不要写utf-8 否则会报错
                                  charset="utf8", port=self.port)
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        # 关闭数据库
        self.db.close()

    def process_item(self, item, spider):
        print(item["title"])
        data = dict(item)
        keys = ", ".join(data.keys())
        values = ", ".join(['%s'] * len(data))
        sql = "insert into %s (%s) values (%s)" % (item.table, keys, values)
        # 将与图片相关的数据插入MySQL数据库的images表中
        self.cursor.execute(sql, tuple(data.values()))
        self.db.commit()
        return item
