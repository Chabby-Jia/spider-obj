import os
import sys
PATH_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PATH_DIR)

from requests import RequestException
import requests, re
import urllib.parse
import json
import logging
logging.captureWarnings(True)  # 用于取消requests中 取消SSL认证的报错信息





class BaiduMouth(object):
    def __init__(self, wd):
        self.wd = wd
        self.url = 'https://koubei.baidu.com/search/getsearchresultajax?wd={}&page=1'.format(urllib.parse.quote(self.wd))
        self.ma_x = []
        self.title = []
        self.title_name = []
        self.content = {
            "name" : "",  #公司名称
            "mouth_count" : 0   #对应口碑  百分比
        }

    def start_page(self):
        n = 0
        while n <= 2:
            try:
                requests.session().keep_alive = False
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
                    "Referer": "https://koubei.baidu.com/search?query={}&fr=search".format(urllib.parse.quote(self.wd))
                }
                response = requests.get(self.url, headers=headers, verify=False)
                if response.status_code == 200:
                    # 每个网页使用编码都不相同，获取编码格式后指定更改
                    cher = response.apparent_encoding
                    response.encoding = cher
                    content = response.text
                    response.close()
                    return content
            except RequestException as e:
                print(e)
                if n == 2:
                    return None
                n += 1

    def mouth_spider(self):
        # 网站采用的是防盗链  使用ajax加载，返回json数据，解析思路：添加headers中referer  即可进入url中的链接！

        mouth_return = self.start_page()
        if mouth_return:
            json_obj = json.loads(mouth_return)  # 获取所有json数据 并转为字典格式
            datas = json_obj['data']['mems']
            if datas != []:
                if 'compname' in datas[0]:
                    compname = datas[0]['compname']
                    if compname:
                        if compname == self.wd:
                            self.content['name'] = compname
                for da in datas:
                    self.ma_x.append(da['praise'])
                # 返回字段和分值
                if self.ma_x:
                    self.content['mouth_count'] = max(self.ma_x)


    def run(self):
        try:
            self.mouth_spider()
        except Exception as e :
            print(e)
        return (self.content['name'],self.content['mouth_count'])






if __name__ == '__main__':

    content = '此处填写公司名称'
    mouth = BaiduMouth(content)
    mouth.run()
