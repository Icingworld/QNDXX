import requests
from bs4 import BeautifulSoup
import re
import time
import json
import random


class Login:
    # 登录接口
    url1 = "https://service.jiangsugqt.org/youth/lesson"
    # 确认接口
    url2 = "https://service.jiangsugqt.org/youth/lesson/confirm"
    # 大学习事件接口
    url4 = "https://gqti.zzdtec.com/api/event"
    # 截图接口
    url5 = "https://h5.cyol.com/special/daxuexi/{lesson}/images/end.jpg"

    # 登录请求头 url1
    headers1 = {
        "Host": "service.jiangsugqt.org",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Cookie": "",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.29(0x18001d35) NetType/WIFI Language/zh_CN",
        "Accept-Language": "zh-cn",
        "Accept-Encoding": "gzip, deflate, br"
    }

    # 确认请求头 url2
    headers2 = {
        "Origin": "service.jiangsugqt.org",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Cookie": "",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.29(0x18001d35) NetType/WIFI Language/zh_CN",
        "Accept-Language": "zh-cn",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Referer": "https://service.jiangsugqt.org/youth/lesson/confirm"
    }

    # 获取大学习页面请求头 m.index
    headers3 = {
        "Host": "h5.cyol.com",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Cookie": "",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.29(0x18001d34) NetType/WIFI Language/zh_CN",
        "Accept-Language": "zh-cn",
        "Referer": "https://h5.cyol.com/special/daxuexi/dok1p3vh1x/index.html",
        "Accept-Encoding": "gzip, deflate, br"
    }

    # 事件请求头 event
    headers4 = {
        "Accept": "*/*",
        "Content-Type": "text/plain",
        "Origin": "https://h5.cyol.com",
        "Accept-Language": "zh-cn",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.29(0x18001d34) NetType/WIFI Language/zh_CN",
        "Referer": "https://h5.cyol.com/",
        "Accept-Encoding": "gzip, deflate, br"
    }

    # 截图请求头 end
    headers5 = {
        "Accept": "image/webp,image/png,image/svg+xml,image/*;q=0.8,video/*;q=0.8,*/*;q=0.5",
        "Accept-language": "zh-cn",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.29(0x18001d34) NetType/WIFI Language/zh_CN",
        "Host": "h5.cyol.com",
        "Accept-Encoding": "gzip, deflate, br"
    }

    # 登录
    data1 = {
        "s": "/youth/lesson",
        "from": "singlemessage",
        "isappinstalled": "0"
    }

    # 获取大学习页面 url2
    data2 = {
        "_token": "",
        "lesson_id": ""
    }

    def __init__(self, laravel_session, city):
        self.laravel_session = laravel_session
        self.headers1["Cookie"] = "laravel_session=" + self.laravel_session
        self.headers2["Cookie"] = "laravel_session=" + self.laravel_session
        self.url = ""
        self.key = ["打开页面", "开始学习", "播放完成", "课后答题"]
        self.city = city
        self.info = ""
        self.guid = ""
        self.tc = ""
        self.tn = ""
        self.n = ""
        self.u = ""
        self.r = ""
        self.d = "cyol.com"
        self.w = 390
        self.m = ""

    def login(self):
        # get https://service.jiangsugqt.org/youth/lesson
        requests.get(url=self.url1, headers=self.headers1, params=self.data1)
        # get https://service.jiangsugqt.org/youth/lesson/confirm
        r2 = requests.get(url=self.url2, headers=self.headers1)
        b2 = BeautifulSoup(r2.content, "lxml")
        extract_content = self.extract_content(b2)
        self.data2["token"] = extract_content[0]
        self.data2["lesson_id"] = extract_content[1]
        # post https://service.jiangsugqt.org/youth/lesson/confirm
        r3 = requests.post(url=self.url2, headers=self.headers2, data=self.data2)
        b3 = BeautifulSoup(r3.content, "lxml")
        self.url = self.extract_url(b3)
        self.u = "https://h5.cyol.com/special/daxuexi/%s/m.html" % self.url
        self.r = "https://h5.cyol.com/special/daxuexi/%s/index.html" % self.url
        # get https://h5.cyol.com/special/daxuexi/%s/m.html
        self.headers3["Cookie"] = "wdlast=%s" % self.get_time(11)
        r4 = requests.get(url=self.u, headers=self.headers3)
        b4 = BeautifulSoup(r4.content, "lxml")
        self.info = self.extract_m(b4)
        self.tc = self.get_time(14)
        self.guid = self.generate_guid()

    def run(self):
        info = ["[%s]" % self.info,
                "[%s,\"prov\":\"10\",\"city\":\"%s\"}]" % (self.info, self.city)]
        self.tc = self.get_time(14)
        for i in range(4):
            self.tn = self.get_time(14)
            self.n = self.key[i]
            self.m = info[0] if i == 0 else info[1]
            data3 = {
                "guid": self.guid,
                "tc": self.tc,
                "tn": self.tn,
                "n": self.n,
                "u": self.u,
                "d": self.d,
                "r": self.r,
                "w": 390,
                "m": self.m
            }
            # post https://gqti.zzdtec.com/api/event
            post = requests.post(url=self.url4, headers=self.headers4, data=json.dumps(data3))
            b = BeautifulSoup(post.content, "lxml")
            if "ok" in str(b):
                print("模块 %s 成功" % self.n)
            else:
                raise Exception("登录错误")
            time.sleep(3)

    def save_img(self):
        self.url5 = self.url5.replace("{lesson}", self.url)
        result = requests.get(url=self.url5, headers=self.headers5)
        with open("result.jpg", "wb") as f:
            f.write(result.content)

    @staticmethod
    def extract_content(content: BeautifulSoup) -> tuple:
        token = re.search('[0-9a-zA-Z]{40}', str(content)).group(0)
        lesson_id = re.search("'lesson_id':[0-9]+", str(content)).group(0)
        lesson_id = re.search('[0-9]+', lesson_id).group(0)
        return token, lesson_id

    @staticmethod
    def extract_url(content: BeautifulSoup) -> str:
        url = re.search("daxuexi\\\/[0-9a-zA-Z]+\\\/index.html", str(content)).group(0)[9:-12]
        return url

    @staticmethod
    def extract_m(content: BeautifulSoup) -> str:
        data = json.loads(re.search("打开页面.+;", str(content)).group(0)[8:-3])
        m = "{\"c\":\"%s\",\"s\":\"%s\"}" % (data["c"], data["s"])
        return m

    @staticmethod
    def get_time(i) -> str:
        return str(time.time())[:i].replace(".", "")

    def generate_guid(self) -> str:
        guid = self.generate_num() + self.generate_num() + "-" + self.generate_num() + \
               "-" + self.generate_num() + "-" + self.generate_num() + "-" + \
               self.generate_num() + self.generate_num() + self.generate_num()
        return guid

    @staticmethod
    def generate_num() -> str:
        num = str(hex(random.randint(65536, 131072)))[2:6]
        return num


new = Login("", "")
new.login()
new.run()
new.save_img()
