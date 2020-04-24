import os
import sys
PATH_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PATH_DIR)

from requests import RequestException
from lxml import etree
import re
import requests
import urllib.parse
import logging
logging.captureWarnings(True) # 用于取消requests中 取消SSL认证的报错信息






class BaiduVeido(object):
    def __init__(self,wd ):
        self.wd = wd
        self.brand_list = []
        self.url_list = []
        self.content = {
            "name" : "",
        }


    def start_page(self,url):
        n = 0
        while n <= 3:
            try:
                requests.session().keep_alive = False
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",}
                response = requests.get(url,headers=headers,verify=False)
                if response.status_code == 200:
                    # 每个网页使用编码都不相同，获取编码格式后指定更改
                    cher = response.apparent_encoding
                    response.encoding = cher
                    content = response.text
                    response.close()
                    return content
            except RequestException as e:
                print(e)
                if n == 3:
                    return None
                n += 1

    def veido_spider(self):
        """
        百度视频
        :param wd:
        :return:
        """
        url_list = []
        pages = [0,10,20,30]

        for page in pages:
            # 此url 为按照时间 由近到远的来排序
            url = 'https://www.baidu.com/sf/vsearch?wd={}&pd=video&async=1&pn={}'.format(urllib.parse.quote(self.wd),page)  #,encoding="GBK"
            url_list.append(url)

        print('获取url进行页面解析')
        for url in url_list:
            print(url)
            res = self.parse_one_page(url)
            if res:
                break


    def parse_one_page(self,url):
        response = self.start_page(url)
        if response:
            html = etree.HTML(response)
            html_data = html.xpath('/html/body/div')
            if html_data:
                for ju_data in html_data:
                    title = ju_data.xpath('./div/a')
                    conts = ju_data.xpath('.//div[@class="video_list_intro_small"]')  # 简介
                    if title:
                        titles = title[0].xpath('string(.)').replace(' ', '').replace('\r', '').replace('\n', '')
                        name = re.findall(r'({brand})'.format(brand=self.wd), titles)
                        if name:
                            self.content['name'] = name[0]
                            print('name *****: ', name)
                            return 1
                    if conts:
                        cont = conts[0].xpath('string(.)').replace(' ', '').replace('\r', '').replace('\n', '')
                        name2 = re.findall(r'({brand})'.format(brand=self.wd), cont)
                        if name2:
                            self.content['name'] = name2[0]
                            print('cont *****: ', name2)
                            return 1




    def run(self):

        try:
            self.veido_spider()
        except Exception as e:
            print(e)
        return self.content



if __name__ == '__main__':

    wd = '奥特曼'
    baiduveido = BaiduVeido(wd)
    res = baiduveido.run()
    print('返回结果输出:', res)