#慧聪网
import os
import sys

PATH_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PATH_DIR)

from multiprocessing import Process
from requests import RequestException
from lxml import etree
import requests
import time
import urllib.parse
import logging
logging.captureWarnings(True)  # 用于取消requests中 取消SSL认证的报错信息



class HuiCongWang(object):
    def __init__(self, wd):
        self.wd = wd
        self.title_list = []
        self.url = 'https://s.hc360.com/company/search.html?kwd={}'.format(urllib.parse.quote(self.wd))
        self.content = {
            "name": "",
        }

    def start_page(self):
        n = 0
        while n <= 3:
            try:
                requests.session().keep_alive = False
                headers = {
                    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
                }
                response = requests.get(self.url, headers=headers, verify=False)
                if response.status_code == 200:
                    cher = response.apparent_encoding  # 每个网页使用编码都不相同，获取编码格式后指定更改
                    response.encoding = cher
                    content = response.text
                    response.close()
                    del (response)
                    print("网页获取成功~~")
                    return content
                else:
                    print('请求失败.')
            except RequestException as e:
                print(e)
                if n == 3:
                    return None
                n += 1

    def huicong_spider(self):
        """
        爬取慧聪网电商网站，初需求查询第一页内容
        :return:
        """
        huicong_return = self.start_page()

        if huicong_return:
            print("开始数据寻找")
            html = etree.HTML(huicong_return)
            contents = html.xpath('//div[@class="cont-left"]//div[@class="col"]')
            if contents:
                for cont in contents:
                    title = cont.xpath(".//h3/a[1]/text()")
                    if title:    # 判断获取到的数据是否存在，不存在则pass，存在则去掉换行、空格等没用的字符
                        title = title[0].strip()
                        self.title_list.append(title)
            else:
                print('无指定内容')
        if self.wd in self.title_list:
            self.content["name"] = self.wd


    def run(self):
        try:
            self.huicong_spider()
        except Exception as e:
            print(e)
        return self.content





if __name__ == '__main__':

    wd = '输入公司名'
    huicong = HuiCongWang(wd=wd)
    huicong.run()