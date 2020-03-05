from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import requests
import Geohash
import urllib.request
import urllib.parse
import json
import random
from time import sleep


#  各个市区名称  https://www.ele.me/restapi/shopping/v1/cities

class ElemeSpider():


    def get_city(slef):
        url_city = 'https://www.ele.me/restapi/shopping/v1/cities'
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }
        request = urllib.request.Request(url=url_city, headers=headers)
        slef.json_text = urllib.request.urlopen(request).read().decode()
        slef.json_obj = json.loads(slef.json_text) #获取所有城市json数据 并转为字典格式

        slef.objs = []
        for i in slef.json_obj:
            for j in slef.json_obj[i]:
                slef.objs.append(j)

        #{'abbr': 'AX', 'id': 608, 'latitude': 38.935349, 'longitude': 115.935638, 'name': '安新', 'pinyin': 'anxin'}
        # 城市参数 有  latitude 和 longitude   这两个参数是 经纬度 用于后面的url输入 以及 经纬度计算
        slef.city_all = []
        for city in slef.objs: slef.city_all.append(city['name'])
        slef.name = input("请输入您要下载数据的城市：")
        while slef.name not in slef.city_all:
                    name = input('输入错误!!!   请重新输入：')
        for slef.ci in slef.objs:
            if slef.ci['name'] == slef.name:
                slef.latitude = slef.ci['latitude']
                slef.longitude = slef.ci['longitude']
                return slef.latitude, slef.longitude, slef.name

    def get_page(slef):
        ## 整合url    获取json数据
        slef.url = 'https://www.ele.me/restapi/shopping/restaurants?extras%5B%5D=activities&geohash={geohash}&latitude={latitude}&limit=24&longitude={longitude}&offset={offset}&terminal=web'.format(
            geohash=slef.g, latitude=slef.latitude, offset=slef.limit_num, longitude=slef.longitude)

        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
            # "Cookie": "ubt_ssid=svtvgn7ep4drs469ugn5dt8uyy1eup6z_2019-02-18;cna=cTzDFCkqImcCAT2jiRe1Kpzu;_utrace=513c3b5f731e7ec61b6074db91ceca8f_2019-05-13;track_id=1557720030|78a0d91f4d21b175fe023ccbc02a537ce3521d70589a232a06|28ad797b23a60dc91ec9c4a88a48c211;USERID=1455542994;UTUSER=1455542994;SID=686uNd5uE82DP7buje8eUdsq2BqR8o6rfLeQ",
            "Cookie": "ubt_ssid=hho78270acbwbes4xcmp9scrxb38pj8l_2019-05-13;cna=cTzDFCkqImcCAT2jiRe1Kpzu;track_id=1557763499|f5dfc8f26b695678fbb6bc91251842448202e4fb95e5055833|db79e04421857b679cf347393a59dd94;pizza73686f7070696e67=BWqMca04FSHEC-VmsFYh-MXIgx-KcjUV5XSdbRhrQ_VGisiBEi5A7_tFG3YwyQi6;USERID=6155587978;UTUSER=6155587978;SID=eEBQdPdAvOmoFfSIvLJhDrIfV2t5cIU9ikHA;",
        }
        re = json.loads(requests.get(slef.url, headers=headers).text)
        print('正在载入中......')

        ##写入文件
        f = open('elm.txt', 'w', encoding='utf-8')
        for i in re:
                f.write('----------------------------------------\n')
                f.write('店名：' + str(i.get('name')) + '\n')
                f.write('月销售量：' + str(i.get('recent_order_num')) + '\n')
                f.write('地址：' + str(i.get('address')) + '\n')
                f.write('配送费：' + str(i.get('float_delivery_fee')) + '\n')
                f.write('配送时间：' + str(i.get('order_lead_time')) + '\n')
                f.write('距离：' + str(i.get('distance')) + '\n')
                f.write('起送价：' + str(i.get('float_minimum_order_amount')) + '\n')
                f.write('评分：' + str(i.get('rating')) + '\n')

        f.close()
        print('爬取完毕')

    def selen_auto(slef):
        """可使用无头，直接自动化操作谷歌会更直观点，的登录的时候好操作"""
        #  https://www.ele.me/place/ws105tg30kcy?latitude=22.531784&longitude=114.064535
        # 先使用无头浏览器动态加载页面，而后记录最终数据量的标签汇总，记录limit的值
        # 根据 limit进行爬取，非无头爬取
        # chrome_options = Options()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        # 驱动路径
        # path = r'D:\workon_home\venv_scrapt\Scripts\chromedriver.exe'
        # 创建浏览器对象
        # browser = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)
        browser = webdriver.Chrome()

        slef.g = Geohash.encode(slef.latitude, slef.longitude)
        phone = str(input('请输入手机号码进行登录：'))
        url_log= 'https://h5.ele.me/login/#redirect=https%3A%2F%2Fwww.ele.me%2Fhome%2F'
        browser.get(url_log)
        print('获取登陆页面')
        sleep(random.uniform(1, 3))
        browser.find_element_by_xpath('//input[@placeholder="手机号"]').send_keys(phone[:3])#模拟输入手机号前三位
        sleep(random.uniform(1, 3))
        browser.find_element_by_xpath('//input[@placeholder="手机号"]').send_keys(phone[3:7])#模拟输入手机号中间三
        sleep(random.uniform(1, 3))
        browser.find_element_by_xpath('//input[@placeholder="手机号"]').send_keys(phone[7:])#输入手机号后四位
        sleep(random.uniform(1, 3))
        print('手机号码输入完毕！')
        browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/form/section[1]/button').click() #点击获取验证码
        sleep(random.uniform(1, 3))
        print('点击验证码！')

        try:
            code_jpg = browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div/div')#是否有图形验证码
            code_root = browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div/div')#是否有跟状验证码

            # //*[@id="nc_1_n1z"]
            #判断 如果有图形验证码
            if code_jpg:
                print('图形验证码已保存！')
                browser.save_screenshot("图形验证码.png")
                sleep(random.uniform(2,3))
                img_code = input('请输入图形验证码：')
                browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div/div/div[1]/div/input').send_keys(img_code[:2])
                sleep(random.uniform(1,2))
                browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div/div/div[1]/div/input').send_keys(img_code[2:])
                sleep(random.uniform(1,2))
                # 点击确定
                browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div/div/div[2]/button[2]').click()
                sleep(random.uniform(1,2))
            elif code_root:
                print('正在进行条形验证码验证！')

        except Exception as e:
            print(e)
        finally:
            sleep(random.uniform(1,3))
            send_code = str(input('请输入验证码：'))
            browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/form/section[2]/input').send_keys(send_code)#填写验证码
            sleep(random.uniform(1,3))
            browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/form/button').click() #点击登陆按钮
            print('点击登陆按钮')
            sleep(random.uniform(1,5))

            # 经纬计算这个库进行 geohash计算
            slef.g = Geohash.encode(slef.latitude, slef.longitude)

            url_ = 'https://www.ele.me/place/{geohash}?latitude={latitude}&longitude={longitude}'.format(
                geohash=slef.g, latitude=slef.latitude, longitude=slef.longitude)
            browser.get(url_)
            sleep(random.uniform(1, 3))


            ##模拟鼠标向下滚动
            m = 0
            while m < 6 :
                n = 0
                while n < 6:
                    #模拟鼠标滚动向下，距离3000
                    browser.execute_script("window.scrollBy(0,3000)")
                    sleep(random.uniform(1, 3))
                    n += 1
                    print('滚动第{}次'.format(n))
                try:
                    click_gengduo = browser.find_element_by_id('fetchMoreRst')  # 判断是否有点击更多按钮
                    m += 1
                    if click_gengduo:
                        sleep(random.uniform(1, 3))
                        print('点击更多按钮第{}次'.format(m))
                        browser.find_element_by_id('fetchMoreRst').click()
                        sleep(random.uniform(1, 3))
                except Exception as e:
                    print('没有点击按钮出现，跳出循环')
                    print(e)
                    break
            print('查看商家个数，定位中...')
            slef.limit_len = browser.find_elements_by_xpath('//a[contains(@href, "/shop")]')
            sleep(random.uniform(1, 3))
            slef.limit_num = len(slef.limit_len)
            print('{name}地区的商家总共有：{len}家!'.format(name = slef.name,len=slef.limit_num))

            browser.quit()



if __name__ == '__main__':
    eleme = ElemeSpider()
    eleme.get_city() #首先获取所有城市地区
    eleme.selen_auto()
    eleme.get_page()
