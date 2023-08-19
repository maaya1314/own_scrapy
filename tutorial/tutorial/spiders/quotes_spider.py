# Scrapy的爬虫结构是固定的，定义一个类，继承自scrapy.Spider，类中定义属性【爬虫名称，域名，起始url】，重写父类方法【parse】，
# 根据需要爬取的页面逻辑不同，在parse中定制不同的爬虫代码

from pathlib import Path

import scrapy
from tutorial.items import TutorialItem


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    # start_urls = [
    #     'https://quotes.toscrape.com/page/1/',
    #     'https://quotes.toscrape.com/page/2/',
    # ]

    def start_requests(self):
        urls = [
            'https://quotes.toscrape.com/page/1/',
            # 'https://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        print("*********quotes_spider")
        # page = response.url.split("/")[-2]
        # filename = f'quotes-{page}.html'
        # Path(filename).write_bytes(response.body)
        # self.log(f'Saved file {filename}')

        item = TutorialItem()

        for quote in response.css('div.quote'):
            # yield {
            #     'text': quote.css('span.text::text').get(),
            #     'author': quote.css('small.author::text').get(),
            #     'tags': quote.css('div.tags a.tag::text').getall(),
            # }
            item['text'] = quote.css('span.text::text').get()
            item['author'] = quote.css('small.author::text').get()
            item['tags'] = quote.css('div.tags a.tag::text').getall()
            yield item

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

        # for quote in response.css('div.col-md-8'):
        #     yield {
        #         'text': quote.css('div.quote span.text::text').getall(),
        #         'author': quote.css('div.quote small.author::text').getall(),
        #         'tags': quote.css('div.quote div.tags a.tag::text').getall(),
        #     }