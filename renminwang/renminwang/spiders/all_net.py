import scrapy

from renminwang.items import RenminwangItem


class AllNetSpider(scrapy.Spider):
    name = "all_net"
    allowed_domains = ["people.com.cn"]
    start_urls = ["http://people.com.cn/"]
    tab_category_1 = ["党网 · 时政"]
    tab_category_2 = ["人事", "反腐"]

    def parse(self, response, **kwargs):
        menu_list = response.xpath('//*[@id="rm_topnav"]/div/div/ul/li[@class="menu_item"]')
        for menu in menu_list:
            tab_list = menu.xpath('./div/ul/li')
            for tab in tab_list:
                cur_tab = tab.xpath('./a/text()').extract_first()
                # print("cur_tab:", cur_tab)
                if cur_tab in self.tab_category_1:
                    url = tab.xpath('./a/@href').extract_first()
                    yield scrapy.Request(url, self.parse_tc1)
                elif cur_tab in self.tab_category_2:
                    url = tab.xpath('./a/@href').extract_first()
                    yield scrapy.Request(url, self.parse_tc2)
                else:
                    pass

    def parse_tc1(self, response, **kwargs):
        data_list = response.xpath('//div[@class="calendar-news-wrap"]/ul/li')
        for data in data_list:
            item = RenminwangItem()
            link = data.xpath('./div/span/a/@href').extract_first()
            if link:
                item['link'] = response.urljoin(link)
            else:
                item['link'] = None
            item['title'] = data.xpath('./div/span/a/text()').extract_first()
            item['date'] = ''
            yield item

    def parse_tc2(self, response, **kwargs):
        data_list = response.xpath("//div[@class='fl']")
        for data in data_list:
            ul_list = data.xpath('./ul')
            for ul in ul_list:
                li_list = ul.xpath('./li')
                for li in li_list:
                    item = RenminwangItem()
                    link = li.xpath('./a/@href').extract_first()
                    if link:
                        item['link'] = response.urljoin(link)
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
                url=url,
                callback=self.parse_tc2,
            )