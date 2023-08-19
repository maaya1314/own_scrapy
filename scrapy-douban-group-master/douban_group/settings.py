# -*- coding: utf-8 -*-

BOT_NAME = 'douban_group'

SPIDER_MODULES = ['douban_group.spiders']
NEWSPIDER_MODULE = 'douban_group.spiders'

ITEM_PIPELINES = {
    #'douban_group.pipelines.MongoDBPipeline':300,
    #'douban_group.pipelines.MyImagesPipeline':200
    #'scrapy.contrib.pipeline.images.ImagesPipeline':200
    #'douban_group.pipelines.FilePipeline':200
}

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
    'douban_group.random_useragent.RandomUserAgentMiddleware' :400
}

#IMAGES_STORE = '/home/demo/Pictures/girls'
#IMAGES_EXPIRES = 90
#IMAGES_THUMBS = {
#    'big': (150, 200)
#}

EXTENSIONS = {
    'scrapy.telnet.TelnetConsole': 300
}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36'

#COOKIES_ENABLED = False

#MONGODB_SERVER = "localhost"
#MONGODB_PORT = 27017
#MONGODB_DB = BOT_NAME
#MONGODB_COLLECTION = "haixiuzu"
