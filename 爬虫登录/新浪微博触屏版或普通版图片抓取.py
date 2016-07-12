import requests
import re
import json
import base64
import time
import math
import random
from PIL import Image
try:
    from urllib.parse import quote_plus
except:
    from urllib import quote_plus

from bs4 import BeautifulSoup
import os
import urllib.request

'''
3.4
所有的请求都分析的好了
模拟请求 一直不成功
在考虑是哪里出了问题
以后学了新的知识后 再来更新
'''

# 构造 Request headers
agent = 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36'
global headers
headers = {
    "Host": "passport.weibo.cn",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    'User-Agent': agent
}

session = requests.session()
# 访问登录的初始页面
# index_url = "https://passport.weibo.cn/signin/login"
# session.get(index_url, headers=headers)

class yaocheng_tupian:
    def __init__(self,url,page_start,page_end,filename):
        self.index_url="https://passport.weibo.cn/signin/login"
        self.url=url
        self.page_start=page_start
        self.page_end=page_end
        self.filename=filename

    def get_su(self,username):
        """
        对 email 地址和手机号码 先 javascript 中 encodeURIComponent
        对应 Python 3 中的是 urllib.parse.quote_plus
        然后在 base64 加密后decode
        """
        username_quote = quote_plus(username)
        username_base64 = base64.b64encode(username_quote.encode("utf-8"))
        return username_base64.decode("utf-8")


    def login_pre(self,username):
        # 采用构造参数的方式
        params = {
            "checkpin": "1",
            "entry": "mweibo",
            "su": self.get_su(username),
            "callback": "jsonpcallback" + str(int(time.time() * 1000) + math.floor(random.random() * 100000))
        }
        '''真是日了狗，下面的这个写成 session.get(login_pre_url，headers=headers) 404 错误
            这条 3.4 号的注释信息，一定是忽略了 host 的变化，真是逗比。
        '''
        pre_url = "https://login.sina.com.cn/sso/prelogin.php"
        headers["Host"] = "login.sina.com.cn"
        headers["Referer"] = self.index_url
        pre = session.get(pre_url, params=params, headers=headers)
        pa = r'\((.*?)\)'
        res = re.findall(pa, pre.text)
        if res == []:
            print("好像哪里不对了哦，请检查下你的网络，或者你的账号输入是否正常")
        else:
            js = json.loads(res[0])
            if js["showpin"] == 1:
                headers["Host"] = "passport.weibo.cn"
                capt = session.get("https://passport.weibo.cn/captcha/image", headers=headers)
                capt_json = capt.json()
                capt_base64 = capt_json['data']['image'].split("base64,")[1]
                with open('capt.jpg', 'wb') as f:
                    f.write(base64.b64decode(capt_base64))
                    f.close()
                im = Image.open("capt.jpg")
                im.show()
                im.close()
                cha_code = input("请输入验证码\n>")
                return cha_code, capt_json['data']['pcid']
            else:
                return ""


    def login(self,username, password, pincode):
        postdata = {
            "username": username,
            "password": password,
            "savestate": "1",
            "ec": "0",
            "pagerefer": "",
            "entry": "mweibo",
            "wentry": "",
            "loginfrom": "",
            "client_id": "",
            "code": "",
            "qq": "",
            "hff": "",
            "hfp": "",
        }
        if pincode == "":
            pass
        else:
            postdata["pincode"] = pincode[0]
            postdata["pcid"] = pincode[1]
        headers["Host"] = "passport.weibo.cn"
        headers["Reference"] = self.index_url
        headers["Origin"] = "https://passport.weibo.cn"
        headers["Content-Type"] = "application/x-www-form-urlencoded"

        post_url = "https://passport.weibo.cn/sso/login"
        login = session.post(post_url, data=postdata, headers=headers)
        # print(login.cookies)
        # print(login.status_code)
        js = login.json()
        # print(js)
        uid = js["data"]["uid"]
        crossdomain = js["data"]["crossdomainlist"]
        # print(crossdomain)
        # cn = "https:" + crossdomain["sina.com.cn"]
        # 下面两个对应不同的登录 weibo.com 还是 m.weibo.cn
        # 一定要注意更改 Host
        mcn = "https:" + crossdomain["weibo.cn"]
        # com = "https:" + crossdomain['weibo.com']
        headers["Host"] = "login.sina.com.cn"
        session.get(mcn, headers=headers)
        headers["Host"] = "m.weibo.cn"

    def get_image_urls(self):
        page_start=self.page_start
        page_end=self.page_end
        url=self.url
        data=[]
        for i in range(page_start,page_end+1):
            real_url=url+str(i)
            ht = session.get(real_url,headers=headers)
            # print(ht.url)
            # print(session.cookies)

            pa = r'<title>(.*?)</title>'
            # res = re.findall(pa, ht.text)
            # print("你好%s，你正在使用 xchaoinfo 写的模拟登录" % res[0])
            # print(cn, com, mcn)

            soup1 = BeautifulSoup(ht.text, 'lxml').text
            encodedjson = json.dumps(soup1)
            pa = r'\"pic_small\\\"\:\\(.*?)\.jpg\\\"'
            res = re.findall(pa, encodedjson)
            for res_1 in res:
                data.append(res_1[1:].replace('\\', '') + '.jpg')
        return data

    def get_path(self):
        filename=self.filename
        path=os.getcwd()+'/'+filename+'/'
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def save_images(self):
        path=self.get_path()
        images_urls=self.get_image_urls()
        print(images_urls)
        try:
            count=0
            for image_url in images_urls:
                count += 1
                print('正在保存第%d张照片:%s'%(count,image_url))
                urllib.request.urlretrieve(image_url,path+str(count)+'.jpg')
            print('Download success')
        except:
            print('Download fail')

if __name__ == "__main__":

    username = "18610350748"
    password = "6129216"
    yao_url_main='http://m.weibo.cn/page/json?containerid=103003index1266321801_-_photo_all_l&page='
    xu_url_main='http://m.weibo.cn/page/json?containerid=103003index1752164320_-_photo_all_l&page='
    t_ara_url_main='http://m.weibo.cn/page/json?containerid=103003index1810528510_-_photo_all_l&page='
    file_name='T-ara'
    class_1=yaocheng_tupian(t_ara_url_main,1,1000,file_name)
    pincode = class_1.login_pre(username)
    class_1.login(username, password, pincode)
    class_1.save_images()