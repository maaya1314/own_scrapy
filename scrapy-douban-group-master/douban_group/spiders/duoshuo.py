# -*- coding: utf-8 -*-
import scrapy
from douban_group.items import DoubanGroupItem
from scrapy.http import Request
from scrapy import log
import re
import json
from StringIO import StringIO
from base64 import b64decode
from html2text import html2text
from douban_group.utils import get_loc_from_db
from douban_group.utils import topic_exists


class DuoshuoSpider(scrapy.Spider):
    name = "duoshuo"
    allowed_domains = ["duoshuo.com", "douban.com"]
    start_urls = [
        'http://api.duoshuo.com/threads/listPosts.json?order=desc&thread_key=haixiuzu&short_name=database&page=1&limit=200',
    ]
    download_delay = 2

    def parse(self, response):
        item = DoubanGroupItem()
        root = json.loads(response.body)
        for one in root['parentPosts'].items():
            last_reply_time = one[1]['created_at'].replace('T', ' ')[:-6]
            one = json.loads(b64decode(one[1]['message']))
            item['title'] = one['title']
            item['title_url'] = one['url']
            item['author'] = one['author']
            item['comment_count'] = "0"
            item['last_reply_time'] = last_reply_time
            item['author_url'] = one['author_url']
            item['image_urls'] = one['imgs']
            id = re.search('\d+', one['url']).group()
            item['_id'] = str(id)
            # if exists, continue next one
            if topic_exists(item['title_url']):
                log.msg('topic exists: ' + item['title_url'])
                continue
            loc = get_loc_from_db(item['author_url'])
            if not loc:
                yield Request(item['author_url'], callback = self.parse_loc, meta = {'item':item})
            else:
                log.msg('crawl location from local db:' + item['author_url'])
                item['loc'] = loc
                yield item

    # 2. parse author location
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
