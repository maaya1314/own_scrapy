# -*- coding: utf-8 -*-
import scrapy
from douban_group.items import TumblrGirlsItem
import scrapy
from scrapy.http import Request
from scrapy import log
import os


class DownloadSpider(scrapy.Spider):
    name = "download"
    allowed_domains = ["tumblr.com"]
    start_urls = [ i.strip() for i in open("/home/demo/distinct.txt").readlines() ]

    def start_requests(self):
        for url in self.start_urls:
            filename = url[url.rfind('/')+1:]
            filepath = "/mnt/F/Src/girls/" + filename
            if os.path.exists(filepath):
                log.msg("file:[" + filename + "] exists. skipped.")
                continue
            else:
                yield self.make_requests_from_url(url)

    def parse(self, response):
        item = TumblrGirlsItem()
        filename = response.url[response.url.rfind('/')+1:]
        filepath = "/mnt/F/Src/girls/" + filename
        if os.path.exists(filepath):
            log.msg("################# file exists #######################")
        fp = open(filepath, "wb")
        fp.write(response.body)
        fp.flush()
        item["file_path"] = filepath
        yield item
