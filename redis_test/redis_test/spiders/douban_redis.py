import scrapy
from redis_test.items import RedisTestItem
# 1. 导入分布式爬虫类
from scrapy_redis.spiders import RedisSpider


# 2.继承分布式爬虫类
class DoubanRedisSpider(RedisSpider):
    name = "douban_redis"
    # 3.注释
    allowed_domains = ["douban.com"]
    # start_urls = ["https://movie.douban.com/top250"]

    # 4.设置redis-key
    redis_key = 'py21'

    # 5.设置init
    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domains = list(filter(None, domain.split(',')))
        super(DoubanRedisSpider, self).__init__(*args, **kwargs)

    def parse(self, response, **kwargs):
        el_list = response.xpath('//*[@class="info"]')

        # print(len(el_list))

        for el in el_list:
            item = RedisTestItem()
            item['name'] = el.xpath('./div[1]/a/span[1]/text()').extract_first()
            item['info'] = (el.xpath('./div[2]/p[1]/text()[2]').extract_first()).strip()
            item['score'] = el.xpath('./div[2]/div/span[2]/text()').extract_first()
            item['comment'] = el.xpath('./div[2]/p[2]/span/text()').extract_first()
            yield item

        url = response.xpath('//span[@class="next"]/a/@href').extract_first()
        if url != None:
            url = response.urljoin(url)
            yield scrapy.Request(
                url=url
            )
