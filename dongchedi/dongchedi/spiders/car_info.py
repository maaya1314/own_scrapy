import json
import re

import scrapy


class CarInfoSpider(scrapy.Spider):
    name = "car_info"
    allowed_domains = ["dongchedi.com"]
    start_urls = ["https://www.dongchedi.com/search?keyword={car_name}&currTab=1&"
                  "city_name={city_name}&search_mode=history"]

    def start_requests(self):
        # 搜索汽车名称url
        # get_car_id_url = "https://www.dongchedi.com/search?keyword={car_name}&currTab=1&city_name={city_name}" \
        #                  "&search_mode=history"
        car_list = ["本田", "比亚迪"]
        for car in car_list:
            carid_url = self.start_urls[0].format(car_name=car, city_name="汕头")
            yield scrapy.Request(url=carid_url, callback=self.parse)

    def parse(self, response, **kwargs):
        car_id_list = response.xpath("//*[@id='__next']/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/a")
        # print(car_id_list)

        if not car_id_list:
            # selector = Selector(text=response)
            # car_message = response.css('''.dcd-car-series a::attr(data-log-click)''').extract_first()
            car_message = response.xpath("//*[@id='__next']/div/div[2]/div/div/div[2]/p/a/@data-log-click").extract_first()

            car_message = json.loads(car_message)
            car_id = car_message.get("car_series_id")
            # 汽车详情url
            get_car_detail_url = "https://www.dongchedi.com/motor/pc/car/series/car_list?" \
                                 "series_id={car_id}&city_name={city_name}".format(car_id=car_id, city_name="汕头")
            yield scrapy.Request(
                url=get_car_detail_url,
                callback=self.parse_detail,
                meta={"car_id": car_id}
            )
        else:
            for car_id_href in car_id_list:
                car_id_str = car_id_href.xpath("@href").extract_first()
                car_id = re.search('\d+', car_id_str).group()
                if not car_id:
                    continue
                # 汽车详情url
                get_car_detail_url = "https://www.dongchedi.com/motor/pc/car/series/car_list?" \
                                     "series_id={car_id}&city_name={city_name}".format(car_id=car_id, city_name="汕头")
                yield scrapy.Request(
                    url=get_car_detail_url,
                    callback=self.parse_detail,
                    meta={"car_id": car_id}
                )

        # 车友评论url
        # get_carfrind_comment = "https://www.dongchedi.com/motor/pc/car/series/get_review_list?" \
        #                        "series_id={car_id}&sort_by=default&only_owner=0&page=1&count=5".format(car_id=car_id)
        # yield scrapy.Request(
        #     url=get_carfrind_comment,
        #     callback=self.parse_comment
        # )

    def parse_detail(self, response, **kwargs):
        car_id = response.meta['car_id']
        car_dict = json.loads(response.text)
        online_all_list = car_dict.get("data").get("tab_list")[0].get("data")
        # print(online_all_list)
        for car_cls in online_all_list:
            car_type_dict = {}
            car_cls = car_cls.get("info")
            if car_cls.get("id"):
                car_name = car_cls.get("series_name")
                car_type = car_cls.get("car_name")
                price = car_cls.get("price")
                owner_price = car_cls.get("owner_price")
                dealer_price = car_cls.get("dealer_price")
                upgrade = car_cls.get("upgrade_text")
                # tags = "".join(car_cls.get("tags"))
                tags = car_cls.get("tags")
                if car_cls.get("diff_config_with_no_pic"):
                    configure = [i.get('config_group_key') + "-" + i.get('config_key') for i in
                                 car_cls.get("diff_config_with_no_pic")]
                else:
                    configure = ""
                car_type_dict["车辆名称"] = car_name
                car_type_dict["车辆类型"] = car_type
                car_type_dict["官方指导价"] = price
                car_type_dict["经销商报价"] = dealer_price
                car_type_dict["车主参考价"] = owner_price
                car_type_dict["车辆升级类型"] = upgrade
                car_type_dict["车辆标签"] = tags
                car_type_dict["车辆配置"] = configure
                yield car_type_dict
                # 车友评论url
                # get_carfrind_comment = "https://www.dongchedi.com/motor/pc/car/series/get_review_list?" \
                #                        "series_id={car_id}&sort_by=default&only_owner=0&page=1&count=5".format(car_id=car_id)
                # yield scrapy.Request(
                #     url=get_carfrind_comment,
                #     callback=self.parse_comment,
                #     meta={"car_info": car_type_dict}
                # )

    def parse_comment(self, response, **kwargs):
        car_info = response.meta['car_info']
        car_info_list = []
        comment_dict = json.loads(response.text)
        car_frind_comment_list = comment_dict.get("data").get("review_list")
        for car_frind_comment in car_frind_comment_list:
            car_frind_dict = {}
            buy_car_info = car_frind_comment.get("buy_car_info")
            if buy_car_info:
                bought_time = buy_car_info.get("bought_time")
                location = buy_car_info.get("location")
                price = buy_car_info.get("price")
                series_name = buy_car_info.get("series_name")
                car_name = buy_car_info.get("car_name")
                buy_car_info = f'''{bought_time}  {location}  {price} {series_name}-{car_name}'''
            else:
                buy_car_info = ""
            car_content = car_frind_comment.get("content")
            car_frind_dict["车主成交信息"] = buy_car_info
            car_frind_dict["车主评论"] = car_content
            car_info_list.append(car_frind_dict)
        car_info["其他信息"] = car_info_list
        yield car_info
