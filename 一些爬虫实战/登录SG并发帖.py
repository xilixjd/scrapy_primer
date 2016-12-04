from selenium import webdriver
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
# html=driver.page_source
# soup1=BeautifulSoup(html,'lxml')
# imgs=soup1.select('img.vm')
# img_url='http://bbs.sgamer.com/'+(imgs[1].get('src'))
# print(img_url)
# urllib.request.urlretrieve(img_url,'1.jpg')
# img=Image.open('1.jpg')
# img.show()
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
    # if i >150:
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
        tieziRandomInt = random.randint(0, len(tiezis))
        tiezi = tiezis[tieziRandomInt]

        random_tie = random.randint(0, len(tiezis))
        tieziHref = 'http://bbs.sgamer.com/' + tiezi.select('a.s.xst')[0].get('href')
        tiezeTime = tiezi.select('em > span > span')[0].text

        j = 1
        while j <= len(tiezis) - tieziRandomInt:
            if (tieziHref in data_tiezi) or ('昨天' in tiezeTime) or ('前天' in tiezeTime) or ('2016' in tiezeTime) or ('2015' in tiezeTime) or ('2014' in tiezeTime) or ('2013' in tiezeTime) or ('2012' in tiezeTime) or ('2011' in tiezeTime):
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
        time_interval = 30
        time.sleep(time_interval)
    except:
        print('发帖失败')