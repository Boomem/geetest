import rsa
import binascii
import hashlib
import execjs
import random
import json
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


js = open("gee.js", "r", encoding="utf-8").read()
ctx = execjs.compile(js)

def rsa_encrypt(aes_key):
    public_key_n = "00C1E3934D1614465B33053E7F48EE4EC87B14B95EF88947713D25EECBFF7E74C7977D02DC1D9451F79DD5D1C10C29ACB6A9B4D6FB7D0A0279B6719E1772565F09AF627715919221AEF91899CAE08C0D686D748B20A3603BE2318CA6BC2B59706592A9219D0BF05C9F65023A21D2330807252AE0066D59CEEFA5F2748EA80BAB81"
    public_key_e = '10001'

    # 转换为RSA可使用的十进制类型.
    rsa_n = int(public_key_n, 16)
    rsa_e = int(public_key_e, 16)
    # 使用n, e值生成公钥.
    key = rsa.PublicKey(rsa_n, rsa_e)

    # 用公钥把数据加密.
    endata = rsa.encrypt(aes_key.encode(), key)
    endata = binascii.b2a_hex(endata)
    # print(endata)

    # 以string类型 输出. 数据很长...
    h8j = endata.decode()
    print("h8j:",h8j)
    return h8j

def W8j(info):
    # rp
    s = info["gt"] + info["challenge"][:-2] + str(info["passtime"])
    b = hashlib.md5()
    b.update(s.encode())
    rp = b.hexdigest()
    # ep f
    a = hashlib.md5()
    a.update((info["gt"] + info["challenge"]).encode())
    w8j = {
        "lang": "zh-cn",
        "userresponse": ctx.call("userresponse", 38, info["challenge"]),
        "passtime": info["passtime"],
        "imgload": info["imgload"],
        "aa": ctx.call("aa", info["track"], info["c"], info["s"]),
        "ep":{
            "v": "7.5.5",
            # md5(gt + challeng)
            "f": a.hexdigest(),
            "te": "false",
            "me": "true",
            # 跟当前时间戳有关，可能是图片加载时间点
            "tm": info["tm"]
        },
        "rp": rp
    }
    return str(json.dumps(w8j).replace(" ",""))

def aes_encrypt(text,key):
    # pkcs7补齐方式
    BS = AES.block_size
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)

    # key = '3df48de799da0509'
    mode = AES.MODE_CBC
    iv = b'0000000000000000'
    # text = add_to_16(text)
    cryptos = AES.new(key.encode('utf-8'), mode, iv)
    cipher_text = cryptos.encrypt(pad(text).encode('utf-8'))
    # 因为AES加密后的字符串不一定是ascii字符集的，输出保存可能存在问题，所以这里转为16进制字符串
    return b2a_hex(cipher_text)

def boom(info):
    # aes加密参数的key，随机生成
    aes_key = hex(int((random.random() + 1) * 65536)).replace("0x", "")[1:] + hex(
        int((random.random() + 1) * 65536)).replace("0x", "")[1:] + hex(int((random.random() + 1) * 65536)).replace(
        "0x", "")[1:] + hex(int((random.random() + 1) * 65536)).replace("0x", "")[1:]
    print("aes_key:", aes_key)

    # 将用于aes加密的key使用rsa加密传输
    h8j = rsa_encrypt(aes_key)
    print(h8j)

    # 包含轨迹加密，时间等参数的信息
    w8j = W8j(info)
    print(w8j)

    # 将信息进行aes加密
    # w8j = '{"lang":"zh-cn","userresponse":"11111717a","passtime":325,"imgload":187,"aa":"N-.X11100(!!Jss7u(!)!*!)!*(R(yttt(!!(9,21200t20212/2$,7","ep":{"v":"7.5.5","f":"f67fcbaf3ef5bb5ed0e183bbcd3e9a8e","te":false,"me":true,"tm":{"a":1558083927933,"b":1558083928054,"c":1558083928059,"d":0,"e":0,"f":1558083927934,"g":1558083927978,"h":1558083927997,"i":1558083927997,"j":1558083928022,"k":1558083928010,"l":1558083928022,"m":1558083928045,"n":1558083928111,"o":1558083928072,"p":1558083928787,"q":1558083928787,"r":1558083928787,"s":1558083928953,"t":1558083928953,"u":1558083928954}},"rp":"4f3c8883b254f6ae75f58435dba11233"}'
    encrypt_text = aes_encrypt(w8j,aes_key).decode()
    print(encrypt_text)
    # 特定方法生成数组
    w2i = ctx.call("p2",encrypt_text)
    print(w2i)
    d8j = ctx.call("d8j",w2i)
    print(d8j)

    # z8j 按照特定方法生成加密字符串
    z8j = ctx.call("pd",d8j)
    print(z8j)
    return z8j + h8j

if __name__ == '__main__':
    info = {
        # 轨迹，自己滚去伪造
        "track": [[-33, -36, 0], [0, 0, 0], [1, 0, 6], [2, 0, 30], [2, -1, 38], [4, -1, 134], [4, -1, 159],
                  [4, -1, 239]],
        "c": [12, 58, 98, 36, 43, 95, 62, 15, 12],
        # s,gt,challenge接口里面都有
        "s": "746d296a",
        "gt": "fe23d6148baf995e34decea58c12b5e4",
        "challenge": "adb53a1f7acf99015cc3047bb027f25dbu",
        # 滑动时间和图片加载时间
        "passtime": 510,
        "imgload": 8527,
        # 不知道啥玩意，反正跟当前时间戳差不多
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
    print(boom(info))

# aes = '2bb171677c17dae334409c2f9d590e2ed5b9c7737c327368fc456ebbda1ce5c76438b20090ef8f5bea4b09d6cffa311f2b98e4e4881e71ddb6de8ff35ad77fbf7cf33c443d325474f94ac5f33a45bef2d38d8e3a928175dc4a425bf5ffe7579606666d6a3f5de7c15249937579c471bdb7fd3c79164d93c1a980d257f594c7be043da3716b905dbe2be37f9481fa08eb7f64f71ede41106b750361bc1059a7e969be1dd36f7c4bd92ec662465a50fad1c7809ae0d4d4c41cc23921745643823a7e2d003d8a13d575a17883cbc00428d0efa404003668793493616c870a679116f6460dc44e0f77e01893b420bd9581c3e8dfbbccb8283aa4baf255984b0f347cc32f44f196d99002f02b5ffad0c05e572a7c60780daeb89ded974e424ab36e5c2ae3b4ee33f8cd419a4384bc30771cd6fecf282e3d8cc5acf1f9b9236b1bd0704c5011e54081e3299edb8622b41fcbb06ccd32926dee5df3eac4404d18e5760be53349af8a6ddea93df16a035647b04a09c1cf7ff57be1f7ca692125eed8d150d3aea2ac459f52faa8e70e428311090c4363331ffc9fb2046325d4543076aaca112fff2faffce415b6e8cf84848cb3d7c01cfff3e2470a38e3f0863c0dbaca8d9fa608faa8dd27aa447e8a89ec5ff22f0ed7d7b1ab237d7ac634fd1ed604172b9ad1397fa461261c9db575d19f140b452b0bad755f534b1ef626969fc5e7b19627a282ad0ad2c59812e16b2dd5a2c3d42917e7d79fd6559462c7ea26d0a875097d5c987bf692f5dc646a5a027e39d2e77e3389a7869f30f47b982bead160d6eaab658691ef50a108ddbfe9a504195d980b0ea8432ed5f3c38f05c270cc8f463da7705aaf44978a1b71d5109ce178036b'
# aes = '2bb171677c17dae334409c2f9d590e2ed5b9c7737c327368fc456ebbda1ce5c76438b20090ef8f5bea4b09d6cffa311f2b98e4e4881e71ddb6de8ff35ad77fbf7cf33c443d325474f94ac5f33a45bef2d38d8e3a928175dc4a425bf5ffe7579606666d6a3f5de7c15249937579c471bdb7fd3c79164d93c1a980d257f594c7be043da3716b905dbe2be37f9481fa08eb7f64f71ede41106b750361bc1059a7e969be1dd36f7c4bd92ec662465a50fad1c7809ae0d4d4c41cc23921745643823a7e2d003d8a13d575a17883cbc00428d0efa404003668793493616c870a679116f6460dc44e0f77e01893b420bd9581c3e8dfbbccb8283aa4baf255984b0f347cc32f44f196d99002f02b5ffad0c05e572a7c60780daeb89ded974e424ab36e5c2ae3b4ee33f8cd419a4384bc30771cd6fecf282e3d8cc5acf1f9b9236b1bd0704c5011e54081e3299edb8622b41fcbb06ccd32926dee5df3eac4404d18e5760be53349af8a6ddea93df16a035647b04a09c1cf7ff57be1f7ca692125eed8d150d3aea2ac459f52faa8e70e428311090c4363331ffc9fb2046325d4543076aaca112fff2faffce415b6e8cf84848cb3d7c01cfff3e2470a38e3f0863c0dbaca8d9fa608faa8dd27aa447e8a89ec5ff22f0ed7d7b1ab237d7ac634fd1ed604172b9ad1397fa461261c9db575d19f140b452b0bad755f534b1ef626969fc5e7b19627a282ad0ad2c59812e16b2dd5a2c3d42917e7d79fd6559462c7ea26d0a875097d5c987bf692f5dc646a5a027e39d2e77e3389a7869f30f47b982bead160d6eaab658691ef50a108ddbfe9a504195d980b0ea8432ed5f3c38f05c270cc8f463da7705aaf44978a1b71d5109ce178036b'
# z8i = 'bOGZ3HzDq8vIgLRPNy1GeLmtnmvcSWsc8xleb67E1ptYYeIAA99nrc4XJLp362HHbKR40oTGxb3qu5e7qbvff3y7cRjNSTjY5w5xz2ZRe(qzNpaOC4HZsw4Srfn)3jviGFpd6HfV3omSpKPZ5ZiZd)P9cW3CtKMxZoCynfngnvZAdcOZ7KDVe0c7)bAh6wQ))Vj7Ob4RAU)ZDEnsAS1r5k3uNatf8Q(1eJoamC6Q66lzAqY4k7hwMYqNRHjSjIKO(VUAdYaDl3kp4YM3ghAMg99oEADK4G3ID0lcHgZbBzL6mBVwuBfbwiSjU0DtF4Ez4r(vsuQMadCuyzmkrBfI8YtPkOnip6ACw0fX66gwuTsO8UicNNasN93juAoWT17UaMvo(mO8tgmmjJDsQXvEm)53YFbNMplsx(2tTE(Hg2hUgSF5gIE7ZLa3GkLoPY(o8J2KC11(tes(kghVIdnaLNmLpNcm9L4tdekeDDpTQw4Fhp)f1285344dRFF(o6mQj9Yqchnnie4s3hYSDiEFMAsbTTf8P(JAzFHwkWDaao6BfP9Pfvx4FfI8vpBgMuPzgjT)z8pTKGQ7w5LMNOY2NrdqIO4st1MukH4mJtzXy1dGn7upbkPd6ZrI9zbyEDMPK6mN)dAZWDTlV3mxPzAHlEcHdnnXjQ)G21LiP5l7R7JLSoJtKKpxIyI57FXxSovwZDN7n7fylbAans5Kg8TZJH3UI2)6C)n00E6WCH6Ni9veTYVrGreI02(kbM6xwLo(blliB9(QRgT1f81pECXVIwdGYgtOl(szPhEywZxnmHVrwS5vkLMmLWnxAbQ54QMf'
# z8i = 'bOGZ3HzDq8vIgLRPNy1GeLmtnmvcSWsc8xleb67E1ptYYeIAA99nrc4XJLp362HHbKR40oTGxb3qu5e7qbvff3y7cRjNSTjY5w5xz2ZRe(qzNpaOC4HZsw4Srfn)3jviGFpd6HfV3omSpKPZ5ZiZd)P9cW3CtKMxZoCynfngnvZAdcOZ7KDVe0c7)bAh6wQ))Vj7Ob4RAU)ZDEnsAS1r5k3uNatf8Q(1eJoamC6Q66lzAqY4k7hwMYqNRHjSjIKO(VUAdYaDl3kp4YM3ghAMg99oEADK4G3ID0lcHgZbBzL6mBVwuBfbwiSjU0DtF4Ez4r(vsuQMadCuyzmkrBfI8YtPkOnip6ACw0fX66gwuTsO8UicNNasN93juAoWT17UaMvo(mO8tgmmjJDsQXvEm)53YFbNMplsx(2tTE(Hg2hUgSF5gIE7ZLa3GkLoPY(o8J2KC11(tes(kghVIdnaLNmLpNcm9L4tdekeDDpTQw4Fhp)f1285344dRFF(o6mQj9Yqchnnie4s3hYSDiEFMAsbTTf8P(JAzFHwkWDaao6BfP9Pfvx4FfI8vpBgMuPzgjT)z8pTKGQ7w5LMNOY2NrdqIO4st1MukH4mJtzXy1dGn7upbkPd6ZrI9zbyEDMPK6mN)dAZWDTlV3mxPzAHlEcHdnnXjQ)G21LiP5l7R7JLSoJtKKpxIyI57FXxSovwZDN7n7fylbAans5Kg8TZJH3UI2)6C)n00E6WCH6Ni9veTYVrGreI02(kbM6xwLo(blliB9(QRgT1f81pECXVIwdGYgtOl(szPhEywZxnmHVrwS5vkLMmLWnxAbQ54QMf'
# z8i = "bOGZ3HzDq8vIgLRPNy1GeLmtnmvcSWsc8xleb67E1ptYYeIAA99nrc4XJLp362HHbKR40oTGxb3qu5e7qbvff3y7cRjNSTjY5w5xz2ZRe(qzNpaOC4HZsw4Srfn)3jviGFpd6HfV3omSpKPZ5ZiZd)P9cW3CtKMxZoCynfngnvZAdcOZ7KDVe0c7)bAh6wQ))Vj7Ob4RAU)ZDEnsAS1r5k3uNatf8Q(1eJoamC6Q66lzAqY4k7hwMYqNRHjSjIKO(VUAdYaDl3kp4YM3ghAMg99oEADK4G3ID0lcHgZbBzL6mBVwuBfbwiSjU0DtF4Ez4r(vsuQMadCuyzmkrBfI8YtPkOnip6ACw0fX66gwuTsO8UicNNasN93juAoWT17UaMvo(mO8tgmmjJDsQXvEm)53YFbNMplsx(2tTE(Hg2hUgSF5gIE7ZLa3GkLoPY(o8J2KC11(tes(kghVIdnaLNmLpNcm9L4tdekeDDpTQw4Fhp)f1285344dRFF(o6mQj9Yqchnnie4s3hYSDiEFMAsbTTf8P(JAzFHwkWDaao6BfP9Pfvx4FfI8vpBgMuPzgjT)z8pTKGQ7w5LMNOY2NrdqIO4st1MukH4mJtzXy1dGn7upbkPd6ZrI9zbyEDMPK6mN)dAZWDTlV3mxPzAHlEcHdnnXjQ)G21LiP5l7R7JLSoJtKKpxIyI57FXxSovwZDN7n7fylbAans5Kg8TZJH3UI2)6C)n00E6WCH6Ni9veTYVrGreI02(kbM6xwLo(blliB9(QRgT1f81pECXVIwdGYgtOl(szPhEywZxnmHVrwS5vkLMmLWnxAbQ54QMf"


