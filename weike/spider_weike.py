#一品威客

import requests
from lxml import etree


epwk_url = 'http://www.epwk.com'


def requests_get(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36", }
    try:
        res = requests.get(url=url,headers=headers,)
        if res.status_code == 200:
            return res
        else:
            return None
    except Exception as e:
        print(e)


def get_shouye_url():
    #  首页获取二级页面
    res = requests_get(epwk_url)
    if res:
        html = etree.HTML(res)
        li_s = html.xpath('//*[@id="show_talent"]/li')
        if li_s:
            href_list = set()
            for li in li_s:
                content = li.xpath('./div[2]/span')
                if content:
                    for i in content:
                        href = i.xpath('./a/@href')
                        if href:
                            ep_link = href[0].replace(' ','')
                            href_list.add(ep_link)
                leftincatys = li.xpath('.//div[@class="leftincaty"]/a/@href')
                if leftincatys:
                    for i in leftincatys:
                        href = i.replace(' ','').replace('\n', '')
                        href_list.add(href)
                letilistcatys = li.xpath('.//div[@class="letilistcaty"]/a/@href')
                if letilistcatys:
                    for i in letilistcatys:
                        href = i.replace(' ','').replace('\n', '')
                        href_list.add(href)
            print('二级链接：',len(href_list))
            # print(href_list)
            return href_list



#{'https://www.epwk.com/talent/dianzhao/?utm_content=cpfl', 'https://www.epwk.com/talent/yxch/?utm_content=cpfl', 'http://www.epzcw.com/shangbiaobg/sbxz.html?epi=930001&utm_source=epwk&utm_medium=banner&utm_campaign=&utm_content=&utm_term=%E5%95%86%E6%A0%87%E6%9F%A5%E8%AF%A2', 'http://www.epzcw.com/zt/zhuanlicx/?utm_source=epwk&utm_content=cpfl', 'https://www.epwk.com/talent/yxui/?utm_content=cpfl', 'https://www.epwk.com/talent/ppqm/?utm_content=cpfl', 'https://www.epwk.com/talent/zhuanyedb/?utm_content=cpfl', 'http://fy.epwk.com/', 'https://www.epwk.com/talent/wangyeui/?utm_content=cpfl', 'https://www.epwk.com/talent/logo/?utm_content=cpfl', 'https://www.epwk.com/talent/haibaosj/?utm_content=cpfl', 'https://www.epwk.com/talent/gysheji/?utm_content=cpfl', 'https://www.epwk.com/talent/youxi/?utm_content=cpfl', 'http://www.youqiwu.com/?utm_source=epwk&utm_content=cpfl', 'https://www.epwk.com/talent/biaoqian/?utm_content=cpfl', 'https://www.epwk.com/talent/qianmingsj/?utm_content=cpfl', 'https://www.epwk.com/talent/jixianwusj/?utm_content=cpfl', 'https://www.epwk.com/talent/jbzz/?utm_content=cpfl', 'https://www.epwk.com/talent/yxdl/?utm_content=cpfl', 'https://www.epwk.com/talent/hdysj/?utm_content=cpfl', 'https://www.epwk.com/talent/duomeiti/?utm_content=cpfl', 'https://www.epwk.com/talent/wxdyy/?utm_content=cpfl', 'https://www.epwk.com/talent/rwfb/?utm_content=cpfl', 'https://www.epwk.com/talent/kejifuwu/?utm_content=cpfl', 'https://www.epwk.com/talent/heka/?utm_content=cpfl', 'https://www.epwk.com/talent/promotion/xiaohongshudaiyunying/?utm_content=cpfl', 'https://www.epwk.com/talent/dhwz/?utm_content=cpfl', 'https://www.epwk.com/talent/duanshipin/?utm_content=cpfl', 'https://www.epwk.com/talent/yilabao/?utm_content=cpfl', 'https://www.epwk.com/talent/vrcj/?utm_content=cpfl', 'https://www.epwk.com/talent/hanhua/?utm_content=cpfl', 'https://www.epwk.com/talent/dpqm/?utm_content=cpfl', 'https://www.epwk.com/talent/duanshipin/taobaoshipin/?utm_content=cpfl', 'https://www.epwk.com/talent/mhwz/?utm_content=cpfl', 'https://www.epwk.com/talent/mtfg/?utm_content=cpfl', 'https://www.epwk.com/talent/hqch/?utm_content=cpfl', 'https://www.epwk.com/talent/webtui/?utm_content=cpfl', 'https://www.epwk.com/talent/mpsj/?utm_content=cpfl', 'https://www.epwk.com/talent/jiqiren/?utm_content=cpfl', 'https://www.epwk.com/talent/wlmt/?utm_content=cpfl', 'https://www.epwk.com/talent/gongye/?utm_content=cpfl', 'https://www.epwk.com/talent/qrs/?utm_content=cpfl', 'https://www.epwk.com/talent/wzmb/?utm_content=cpfl', 'https://www.epwk.com/talent/qiming/?utm_content=cpfl', 'https://www.epwk.com/talent/3ddy/?utm_content=cpfl', 'http://www.epzcw.com/banquan/bqbg.html?epi=930001&utm_source=epwk&utm_medium=banner&utm_campaign=&utm_content=cpfl&utm_term=%E4%BD%9C%E5%93%81%E7%89%88%E6%9D%83', 'https://www.epwk.com/talent/dbsj/?utm_content=cpfl', 'https://www.epwk.com/talent/zhaopai/?utm_content=cpfl', 'https://www.epwk.com/talent/cjkf/?utm_content=cpfl', 'https://www.epwk.com/talent/jjjc/?utm_content=cpfl', 'https://www.epwk.com/talent/stdsj/?utm_content=cpfl', 'https://www.epwk.com/talent/wzkaifa/?utm_content=cpfl', 'http://www.epjike.com/', 'https://www.epwk.com/talent/paiban/?utm_content=cpfl', 'https://www.epwk.com/talent/sjmt/?utm_content=cpfl', 'https://www.epwk.com/talent/ppch/?utm_content=cpfl', 'https://www.epwk.com/talent/swsj/?utm_content=cpfl', 'https://www.epwk.com/talent/dswz/?utm_content=cpfl', 'http://www.epbiao.com/zt/sbcx17/?utm_source=epwk&utm_content=cpfl', 'https://www.epwk.com/talent/qygl/?utm_content=cpfl', 'https://www.epwk.com/talent/cjgj/?utm_content=cpfl', 'https://www.epwk.com/talent/sql/?utm_content=cpfl', 'https://www.epwk.com/talent/xcxtg/?utm_content=cpfl', 'https://www.epwk.com/talent/lipin/?utm_content=cpfl', 'https://www.epwk.com/talent/soft/?utm_content=cpfl', 'https://www.epwk.com/talent/fuzhuang/?utm_content=cpfl', 'https://www.epwk.com/talent/seo/?utm_content=cpfl', 'https://www.epwk.com/talent/qqgp/?utm_content=cpfl', 'https://www.epwk.com/talent/yxtg/?utm_content=cpfl', 'https://www.epwk.com/talent/yyui/?utm_content=cpfl', 'https://www.epwk.com/talent/gjrj/?utm_content=cpfl', 'https://www.epwk.com/talent/xccy/?utm_content=cpfl', 'https://www.epwk.com/talent/wap/?utm_content=cpfl', 'https://www.epwk.com/talent/dhzz/?utm_content=cpfl', 'https://www.epwk.com/talent/dianlu/?utm_content=cpfl', 'http://bang.epwk.com/', 'https://www.epwk.com/talent/weixinyx/?utm_content=cpfl', 'https://www.epwk.com/talent/wswa/?utm_content=cpfl', 'https://www.epwk.com/talent/jdsm/?utm_content=cpfl', 'https://www.epwk.com/talent/logovi/?utm_content=cpfl', 'https://www.epwk.com/talent/qiye/?utm_content=cpfl', 'https://www.epwk.com/talent/jiaohusj/?utm_content=cpfl', 'https://www.epwk.com/talent/qtkf/?utm_content=cpfl', 'http://www.epzcw.com/banquan/bqzr.html?epi=930001&utm_source=epwk&utm_medium=banner&utm_campaign=&utm_content=cpfl&utm_term=%E4%BD%9C%E5%93%81%E7%89%88%E6%9D%83', 'https://www.epwk.com/talent/chanpin/?utm_content=cpfl', 'https://www.epwk.com/talent/wdch/?utm_content=cpfl', 'https://www.epwk.com/talent/wxyx/?utm_content=cpfl', 'https://www.epwk.com/talent/gjrj/shualianzhifu/?utm_content=cpfl', 'https://www.epwk.com/talent/ditui/?utm_content=cpfl', 'https://www.epwk.com/talent/xmch/?utm_content=cpfl', 'https://www.epwk.com/talent/sywa/?utm_content=cpfl', 'https://www.epwk.com/talent/wsyx/?utm_content=cpfl', 'https://www.epwk.com/talent/pcbg/?utm_content=cpfl', 'https://www.epwk.com/talent/duanshipin/jianjipeiyin/?utm_content=cpfl', 'https://www.epwk.com/talent/cych/?utm_content=cpfl', 'https://www.epwk.com/talent/gzhtg/?utm_content=cpfl', 'https://www.epwk.com/talent/kejifuwu/shuangruanpinggu/?utm_content=cpfl', 'https://www.epwk.com/talent/vryx/?utm_content=cpfl', 'https://www.epwk.com/talent/xiezuo/?utm_content=cpfl', 'https://www.epwk.com/talent/duanshipin/huoshanxiaoshipin/?utm_content=cpfl', 'https://www.epwk.com/talent/xcwa/?utm_content=cpfl', 'https://www.epwk.com/talent/wuxian/?utm_content=cpfl', 'https://www.epwk.com/talent/qtmt/?utm_content=cpfl', 'https://www.epwk.com/talent/mtyx/?utm_content=cpfl', 'https://www.epwk.com/talent/weidian/?utm_content=cpfl', 'https://www.epwk.com/talent/baobei/?utm_content=cpfl', 'http://shang.epwk.com/', 'http://www.epzcw.com/shangbiao/dbzc.html?epi=930001&utm_source=epwk&utm_medium=banner&utm_campaign=&utm_content=&utm_term=%E5%95%86%E6%A0%87%E6%9F%A5%E8%AF%A2', 'https://www.epwk.com/talent/henfu/?utm_content=cpfl', 'https://www.epwk.com/talent/seoyh/?utm_content=cpfl', 'https://www.epwk.com/talent/jixie/?utm_content=cpfl', 'https://www.epwk.com/talent/ui/?utm_content=cpfl', 'https://www.epwk.com/talent/dmt/?utm_content=cpfl', 'https://www.epwk.com/talent/wytg/?utm_content=cpfl', 'https://www.epwk.com/talent/zhibeisj/?utm_content=cpfl', 'https://www.epwk.com/talent/jiekou/?utm_content=cpfl', 'http://www.epcsw.com/chaxun/?utm_source=epwk&utm_content=cpfl', 'https://www.epwk.com/talent/bjjd/?utm_content=cpfl', 'http://www.epcsw.com/jizhang/?utm_source=epwk&utm_content=cpfl', 'https://www.epwk.com/talent/gsqm/?utm_content=cpfl', 'https://www.epwk.com/talent/sdcad/?utm_content=cpfl', 'https://www.epwk.com/talent/qitawz/?utm_content=cpfl', 'https://www.epwk.com/talent/crgm/?utm_content=cpfl', 'https://www.epwk.com/talent/zctg/?utm_content=cpfl', 'http://www.epjike.com/ckxm/', 'https://www.epwk.com/talent/huiyuan/?utm_content=cpfl', 'https://www.epwk.com/talent/toupiao/?utm_content=cpfl', 'https://www.epwk.com/talent/juben/?utm_content=cpfl', 'https://www.epwk.com/talent/txrj/?utm_content=cpfl', 'https://www.epwk.com/talent/hcch/?utm_content=cpfl', 'https://www.epwk.com/talent/cpwa/?utm_content=cpfl', 'https://www.epwk.com/talent/qtgjrj/?utm_content=cpfl', 'https://www.epwk.com/talent/arkf/?utm_content=cpfl', 'http://www.epjike.com/cydst/', 'https://www.epwk.com/talent/jsfw/?utm_content=cpfl', 'https://www.epwk.com/talent/yhfa/?utm_content=cpfl', 'https://www.epwk.com/talent/kapian/?utm_content=cpfl', 'https://www.epwk.com/talent/ceshi/?utm_content=cpfl', 'https://www.epwk.com/talent/hdch/?utm_content=cpfl', 'https://www.epwk.com/talent/apptg/?utm_content=cpfl', 'http://www.epzcw.com/gjsb/?epi=930001&utm_source=epwk&utm_medium=banner&utm_campaign=&utm_content=&utm_term=%E5%95%86%E6%A0%87%E6%9F%A5%E8%AF%A2', 'https://www.epwk.com/talent/bbqm/?utm_content=cpfl', 'https://www.epwk.com/talent/cxxg/?utm_content=cpfl', 'https://www.epwk.com/talent/wxtp/?utm_content=cpfl', 'http://www.epjike.com/cyhd/', 'https://www.epwk.com/logo/?utm_content=cpfl', 'https://www.epwk.com/talent/games/?utm_content=cpfl', 'http://zhizao.epwk.com/', 'http://www.epzcw.com/shangbiaobg/sbzx.html?epi=930001&utm_source=epwk&utm_medium=banner&utm_campaign=&utm_content=&utm_term=%E5%95%86%E6%A0%87%E6%9F%A5%E8%AF%A2', 'https://www.epwk.com/talent/wxcx/?utm_content=cpfl', 'https://www.epwk.com/talent/banweisj/?utm_content=cpfl', 'https://www.epwk.com/talent/wxzh/?utm_content=cpfl', 'http://www.epzcw.com/zt/shangbiaozc/?epi=930001&utm_source=epwk&utm_medium=banner&utm_campaign=&utm_content=&utm_term=%E5%95%86%E6%A0%87%E6%9F%A5%E8%AF%A2', 'https://www.epwk.com/talent/ppys/?utm_content=cpfl', 'https://www.epwk.com/talent/ercikf/?utm_content=cpfl', 'https://www.epwk.com/talent/ggch/?utm_content=cpfl', 'https://www.epwk.com/talent/nettui/?utm_content=cpfl', 'https://www.epwk.com/talent/bgrj/?utm_content=cpfl', 'http://www.epbiao.com/zt/banquan/zpbq.html?utm_source=epwk&utm_content=cpfl', 'https://www.epwk.com/talent/bdtg/?utm_content=cpfl', 'https://www.epwk.com/talent/ydtx/?utm_content=cpfl', 'https://www.epwk.com/talent/kejifuwu/renzheng/?utm_content=cpfl', 'http://www.epbiao.com/?utm_source=epwk&utm_content=cpfl', 'https://www.epwk.com/talent/guanggao/?utm_content=cpfl', 'https://www.epwk.com/talent/mtyx/jingjiaguanggao/?utm_content=cpfl', 'https://www.epwk.com/talent/ziti/?utm_content=cpfl', 'https://www.epwk.com/talent/znyj/wulianwang/?utm_content=cpfl', 'http://www.epzcw.com/shangbiaobg/sbbg.html?epi=930001&utm_source=epwk&utm_medium=banner&utm_campaign=&utm_content=&utm_term=%E5%95%86%E6%A0%87%E6%9F%A5%E8%AF%A2', 'https://www.epwk.com/talent/ggyh/?utm_content=cpfl', 'https://www.epwk.com/talent/bkzx/?utm_content=cpfl', 'http://dm.epwk.com/', 'https://www.epwk.com/talent/zbtg/?utm_content=cpfl', 'https://www.epwk.com/talent/pcba/?utm_content=cpfl', 'https://www.epwk.com/talent/wdmb/?utm_content=cpfl', 'https://www.epwk.com/talent/beijing/?utm_content=cpfl', 'https://www.epwk.com/talent/ch/?utm_content=cpfl', 'https://www.epwk.com/talent/zhantaisj/?utm_content=cpfl', 'https://www.epwk.com/talent/yuanxingsj/?utm_content=cpfl', 'https://www.epwk.com/talent/taili/?utm_content=cpfl', 'https://www.epwk.com/talent/cover/?utm_content=cpfl', 'https://www.epwk.com/talent/dykf/?utm_content=cpfl', 'https://www.epwk.com/talent/xtgj/?utm_content=cpfl', 'http://www.epzcw.com/theme/zhuanlishenqing/?utm_source=epwk&utm_content=cpfl', 'https://www.epwk.com/talent/ggy/?utm_content=cpfl', 'https://www.epwk.com/talent/wdfw/?utm_content=cpfl', 'https://www.epwk.com/talent/wangtui/?utm_content=cpfl', 'https://www.epwk.com/talent/hzch/?utm_content=cpfl', 'https://www.epwk.com/talent/h5sj/?utm_content=cpfl', 'https://www.epwk.com/talent/sjcdsj/?utm_content=cpfl', 'https://www.epwk.com/talent/wzdh/?utm_content=cpfl', 'https://www.epwk.com/talent/rjui/?utm_content=cpfl', 'https://www.epwk.com/vrar/?utm_content=cpfl', 'https://www.epwk.com/talent/flash/?utm_content=cpfl', 'https://www.epwk.com/talent/zimt/?utm_content=cpfl', 'https://www.epwk.com/talent/kpzz/?utm_content=cpfl', 'https://www.epwk.com/talent/sb/?utm_content=cpfl', 'http://www.epzcw.com/zt/banquan/rjzzq.html?epi=930001&utm_source=epwk&utm_medium=banner&utm_campaign=&utm_content=cpfl&utm_term=%E8%BD%AF%E4%BB%B6%E8%91%97%E4%BD%9C%E6%9D%83', 'https://www.epwk.com/talent/baozhuang/?utm_content=cpfl', 'https://www.epwk.com/talent/weixinyx/wxhd/?utm_content=cpfl', 'https://www.epwk.com/talent/ebook/?utm_content=cpfl', 'http://www.epwk.com/zt/channel/hezuo/', 'https://www.epwk.com/talent/zjcy/?utm_content=cpfl', 'https://www.epwk.com/talent/vrps/?utm_content=cpfl', 'https://www.epwk.com/talent/kejifuwu/zizhirenzheng/?utm_content=cpfl', 'https://www.epwk.com/talent/duanshipin/douyinshipin/?utm_content=cpfl', 'https://www.epwk.com/talent/jqch/?utm_content=cpfl', 'https://www.epwk.com/talent/caiyesj/?utm_content=cpfl', 'https://www.epwk.com/yingxiao/?utm_content=cpfl', 'https://www.epwk.com/talent/dzsb/?utm_content=cpfl', 'https://www.epwk.com/talent/ppt/?utm_content=cpfl', 'http://www.epcsw.com/?utm_source=epwk&utm_content=cpfl', 'https://www.epwk.com/talent/dsdyy/?utm_content=cpfl', 'https://www.epwk.com/talent/vrkf/?utm_content=cpfl', 'https://www.epwk.com/talent/xwmt/?utm_content=cpfl', 'https://www.epwk.com/talent/qitasj/?utm_content=cpfl', 'http://www.epjike.com/cysl/', 'https://www.epwk.com/talent/sptg/?utm_content=cpfl', 'https://www.epwk.com/talent/ruanjian/chengpin/?utm_content=cpfl', 'http://www.epcsw.com/zhuce/?utm_source=epwk&utm_content=cpfl', 'https://www.epwk.com/talent/ruanjian/pdui/?utm_content=cpfl', 'https://www.epwk.com/talent/waimao/?utm_content=cpfl', 'https://www.epwk.com/talent/aqws/?utm_content=cpfl', 'https://www.epwk.com/talent/dianxiu/?utm_content=cpfl', 'https://www.epwk.com/talent/lpksj/?utm_content=cpfl', 'https://www.epwk.com/talent/cxkf/?utm_content=cpfl', 'https://www.epwk.com/talent/wangyou/youxijianmo/?utm_content=cpfl', 'https://www.epwk.com/talent/bdyh/?utm_content=cpfl', 'https://www.epwk.com/talent/vrdc/?utm_content=cpfl', 'https://www.epwk.com/talent/hyrjkf/?utm_content=cpfl', 'https://www.epwk.com/talent/wxjf/?utm_content=cpfl', 'https://www.epwk.com/talent/zhanshisj/?utm_content=cpfl', 'https://www.epwk.com/talent/weixin/?utm_content=cpfl', 'https://www.epwk.com/talent/nxpsj/?utm_content=cpfl', 'https://www.epwk.com/talent/h5kf/?utm_content=cpfl', 'https://www.epwk.com/talent/ysch/?utm_content=cpfl', 'https://www.epwk.com/talent/vrly/?utm_content=cpfl', 'https://www.epwk.com/talent/znyj/?utm_content=cpfl', 'https://www.epwk.com/talent/kejifuwu/gaoqirending/?utm_content=cpfl', 'http://daka.epwk.com/', 'http://mall.epzcw.com/?epi=930001&utm_source=epwk&utm_medium=banner&utm_campaign=&utm_content=&utm_term=%E5%95%86%E6%A0%87%E6%9F%A5%E8%AF%A2', 'http://www.epzcw.com/zt/banquan/zpbq.html?epi=930001&utm_source=epwk&utm_medium=banner&utm_campaign=&utm_content=cpfl&utm_term=%E4%BD%9C%E5%93%81%E7%89%88%E6%9D%83', 'https://www.epwk.com/talent/kejifuwu/xmsb/?utm_content=cpfl', 'http://dasai.epwk.com/', 'https://www.epwk.com/talent/youxiqt/?utm_content=cpfl', 'https://www.epwk.com/talent/gamesj/?utm_content=cpfl', 'https://www.epwk.com/talent/huacesheji/?utm_content=cpfl', 'https://www.epwk.com/talent/mtyx/pengyouquanguanggao/?utm_content=cpfl', 'https://www.epwk.com/talent/mtyx/xinxiliuguanggao/?utm_content=cpfl', 'https://www.epwk.com/talent/vi/?utm_content=cpfl', 'https://www.epwk.com/talent/rybh/?utm_content=cpfl', 'http://www.epbiao.com/theme/zhuanlishenqing/?utm_source=epwk&utm_content=cpfl', 'https://www.epwk.com/talent/pinpaigs/?utm_content=cpfl', 'https://www.epwk.com/talent/xiezhensj/?utm_content=cpfl', 'https://www.epwk.com/talent/xcp/?utm_content=cpfl', 'https://www.epwk.com/talent/xcdsj/?utm_content=cpfl', 'https://www.epwk.com/talent/haibao/?utm_content=cpfl', 'https://www.epwk.com/talent/wdqm/?utm_content=cpfl', 'javascript:;', 'https://www.epwk.com/talent/yxfa/?utm_content=cpfl', 'http://www.epzcw.com/banquan/bqbz.html?epi=930001&utm_source=epwk&utm_medium=banner&utm_campaign=&utm_content=cpfl&utm_term=%E4%BD%9C%E5%93%81%E7%89%88%E6%9D%83'}
"""
输出如下：
D:\WORKON_HOME\spidervenv\Scripts\python.exe E:/git_spider_obj/spider-obj/weike/spider_weike.py
二级链接： 260
url: https://www.epwk.com/talent/caiyesj/?utm_content=cpfl        page: [' 1 / 42页']
url: https://www.epwk.com/talent/vi/?utm_content=cpfl        page: [' 1 / 340页']
url: https://www.epwk.com/talent/wap/?utm_content=cpfl        page: [' 1 / 121页']
url: https://www.epwk.com/talent/banweisj/?utm_content=cpfl        page: [' 1 / 17页']
url: https://www.epwk.com/talent/dhwz/?utm_content=cpfl        page: [' 1 / 109页']
url: https://www.epwk.com/talent/duanshipin/huoshanxiaoshipin/?utm_content=cpfl        page: [' 1 / 2页']
url: https://www.epwk.com/talent/ebook/?utm_content=cpfl        page: [' 1 / 27页']
url: https://www.epwk.com/talent/henfu/?utm_content=cpfl        page: [' 1 / 59页']
url: https://www.epwk.com/talent/ysch/?utm_content=cpfl        page: [' 1 / 7页']
url: https://www.epwk.com/talent/hdysj/?utm_content=cpfl        page: [' 1 / 48页']
url: https://www.epwk.com/talent/sql/?utm_content=cpfl        page: [' 1 / 56页']
...

"""

def get_two_url(url):
    #爬取二级链接，  商户列表
    #一、先获取底部最大页数
    #二、遍历翻页请求
    #三、获取所有的商铺链接
    res = requests_get(url)
    if res:
        html = etree.HTML(res.text)
        pages = html.xpath('/html/body/div[10]/div[2]/div[1]/div[6]/div[42]/span/text()')
        if pages:
            print('url:',url,'       page:',pages)
            # 分析 可得出每个页面下的所有商铺
            # 可将每个商铺的url进行临时存储， 或者是开多线程 多进程批量请求


def get_three_url():
    #爬取第三级链接，    商户详情页
    #根据标签定位详情
    pass



if __name__ == '__main__':

    href_list = get_shouye_url()
    for url in href_list:
        get_two_url(url)

