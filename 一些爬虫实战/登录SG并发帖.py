from selenium import webdriver
import urllib
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import random
import datetime

driver=webdriver.Chrome()
driver.set_page_load_timeout(15)
driver.get("http://bbs.sgamer.com/member.php?mod=logging&action=login")
driver.find_element_by_name('username').send_keys('react')
driver.find_element_by_name('password').send_keys('6129216')
html=driver.page_source
soup1=BeautifulSoup(html,'lxml')
imgs=soup1.select('img.vm')
img_url='http://bbs.sgamer.com/'+(imgs[1].get('src'))
print(img_url)
urllib.request.urlretrieve(img_url,'1.jpg')
# img=Image.open('1.jpg')
# img.show()

import json
#----------------------------------
# 验证码识别调用示例代码 － 聚合数据
# 在线接口文档：http://www.juhe.cn/docs/60
#----------------------------------

#识别验证码
def request1(appkey, m="GET"):
    url = "http://op.juhe.cn/vercode/index"
    params = {
        "key" : appkey, #您申请到的APPKEY
        "codeType" : "", #验证码的类型，&lt;a href=&quot;http://www.juhe.cn/docs/api/id/60/aid/352&quot; target=&quot;_blank&quot;&gt;查询&lt;/a&gt;
        "image" : "", #图片文件
        "dtype" : "", #返回的数据的格式，json或xml，默认为json
    }
    params = urllib.parse.urlencode(params)
    if m =="GET":
        f = urllib.urlopen("%s?%s" % (url, params))
    else:
        f = urllib.urlopen(url, params)

    content = f.read()
    res = json.loads(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            #成功请求
            print(res["result"])
        else:
            print("%s:%s" % (res["error_code"],res["reason"]))
    else:
        print("request api error")

#配置您申请的APPKey
appkey = "50b734d08501000d5e5a5ff9d7e6d750"
#1.识别验证码
request1(appkey,"POST")

yanzhengma=input('yanzhengma:')
driver.find_element_by_name('seccodeverify').send_keys(yanzhengma)
driver.find_element_by_name('loginsubmit').click()
cookie=driver.get_cookies()
time.sleep(4)
i=0
data_tiezi=set()
while True:
    date_hour = int(datetime.datetime.now().strftime('%H'))
    # date_min = int(datetime.datetime.now().strftime('%M'))
    # if i > 150:
    #     break
    # if 0 <= date_hour <= 8:
    #     break
    try:
        driver.get('http://bbs.sgamer.com/forum-44-1.html')
        time.sleep(2)

        shouye_html=driver.page_source
        soup1=BeautifulSoup(shouye_html,'lxml')
        tiezisHtml = soup1.select('tbody > tr')
        tiezisHtmlCut = ""
        for bs4Tag in tiezisHtml[21:]:
            tiezisHtmlCut += str(bs4Tag)

        tiezisHtmlCutSoup = BeautifulSoup(tiezisHtmlCut, 'lxml')

        tiezis = tiezisHtmlCutSoup.select('tr')
        # tieziRandomInt = random.randint(0, len(tiezis))
        tieziRandomInt = 0
        tiezi = tiezis[tieziRandomInt]

        random_tie = random.randint(0, len(tiezis))
        tieziHref = 'http://bbs.sgamer.com/' + tiezi.select('a.s.xst')[0].get('href')
        tiezeTime = tiezi.select('em > span > span')[0].text

        j = 1
        while j <= len(tiezis) - tieziRandomInt:
            if (tieziHref in data_tiezi) or ('天前' in tiezeTime) or ('昨天' in tiezeTime) or ('前天' in tiezeTime) or ('2016' in tiezeTime) or ('2015' in tiezeTime) or ('2014' in tiezeTime) or ('2013' in tiezeTime) or ('2012' in tiezeTime) or ('2011' in tiezeTime):
                tieziHref = 'http://bbs.sgamer.com/' + tiezis[tieziRandomInt + j].select('a.s.xst')[0].get('href')
                tiezeTime = tiezis[tieziRandomInt + j].select('em > span > span')[0].text
                j += 1
            else:
                break
        if j == len(tiezis) - tieziRandomInt:
            continue

        time.sleep(2)
        driver.get(tieziHref)
        tiezi_html=driver.page_source
        time.sleep(3)
        soup2=BeautifulSoup(tiezi_html,'lxml')
        titles=soup2.select('#thread_subject')
        title=titles[0].get_text()
        if ('react' in title) or ('脚本' in title) or ('举报' in title) or ('测试' in title) or ('test' in title) or ('机器' in title):
            continue
        # tiezi_content = soup2.select('div#postlist > div > table > tbody > tr> td.plc > div.pct > div > div.pcbs > table > tbody > tr')
        # print(tiezi_content)


        time.sleep(3)
        driver.find_element_by_css_selector('#vmessage').clear()
        driver.find_element_by_css_selector('#fastpostmessage').send_keys(title)
        time.sleep(3)
        driver.find_element_by_id('fastpostsubmit').click()
        i+=1
        print('第%d贴'%i, tiezeTime + " " + title + " " + tieziHref)
        data_tiezi.add(tieziHref)
        time_interval = 50
        time.sleep(time_interval)
    except:
        print('发帖失败')