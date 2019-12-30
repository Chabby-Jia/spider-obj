
import requests, re, time, json, logging
from requests import RequestException
from urllib.parse import quote


logging.captureWarnings(True)  # 用于取消requests中 取消SSL认证的报错信息


class BaiduBTwoB(object):
    def __init__(self, wd):
        self.wd = wd
        self.ma_x = []
        self.title = []
        self.title_name = []
        self.content = {
            "name" : "",
        }

    def start_page(self,url):
        n = 0
        while n <= 2:
            try:
                requests.session().keep_alive = False
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
                }
                response = requests.get(url=url, headers=headers, verify=False)
                print(response.status_code,'  >  ',response.url)
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

    def b2b_spider(self):
        #
        url = f'https://b2b.baidu.com/c?q={quote(self.wd)}&from=sug'
        b2b_return = self.start_page(url)
        if b2b_return:
            b2b_content = re.findall('window.data = (.*}]}]});', b2b_return, re.S)
            if b2b_content:
                json_obj = json.loads(b2b_content[0])  # 获取所有json数据 并转为字典格式
                if 'entList' in json_obj:
                    entList = json_obj['entList']
                    for ent in entList:
                        url = ent['jumpUrl']
                        title = ent['title']
                        if title == self.wd:
                            self.content['name'] = title
                            return True
            else:
                print('未找到搜索的厂家...')


    def run(self):

        try:
            self.b2b_spider()
        except Exception as e :
            print(e)
        return self.content




if __name__ == '__main__':

    wd = '郑州豫郑机械设备有限公司'

    start = time.time()
    bb = BaiduBTwoB(wd)
    res = bb.run()
    print(f'返回结果：{res}')
    new_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 当前时间
    end_time = time.time() - start
    print('{} 百度b2b渠道用时：{}秒'.format(new_time,end_time))