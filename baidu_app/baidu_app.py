import os
import sys



PATH_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PATH_DIR)

from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml import etree
from requests.sessions import RequestsCookieJar
import time, requests, re,logging, json
logging.captureWarnings(True)  # 用于取消requests中 取消SSL认证的报错信息



class BaiduApp(object):

    def __init__(self,wd):
        self.wd = wd
        self.sql_cookie_status = []
        self.brand_list = []
        self.cookies = []
        self.max_html = ''
        self.S = requests.session()
        self.url = 'http://m.baidu.com/s?&word={wd}'
        self.error_status = ""
        self.content = {
            "name" : "",
            "xcx" : ""
        }


    def html_xpath(self,cont):

        one_content = cont.replace(' ', '')
        two_content = re.findall(r'<em>(\w+)</em>-智能小程序', one_content)
        if two_content:
            self.content['xcx'] = two_content[0]
            print('获取到智能小程序：  ', two_content)
            self.save_sql_content(two_content[0],self.wd)
            return True

        html = etree.HTML(cont)
        ss = html.xpath('//script/text()')
        for i in ss:
            aaa = str(i)
            try:
                bbb = json.loads(aaa)
                if 'data' in bbb:
                    if 'title' in bbb['data']:
                        title = bbb['data']['title']
                        ttt = title.replace(' ', '')
                        sss = re.findall(r'<em>(\w+)</em>-智能小程序', ttt)
                        if sss:
                            self.content['xcx'] = sss[0]
                            self.save_sql_content(sss[0], self.wd)
                            print('获取到智能小程序：  ', sss)
                            return True
            except Exception as e:
                self.error_status = str(e)
        print(self.error_status)


    def baiduapp_spider(self):

        url = self.url.format(wd=wd)
        response = self.rsp_content(url)

    def rsp_content(self,url):
        n = 0
        while True:
            time.sleep(2)
            headers = {
                "User-Agent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive",
                "Host": "m.baidu.com",
                "Referer": "http://m.baidu.com/",
                "Upgrade-Insecure-Requests": "1",
            }
            try:
                S = requests.session()
                jar = RequestsCookieJar()
                for c in self.cookies:
                    jar.set(c['name'], c['value'])
                S.cookies.update(jar)
                S.keep_alive = False
                r = S.get(url=url, headers=headers, verify=False, timeout=5) # ,proxies=proxy
            except Exception as e:
                print('百度app请求报错：',e)
                if n==3:
                    break
                continue
            print('请求状态为：',r.status_code, '   >   url：',r.url)
            if r.status_code == 200:
                # 每个网页使用编码都不相同，获取编码格式后指定更改
                cher = r.apparent_encoding
                print('cher:   ', cher)
                # UTF-8-SIG
                if cher == 'Windows-1254':  # 编码值为 Windows-1254
                    cont = r.text.encode(r.encoding).decode('utf-8')
                    r.close()
                    if self.html_xpath(cont):
                        return True
                elif cher == 'ascii':
                    print('charset == ascii，进入下个循环')
                    if n == 10:
                        return None
                    n+=1
                    continue
                else:
                    print(23)
                    r.encoding = cher
                    cont = r.text
                    if self.html_xpath(cont):
                        return True
                break

    def select_sql(self):
        # 查询离线数据有无
        self.cur.execute("select * from baidu_xcx where company = '{}'".format(self.wd))
        result1 = self.cur.fetchone()
        if result1:
            print('已收录')
            self.content['xcx'] = result1[1]
            print(result1)
            return result1

        if self.brand:
            self.cur.execute("select * from baidu_xcx where name = '{}'".format(self.brand))
            result2 = self.cur.fetchone()
            if result2:
                print('已收录')
                self.content['xcx'] = result2[1]
                print(result2)
                return result2


    def save_sql_content(self,name,company):
        # 保存离线数据
        insert_into = 'insert into baidu_xcx( `name`,`company`)value("%s","%s")' % (name,company)
        try:
            self.cur.execute(insert_into)
            self.mysqldb.commit()
            print(f'{self.wd} over!  ')
        except Exception as e:
            print('写入失败: ',e)



    def save_sql(self,cookie):
        # 保存cookie
        insert_into = 'insert into baidu_xcx_cookie( `cookie`)value("%s")' % (cookie)
        try:
            self.cur.execute(insert_into)
            self.mysqldb.commit()
            print('cookie over!  ')
        except Exception as e:
            print('写入失败: ',e)

    def update_cookie(self):

        result = ''#self.select_sql()
        if result:
            pass
            # self.cookies.append(result[1])
        else:
            c_service = Service(self.chromedriver_path)  # chromedriver_path 需自行配置chromedriver路径
            c_service.command_line_args()
            c_service.start()
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')  # 这个配置很重要
            driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=self.chromedriver_path)
            try:
                print(1)
                print('获取移动端cookie')
                url = 'https://m.baidu.com/?tn=&from='
                driver.get(url)
                assert "百度" in driver.title
                time.sleep(3)
                cookie = driver.get_cookies()
                if cookie:
                    # for cook in cookie:
                    self.cookies.append(cookie[0])
                    # print('cookie获取完毕')
                    # print(len(cookie))
                    # print(cookie)
            except Exception as e:
                print(e)
            driver.quit()
            c_service.stop()




    def run(self):

        self.update_cookie()  # 获取cookie  后访问内容
        try:
            self.baiduapp_spider()
        except Exception as e:
            print(e)
        return (self.content['xcx'],)




if __name__ == '__main__':


    wd = '搜索内容'
    baiduapp = BaiduApp(wd)
    baiduapp.run()


