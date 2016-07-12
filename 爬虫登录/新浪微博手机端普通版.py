import requests
from bs4 import BeautifulSoup
import urllib.request
from PIL import Image
from lxml import etree

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0',
    "Host": "login.weibo.cn",
    "Origin": "https://login.weibo.cn",
    "Referer": "https://login.weibo.cn/login/"
}

url='http://weibo.cn/1752164320/photo'
url_login='https://login.weibo.cn/login/'
#image_url='http://weibo.cn/interface/f/ttt/captcha/show.php?cpt=4_9d8da92ff4660361'

session=requests.session()

html=session.get(url_login,headers=headers)
soup=BeautifulSoup(html.text,'lxml')
passwords=soup.select('div > input[type="password"]')
password=passwords[0].get('name')
vks=soup.select('div > input[type="hidden"]')
vk=(vks[-2].get('value'))
actions=soup.select('body > div > form')
action=(actions[0].get('action'))
capids=soup.select('div > input[type="hidden"]')
capid=(capids[-1].get('value'))
image_urls=soup.select('div > img')
image_url=(image_urls[0].get('src'))
print(vk+'\n'+action+'\n'+capid)

new_url = url_login + action

file_path='/Users/xilixjd/Desktop/weibo_1.jpg'
urllib.request.urlretrieve(image_url,file_path)
img=Image.open(file_path)
img.show()
code=input('验证码中的字:\n')

data = {
    'mobile': '18610350748',
    'password': '6129216',
    'code': code,
    'remember':'on',
    'backURL':url,
    'backTitle':'微博',
    'tryCount':'',
    'vk':vk,
    'submit':'登录'
}
postdata = {
    "mobile": '18610350748',
    "code": code,
    "remember": "on",
    "backURL": 'http%3A%2F%2Fweibo.cn%2F1752164320%2Fphoto',  # "http%3A%2F%2Fweibo.cn",
    "backTitle": '微博',  # "手机新浪网",
    "tryCount": "",
    "vk": vk,
    "capId": capid,
    "submit": "登录",
    password:'6129216',
}

new_html=session.post(new_url,data=postdata,headers=headers)
index=session.get(url)
soup1=BeautifulSoup(index.text,'lxml')
image_xus=soup1.select('tr td div.c a')
data_image_urls=[]
for image_xu in image_xus:
    data_image_urls.append('http://weibo.cn/'+image_xu.get('href'))
print(data_image_urls)
data_image=session.get(data_image_urls[2])
soup2=BeautifulSoup(data_image.text,'lxml')
data_image_xu_page1s=soup2.select('a img.c')
data_photo_xu_page1=[]
for data_image_xu_page1 in data_image_xu_page1s:
    data_photo_xu_page1.append(data_image_xu_page1.get('src'))
print(data_photo_xu_page1)

# if __name__ == "__main__":
#     cha_code = code
#     # email = input("请输入你的邮箱账号或者手机号码")
#     password_input = input("请输入你的密码")
#     postdata = {
#         "mobile": '18610350748',
#         "code": cha_code,
#         "remember": "on",
#         "backURL": 'http%3A%2F%2Fweibo.cn%2F1752164320%2Fphoto',#"http%3A%2F%2Fweibo.cn",
#         "backTitle": '微博',#"手机新浪网",
#         "tryCount": "",
#         "vk": vk,
#         "capId": capid,
#         "submit": "登录",
#     }
#     postdata[password] = password_input
#     post_url = url_login + action
#     page = session.post(post_url, data=postdata, headers=headers)
#     index = session.get("http://weibo.cn/1752164320/photo")
#     print(index.text)