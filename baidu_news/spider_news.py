import os
import sys
PATH_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PATH_DIR)

from requests import RequestException
import requests
from lxml import etree
import urllib.parse
import re

import logging
logging.captureWarnings(True)  # 用于取消requests中 取消SSL认证的报错信息

#########
## wd 为公司名称全称用与最后对比

class BaiduNew(object):
    def __init__(self, wd):
        self.wd = wd
        self.brand_list = []
        self.content = {
            "name" : ""
        }

    def start_page(self, url):
        n = 0
        while n <= 2:
            try:
                requests.session().keep_alive = False
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"}
                response = requests.get(url, headers=headers, verify=False)
                if response.status_code == 200:
                    cher = response.apparent_encoding# 每个网页使用编码都不相同，获取编码格式后指定更改
                    response.encoding = cher
                    congtent = response.text
                    response.close()
                    return congtent
            except RequestException as e:
                print(e)
                if n == 2:
                    return None
                n += 1

    def news_spider(self):

        url_list = []
        pages = [0, 10, 20, 30, 40]
        for page in pages:
            for u in self.brand_list:
                url = 'https://www.baidu.com/s?tn=news&rtt=4&bsst=1&cl=2&wd={}&lqst=1&x_bd_lqst=1&tngroupname=organic_news&rsv_dl=news_b_pn&pn={}'.format(
                    urllib.parse.quote(u), page)
                url_list.append(url)
        for url in url_list:
            res = self.xpath_content(url)
            if res:
                break



    def xpath_content(self, url):
        response = self.start_page(url)
        if response:
            html = etree.HTML(response)
            contents = html.xpath('//div[@class="result"]')
            if contents:# 以百度搜索内容为例，如果有内容则继续，没有则不作为
                for content in contents:# 获取到搜索结
                    titles = content.xpath('string(.)')
                    names = titles.replace(' ','').replace('\r','').replace('\n','')
                    for brands in self.brand_list:
                        if brands:
                            ####  注意 带有括号的需要转义，否则将会匹配 括号内的内容
                            brand = brands.replace('(', '\(').replace(')', '\)')
                            name = re.findall(r'({brand})'.format(brand=brand),names)
                            if name:
                                self.content['name'] = name[0]
                                return 1



    def run(self):
        try:
            self.news_spider()
        except Exception as e:
            print(e)
        return self.content['name']





if __name__ == '__main__':
    content = '输入查询新闻内容'
    baidunews = BaiduNew(content)
    baidunews.run()