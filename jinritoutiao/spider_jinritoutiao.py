# -*- coding:UTF-8 -*-

import os
import sys
PATH_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PATH_DIR)

import os
import requests , urllib.parse ,re ,time,json
import logging
logging.captureWarnings(True) # 用于取消requests中 取消SSL认证的报错信息





class JinriToutiao(object):
    def __init__(self):
        self.wd = input('请输入需要查询内容：')
        pages = input('请输入查询的阿拉伯数字页数 (默认第一页，最大不超过5) ： ')
        if pages and int(pages) < 6:
            self.page = int(pages)
        else:
            self.page = 1
        self.n = 0
        self.content = []


    def jinritoutiao_spider(self,cookie):
        if self.wd:
            for pg in range(self.page):
                tmp = int(time.time() * 1000)
                url = 'https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search&offset={pg}&format=json&keyword={wd}&autoload=true&count=20&en_qc=1&cur_tab=1&from=search_tab&pd=synthesis&timestamp={tmp}'.format(pg=pg, wd=urllib.parse.quote(self.wd), tmp= tmp)
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
                    "Cookie" : cookie
                }
                print(url)
                requests.session().keep_alive = False
                res = requests.get(url=url, headers=headers, verify=False)
                if res:
                    res_title = self.jinritoutiao_response(res)
                    if res_title:
                        return 1
        else:
            print('未输入查询内容！')



    def jinritoutiao_response(self,res):

        cotents = json.loads(res.text)
        if 'data' in cotents:
            con = cotents['data']
            for c in con:
                if 'ala_src' in c:
                    if 'toutiao_web' == c.get('ala_src'):
                        title = c.get('title')  #新闻标题
                        summary = c.get('display').get('emphasized').get('summary')  # 内容
                        dic = {"title":title,"content":summary}
                        self.content.append(dic)
                        self.n+=1

                    if 'news' == c.get('ala_src'):
                        if 'merge_article' in c:
                            merge_article = c.get('merge_article')
                            for merge in merge_article:
                                if merge:
                                    title = merge.get('title')  #标题
                                    content = merge.get('abstract')   #内容
                                    dic = {"title": title,"content": content}
                                    self.content.append(dic)
                                    self.n += 1


                if 'abstract' in c:
                    title = c.get('title')
                    content = c.get('abstract')
                    dic = {"title": title,"content": content}
                    self.content.append(dic)
                    self.n += 1


    def set_cookie(self):
        #将文件中的cookie读取出来进行免登录爬取
        #将cookie赋值给 s.cookie
        cookie_list = []
        path_f = os.path.dirname(__file__)
        with open( path_f + "\\jinri_cookie.json", "r") as fp:   #win系统加绝对路径 \\
            try:
                cookies = json.load(fp)
                for dict in cookies:
                    cookie = dict['name'] + '=' + dict['value']
                    cookie_list.append(cookie)
            except Exception as e:
                return None
        #将多个内容用分号拼接
        h_cookie = ';'.join(cookie_list)
        return h_cookie


    def run(self):
        try:
            cookie = self.set_cookie()
            if cookie:
                self.jinritoutiao_spider(cookie)
        except Exception as e:
            pass

        # 打印内容
        for i in self.content:
            print(i)


if __name__ == '__main__':


    jinritoutiao = JinriToutiao()
    jinritoutiao.run()