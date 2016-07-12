
from selenium import webdriver
import time
from bs4 import BeautifulSoup


driver=webdriver.Chrome('/usr/local/bin/chromedriver')
driver.get("http://www.zhihu.com")
time.sleep(2)
driver.find_element_by_link_text('登录').click()
time.sleep(2)
driver.find_element_by_name('account').send_keys('18570322883')
time.sleep(2)
driver.find_element_by_name('password').send_keys('6129216')
time.sleep(2)
try:
    yanzhengma=input('验证码:')
    driver.find_element_by_name('captcha').send_keys(yanzhengma)
    driver.find_element_by_css_selector('div.button-wrapper.command > button').click()
except:
    print('no capcha or capcha too complicated')
cookie=driver.get_cookies()
time.sleep(3)
driver.get('https://www.zhihu.com/topic/19551137/hot')
# try:
#     element=WebDriverWait(driver,10).until(
#         EC.presence_of_element_located((By.CSS_SELECTOR,'div.zm-topic-list-container > a'))
#     )
# except:
#     print('error')
time.sleep(5)

js="var q=document.body.scrollTop=10000"
def execute_times(times):
    for i in range(times + 1):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
execute_times(10)
html=driver.page_source
soup1=BeautifulSoup(html,'lxml')
authors=soup1.select('a.author-link')
authors_alls=[]
authors_hrefs=[]
for author in authors:
    authors_alls.append(author.get_text())
    authors_hrefs.append('http://www.zhihu.com'+author.get('href'))
authors_intros_urls=soup1.select('span.bio')
authors_intros=[]
for authors_intros_url in authors_intros_urls:
    authors_intros.append(authors_intros_url.get_text())

for authors_all,authors_href,authors_intro in zip(authors_alls,authors_hrefs,authors_intros):
    data={
        'author':authors_all,
        'href':authors_href,
        'intro':authors_intro
    }
    print(data)
