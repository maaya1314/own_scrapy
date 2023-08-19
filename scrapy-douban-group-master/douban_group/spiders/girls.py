# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from douban_group.items import TumblrGirlsItem

from scrapy.http import Request
from scrapy import log
import re
from html2text import html2text
#from tumblr_girls.utils import get_loc_from_db
#from tumblr_girls.utils import topic_exists

class GirlsSpider(CrawlSpider):
    name = 'girls'
    allowed_domains = ['tumblr.com']
    start_urls = ['http://sexo-gif.tumblr.com/']
    #rules = (
    #    Rule(LinkExtractor(allow=(), restrict_xpaths=('//div[@id="navigation"]/a[1]/@href')), 
    #        callback="parse_item", 
    #        follow= True)
    #)

    rules = (Rule(SgmlLinkExtractor(allow = ('page/\d+$')),callback = 'parse_item',follow=True),)

    def parse_item(self, response):
        for sel in  response.xpath('//div[@class="post"]'):
            item = TumblrGirlsItem()
            item['link_url'] = sel.xpath('a[1]//@href').extract()[0]
            item['_id'] = re.search('\d+', item['link_url']).group()
            image_url = ''.join(sel.xpath('div[@class="media"]/a/img/@src').extract()).strip()
            if image_url == "":
                continue
            else:
                item['image_url'] = image_url
            item['create_date'] = sel.xpath('a[1]/div[1]/div[1]/text()').extract()[0].strip('\r\n \t')
            item['vote_count'] = sel.xpath('a[1]/div[1]/div[2]/text()').extract()[0].strip()
            #from scrapy.shell import inspect_response
            #inspect_response(response, self)
            yield item
