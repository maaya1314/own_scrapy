# -*- coding: utf-8 -*-
import scrapy
from douban_group.items import DoubanGroupItem
from scrapy.http import Request
from scrapy import log
import re
from html2text import html2text
from douban_group.utils import get_loc_from_db
from douban_group.utils import topic_exists


class HaixiuzuSpider(scrapy.Spider):
    name = "haixiuzu"
    allowed_domains = ["douban.com"]
    start_urls = [
        'http://www.douban.com/group/haixiuzu/discussion',
    ]
    download_delay = 2

    # 1. parse title etc
    def parse(self, response):
        for sel in  response.xpath('//tr[@class=""]'):
            item = DoubanGroupItem()
            item['title'] = sel.xpath('td[1]/a//text()').extract()[0]
            item['title_url'] = sel.xpath('td[1]/a//@href').extract()[0]
            item['_id'] = re.search('\d+', item['title_url']).group()
            item['author'] = sel.xpath('td[2]/a//text()').extract()[0]
            item['author_url'] = sel.xpath('td[2]/a//@href').extract()[0]
            item['comment_count'] = sel.xpath('td[3]/text()').extract()
            if len(item['comment_count']) == 0:
                item['comment_count'] = 0
            else:
                item['comment_count'] = int(item['comment_count'][0])
            item['last_reply_time'] = sel.xpath('td[4]/text()').extract()[0]

            # if exists, drop it
            if topic_exists(item['title_url']):
                log.msg('topic exists: ' + item['title_url'])
                continue
            yield Request(item['title_url'], callback = self.parse_item, meta = {'item':item})

    # 2. parse image urls
    def parse_item(self, response):
        item = response.meta['item']
        image_urls= response.xpath('//div[@class="topic-figure cc"]/img/@src').extract()
        if len(image_urls) == 0:
            log.msg("there is no any pictures found in this topic:" + item['title_url'], level=log.WARNING)
            return
        item['image_urls'] = image_urls
        loc = get_loc_from_db(item['author_url'])
        if not loc:
            yield Request(item['author_url'], callback = self.parse_loc, meta = {'item':item})
        else:
            log.msg('crawl location from local db:' + item['author_url'])
            item['loc'] = loc
            yield item

    # 3. parse author location
    def parse_loc(self, response):
        item = response.meta['item']
        l = response.xpath('//div[@class="mod user-card"]/div[2]/ul[1]/li[2]/text()').extract()
        if len(l) == 0:
            loc = "Dead"
        else:
            loc = html2text(l[0]).strip('\n ')
        if loc == "":
            loc = "Uknown"
        item['loc'] = loc
        yield item
