import json

import scrapy
from scrapy.linkextractors import LinkExtractor


class Login2Spider(scrapy.Spider):
    name = "login2"
    allowed_domains = ["17k.com"]
    start_urls = ["https://user.17k.com/ck/author/shelf?page=1&appKey=2406394919"]

    def start_requests(self):
        url = 'https://passport.17k.com/ck/user/login'
        post_data ={
            'loginName': '15521083627',
            'password': 'srq19950824'
        }
        yield scrapy.FormRequest(
            url=url,
            callback=self.parse,
            formdata=post_data
        )

    def parse(self, response, **kwargs):
        # print(response.status)
        yield scrapy.Request(self.start_urls[0], callback=self.check_login)

    def check_login(self, response):
        # print(response.text)
        # print(response.xpath('/html/head/title/text()').extract_first())
        # book_list = response.xpath('//*[@id="pageListForm"]/table/tbody/tr')
        # print(book_list)
        # for book in book_list:
        #     item = {}
        #     item['title'] = book.xpath('./td[3]/a/text()').extract_first()
        #     item['author'] = book.xpath('./td[6]/text()').extract_first()
        #     print(item)

        # print(response.text)
        data_list = json.loads(response.text)['data']
        print(data_list)
        for data in data_list:
            item = {}
            item['title'] = data.get('bookName', '')
            item['author'] = data.get('authorPenName', '')
            print(item)
