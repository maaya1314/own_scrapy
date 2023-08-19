import scrapy
from douban.items import DoubanItem
from douban.my_request import SeleniumRequest


class MovieSpider(scrapy.Spider):
    name = "movie"
    allowed_domains = ["douban.com"]
    start_urls = ["https://movie.douban.com/top250"]

    def start_requests(self):
        yield SeleniumRequest(
            url=self.start_urls[0],
            callback=self.parse
        )

    def parse(self, response, **kwargs):
        el_list = response.xpath('//*[@class="info"]')

        # print(len(el_list))

        for el in el_list:
            item = DoubanItem()
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
