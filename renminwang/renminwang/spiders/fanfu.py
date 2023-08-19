import scrapy

from renminwang.items import RenminwangItem


class FanfuSpider(scrapy.Spider):
    name = "fanfu"
    allowed_domains = ["people.com.cn"]
    start_urls = ["http://fanfu.people.com.cn/"]

    def start_requests(self):
        start_url = self.start_urls[0]
        yield scrapy.Request(start_url, self.parse)

    def parse(self, response, **kwargs):
        data_list = response.xpath("//div[@class='fl']")
        for data in data_list:
            ul_list = data.xpath('./ul')
            for ul in ul_list:
                li_list = ul.xpath('./li')
                for li in li_list:
                    item = RenminwangItem()
                    link = li.xpath('./a/@href').extract_first()
                    if link:
                        item['link'] = self.start_urls[0] + link
                    else:
                        item['link'] = None
                    item['title'] = li.xpath('./a/text()').extract_first()
                    item['date'] = li.xpath('./i/text()').extract_first()
                    yield item
        # url = response.xpath('//div[@class="page"]/a[8]/@href').extract_first()
        url = None
        for l in response.xpath('//div[@class="page"]/a'):
            if l.xpath('./text()').extract_first() == "下一页":
                url = l.xpath('./@href').extract_first()
                break
        # print("xxxxxxxxxxxurl:", url)
        if url != None:
            url = response.urljoin(url)
            yield scrapy.Request(
                url=url
            )
