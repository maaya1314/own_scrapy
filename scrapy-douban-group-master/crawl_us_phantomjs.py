from selenium import webdriver
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def traditional():
    url = "http://zhuanlan.zhihu.com/Weekly/20443867"
    req = requests.get(url)
    open("zhihu.html", "w").write(req.text)
    

def demo():
    driver = webdriver.PhantomJS()
    #driver = webdriver.Chrome()
    driver.get("http://zhuanlan.zhihu.com/Weekly/20443867")
    print driver.page_source
    print driver.title
    print driver.current_url
    open("zhihu.html", "w").write(driver.page_source)
    driver.save_screenshot("zhihu.png")

if __name__ == '__main__':
    demo()
    #traditional()
