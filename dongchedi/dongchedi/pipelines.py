# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class DongchediPipeline:

    def open_spider(self, spider):
        self.file = open('car_info.json', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        print("*********pipelines")
        # 将字典数据序列化
        json_data = json.dumps(item, ensure_ascii=False) + ',\n'  # , ensure_ascii=False
        self.file.write(json_data)
        return item
        # adapter = ItemAdapter(item)
        # if adapter.get('price'):
        #     if adapter.get('price_excludes_vat'):
        #         adapter['price'] = adapter['price'] * self.vat_factor
        #     return item
        # else:
        #     raise DropItem(f"Missing price in {item}")

