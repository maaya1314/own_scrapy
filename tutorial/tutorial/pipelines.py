# Define your item pipelines here
# 对抓取的数据进行处理
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class TutorialPipeline:

    def open_spider(self, spider):
        self.file = open('items.jsonl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        print("*********pipelines")
        # print("innnnnnnnnnnnnnnnnnnnnn")
        # return item
        # adapter = ItemAdapter(item)
        # if adapter.get('price'):
        #     if adapter.get('price_excludes_vat'):
        #         adapter['price'] = adapter['price'] * self.vat_factor
        #     return item
        # else:
        #     raise DropItem(f"Missing price in {item}")

        adapter = ItemAdapter(item)
        # print("xxxxx", item, adapter)
        if adapter.get('author'):
            adapter['author'] = adapter['author'] + " mashiro"
            return item
        else:
            raise DropItem(f"Missing price in {item}")