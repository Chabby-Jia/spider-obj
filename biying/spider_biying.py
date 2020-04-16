import os
import sys
PATH_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PATH_DIR)

import json
import re
import time
import requests
from lxml import etree
from lxml.etree import tostring


class BiYing():
    def __init__(self):

        self.url = 'https://cn.bing.com/'
    def requests_data(self):
        res = requests.get(self.url)
        if res.status_code == 200:
            html = etree.HTML(res.content)
            tag_href = html.xpath('//*[@id="bgImgProgLoad"]')
            if tag_href:
                href = tostring(tag_href[0], encoding='utf-8').decode('utf-8')  #获取指定标签内的所有，包括标签字段本身
                manage_href = re.findall('data-ultra-definition-src="(.*)" data-explicit-bing-load',href)
                if manage_href:
                    url = self.url + manage_href[0]
                    res = requests.get(url)
                    file_name = str(int(time.time()))
                    with open(file_name + '.jpg', 'wb') as f:
                        f.write(res.content)





    def run(self):
        self.requests_data()



if __name__ == '__main__':
    by = BiYing()
    by.run()

