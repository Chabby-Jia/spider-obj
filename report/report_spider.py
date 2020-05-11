


#  目标网址   https://www.questmobile.com.cn/


import requests
import json
import os
import logging
logging.captureWarnings(True)  # 用于取消requests中 取消SSL认证的报错信息




def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        print(path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return False








def get_content(url,num, referer):

    img_url = url + str(num) + '.JPG'
    hreads = {
        "Referer" : referer,
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
    }
    # print(img_url)
    res = requests.get(url=img_url, headers=hreads, verify=False )
    if res.status_code == 200:
        return res






url = 'https://www.questmobile.com.cn/api/v1/research/reports?categoryId=0&labelId=0&version=0&currentPage=1&limit=100'
res = requests.get(url)
# print(res.text)
aa = res.json()
# aa = json.loads(ss)
for i in aa['data']:
    title = i['title']    #标题
    source = i['source']    #作者
    introduction = i['introduction']    # 介绍
    url = i['url']      # 目标url
    bigImgUrl = i['bigImgUrl']   #展示图
    contentImgUrl = i['contentImgUrl']   #内容链接
    publishTime = i['publishTime']    #时间
    contentNum = i['contentNum']    # 内容数量
    categories = i['categories']    #类别
    keywords = i['keywords']    #关键字
    ospath = "F:\\ceshi\\alibaba_shop\\report\\" +title

    if mkdir(ospath):
        print('*' * 20)
        with open(f'{ospath}\\详细信息.txt', 'w') as f:
            f.write(f'标题： {title}\n')
            f.write(f'作者： {source}\n')
            f.write(f'介绍： {introduction}\n')
            f.write(f'目标网址： {url}\n')
            f.write(f'展示图网址： {bigImgUrl}\n')
            f.write(f'发布时间： {publishTime}\n')
            f.write(f'类别： {categories}\n')
            f.write(f'关键字： {keywords}\n')

        for nums in range(1 ,contentNum + 1):
            img_content = get_content(contentImgUrl, nums , url)
            print('----- ', f"{ospath}\\{nums}.jpg" , '')
            with open(f"{ospath}\\{nums}.jpg", "wb")as f:
                f.write(img_content.content)
                print('保存完毕')

