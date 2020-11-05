import requests
import json
import rsa
import base64
import time
from itertools import groupby
from functools import reduce
from random import choice
import hashlib
from datetime import datetime, timedelta
import os


# 喜马拉雅极速版
# 使用参考 xmly_speed.md

###################################################
# 对应方案2: 下载到本地,需要此处填写
cookies1 = ""
# 本地运行账号填写
cookies2 = ""
cookiesList = [cookies1, ]  # 多账号准备
XMLY_ACCUMULATE_TIME = 0    # 希望刷时长的,此处置1

###################################################
# 对应方案1:  GitHub action自动运行,此处无需填写;
if "XMLY_SPEED_COOKIE" in os.environ:
    """
    判断是否运行自GitHub action,"XMLY_SPEED_COOKIE" 该参数与 repo里的Secrets的名称保持一致
    """
    print("执行自GitHub action")
    xmly_speed_cookie = os.environ["XMLY_SPEED_COOKIE"]
    cookiesList = []  # 重置cookiesList
    for line in xmly_speed_cookie.split('\n'):
        if not line:
            continue
        cookiesList.append(line)
    # GitHub action运行需要填写对应的secrets
    if "XMLY_ACCUMULATE_TIME" in os.environ and os.environ["XMLY_ACCUMULATE_TIME"] == 'zero_s1':
        XMLY_ACCUMULATE_TIME = 1
        print("action 自动刷时长打开")

###################################################
UserAgent = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 iting/1.0.12 kdtunion_iting/1.0 iting(main)/1.0.12/ios_1"
# 非iOS设备的需要的自行修改,自己抓包 与cookie形式类似


def str2dict(str_cookie):
    if type(str_cookie) == dict:
        return str_cookie
    tmp = str_cookie.split(";")
    dict_cookie = {}
    try:
        for i in tmp:
            j = i.split("=")
            if not j[0]:
                continue
            dict_cookie[j[0].strip()] = j[1].strip()
    except:
        print("cookie格式填写错误")
        # exit()
    return dict_cookie


if not cookiesList[0]:
    print("cookie为空 跳出X")
    exit()
mins = int(time.time())
date_stamp = (mins-57600) % 86400
utc_dt = datetime.utcnow()  # UTC时间
bj_dt = utc_dt+timedelta(hours=8)  # 北京时间
_datatime = bj_dt.strftime("%Y%m%d", )
print(f"北京时间: {bj_dt}")
print(_datatime)
print("今日已过秒数: ", date_stamp)
print("当前时间戳", mins)


def read(cookies, uid):
    print("\n【阅读】")
    headers = {
        'Host': '51gzdhh.xyz',
        'accept': 'application/json, text/plain, */*',
        'origin': 'http://xiaokuohao.work',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MI 6 Plus Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 iting(main)/1.8.18/android_1 kdtUnion_iting/1.8.18',
        'referer': 'http://xiaokuohao.work/static/web/dxmly/index.html',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,en-US;q=0.8',
        'x-requested-with': 'com.ximalaya.ting.lite',
    }
    params = (
        ('hid', '233'),
    )
    try:
        response = requests.get(
            'https://51gzdhh.xyz/api/new/newConfig', headers=headers, params=params)
    except:
        print("网络请求异常,为避免GitHub action报错,直接退出")
        exit()
    result = response.json()
    pid = str(result["pid"])
    headers = {
        'Host': '51gzdhh.xyz',
        'content-length': '37',
        'accept': 'application/json, text/plain, */*',
        'origin': 'http://xiaokuohao.work',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MI 6 Plus Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 iting(main)/1.8.18/android_1 kdtUnion_iting/1.8.18',
        'content-type': 'application/x-www-form-urlencoded',
        'referer': 'http://xiaokuohao.work/static/web/dxmly/index.html',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,en-US;q=0.8',
        'x-requested-with': 'com.ximalaya.ting.lite',
    }
    data = {"pid": str(pid), "mtuserid": uid}
    try:
        response = requests.post(
            'https://51gzdhh.xyz/api/new/hui/complete', headers=headers, data=json.dumps(data))
    except:
        print("网络请求异常,为避免GitHub action报错,直接退出")
        exit()
    result = response.json()
    # print(result)
    if result["status"] == -2:
        print("无法阅读,尝试从安卓端手动开启")
        return
    print(result["completeList"])
    if result["isComplete"]:
        print("今日完成阅读")
        return
    headers = {
        'Host': '51gzdhh.xyz',
        'accept': 'application/json, text/plain, */*',
        'origin': 'http://xiaokuohao.work',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MI 6 Plus Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 iting(main)/1.8.18/android_1 kdtUnion_iting/1.8.18',
        'referer': 'http://xiaokuohao.work/static/web/dxmly/index.html',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,en-US;q=0.8',
        'x-requested-with': 'com.ximalaya.ting.lite',
    }
    taskIds = set(['242', '239', '241', '240', '238', '236',
                   '237', '235', '234'])-set(result["completeList"])
    params = (
        ('userid', str(uid)),
        ('pid', pid),
        ('taskid', taskIds.pop()),
        ('imei', ''),
    )
    try:
        response = requests.get(
            'https://51gzdhh.xyz/new/userCompleteNew', headers=headers, params=params)
    except:
        print("网络请求异常,为避免GitHub action报错,直接退出")
        exit()
    result = response.json()
    print(result)


def ans_receive(cookies, paperId, lastTopicId, receiveType):
    headers = {
        'User-Agent': UserAgent,
        'Content-Type': 'application/json;charset=utf-8',
        'Host': 'm.ximalaya.com',
        'Origin': 'https://m.ximalaya.com',
        'Referer': 'https://m.ximalaya.com/growth-ssr-speed-welfare-center/page/quiz',
    }
    _checkData = f"""lastTopicId={lastTopicId}&numOfAnswers=3&receiveType={receiveType}"""
    checkData = rsa_encrypt(str(_checkData), pubkey_str)
    data = {
        "paperId": paperId,
        "checkData": checkData,
        "lastTopicId": lastTopicId,
        "numOfAnswers": 3,
        "receiveType": receiveType
    }
    try:
        response = requests.post('https://m.ximalaya.com/speed/web-earn/topic/receive',
                                 headers=headers, cookies=cookies, data=json.dumps(data))
    except:
        print("网络请求异常,为避免GitHub action报错,直接退出")
        exit()
    print(response.text)


def ans_restore(cookies):
    headers = {
        'User-Agent': UserAgent,
        'Content-Type': 'application/json;charset=utf-8',
        'Host': 'm.ximalaya.com',
        'Origin': 'https://m.ximalaya.com',
        'Referer': 'https://m.ximalaya.com/growth-ssr-speed-welfare-center/page/quiz',
    }
    checkData = rsa_encrypt("restoreType=2", pubkey_str)

    data = {
        "restoreType": 2,
        "checkData": checkData,
    }
    try:
        response = requests.post('https://m.ximalaya.com/speed/web-earn/topic/restore',
                                 headers=headers, cookies=cookies, data=json.dumps(data))
    except:
        print("网络请求异常,为避免GitHub action报错,直接退出")
        exit()
    print(response.text)


def ans_getTimes(cookies):
    headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-cn',
        'Referer': 'https://m.ximalaya.com/growth-ssr-speed-welfare-center/page/quiz',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    try:
        response = requests.get(
            'https://m.ximalaya.com/speed/web-earn/topic/user', headers=headers, cookies=cookies)
    except:
        print("网络请求异常,为避免GitHub action报错,直接退出")
        exit()
    result = json.loads(response.text)
    stamina = result["data"]["stamina"]
    remainingTimes = result["data"]["remainingTimes"]
    return {"stamina": stamina,
            "remainingTimes": remainingTimes}


def ans_start(cookies):
    headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-cn',
        'Referer': 'https://m.ximalaya.com/growth-ssr-speed-welfare-center/page/quiz',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    try:
        response = requests.get(
            'https://m.ximalaya.com/speed/web-earn/topic/start', headers=headers, cookies=cookies)
    except:
        print("网络请求异常,为避免GitHub action报错,直接退出")
        exit()
    result = json.loads(response.text)
    paperId = result["data"]["paperId"]
    dateStr = result["data"]["dateStr"]
    lastTopicId = result["data"]["topics"][2]["topicId"]
    print(paperId, dateStr, lastTopicId)
    return paperId, dateStr, lastTopicId


def _str2key(s):
    b_str = base64.b64decode(s)
    if len(b_str) < 162:
        return False
    hex_str = ''
    for x in b_str:
        h = hex(x)[2:]
        h = h.rjust(2, '0')
        hex_str += h
    m_start = 29 * 2
    e_start = 159 * 2
    m_len = 128 * 2
    e_len = 3 * 2
    modulus = hex_str[m_start:m_start + m_len]
    exponent = hex_str[e_start:e_start + e_len]
    return modulus, exponent


def rsa_encrypt(s, pubkey_str):
    key = _str2key(pubkey_str)
    modulus = int(key[0], 16)
    exponent = int(key[1], 16)
    pubkey = rsa.PublicKey(modulus, exponent)
    return base64.b64encode(rsa.encrypt(s.encode(), pubkey)).decode()


pubkey_str = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCVhaR3Or7suUlwHUl2Ly36uVmboZ3+HhovogDjLgRE9CbaUokS2eqGaVFfbxAUxFThNDuXq/fBD+SdUgppmcZrIw4HMMP4AtE2qJJQH/KxPWmbXH7Lv+9CisNtPYOlvWJ/GHRqf9x3TBKjjeJ2CjuVxlPBDX63+Ecil2JR9klVawIDAQAB"


def lottery_info(cookies):
    print("\n【幸运大转盘】")
    """
    转盘信息查询
    """
    headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-cn',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-ad-sweepstake-h5/home',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    try:
        response = requests.get(
            'https://m.ximalaya.com/speed/web-earn/inspire/lottery/info', headers=headers, cookies=cookies)
    except:
        print("网络请求异常,为避免GitHub action报错,直接退出")
        exit()
    result = response.json()
    remainingTimes = result["data"]["remainingTimes"]
    print(f'转盘info: {result["data"]}\n')
    if remainingTimes in [0, 1]:
        print("今日完毕")
        return
    response = requests.get(
        'https://m.ximalaya.com/speed/web-earn/inspire/lottery/token', headers=headers, cookies=cookies)
    print("token", response.text)
    token = response.json()["data"]["id"]
    data = {
        "token": token,
        "sign": rsa_encrypt(f"token={token}&userId={uid}", pubkey_str),
    }
    response = requests.post('https://m.ximalaya.com/speed/web-earn/inspire/lottery/chance',
                             headers=headers, cookies=cookies, data=json.dumps(data))

    result = response.json()
    print("chance", result)
    data = {
        "sign": rsa_encrypt(str(result["data"]["chanceId"]), pubkey_str),
    }
    response = requests.post('https://m.ximalaya.com/speed/web-earn/inspire/lottery/action',
                             headers=headers, cookies=cookies, data=json.dumps(data))
    print(response.text)


def index_baoxiang_award(cookies):
    print("\n  【首页、宝箱奖励及翻倍】")
    headers = {
        'User-Agent': UserAgent,
        'Host': 'mobile.ximalaya.com',
    }
    uid = cookies["1&_token"].split("&")[0]
    currentTimeMillis = int(time.time()*1000)-2
    response = requests.post('https://mobile.ximalaya.com/pizza-category/activity/getAward?activtyId=baoxiangAward',
                             headers=headers, cookies=cookies)

    result = response.json()
    print("宝箱奖励: ", result)
    if "ret" in result and result["ret"] == 0:
        awardReceiveId = result["awardReceiveId"]
        headers = {
            'Host': 'mobile.ximalaya.com',
            'Accept': '*/*',
            'User-Agent': UserAgent,
            'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }

        params = (
            ('activtyId', 'baoxiangAward'),
            ('awardReceiveId', awardReceiveId),
        )
        try:
            response = requests.get('http://mobile.ximalaya.com/pizza-category/activity/awardMultiple',
                                    headers=headers, params=params, cookies=cookies)
        except:
            print("网络请求异常,为避免GitHub action报错,直接退出")
            exit()
        print("翻倍 ", response.text)
    ###################################
    params = (
        ('activtyId', 'indexSegAward'),
        ('ballKey', str(uid)),
        ('currentTimeMillis', str(currentTimeMillis)),
        ('sawVideoSignature', f'{currentTimeMillis}+{uid}'),
        ('version', '2'),
    )
    try:
        response = requests.get('https://mobile.ximalaya.com/pizza-category/activity/getAward',
                                headers=headers, cookies=cookies, params=params)
    except:
        print("网络请求异常,为避免GitHub action报错,直接退出")
        exit()
    result = response.json()
    print("首页奖励: ", result)
    if "ret" in result and result["ret"] == 0:
        awardReceiveId = result["awardReceiveId"]
        headers = {
            'Host': 'mobile.ximalaya.com',
            'Accept': '*/*',
            'User-Agent': UserAgent,
            'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }

        params = (
            ('activtyId', 'indexSegAward'),
            ('awardReceiveId', awardReceiveId),
        )
        try:
            response = requests.get('http://mobile.ximalaya.com/pizza-category/activity/awardMultiple',
                                    headers=headers, params=params, cookies=cookies)
        except:
            print("网络请求异常,为避免GitHub action报错,直接退出")
            exit()
        print("翻倍: ", response.text)


def checkin(cookies):
    print("\n【连续签到】")
    headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-cn',
        'Referer': 'https://m.ximalaya.com/growth-ssr-speed-welfare-center/page/welfare',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    params = (
        ('time', f"""{int(time.time()*1000)}"""),
    )
    try:
        response = requests.get('https://m.ximalaya.com/speed/task-center/check-in/record',
                                headers=headers, params=params, cookies=cookies)
    except:
        print("网络请求异常,为避免GitHub action报错,直接退出")
        exit()
    result = json.loads(response.text)
    # print(result)
    print(f"""连续签到{result["continuousDays"]}/{result["historyDays"]}天""")
    print(result["isTickedToday"])
    if result["isTickedToday"] == False:
        print("!!!未签到")
        pass


def ad_score(cookies, businessType, taskId):
    headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain ,*/*',
        'Connection': 'keep-alive',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-cn',
        'Content-Type': 'application/json;charset=utf-8',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    try:
        response = requests.get(
            'https://m.ximalaya.com/speed/task-center/ad/token', headers=headers, cookies=cookies)
    except:
        print("网络请求异常,为避免GitHub action报错,直接退出")
        exit()
    result = response.json()
    token = result["id"]
    data = {
        "taskId": taskId,
        "businessType": businessType,
        "rsaSign": rsa_encrypt(f"""businessType={businessType}&token={token}&uid={uid}""", pubkey_str),
    }
    try:
        response = requests.post(f'https://m.ximalaya.com/speed/task-center/ad/score',
                                 headers=headers, cookies=cookies, data=json.dumps(data))
    except:
        print("网络请求异常,为避免GitHub action报错,直接退出")
        exit()
    print(response.text)
    print("\n")


def bubble(cookies):
    print("\n【bubble】")
    headers = {
        'User-Agent': UserAgent,
        'Content-Type': 'application/json;charset=utf-8',
        'Host': 'm.ximalaya.com',
        'Origin': 'https://m.ximalaya.com',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-open-components/bubble',
    }

    data = {"listenTime": "41246", "signature": "2b1cc9ee020db596d28831cff8874d9c",
            "currentTimeMillis": "1596695606145", "uid": uid, "expire": False}
    try:
        response = requests.post('https://m.ximalaya.com/speed/web-earn/listen/bubbles',
                                 headers=headers, cookies=cookies, data=json.dumps(data))
    except:
        print("网络请求异常,为避免GitHub action报错,直接退出")
        exit()
    result = response.json()
    if not result["data"]["effectiveBubbles"]:
        print("暂无有效气泡")
        return
    for i in result["data"]["effectiveBubbles"]:
        print(i["id"])
        receive(cookies, i["id"])
        time.sleep(1)
        ad_score(cookies, 7, i["id"])
    for i in result["data"]["expiredBubbles"]:
        ad_score(cookies, 6, i["id"])


def receive(cookies, taskId):
    headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-cn',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-open-components/bubble',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    try:
        response = requests.get(
            f'https://m.ximalaya.com/speed/web-earn/listen/receive/{taskId}', headers=headers, cookies=cookies)
    except:
        print("网络请求异常,为避免GitHub action报错,直接退出")
        exit()
    print("receive: ", response.text)


def getOmnipotentCard(cookies):
    print("\n 【领取万能卡】")
    headers = {
        'User-Agent': UserAgent,
        'Content-Type': 'application/json;charset=utf-8',
        'Host': 'm.ximalaya.com',
        'Origin': 'https://m.ximalaya.com',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-activities/card-collection/home',
    }
    try:
        count = requests.get('https://m.ximalaya.com/speed/web-earn/card/omnipotentCardInfo',
                             headers=headers, cookies=cookies,).json()["data"]["count"]
    except:
        print("网络请求异常,为避免GitHub action报错,直接退出")
        exit()
    if count == 5:
        print("今日已满")
        return

    token = requests.get('https://m.ximalaya.com/speed/web-earn/card/token/1',
                         headers=headers, cookies=cookies,).json()["data"]["id"]
    data = {
        "listenTime": mins-date_stamp,
        "signData": rsa_encrypt(f"{_datatime}{token}{uid}", pubkey_str),
        "token": token
    }
    try:
        response = requests.post('https://m.ximalaya.com/speed/web-earn/card/getOmnipotentCard',
                                 headers=headers, cookies=cookies, data=json.dumps(data))
    except:
        print("网络请求异常,为避免GitHub action报错,直接退出")
        exit()
    print(response.text)


def cardReportTime(cookies):
    print("\n【收听获得抽卡机会】")
    headers = {
        'User-Agent': UserAgent,
        'Content-Type': 'application/json;charset=utf-8',
        'Host': 'm.ximalaya.com',
        'Origin': 'https://m.ximalaya.com',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-activities/card-collection/home',
    }
    listenTime = mins-date_stamp
    data = {"listenTime": listenTime,
            "signData": rsa_encrypt(f"{_datatime}{listenTime}{uid}", pubkey_str), }
    try:
        response = requests.post('https://m.ximalaya.com/speed/web-earn/card/reportTime',
                                 headers=headers, cookies=cookies, data=json.dumps(data)).json()
    except:
        print("网络请求异常,为避免GitHub action报错,直接退出")
        exit()
    if response["data"]["upperLimit"]:
        print("今日已达上限")


def account(cookies):
    print("\n【 打印账号信息】")
    headers = {
        'Host': 'm.ximalaya.com',
        'Content-Type': 'application/json;charset=utf-8',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': UserAgent,
        'Referer': 'https://m.ximalaya.com/speed/web-earn/wallet',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    try:
        response = requests.get(
            'https://m.ximalaya.com/speed/web-earn/account/coin', headers=headers, cookies=cookies)
    except:
        print("网络请求异常,为避免GitHub action报错,直接退出")
        exit()
    result = response.json()
    print(f"""
当前剩余:{result["total"]/10000}
今日获得:{result["todayTotal"]/10000}
累计获得:{result["historyTotal"]/10000}

""")


def answer(cookies):
    print("\n【答题】")
    ans_times = ans_getTimes(cookies)
    if ans_times["stamina"] == 0:
        print("时间未到")
    for _ in range(ans_times["stamina"]):
        paperId, _, lastTopicId = ans_start(cookies)
        ans_receive(cookies, paperId, lastTopicId, 1)
        time.sleep(1)
        ans_receive(cookies, paperId, lastTopicId, 2)
        time.sleep(1)

    if ans_times["remainingTimes"] > 0:
        print("[看视频回复体力]")
        ans_restore(cookies)
        for _ in range(5):
            paperId, _, lastTopicId = ans_start(cookies)
            ans_receive(cookies, paperId, lastTopicId, 1)
            time.sleep(1)
            ans_receive(cookies, paperId, lastTopicId, 2)
            time.sleep(1)


def saveListenTime(cookies):
    print("\n【刷时长1】")
    headers = {
        'User-Agent': UserAgent,
        'Host': 'mobile.ximalaya.com',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    listentime = date_stamp
    print(f"上传本地收听时长1: {listentime//60}分钟")
    currentTimeMillis = int(time.time()*1000)-2
    sign = hashlib.md5(
        f'currenttimemillis={currentTimeMillis}&listentime={listentime}&uid={uid}&23627d1451047b8d257a96af5db359538f081d651df75b4aa169508547208159'.encode()).hexdigest()
    data = {
        'activtyId': 'listenAward',
        'currentTimeMillis': currentTimeMillis,
        'listenTime': str(listentime),
        'nativeListenTime': str(listentime),
        'signature': sign,
        'uid': uid
    }
    try:
        response = requests.post('http://mobile.ximalaya.com/pizza-category/ball/saveListenTime',
                                 headers=headers, cookies=cookies, data=data)
    except:
        print("网络请求异常,为避免GitHub action报错,直接退出")
        exit()
    print(response.text)


def listenData(cookies):
    print("\n【刷时长2】")
    headers = {
        'User-Agent': 'ting_v1.1.9_c5(CFNetwork, iOS 14.0.1, iPhone9,2)',
        'Host': 'm.ximalaya.com',
        'Content-Type': 'application/json',
    }
    listentime = date_stamp
    print(f"上传本地收听时长2: {listentime//60}分钟")
    currentTimeMillis = int(time.time()*1000)-2
    sign = hashlib.md5(
        f'currenttimemillis={currentTimeMillis}&listentime={listentime}&uid={uid}&23627d1451047b8d257a96af5db359538f081d651df75b4aa169508547208159'.encode()).hexdigest()
    data = {
        'currentTimeMillis': currentTimeMillis,
        'listenTime': str(listentime),
        'signature': sign,
        'uid': uid
    }
    try:
        response = requests.post('http://m.ximalaya.com/speed/web-earn/listen/client/data',
                                 headers=headers, cookies=cookies, data=json.dumps(data))
    except:
        print("网络请求异常,为避免GitHub action报错,直接退出")
        exit()
    print(response.text)


def card_exchangeCoin(cookies, themeId, cardIdList):
    headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-cn',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-activities/card-collection/home',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    token = requests.get('https://m.ximalaya.com/speed/web-earn/card/token/3',
                         headers=headers, cookies=cookies,).json()["data"]["id"]
    data = {
        "cardIdList": cardIdList,
        "themeId": themeId,
        "signData": rsa_encrypt(f"{_datatime}{token}{uid}", pubkey_str),
        "token": token
    }
    headers = {
        'User-Agent': UserAgent,
        'Content-Type': 'application/json;charset=utf-8',
        'Host': 'm.ximalaya.com',
        'Origin': 'https://m.ximalaya.com',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-activities/card-collection/home',
    }
    try:
        response = requests.post('https://m.ximalaya.com/speed/web-earn/card/exchangeCoin',
                                 headers=headers, cookies=cookies, data=json.dumps(data))
    except:
        print("网络请求异常,为避免GitHub action报错,直接退出")
        exit()
    print("card_exchangeCoin: ", response.text)


def card_exchangeCard(cookies, toCardAwardId, fromRecordIdList):
    fromRecordIdList = sorted(fromRecordIdList)
    headers = {
        'User-Agent': UserAgent,
        'Content-Type': 'application/json;charset=utf-8',
        'Host': 'm.ximalaya.com',
        'Origin': 'https://m.ximalaya.com',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-activities/card-collection/home',
    }
    data = {
        "toCardAwardId": toCardAwardId,
        "fromRecordIdList": fromRecordIdList,
        "exchangeType": 1,
    }
    try:
        response = requests.post('https://m.ximalaya.com/speed/web-earn/card/exchangeCard',
                                 headers=headers, cookies=cookies, data=json.dumps(data))
    except:
        print("网络请求异常,为避免GitHub action报错,直接退出")
        exit()
    print(response.text)


def draw_5card(cookies, drawRecordIdList):  # 五连抽
    drawRecordIdList = sorted(drawRecordIdList)
    headers = {
        'User-Agent': UserAgent,
        'Content-Type': 'application/json;charset=utf-8',
        'Host': 'm.ximalaya.com',
        'Origin': 'https://m.ximalaya.com',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-activities/card-collection/home',
    }
    data = {
        "signData": rsa_encrypt(f"{''.join(str(i) for i in drawRecordIdList)}{uid}", pubkey_str),
        "drawRecordIdList": drawRecordIdList,
        "drawType": 2,
    }
    try:
        response = requests.post('https://m.ximalaya.com/speed/web-earn/card/draw',
                                 headers=headers, cookies=cookies, data=json.dumps(data))
    except:
        print("网络请求异常,为避免GitHub action报错,直接退出")
        exit()
    print("五连抽: ", response.text)


def card(cookies):
    print("\n【抽卡】")
    headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-cn',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-activities/card-collection/home',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    try:
        response = requests.get(
            'https://m.ximalaya.com/speed/web-earn/card/userCardInfo', headers=headers, cookies=cookies)
    except:
        print("网络请求异常,为避免GitHub action报错,直接退出")
        exit()
    data = response.json()["data"]
    #######
    # 5连抽
    drawRecordIdList = data["drawRecordIdList"]
    print("抽卡机会: ", drawRecordIdList)
    for _ in range(len(drawRecordIdList)//5):
        tmp = []
        for _ in range(5):
            tmp.append(drawRecordIdList.pop())
        draw_5card(cookies, tmp)
    ########
    # 手牌兑换金币
    # 1 万能卡  10 碎片
    print("检查手牌，卡牌兑金币")
    themeId_id_map = {
        2: [2, 3],
        3: [4, 5, 6, 7],
        4: [8, 9, 10, 11, 12],
        5: [13, 14, 15, 16, 17, 18],
        6: [19, 20, 21, 22],
        7: [23, 24, 25, 26, 27],
        8: [28, 29, 30, 31, 32],
        9: [33, 34, 35, 36, 37]
    }
    response = requests.get(
        'https://m.ximalaya.com/speed/web-earn/card/userCardInfo', headers=headers, cookies=cookies)
    data = response.json()["data"]
    userCardsList = data["userCardsList"]  # 手牌
    lstg = groupby(userCardsList, key=lambda x: x["themeId"])
    for key, group in lstg:
        if key in [1, 10]:
            continue
        themeId = key
        ids = list(group)
        tmp_recordId = []
        tmp_id = []
        for i in ids:
            if i["id"] in tmp_id:
                continue
            tmp_recordId.append(i["recordId"])
            tmp_id.append(i["id"])
        if len(tmp_recordId) == len(themeId_id_map[key]):
            print("可以兑换")
            card_exchangeCoin(cookies, themeId, tmp_recordId)
    ###############
    # 万能卡兑换稀有卡
    response = requests.get(
        'https://m.ximalaya.com/speed/web-earn/card/userCardInfo', headers=headers, cookies=cookies)
    data = response.json()["data"]
    userCardsList = data["userCardsList"]
    omnipotentCard = [i for i in userCardsList if i["id"] == 1]
    cityCardId = [i["id"] for i in userCardsList if i["themeId"] == 9]
    need = set(themeId_id_map[9])-set(cityCardId)

    print("万能卡: ", [i['recordId'] for i in omnipotentCard])
    for _ in range(len(omnipotentCard)//4):
        tmp = []
        for _ in range(4):
            tmp.append(omnipotentCard.pop())
        fromRecordIdList = [i['recordId'] for i in tmp]
        if need:
            print("万能卡兑换稀有卡:")
            card_exchangeCard(cookies, need.pop(), fromRecordIdList)

##################################################################


for i in cookiesList:
    print(">>>>>>>>>【账号开始】")
    cookies = str2dict(i)
    try:
        uid = cookies["1&_token"].split("&")[0]
        uuid = cookies["XUM"]
    except:
        print("cookie填写错误")
        exit()
    if XMLY_ACCUMULATE_TIME == 1:
        saveListenTime(cookies)
        listenData(cookies)
    read(cookies, uid)  # 阅读
    bubble(cookies)  # 收金币气泡
    checkin(cookies)  # 自动签到
    # lottery_info(cookies)  # 大转盘4次
    answer(cookies)      # 答题赚金币
    cardReportTime(cookies)  # 卡牌
    getOmnipotentCard(cookies)  # 领取万能卡
    card(cookies)  # 抽卡
    index_baoxiang_award(cookies)  # 首页、宝箱奖励及翻倍
    account(cookies)
