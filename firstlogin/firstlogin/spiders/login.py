import scrapy


class LoginSpider(scrapy.Spider):
    name = "login1"
    allowed_domains = ["17k.com"]
    start_urls = ["https://user.17k.com/www/bookshelf/"]

    def start_requests(self):
        # login cookies登录
        # cookies_str = """
        # GUID=2a06b275-1a02-45a6-a071-c531741d2e9b;
        # sajssdk_2015_cross_new_user=1;
        # Hm_lvt_9793f42b498361373512340937deb2a0=1681377739;
        # __bid_n=18779f0c9cb7ea92de4207;
        # FPTOKEN=e5QA2e/tVqh7rG3X0hJ//k/5IEKDzwJNDe+hUGP5J9jDESxnmQMME2/fLOxCNQF/pHf+2TYnNdXTLm5AHVaxyn/tKoCbt02z587f+93LdumRC2H+P1n6qAE7G6H5dWbnc1rjhl6Qq8pnjVVDDi/UWWjWi64B5Cb3cLk2NFlySLWuU/tMor4SpR5f3+pEehCyQliY6y1Ww6RpkjM1b29HtjWYg9/D2zzuA/1/xULOgfa4BxfWF4+WZGT0SRrY+D2QXznQRBBYXOeQn4zHx1rsBfKdfIR9VGN4ixLlidS/5Paur6JX3S8RwrHQHt5wpF6eHYUobrp/wLsB+7irJRDx6Gb7p6OLwET9WMuALbYj8FTNPZ711EcP2ARStJmPY7frOzdPHfNPqO+SnLUQtHG9XA==|jgZRZXdjf7QKx2bQ+EAzczAFVc/G93L45M7wQJwgdqk=|10|7f82b8071afaf662d7ebda5186b4f3e3;
        # accessToken=nickname=%E4%B9%A6%E5%8F%8B7R129tfuD&avatarUrl=https%3A%2F%2Fcdn.static.17k.com%2Fuser%2Favatar%2F03%2F83%2F28%2F100152883.jpg-88x88%3Fv%3D1681378488233&id=100152883&e=1696930488&s=cf15fef7008c6551;
        # c_channel=0;
        # c_csc=web;
        # sensorsdata2015jssdkcross={"distinct_id":"100152883","$device_id":"18779ec422c13d0-076511ad7e1e95-7e57547b-1474560-18779ec422ddbd","props":{"$latest_traffic_source_type":"引荐流量","$latest_referrer":"https://graph.qq.com/","$latest_referrer_host":"graph.qq.com","$latest_search_keyword":"未取到值"},"first_id":"2a06b275-1a02-45a6-a071-c531741d2e9b"};
        # Hm_lpvt_9793f42b498361373512340937deb2a0=1681378489
        # """
        #
        # cookies = {(i.split('=')[0]).strip(): i.split('=')[-1].strip() for i in cookies_str.split(';')}
        # # print(cookies)
        #
        # yield scrapy.Request(
        #     url=self.start_urls[0],
        #     callback=self.parse,
        #     cookies=cookies
        # )

        # login post方法
        url = "https://passport.17k.com/ck/user/login"
        username = "15521083627"
        password = "srq19950824"

        yield scrapy.Request(
            url=url,
            method='post',
            body=f'loginName={username}&password={password}',
            callback=self.parse
        )

    def parse(self, response):
        yield scrapy.Request(url=LoginSpider.start_urls[0], callback=self.parse_detail)

    def parse_detail(self, response):
        print(response.text)
