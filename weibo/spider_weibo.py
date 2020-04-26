import os
import sys

PATH_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PATH_DIR)


import requests, json, random, re, time
from urllib.parse import quote



class WeiBo():
    def __init__(self, wd):
        self.wd = wd
        self.brand_list = []
        self.url = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D3%26q%3D{wd}%26t%3D0&page_type=searchall'  # .format(wd=quote(wd))
        self.weibo_url = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&type=uid&page={page}&containerid=107603{uid}'  # 107603 和下面230283 雷同
        self.home_page_url = 'https://m.weibo.cn/api/container/getIndex?uid={}&type=uid&value={}&containerid=230283{}'
        self.headers = {
            "User-Agent": random.choice(user_agent_list)
        }
        self.iduserlist = []
        self.attitudes_count = []
        self.comments_count = []
        self.reposts_count = []
        self.content = {
            "attitudes": 0,  # 点赞默认为零
            "comments": 0,  # 评论默认为零
            "reposts": 0,  # 转发默认为零
            "followers": 0,  # 粉丝默认为零
            "mouth_count": 0,  # 月发布量默认零
            "wd": "",  # 返回是否有此用户
            "verified": False  # 企业认证默认为 未认证
        }

    def brand_get_requests(self,url):
        n = 0
        while n <= 2:
            try:
                requests.session().keep_alive = False
                response = requests.get(url=url, headers=self.headers, cookies=random_cookies(), timeout=5)
                if response.status_code == 200:
                    cher = response.apparent_encoding# 每个网页使用编码都不相同，获取编码格式后指定更改
                    response.encoding = cher
                    contents = json.loads(response.text)
                    response.close()
                    return contents
                n += 1
            except Exception as e:
                print('函数 brand_get_requests : ',e)
                time.sleep(1)
                if n == 2:
                    return None
                n += 1



    def main(self):
        """
        搜索到内容后，进入各个微博的主页，查看有无公司名称，有的话根据公司对比，如公司对比成功则添加入列表，依次访问遍历
        :return:
        """
        for brand in self.brand_list:
            if brand:
                n = 1
                print('当前品牌：',brand)
                url = self.url.format(wd=quote(brand))
                contents = self.brand_get_requests(url)
                if contents['data']['cards']:
                    group_list = contents['data']['cards']
                    if 'card_group' in group_list[-1]:
                        user_list = group_list[-1]['card_group']
                        # [self.iduserlist.append(user['user']['id']) for user in user_list]  # 将获取到的user id  和user name合并成元组 后添加到idlist
                        brand_content_list = []
                        for user_info in user_list:
                            _name = user_info['user']['screen_name']
                            brand_content_list.append(_name)
                        print('当前参数查询到微博》： ',brand_content_list)

                        for user_info in user_list:
                            verified = user_info['user']['verified']
                            verified_type = user_info['user']['verified_type']
                            if verified and verified_type == 2:  #  保证检测到的为 蓝V 微博
                                user_id = user_info['user']['id']
                                user_name = user_info['user']['screen_name']
                                print(f'当前认证 {n}: {user_name},uid:{user_id}')
                                n += 1
                                home_page_url = self.home_page_url.format(user_id,user_id,user_id)
                                home_json = self.brand_get_requests(home_page_url)
                                if 'data' in home_json:
                                    if 'cards' in home_json['data']:
                                        cards = home_json['data']['cards']
                                        for card in cards:
                                            if 'card_group' in card:
                                                card_group = card['card_group']
                                                for items in card_group:
                                                    if 'item_content' in items:
                                                        item_content = items['item_content']
                                                        if user_name == self.wd:
                                                            self.iduserlist = []  # 重新定义此列表，因找到所查询微博
                                                            self.iduserlist.append(user_id)
                                                            print('检测到输入品牌与微博名称雷同')
                                                            return True
                                                        #再此判定：
                                                        #搜索出的内容是否有公司匹配项，如能够对应上那么加入到列表
                                                        print('检测出认证公司      :      ',item_content)
                                                        self.iduserlist.append(user_id)


    def yes_or_no_verified(self, weibos):
        """
        第二道认证
        包含：1、字段 verified 为 True，2、微博认证中有包含公司名称和品牌的  均为True
        :param weibos:
        :return:
        """
        if 'mblog' in weibos[-1]:
            users = weibos[-1].get('mblog').get('user')
            if users:
                # 根据微博uid进入微博账户页  进行查看是否认证  根据以下三个方法，微博认证，认证公司名称，以及包含公司名称
                if users['verified']:  # 企业是否认证  True or False
                    if self.y_o_n(self.wd,users['verified_reason']):
                        print('verified_reason此微博已认证:', users['screen_name'])
                        self.content['verified'] = True
                    if re.findall(self.wd,users['screen_name']):
                        print('screen_name此微博已认证:', users['screen_name'])
                        self.content['verified'] = True
                return users['screen_name']

    def y_o_n(self,wd,company):

        if wd == company:
            return True


    def parse_time(self, date):

        if re.match('刚刚', date):
            date1 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        if re.match('\d+分钟前', date):
            minute = re.match('(\d+)', date).group(1)
            date1 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() - float(minute) * 60))
        if re.match('\d+小时前', date):
            hour = re.match('(\d+)', date).group(1)
            date1 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() - float(hour) * 60 * 60))
        if re.match('昨天.*', date):
            date = re.match('昨天(.*)', date).group(1).strip()
            date1 = time.strftime('%Y-%m-%d', time.localtime(time.time() - float(24 * 60 * 60))) + ' ' + date + ':00'
        if re.match('\d{2}-\d{2}', date):
            date1 = time.strftime('%Y-', time.localtime()) + date + ' 00:00:00'
        if re.match('\d{4}-\d{2}-\d{2}', date):
            date1 = time.strftime(date) + ' 00:00:00'
        ddq = time.strptime(date1, "%Y-%m-%d %H:%M:%S")
        dd = int(time.mktime(ddq))
        date_log = time.strftime('%Y-%m-%d', time.localtime(time.time() - float(24 * 60 * 60 * 30))) + " 00:00:00"
        date_log = time.strptime(date_log, "%Y-%m-%d %H:%M:%S")
        date_l = int(time.mktime(date_log))  # 此三行为 三十天的时间戳
        if dd >= date_l:
            print(date)
            return True
        else:
            return False

    def get_content(self,iduserlist):
        """
        请求爬取微博发布json数据（此数据包含微博账户的基本内容）
        :param iduserlist:
        :return:
        """
        page = 1
        while True:
            try:
                requests.session().keep_alive = False
                response = requests.get(url=self.weibo_url.format(uid=iduserlist, page=page), headers=self.headers,
                                        cookies=random_cookies())
                if response.status_code == 200:
                    contents = json.loads(response.text)
                    response.close()
                    if contents.get('ok') and contents.get('data').get('cards'):
                        weibos = contents.get('data').get('cards')
                        screen_name = self.yes_or_no_verified(weibos)  # 判断是否未认证企业，不是认证企业并且与查询条件不符 则不进行下一步
                        if self.content['verified'] == False:
                            print('此微博未认证：',screen_name)
                            return False
                        for weibo in weibos:  # 每页十条微博
                            mblog = weibo.get('mblog')
                            if mblog:
                                if 'title' not in mblog:
                                    created_at = mblog['created_at']  # 每条微博发布时间  根据发布时间收集 一下总数
                                    if self.parse_time(created_at):  # 微博发布时间在本月则返回 True  否则返回False
                                        self.attitudes_count.append(mblog['attitudes_count'])  # 点赞数
                                        self.comments_count.append(mblog['comments_count'])  # 评论数
                                        self.reposts_count.append(mblog['reposts_count'])  # 转发
                                    else:
                                        users = mblog['user']
                                        self.content['wd'] = self.wd
                                        if self.attitudes_count:
                                            for attitudes in self.attitudes_count:
                                                self.content['attitudes'] += int(attitudes)
                                        if self.comments_count:
                                            for comments in self.comments_count:
                                                self.content['comments'] += int(comments)
                                        if self.reposts_count:
                                            for reposts in self.reposts_count:
                                                self.content['reposts'] += int(reposts)
                                        self.content['mouth_count'] = len(self.attitudes_count)
                                        self.content['followers'] = users['followers_count']  # 博主粉丝数量
                                        return True  #证明爬取完毕 返回True
                        page += 1  # 此作为条件页数，如发布微博时间在本月，则可加入下一页搜索条件
            except Exception as e:
                print(e)


    def start_requests(self):
        """
        根据添加的 带有公司标签的微博id 进行遍历
        :return:
        """
        if self.iduserlist:
            for iduserlist in self.iduserlist:
                if self.get_content(iduserlist):
                    break
        else:
            print('self.iduserlist数据没有，用户不存在')


    def run(self):

        try:
            self.main()
            self.start_requests()
        except Exception as e:
            print(e)
        return self.content





if __name__ == '__main__':

        wd = '输入要查询的内容'
        weibo = WeiBo(wd)
        res = weibo.run()