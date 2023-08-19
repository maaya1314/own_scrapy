import json

import scrapy


class CarInfo1Spider(scrapy.Spider):
    name = "car_info_1"
    allowed_domains = ["dongchedi.com"]
    start_urls = ["https://www.dongchedi.com/auto/series/{}"]

    def start_requests(self):
        for i in range(1, 3):
            yield scrapy.Request(url=self.start_urls[0].format(str(i)), callback=self.parse)

    def parse(self, response, **kwargs):
        print(response.text)
        # car_dict = json.loads(response.text)
        # online_all_list = car_dict.get("data").get("tab_list")[0].get("data")
        # print(online_all_list)
        # for car_cls in online_all_list:
        #     car_type_dict = {}
        #     car_cls = car_cls.get("info")
        #     if car_cls.get("id"):
        #         car_name = car_cls.get("series_name")
        #         car_type = car_cls.get("car_name")
        #         price = car_cls.get("price")
        #         owner_price = car_cls.get("owner_price")
        #         dealer_price = car_cls.get("dealer_price")
        #         upgrade = car_cls.get("upgrade_text")
        #         tags = "".join(car_cls.get("tags"))
        #         if car_cls.get("diff_config_with_no_pic"):
        #             configure = [i.get('config_group_key') + "-" + i.get('config_key') for i in
        #                          car_cls.get("diff_config_with_no_pic")]
        #         else:
        #             configure = ""
        #         car_type_dict["车辆名称"] = car_name
        #         car_type_dict["车辆类型"] = car_type
        #         car_type_dict["官方指导价"] = price
        #         car_type_dict["经销商报价"] = dealer_price
        #         car_type_dict["车主参考价"] = owner_price
        #         car_type_dict["车辆升级类型"] = upgrade
        #         car_type_dict["车辆标签"] = tags
        #         car_type_dict["车辆配置"] = configure
        #         yield car_type_dict
