import os
import sys
PATH_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PATH_DIR)

from requests import RequestException
import requests
from urllib.parse import quote
import re, json,time,random



class SouHu(object):
    def __init__(self):
        self.wd = input('请输入需要查询内容：')
        pages = input('请输入查询的阿拉伯数字页数 (默认第一页，最大不超过5) ： ')
        if pages and int(pages) < 6:
            self.page = int(pages)
        else:
            self.page = 1
        self.url = 'http://search.sohu.com/search/meta?keyword={wd}&terminalType=pc&spm-pre=smpc.csrpage.0.0.1561721638721eMZZjdy&SUV=190628193556KMF7&from={pg}&size=10&searchType=news&queryType=edit&refer=http%3A//search.sohu.com/' #,encoding="GBK"
        self.url_list = []
        self.brand_list = []
        self.content = []

    def start_page(self,url):
        n = 0
        while n <= 2:
            try:
                requests.session().keep_alive = False
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",}
                response = requests.get(url,headers=headers,verify=False)
                if response.status_code == 200:
                    cher = response.apparent_encoding# 每个网页使用编码都不相同，获取编码格式后指定更改
                    response.encoding = cher
                    ccc = response.text
                    response.close()
                    return ccc
                n += 1
            except RequestException as e:
                print('请求错误',e)
                if n == 2:
                    return None
                n += 1

    def souhu_spider(self):

        url_list = []
        if self.wd:
            if self.page:
                for pg in range(self.page):
                    url1 = self.url.format(wd=quote(self.wd), pg= pg * 10 )
                    url_list.append(url1)
            else:
                url2 =  self.url.format(wd=quote(self.wd), pg= 0 )
                url_list.append(url2)
        # print('获取url进行页面解析')
        for url in url_list:
            # print(url)
            time.sleep(random.random())
            res = self.parse_one_page(url)


    def parse_one_page(self,url):

        response = self.start_page(url)
        if response:
            conten = json.loads(response)
            if 'data' in conten:
                if 'news' in conten['data']:
                    s = conten.get('data').get('news')
                    for ti_ in s:
                        title = ti_['title']  # 获取标题
                        authorName = ti_['authorName'] # 获取作者
                        href = ti_['url']  #获取连接
                        briefAlg = ti_['briefAlg']  #获取简介
                        dic = {"title":title,"authorName":authorName,"briefAlg":briefAlg,"href":href}
                        self.content.append(dic)



    def run(self):

        try:
            self.souhu_spider()
        except Exception as e:
            pass

        # 打印内容
        for i in self.content:
            print(i)





if __name__ == '__main__':


    souhu = SouHu()
    souhu.run()