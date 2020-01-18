
import json
import requests
from lxml import etree
from lxml.etree import tostring
import re
from urllib.parse import quote
import time


"""

带有反爬，单个ip访问频繁会跳出点击验证码，以及点选文字坐标验证码
具体破解方法可查看博客：https://blog.csdn.net/weixin_41767339

"""


city = 'bj'  #爬取城市首拼字母

xiaoqu = '昌平'  #爬取 哪个区




def lianjiaspider(xiaoqu,pg=1):
    if pg:
        home_url = f'https://{city}.lianjia.com/xiaoqu/pg{pg}rs{quote(xiaoqu)}/'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': f'{city}.lianjia.com',
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
        }

        # 获取lianjia_uuid
        req = requests.get(home_url, headers=headers)
        if req.status_code == 200:
            cher = req.apparent_encoding
            content = req.text

            html = etree.HTML(content)

            all_content_num = html.xpath('/html/body/div[4]/div[1]/div[2]/h2')[0].xpath('string(.)')
            print(all_content_num)
            all_ul = html.xpath('//div[@class="leftContent"]/ul/li')
            for data_info in all_ul:
                title = data_info.xpath('./div[@class="info"]/div[@class="title"]/a/text()')
                houseInfo = data_info.xpath('./div[@class="info"]/div[@class="houseInfo"]')[0].xpath('string(.)').replace(' ','').replace('\n','')
                positionInfo = data_info.xpath('./div[@class="info"]/div[@class="positionInfo"]')[0].xpath('string(.)').replace(' ','').replace('\n','')
                totalPrice_priceDesc = data_info.xpath('./div[@class="xiaoquListItemRight"]')[0].xpath('string(.)').replace(' ','').replace('\n','') #/div[@class="totalPrice"]
                totalSellCount = data_info.xpath('.//div[@class="xiaoquListItemSellCount"]')[0].xpath('string(.)').replace(' ','').replace('\n','')
                print(title[0] + ',  ' + houseInfo + ',  ' + positionInfo + ',  ' , totalPrice_priceDesc + ',  ' + totalSellCount)

            # 页码属于渲染成 requests爬取不到，然而标签中携带的有页码总数，正则出即可
            pages = html.xpath('//*[@class="page-box house-lst-page-box"]')   #[0].xpath('string(.)').replace(' ','').replace('\n','')
            aa = tostring(pages[0], encoding=cher).decode(cher)   # xpath中定位到标签后，输出标签的所有字符
            bb = re.findall('page-data="(.*)"/>',aa)[0].replace('&quot;','"')
            cc = json.loads(bb)
            page_all_num = cc.get('totalPage')  # 总页数
            if pg == page_all_num:
                return True
            print(f'当前爬取第{pg}页完毕')
            print('*'*50, page_all_num)
            pg+=1
            time.sleep(2)
            return lianjiaspider(pg=pg,xiaoqu=xiaoqu)



lianjiaspider(xiaoqu)