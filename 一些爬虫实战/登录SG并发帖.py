from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random

driver=webdriver.Chrome()
driver.get("http://bbs.sgamer.com/member.php?mod=logging&action=login")
driver.find_element_by_name('username').send_keys('xilixjd1')
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
    try:
        driver.get('http://bbs.sgamer.com/forum-44-1.html')
        time.sleep(2)

        shouye_html=driver.page_source
        soup1=BeautifulSoup(shouye_html,'lxml')
        tiezis=soup1.select('a.s.xst')

        random_tie=random.randint(15,51)
        tiezi='http://bbs.sgamer.com/'+tiezis[random_tie].get('href')
        if tiezi in data_tiezi:
            continue
        data_tiezi.add(tiezi)

        time.sleep(2)
        driver.get(tiezi)
        tiezi_html=driver.page_source
        time.sleep(3)
        soup2=BeautifulSoup(tiezi_html,'lxml')
        titles=soup2.select('#thread_subject')
        title=titles[0].get_text()
        # tiezi_content = soup2.select('tbody > tr > td.plc > div.pct > div > div.t_fsz > table > tbody > tr')
        # print(tiezi_content[0])


        time.sleep(3)
        driver.find_element_by_css_selector('#vmessage').clear()
        driver.find_element_by_css_selector('#fastpostmessage').send_keys(title)
        time.sleep(3)
        driver.find_element_by_id('fastpostsubmit').click()
        i+=1
        print('第%d贴'%i)
        time.sleep(random.randint(15,18))
    except:
        print('发帖失败')