import requests
import rsa
import binascii
import hashlib
import execjs
import random
import json
import time
import urllib.parse as parse
from process_img import proc
from w import boom

t = int(time.time()*1000)
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        "Referer": "https://www.geetest.com/show/",
    }
session = requests.Session()
# 请求携带数据接口
def get_gt_challenge():
    url = "https://www.geetest.com/demo/gt/register-slide-official?t={}".format(str(int(time.time()*1000)))
    data = json.loads(session.get(url,headers=headers).text)
    return data

def get_captcha_info(data):
    params = {
        "is_next": "true",
        "type": "slide3",
        "gt": data["gt"],
        "challenge": data["challenge"],
        "lang": "zh-cn",
        "https": "true",
        "protocol": "https://",
        "offline": "false",
        "product": "embed",
        "api_server": "api.geetest.com",
        "isPC": "true",
        "width": "100%",
        "callback": "geetest_{}".format(str(int(time.time()*1000))),
    }
    url1 = "https://api.geetest.com/ajax.php"
    url = "https://api.geetest.com/get.php?is_next=true&type=slide3&gt={}&challenge={}&lang=zh-cn&https=true&protocol=https://&offline=false&product=embed&api_server=api.geetest.com&isPC=true&width=100%25&callback=geetest_{}".format(data["gt"],data["challenge"],str(int(time.time()*1000)))
    session.get(url1,params=params)
    response = session.get(url)
    # print(response.text[22:-1])
    return json.loads(response.text[22:-1])

def process_info(data):
    full_path = "full.png"
    bg_path = "bg.png"
    download_cap("https://static.geetest.com/"+data["fullbg"],full_path)
    download_cap("https://static.geetest.com/"+data["bg"],bg_path)
    info = {
        "full_img_url": full_path,
        "bg_img_url": bg_path,
        "s": 'data["s"]',
        "gt": 'data["gt"]',
        "challenge": 'data["challenge"]',
        "c": 'data["c"]',
    }
    return info

def download_cap(url,path):
    response = requests.get(url)
    with open(path,"wb") as f:
        f.write(response.content)

def px2track(px):
    pass

if __name__ == '__main__':
    # 获取接口信息
    data = get_gt_challenge()

    # 处理接口信息并下载验证码图片
    cap_info = process_info(get_captcha_info(data))
    print(cap_info)

    # 处理图片获得缺口值
    px_v = proc()

    # 构造轨迹
    track = px2track(px_v)

    # 发起验证请求
    info = {
        "track": [[-33, -36, 0], [0, 0, 0], [1, 0, 6], [2, 0, 30], [2, -1, 38], [4, -1, 134], [4, -1, 159],[4, -1, 239]],
        "c": [12, 58, 98, 36, 43, 95, 62, 15, 12],
        "s": cap_info["s"],
        "gt": "fe23d6148baf995e34decea58c12b5e4",
        "challenge": "adb53a1f7acf99015cc3047bb027f25dbu",
        "passtime": 510,
        "imgload": 8527,
        "tm": {
            "a": 1557975287799,
            "b": 1557975287902,
            "c": 1557975287904,
            "d": 0,
            "e": 0,
            "f": 1557975287811,
            "g": 1557975287816,
            "h": 1557975287819,
            "i": 1557975287819,
            "j": 1557975287840,
            "k": 1557975287827,
            "l": 1557975287841,
            "m": 1557975287896,
            "n": 1557975287948,
            "o": 1557975287925,
            "p": 1557975288501,
            "q": 1557975288501,
            "r": 1557975288501,
            "s": 1557975288815,
            "t": 1557975288815,
            "u": 1557975288815,
        }
    }
    params = {
        "gt": "ff3cd843746782b0e0f377c2d234d6a5",
        "challenge": "92f814a581376bccb86c33df921a17d79k",
        "lang": "zh - cn",
        "pt": 0,
        "w": boom(info),
        "callback": "geetest_{}".format(str(int(time.time()*1000)))
    }
    url = "https://api.geetest.com/ajax.php"
    res = session.get(url,headers=headers,params=params)
    print(res.text)