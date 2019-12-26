import gevent
from lxml import etree
import pymysql
import time, requests

# 使用 协程并发请求页面内容后解析 存入数据库


class AiJiKong(object):
    def __init__(self):
        self.db = pymysql.connect(host='localhost',port=3306,user='root',password='root',charset='utf8')
        self.url = 'https://www.aijikong.com/company/search.php?areaid=40&page={}'
        self.num = 30



    def start_spider(self,url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
            #需添加登陆cookie
            "Cookie":""
        }
        try:
            response = requests.get(url=url, headers=headers)
            if response.status_code == 200:
                # 每个网页使用编码都不相同，获取编码格式后指定更改
                cher = response.apparent_encoding
                response.encoding = cher
                content = response.text
                print(response.url)
                response.close()  # 关闭连接池  以防占用pool资源
                return content
            else:
                print('目标网址请求失败：', response.url)
        except Exception as e:
            print(e)


    def url_lists(self):
        url_list = []
        for url in range(1, self.num):
            u = self.url.format(url)
            url_list.append(u)
        return url_list

    def xpath_content(self,cont):

        html = etree.HTML(cont)
        kuang = html.xpath('//tr')  # 框
        for di in kuang:
            # 公司名称
            names = di.xpath('./td[2]/ul/li[1]/a//text()')
            # 公司主营内容
            contents = di.xpath('./td[2]/ul/li[2]//text()')
            # 是否核实
            verifys = di.xpath('./td[2]/ul/li[3]//text()')
            if names:
                name = names[0]
            if contents:
                content = contents[0].replace(' ', '')
            if verifys:
                verify = verifys[0].replace('\n', '').replace('\xa0', '').replace(' ', '')

            insert_sql = "insert into aijikong (name, content, verify) values ('%s', '%s', '%s')" % (
            name, content, verify)
            try:
                cur = self.db.cursor()
                cur.execute(insert_sql)
                self.db.commit()
                print('保存成功')
            except Exception as e:
                print(e)
                self.db.rollback()



    def run(self):

        url_list = self.url_lists()
        threads_content = [gevent.spawn(self.start_spider, href) for href in url_list]
        gevent.joinall(threads_content)
        for content in [response.value for response in threads_content]:
            if content:
                self.xpath_content(content)






if __name__ == '__main__':
    start = time.time()
    aijikong = AiJiKong()
    aijikong.run()
    print(f'用时:{time.time() - start}秒')