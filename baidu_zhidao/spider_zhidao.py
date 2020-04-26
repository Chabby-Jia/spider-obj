# encoding: utf-8

import os
import sys
PATH_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PATH_DIR)

from requests import RequestException
from lxml import etree
import requests
import urllib.parse
import re
import time
import logging
logging.captureWarnings(True) # 用于取消requests中 取消SSL认证的报错信息



class BaiduZhidao(object):
    def __init__(self,wd):
        self.wd = wd
        self.content = {
            "name" : "",
        }


    def start_page(self,url):
        n = 0
        while n <= 2:
            try:
                requests.session().keep_alive = False
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
                           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                            "Accept-Encoding": "gzip, deflate, br",
                           "Accept-Language": "zh-CN,zh;q=0.9",
                           ##加入 Accept-Language  解决报错   requests.exceptions.ConnectionError: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response',))
                           "cookie" : "BAIDUID=DA3FFA2DE7020378D9892CEB79BEE9E6:FG=1; PSTM=1587348923; BIDUPSID=85CF71D79B0DC494C9744D339526FA57; delPer=0; PSINO=6; H_PS_PSSID=; ZD_ENTRY=empty; Hm_lvt_6859ce5aaf00fb00387e6434e4fcc925=1587715085; Hm_lpvt_6859ce5aaf00fb00387e6434e4fcc925=1587715085; shitong_key_id=2; shitong_data=9cab4acdd7ccf5b870d600ad30b784dabc3f305cc5f169eee9f3ee38a2a91e4c504671a6d4b2167ee8ea4bdf1c245fad47e1f9daabf7c99c166518ca06dd9af2aeaf759716046c6563cb2e1eca1ad49de7e0b30e12dddaf28916ce075e90e4ae2bdcaf7eec595bd11d85e0fc3822208166e6e98c728efd1d88c891f73bc688e1; shitong_sign=4ce8a7df"
                           }
                response = requests.get(url,headers=headers, verify=False)
                if response.status_code == 200:
                    cher = response.apparent_encoding# 每个网页使用编码都不相同，获取编码格式后指定更改
                    response.encoding = cher
                    content = response.text
                    response.close()
                    return content
                n += 1
            except RequestException as e:
                print(e)
                time.sleep(1)
                if n == 2:
                    return None
                n += 1

    def zhidao_spider(self):

        url_list = []
        pages = [0,10,20]
        for page in pages:
            url = 'https://zhidao.baidu.com/search?lm=0&rn=10&pn={}&fr=search&ie=gbk&word={}'.format(page, urllib.parse.quote(self.wd, encoding="GBK"))
            url_list.append(url)
        print('获取页面进行解析')
        for url in url_list:
            res = self.parse_one_page(url)
            if res:
                break
    def parse_one_page(self,url):
        response = self.start_page(url)
        if response:
            html = etree.HTML(response)
            contents = html.xpath('//div[@class="picker-header"]/span/text()')
            if contents:# 以百度搜索内容为例，如果有内容则继续，没有则不作为
                div_content = html.xpath('//*[@id="wgt-list"]//dl')# 获取到搜索结果证明有内容，
                for list in div_content:
                    titles = list.xpath('./dt')
                    ccs = list.xpath('./dd[1]')
                    if titles:
                        title = titles[0].xpath('string(.)').replace('\n', '').replace('\r', '').replace(' ', '')
                        name = re.findall(r'({brand})'.format(brand=self.wd), title)
                        if name:
                            self.content['name'] = name[0]
                            print('name *****: ', name)
                            return 1

                    if ccs:
                        cc = ccs[0].xpath('string(.)').replace('\n', '').replace('\r', '').replace(' ', '')
                        name2 = re.findall(r'({brand})'.format(brand=self.wd), cc)
                        if name2:
                            self.content['name'] = name2[0]
                            print('name2 *****: ', name2)
                            return 1


    def run(self):

        try:
            self.zhidao_spider()
        except Exception as e:
            print(e)
        return self.content['name']




if __name__ == '__main__':

    wd = '奥特曼'
    baiduzhidao = BaiduZhidao(wd)
    res = baiduzhidao.run()
    print('结果为：',res)


