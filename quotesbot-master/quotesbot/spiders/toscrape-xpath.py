# -*- coding: utf-8 -*-
import scrapy
from quotesbot.items import QuotesbotItem


class ToScrapeSpiderXPath(scrapy.Spider):
    name = 'toscrape-xpath'
    # download_delay = 2
    start_urls = [
        'http://quotes.toscrape.com/',
    ]

    def parse(self, response):
        # for quote in response.xpath('//div[@class="quote"]'):
        #     yield {
        #         'text': quote.xpath('./span[@class="text"]/text()').extract_first(),
        #         'author': quote.xpath('.//small[@class="author"]/text()').extract_first(),
        #         'tags': quote.xpath('./div[@class="tags"]/a[@class="tag"]/text()').extract()
        #     }

        # next_page_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
        # if next_page_url is not None:
        #     yield scrapy.Request(response.urljoin(next_page_url))

        for quote in response.xpath('/html/body/div/div[2]/div[1]/div'):
            tag_link = quote.xpath('./div/a/@href').extract()
            # item = {
            #     'text': quote.xpath('./span[1]/text()').extract_first(),
            #     'author': quote.xpath('./span[2]/small[@class="author"]/text()').extract_first(),
            #     'tags': quote.xpath('./div/a/text()').extract(),
            #     # 'tag_link': tag_link,
            #     # 'tag_class': quote.xpath('./div/a/@class').extract()
            # }
            item = QuotesbotItem()
            item['text'] = quote.xpath('./span[1]/text()').extract_first()
            item['author'] = quote.xpath('./span[2]/small[@class="author"]/text()').extract_first()
            item['tags'] = quote.xpath('./div/a/text()').extract()

            # yield item
            for tl in tag_link:
                detail_url = response.urljoin(tl)
                yield scrapy.Request(detail_url, callback=self.parse_detail, meta={"item": item})

    def parse_detail(self, response):
        item = response.meta["item"]
        item["cur_tag"] = response.xpath('/html/body/div[1]/h3/a/text()').extract_first()
        # print(item)
        return item
