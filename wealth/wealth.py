import json,time,pymysql,requests



class FourStockIndex():
    def __init__(self):

        # self.conn = pymysql.Connect(host='localhost', port=3306, user='root', password='root', db='test', charset='utf8')
        # self.cursor = self.conn.cursor()

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        }
        """上证指数"""
        self.sh_url = 'http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?rtntype=5&token=4f1862fc3b5e77c150a2b985b12db0fd&cb=jQuery18309808793516462408_1539585111859&id=0000011&type=k&authorityType=&_=1539585113584'
        """大盘"""
        self.dapan_url = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=0000011,3990012,3990052,3990062,hsi5,djia7&sty=MPNSBAS&st=&sr=1&p=1&ps=1000&token=44c9d251add88e27b65ed86506f6e5da&cb=callback018720109689918307&callback=callback018720109689918307&_=1540540619917'
        """深圳指数"""
        self.sz_url = 'http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?rtntype=5&token=4f1862fc3b5e77c150a2b985b12db0fd&cb=jQuery183011483300704417188_1539584931316&id=3990012&type=k&authorityType=&_=1539584933273'
        """中小板"""
        self.medium_small_url = 'http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?rtntype=5&token=4f1862fc3b5e77c150a2b985b12db0fd&cb=jQuery18302147018577210933_1539655549453&id=3990052&type=k&authorityType=&_=1539655551470'
        """创业板"""
        self.start_business_url = 'http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?rtntype=5&token=4f1862fc3b5e77c150a2b985b12db0fd&cb=jQuery18309792964848165895_1539655433458&id=3990062&type=k&authorityType=&_=1539655435548'

    def __request(self,url):
        #请求
        response = requests.get(url=url,headers=self.headers)
        if response.status_code == 200:
            # 每个网页使用编码都不相同，获取编码格式后指定更改
            cher = response.apparent_encoding
            response.encoding = cher
            content = response.text
            response.close()
            return content


    def StartBusiness(self):
        res = self.__request(self.medium_small_url)
        json_text = res.replace('jQuery18309792964848165895_1539655433458(','').replace(')','')
        obj = json.loads(json_text)
        print(type(obj))
        print(obj)
        self.filter_content(obj)


    def MediumSmallIndex(self):
        res = self.__request(self.medium_small_url)
        json_text = res.replace('jQuery18302147018577210933_1539655549453(','').replace(')','')
        obj = json.loads(json_text)
        print(type(obj))
        print(obj)
        self.filter_content(obj)


    def ShenZhenIndex(self):
        res = self.__request(self.sz_url)
        json_text = res.replace('jQuery183011483300704417188_1539584931316(','').replace(')','')
        obj = json.loads(json_text)
        print(type(obj))
        print(obj)
        self.filter_content(obj)

    def ShangHaiIndex(self):
        res = self.__request(self.sh_url)
        json_text = res.replace('jQuery18309808793516462408_1539585111859(','').replace(')','')
        obj = json.loads(json_text)
        print(type(obj))
        print(obj)
        self.filter_content(obj)



    def dapan_rise_and_fall(self):
        #大盘个股
        res = self.__request(self.dapan_url)
        json_text = res.replace('callback018720109689918307(','').replace(')','')
        objs = json.loads(json_text)
        return objs

    def filter_content(self,obj):
        # 抓取内容：股票名称、今收盘，昨收，
        info_list = obj['info']
        # 名称
        name = obj['name']
        # 代码
        code = obj['code']
        # 今开
        now_open = info_list['o']
        now_open = float(now_open)
        # 今收
        now_harvest = info_list['c']
        now_harvest = float(now_harvest)
        # 昨收
        long_harvest = info_list['yc']
        long_harvest = float(long_harvest)
        # 最高
        h = info_list['h']
        h = float(h)
        # 最低
        l = info_list['l']
        l = float(l)
        if now_harvest > long_harvest:
            add_sub = 'up'
        else:
            add_sub = 'down'
        if now_open > now_harvest:
            yin_yang = 'yin'
        else:
            yin_yang = 'yang'
        data = obj['data']
        # 2018-10-19,2460.08,2550.47,2553.39,2449.20,147323558,130095923200,4.19%,0.44
        last = data[-1]
        last = last.split(',')  # 逗号切割 取其中的数据
        # ['2018-10-19', '2460.08', '2550.47', '2553.39', '2449.20', '147323558', '130095923200', '4.19%', '0.44']
        amplitude = last[-2]  # 振幅
        # 时间
        day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        # 涨跌幅
        raf = self.dapan_rise_and_fall()
        objs = raf.split(',')
        rise_and_fall = objs[4]
        print(rise_and_fall)
        # rise_and_fall = re.sub(r'%', '', raf)
        # rise_and_fall = (rise_and_fall)


    def run(self):
        self.ShangHaiIndex()


if __name__ == '__main__':

    stockindex = FourStockIndex()
    stockindex.run()