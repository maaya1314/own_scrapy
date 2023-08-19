douban_scrapy
===========

[感谢豆瓣小组提供数据来源](http://www.douban.com/group)


环境准备
--------

* [Scrapy] (http://scrapy.org/) 
* [MongoDB] (https://www.mongodb.org/) 


快速开始
--------

    #: 安装必要 python 库

    sudo pip install scrapy

    sudo pip install pymongo

    #: 下载图片到本地,并且保存相关信息到MongoDB中.

    scrapy crawl haixiuzu

    #: 生成本地相册需要的json data.

    python check.py

    #: 建立本地http server

    python -m SimpleHTTPServer 80
    
    #: 打开浏览器输入http://localhost/gallary


已实现的功能
--------

* 爬取大家的发贴信息(标题、标题URL、作者、作者URL等)，以及下载图片到本地
* 爬取用户地理位置信息
* 增加RandomUserAgent功能,防止被BAN
* 增加延时抓取功能，防止被BAN
* 由于下载图片较多，故采用hash方法分散到多个目录进行管理，提高打开文件夹速度


计划实现的功能
--------

* 本地相册功能,可以在浏览器内预览图,通过快捷键j,k,space等对图片进行翻页,加红心,删除等功能
* 本地相册功能打算借鉴(fgallery)[http://www.thregr.org/~wavexx/software/fgallery/demo/]
* 如果图片对应的topic已被管理员删除，则高亮显示


更多
-----

* [提交建议，需求，Bug报告](http://git.oschina.net/mktime/scrapy-douban-group/issues)  
* [Fork Me](http://git.oschina.net/mktime/scrapy-douban-group/fork)


