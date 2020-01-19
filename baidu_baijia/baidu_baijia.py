import os
import sys

PATH_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PATH_DIR)

import json
import re
import time
import requests
import threading
import pymysql
import datetime
from queue import Queue
from threading import Thread
from urllib.parse import quote


class BaiDuBaijia():
    def __init__(self, wd):
        self.brand_list = []
        self.wd = wd['wd']
        self.brand = wd['brand']

        self.lock = threading.Lock()
        self.headers = {
            'Cookie': '',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "X-Requested-With": "XMLHttpRequest",
        }
        self.ajaxurl = 'https://v123.baidu.com/xzhpageajax'
        self.content = {
            "baijia_name": "",
            "baijia_article_num": 0,
            "baijia_three_": "",
            "company": ""
        }
        self.url_auth = []  #获取认证公司得百家号url
        self.url_list = []  # 去重
        self.w = 0
        self.n = 0
        self.nn = 0
        self.nnn = 0


    def ajax_article_num(self, uk_id):
        # uk_id = re.findall('"uk":"(.*)","cmt_level":', content)
        if uk_id:
            print('uk_id: ',uk_id)
            S = requests.session()
            ts = '__jsonp0' + str(int(time.time() * 1000))
            n = 0
            for _ in range(2):
                url = f'https://mbd.baidu.com/webpage?tab=article&num=10&uk={uk_id}&type=newhome&action=dynamic&format=jsonp&Tenger-Mhor=3023395301&callback={ts}'
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
                }
                response = S.get(url=url, headers=headers)
                cher = response.apparent_encoding
                response.encoding = cher
                contentss = response.text
                if re.findall('哎呀迷路了', contentss):
                    pass
                if re.findall('__jsonp', contentss):
                    json_content = re.findall('{}\((.*)\)'.format(ts), contentss)
                    if json_content:
                        json_content = json.loads(json_content[0])

                        if 'data' in json_content:
                            if json_content['data']['list']:
                                print('文章内容获取成功:', 1)
                            else:
                                print('文章获取内容为空，', url)
                            if 'query' in json_content['data']:  # 在此获取下一页参数  时间戳
                                ctime = json_content['data']['query']
                            if 'list' in json_content['data']:
                                article_num = len(json_content['data']['list'])
                                response.close()
                                return article_num
                n += 1
                if n == 2:
                    break
                time.sleep(1)

    def getbrand(self):
        sname = re_replace_content(self.wd)  # 获取公司简称
        if not sname:
            sname = ''
        try:
            self.brand_ = getBrand(self.wd)
        except Exception as e:
            print(e)
        if self.brand_:
            for uu in self.brand_:
                self.brand_list.append(uu)
            self.brand_list.insert(0, self.wd)
            self.brand_list.insert(1, sname)
            self.brand_list.insert(2, self.brand)
        else:
            self.brand_list.append(self.wd)
            self.brand_list.append(sname)
            self.brand_list.append(self.brand)
        print('获取品牌： ', self.brand_list)

    def run(self):
        q = Queue()
        result_qu = Queue()
        if self.brand_list:
            start_list = []
            for uu in self.brand_list:
                if uu:
                    q.put(uu)
            print('queue 开始大小 %d' % q.qsize())
            for index in range(10):
                thread = Thread(target=self.action_spider, args=(q, result_qu,), daemon=True)  # 随主线程退出而退出
                thread.start()
                start_list.append(thread)
            for i in start_list:
                i.join()  # 队列消费完 线程结束
        print('爬虫结束')
        return self.content


    def baijia_spider(self,uu,result_qu,page=0):
        url = f"https://m.baidu.com/sf/vsearch?pd=userlist&word={quote(uu)}&tn=vsearch&sa=vs_tab&ms=1&atn=index&pn={page}&data_type=json"
        response = requests.get(url, headers=self.headers)  # ,allow_redirects=False
        if response.status_code == 200:
            # 每个网页使用编码都不相同，获取编码格式后指定更改
            cher = response.apparent_encoding
            response.encoding = cher
            content = response.text
            response.close()
            try:
                print('有内容 size：',len(content))
                cc = json.loads(content)
            except Exception as e:
                print(e)
            if 'data' in cc:
                # bool值
                hasMoreResult = cc['data']['hasMoreResult']  # 有更多结果
                hasNextPage = cc['data']['hasNextPage']  # 有下一页
                hasResult = cc['data']['hasResult']  # 有结果
                time.sleep(2)

                if 'datalist' in cc['data']:
                    datalist = cc['data']['datalist']
                    for data in datalist:
                        title = data['title']
                        third_id = re.findall('\d{16}', data['third_id'])
                        if title and third_id:
                            v_sign = data['v_sign']
                            uk = data['uk']
                            name = title.replace('<em>', '').replace('</em>', '')
                            userurl = 'https://author.baidu.com/home/' + str(data['third_id'])
                            if userurl in self.url_list:  #
                                print('重复url返回')
                                continue
                            else:
                                self.url_list.append(userurl)
                            if v_sign:
                                if v_sign == self.wd:
                                    print('**** 找寻到参数对应公司公众号：',name,v_sign)
                                    article_num = self.ajax_article_num(uk)
                                    # 此地 返回百家号账户 和发布文章数量
                                    if article_num:
                                        if not self.content['baijia_article_num'] or int(
                                                self.content['baijia_article_num']) < int(article_num):
                                            self.content['baijia_article_num'] = article_num
                                        if int(self.content['baijia_article_num']) >= int(article_num):
                                            pass
                                    else:
                                        print(f'title:{name}, article_num{article_num}', )

                                    self.content['baijia_name'] = name
                                    self.content['company'] = v_sign
                                    print('>>>>>>>>匹配成功---名称：{},发布数量：{}<<<<<<<<<<'.format
                                          (self.content['baijia_name'], self.content['baijia_article_num']))
                                    self.url_auth.append(userurl)
                            dic = {
                                "title": name,
                                "url": userurl,
                                "company": v_sign,
                            }
                            result_qu.put(dic)

                if hasMoreResult and hasNextPage and hasResult:
                    print('hasMoreResult',hasMoreResult)
                    page += 10
                    return self.baijia_spider(uu,result_qu,page)
                print('无后一页内容..')

    def action_spider(self, q, result_qu):
        print('百家爬取线程启动成功!')
        while q.empty() is not True:
            uu = q.get()
            try:
                self.baijia_spider(uu,result_qu)
            except Exception as e:
                print('baijia_spider 报错:', e)
                continue
            q.task_done()


def start_spider(content):
    start = time.time()
    baijia = BaiDuBaijia(content)
    baijia.run()
    new_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 当前时间
    end_time = time.time() - start
    print('{} 百度百家号成功用时：{}秒'.format(new_time, end_time))


if __name__ == '__main__':

    info = {"wd":"云集市（广州）科技有限公司","brand":"云集市"}
    start_spider(info)
