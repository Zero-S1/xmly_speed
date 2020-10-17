import requests
import json
import rsa
import base64
import time
from itertools import groupby
from functools import reduce
from random import choice
import hashlib
from datetime import datetime
from dateutil import tz
import os

# 喜马拉雅极速版
# 使用参考 xmly_speed.md
# cookies填写

cookies1 = ""  # 字符串形式 都可以识别
cookies2 = {
}  # 字典形式




cookiesList = [cookies1, ]  # 多账号准备




UserAgent = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 iting/1.0.12 kdtunion_iting/1.0 iting(main)/1.0.12/ios_1"
# 非iOS设备的需要的自行修改,自己抓包 与cookie形式类似


def str2dict(str_cookie):
    if type(str_cookie) == dict:
        return str_cookie
    tmp = str_cookie.split(";")
    dict_cookie = {}
    for i in tmp:
        j = i.split("=")
        if not j[0]:
            continue
        dict_cookie[j[0].strip()] = j[1].strip()
    return dict_cookie




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

if not cookiesList[0]:
    print("cookie为空 跳出X")
    exit()
mins = int(time.time())
date_stamp = (mins-57600) % 86400
#print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print(datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S", ))
_datatime = datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y%m%d", )
print(_datatime)
print("今日已过秒数: ", date_stamp)
print("当前时间戳", mins)


def listenData(cookies):
    headers = {
        'User-Agent': UserAgent,
        'Host': 'm.ximalaya.com',
        'Content-Type': 'application/json',
    }
    listentime = date_stamp
    print(listentime//60)
    currentTimeMillis = int(time.time()*1000)-2
    sign = hashlib.md5(
        f'currenttimemillis={currentTimeMillis}&listentime={listentime}&uid={uid}&23627d1451047b8d257a96af5db359538f081d651df75b4aa169508547208159'.encode()).hexdigest()
    data = {
        # 'activtyId': 'listenAward',
        'currentTimeMillis': currentTimeMillis,
        'listenTime': str(listentime),
        # 'nativeListenTime': str(listentime),
        'signature': sign,
        'uid': uid
    }

    response = requests.post('http://m.ximalaya.com/speed/web-earn/listen/client/data',
                             headers=headers, cookies=cookies, data=json.dumps(data))
    print(response.text)


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
    response = requests.post('https://m.ximalaya.com/speed/web-earn/topic/receive',
                             headers=headers, cookies=cookies, data=json.dumps(data))
    print(response.text)


def ans_restore(cookies):
    """
    看视频回复体力，type=2
    """
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
    response = requests.post('https://m.ximalaya.com/speed/web-earn/topic/restore',
                             headers=headers, cookies=cookies, data=json.dumps(data))
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

    response = requests.get(
        'https://m.ximalaya.com/speed/web-earn/topic/user', headers=headers, cookies=cookies)
    result = json.loads(response.text)
    stamina = result["data"]["stamina"]  # 答题次数
    remainingTimes = result["data"]["remainingTimes"]  # 可回复次数
    print(f"answer_stamina答题次数: {stamina}")
    print(f"answer_remainingTimes可回复次数: {remainingTimes}\n")
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

    response = requests.get(
        'https://m.ximalaya.com/speed/web-earn/topic/start', headers=headers, cookies=cookies)
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
    # 查询信息
    response = requests.get(
        'https://m.ximalaya.com/speed/web-earn/inspire/lottery/info', headers=headers, cookies=cookies)
    result = json.loads(response.text)
    print(result)

    remainingTimes = result["data"]["remainingTimes"]
    print(f'lottery_remainingTimes转盘剩余次数: {remainingTimes}\n')
    if result["data"]["chanceId"] != 0 and result["data"]["remainingTimes"] == 1:
        print("免费抽奖次数")
        return
        data = {
            "sign": rsa_encrypt(str(result["data"]["chanceId"]), pubkey_str),
        }
        response = requests.post('https://m.ximalaya.com/speed/web-earn/inspire/lottery/action',
                                 headers=headers, cookies=cookies, data=json.dumps(data))
        print(response.text)
        return
    if result["data"]["remainingTimes"] in [0, 1]:
        return
    data = {
        "sign": rsa_encrypt(str(result["data"]["chanceId"]), pubkey_str),
    }
    response = requests.post('https://m.ximalaya.com/speed/web-earn/inspire/lottery/action',
                             headers=headers, cookies=cookies, data=json.dumps(data))
    print(response.text)
    # for i in range(3):
    # 获取token
    # exit()
    if remainingTimes > 0:
        headers = {
            'Host': 'm.ximalaya.com',
            'Accept': 'application/json, text/plain, */*',
            'Connection': 'keep-alive',
            'User-Agent': UserAgent,
            'Accept-Language': 'zh-cn',
            'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-ad-sweepstake-h5/home',
            'Accept-Encoding': 'gzip, deflate, br',
        }

        response = requests.get(
            'https://m.ximalaya.com/speed/web-earn/inspire/lottery/token', headers=headers, cookies=cookies)
        print("token", response.text)
        result = json.loads(response.text)
        _id = result["data"]["id"]
        data = {
            "token": _id,
            "sign": rsa_encrypt(f"token={_id}&userId={uid}", pubkey_str),
        }
        headers = {
            'User-Agent': UserAgent,
            'Content-Type': 'application/json;charset=utf-8',
            'Host': 'm.ximalaya.com',
            'Origin': 'https://m.ximalaya.com',
            'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-ad-sweepstake-h5/home',
        }
        response = requests.post('https://m.ximalaya.com/speed/web-earn/inspire/lottery/chance',
                                 headers=headers, cookies=cookies, data=json.dumps(data))
        result = json.loads(response.text)
        print("chance", result)
        data = {
            "sign": rsa_encrypt(str(result["data"]["chanceId"]), pubkey_str),
        }
        response = requests.post('https://m.ximalaya.com/speed/web-earn/inspire/lottery/action',
                                 headers=headers, cookies=cookies, data=json.dumps(data))
        print("action", response.text)


def task_label(cookies):
    print("\n【收听时长 30 60 90 】")
    """
    任务查看
    """
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
        ('taskLabels', '1,2'),
    )

    response = requests.get('https://m.ximalaya.com/speed/task-center/task/record',
                            headers=headers, params=params, cookies=cookies)
    result = json.loads(response.text)
    taskList = result["taskList"]
    print(taskList)
    for i in taskList:
        if i["taskId"] in [79, 80, 81]:  # 收听时长
            if i["status"] == 1:  # 可以领取
                print(i)
                taskRecordId = i["taskRecordId"]
                headers = {
                    'User-Agent': UserAgent,
                    'Host': 'm.ximalaya.com',
                    'Referer': 'https://m.ximalaya.com/growth-ssr-speed-welfare-center/page/welfare',
                    'Origin': 'https://m.ximalaya.com',
                }

                response = requests.post(
                    f'https://m.ximalaya.com/speed/task-center/task/receive/{taskRecordId}', headers=headers, cookies=cookies)
                print(response.text)
                time.sleep(1)

                print("\n")


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
    response = requests.get('https://m.ximalaya.com/speed/task-center/check-in/record',
                            headers=headers, params=params, cookies=cookies)
    result = json.loads(response.text)
    print(result["isTickedToday"])
    if result["isTickedToday"] == False:
        print("!!!未签到")
        pass


def group(cookies):
    print("\n【拼手气参团】")
    headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-cn',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/growth-groupon-h5/home',
        'Accept-Encoding': 'gzip, deflate, br',
    }

    params = (
        ('pageNo', '1'),
        ('pageSize', '10'),
        ('isMain', 'true'),
    )

    response = requests.get('https://m.ximalaya.com/speed/web-earn/group/list',
                            headers=headers, params=params, cookies=cookies)
    result = json.loads(response.text)
    todayJoinGroupCount = result["data"]["todayJoinGroupCount"]
    print(f"""{todayJoinGroupCount}/10""")
    if todayJoinGroupCount != 10:
        group_getReward(cookies, None, uid, "join")  # 加团

    groupInfoList = result["data"]["groupInfoList"][:todayJoinGroupCount]
    for i in groupInfoList:
        if not i["drawConsolationAward"]:         # 看广告
            userId = uid
            group_getReward(cookies, i["id"], userId, "")
            time.sleep(1)


def group_getReward(cookies, groupId, userId, flag):
    # print("\n【拼手气 成团】")
    headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-cn',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/growth-groupon-h5/home',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    """
    token
    """
    response = requests.get(
        'https://m.ximalaya.com/speed/web-earn/group/token', headers=headers, cookies=cookies)
    result = json.loads(response.text)
    print(result)
    token = result["data"]["id"]
    headers = {
        'User-Agent': UserAgent,
        'Content-Type': 'application/json;charset=utf-8',
        'Host': 'm.ximalaya.com',
        'Origin': 'https://m.ximalaya.com',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/growth-groupon-h5/home',
    }

    """
    drawJoin
    """
    data = {
        "groupId": groupId,
        "sign": rsa_encrypt(f"token={token}&userId={userId}", pubkey_str),
        "token": token,
    }
    if flag == "join":
        data["groupType"] = 1

    response = requests.post('https://m.ximalaya.com/speed/web-earn/group/drawJoin',
                             headers=headers, cookies=cookies, data=json.dumps(data))
    print("drawJoin", response.text, "\n")


def divide(cookies):
    print("\n【瓜分】")

    headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'XMSonicCacheURLHeader': '',
        'User-Agent': UserAgent,
        'Referer': 'http://m.ximalaya.com/growth-ssr-speed-welfare-center/page/divide-coin',
        'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
    }
    response = requests.get(
        f'http://m.ximalaya.com/speed/web-earn/carve/multipleInfo?ts={int(time.time()*1000)}', headers=headers, cookies=cookies)
    print(response.text)
    current = json.loads(response.text)["data"]["currentMultiple"]
    print(f"""{current}/5""")
    for i in range(5-current):
        print(i)
        response = requests.get(
            'http://m.ximalaya.com/speed/web-earn/carve/token', headers=headers, cookies=cookies)
        token = json.loads(response.text)["data"]["id"]

        data = {
            "data": rsa_encrypt(token+uid+uuid, pubkey_str),
            "token": token}
        headers = {
            'User-Agent': UserAgent,
            'Content-Type': 'application/json;charset=utf-8',
            'Host': 'm.ximalaya.com',
            'Origin': 'http://m.ximalaya.com',
            'Referer': 'http://m.ximalaya.com/growth-ssr-speed-welfare-center/page/divide-coin',
        }
        response = requests.post(
            'http://m.ximalaya.com/speed/web-earn/carve/add', headers=headers, cookies=cookies, data=json.dumps(data))
        print(response.text)
        time.sleep(1)


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

    response = requests.get(
        'https://m.ximalaya.com/speed/task-center/ad/token', headers=headers, cookies=cookies)
    result = response.json()
    token = result["id"]
    data = {
        "taskId": taskId,
        "businessType": businessType,
        "rsaSign": rsa_encrypt(f"""businessType={businessType}&token={token}&uid={uid}""", pubkey_str),
    }
    response = requests.post(f'https://m.ximalaya.com/speed/task-center/ad/score',
                             headers=headers, cookies=cookies, data=json.dumps(data))
    print(response.text)
    print("\n")


def ad_score_8(cookies, businessType, taskId, stage):

    headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain ,*/*',
        'Connection': 'keep-alive',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-cn',
        'Content-Type': 'application/json;charset=utf-8',
        'Accept-Encoding': 'gzip, deflate, br',
    }

    response = requests.get(
        'https://m.ximalaya.com/speed/task-center/ad/token', headers=headers, cookies=cookies)
    result = response.json()
    token = result["id"]
    data = {
        "taskId": taskId,
        "businessType": businessType,
        "rsaSign": rsa_encrypt(f"""businessType={businessType}&token={token}&uid={uid}""", pubkey_str),
        "extendMap": {"stage": stage}
    }
    response = requests.post(f'https://m.ximalaya.com/speed/task-center/ad/score',
                             headers=headers, cookies=cookies, data=json.dumps(data))
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

    response = requests.post('https://m.ximalaya.com/speed/web-earn/listen/bubbles',
                             headers=headers, cookies=cookies, data=json.dumps(data))
    result = response.json()
    print(result)
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

    response = requests.get(
        f'https://m.ximalaya.com/speed/web-earn/listen/receive/{taskId}', headers=headers, cookies=cookies)
    print("receive: ", response.text)


def stage_(cookies):
    """阶段红包"""
    print("\n【阶段红包】")
    headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-cn',
        'Referer': 'https://m.ximalaya.com/growth-ssr-speed-welfare-center/page/welfare',
        'Accept-Encoding': 'gzip, deflate, br',
    }

    response = requests.get(
        f'https://m.ximalaya.com/speed/web-earn/task/stage-rewards-daily', headers=headers, cookies=cookies)
    result = response.json()  # ["data"]
    if "errorCode" in result:
        print(result)
        return
    result = result["data"]["stageRewards"]
    j = 1
    enable_index = [i["status"] == 1 for i in result]
    for i in enable_index:
        if i:
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
                ('stage', str(j)),
            )

            response = requests.get('https://m.ximalaya.com/speed/web-earn/task/stage-reward-daily/receive',
                                    headers=headers, params=params, cookies=cookies)
            print(response.text)
            time.sleep(1)
            ad_score_8(cookies, 8, 120, j)
        j += 1

    print(enable_index)


def get_card_coin(cookies, themeId, cardIdList):
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
    response = requests.post('https://m.ximalaya.com/speed/web-earn/card/exchangeCoin',
                             headers=headers, cookies=cookies, data=json.dumps(data))
    print(response.text)


def exchangeCard(cookies, toCardAwardId, fromId):
    headers = {
        'User-Agent': UserAgent,
        'Content-Type': 'application/json;charset=utf-8',
        'Host': 'm.ximalaya.com',
        'Origin': 'https://m.ximalaya.com',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-activities/card-collection/home',
    }
    data = {
        "toCardAwardId": toCardAwardId,
        "fromId": fromId,
    }
    response = requests.post('https://m.ximalaya.com/speed/web-earn/card/exchangeCard',
                             headers=headers, cookies=cookies, data=json.dumps(data))
    print(response.text)


def card(cookies):
    headers = {
        'Host': 'm.ximalaya.com',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-cn',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-activities/card-collection/home',
        'Accept-Encoding': 'gzip, deflate, br',
    }

    response = requests.get(
        'https://m.ximalaya.com/speed/web-earn/card/userCardInfo', headers=headers, cookies=cookies)
    # print(response.text)
    userCardsList = response.json()["data"]["userCardsList"]
    allIds = set([i["id"] for i in userCardsList if i["id"] != 1])
    delt = set(range(2, 19))-allIds
    print(delt)
    OmnipotentCard = [i for i in userCardsList if i["id"] == 1]
    if delt and OmnipotentCard:
        exchangeCard(cookies, choice(list(delt)),
                     OmnipotentCard[0]["recordId"])

    jixiangwu2 = [i for i in userCardsList if i["id"] in [2, 3]]
    shangsiji4 = [i for i in userCardsList if i["id"] in [4, 5, 6, 7]]
    shuiguolao5 = [i for i in userCardsList if i["id"] in [8, 9, 10, 11, 12]]
    shangminghui6 = [i for i in userCardsList if i["id"]
                     in [13, 14, 15, 16, 17, 18]]
    _map = {
        2: [2, 3],
        3: [4, 5, 6, 7],
        4: [8, 9, 10, 11, 12],
        5: [13, 14, 15, 16, 17, 18]
    }
    for i in [jixiangwu2, shangsiji4, shuiguolao5, shangminghui6]:
        if not i:
            continue
        card_theme = i
        themeId = card_theme[0]["themeId"]
        print(f""">>>>{themeId} {_map[themeId]}""")
        recordIdList = []
        for _, v in groupby(card_theme, key=lambda x: x["id"]):
            recordIdList.append(list(v)[0])
        if len(recordIdList) == len(_map[themeId]):
            print("满足")
            cardIdList = [i["recordId"] for i in recordIdList]
            print(themeId, cardIdList)
            get_card_coin(cookies, themeId, cardIdList)


def getOmnipotentCard(cookies):
    print("\n 【万能卡】")
    headers = {
        'User-Agent': UserAgent,
        'Content-Type': 'application/json;charset=utf-8',
        'Host': 'm.ximalaya.com',
        'Origin': 'https://m.ximalaya.com',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-activities/card-collection/home',
    }
    result = requests.get('https://m.ximalaya.com/speed/web-earn/card/omnipotentCardInfo',
                         headers=headers, cookies=cookies,).json()
    print(result)
    count=result["data"]["count"]
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

    response = requests.post('https://m.ximalaya.com/speed/web-earn/card/getOmnipotentCard',
                             headers=headers, cookies=cookies, data=json.dumps(data))
    print(response.text)


def reportTime(cookies):
    print("\nreportTime\n")
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
    response = requests.post('https://m.ximalaya.com/speed/web-earn/card/reportTime',
                             headers=headers, cookies=cookies, data=json.dumps(data))
    print(response.text)


def hand(cookies):
    print("\n 【猜拳】")
    headers = {
        'User-Agent': UserAgent,
        'Host': 'm.ximalaya.com',
        'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-activities/finger-game/home',
    }
    response = requests.get(
        'https://m.ximalaya.com/speed/web-earn/mora/remainingTimes', headers=headers, cookies=cookies)
    lastTimes = response.json()["data"]
    print(lastTimes)
    for _ in range(lastTimes):
        headers = {
            'User-Agent': UserAgent,
            'Content-Type': 'application/json;charset=utf-8',
            'Host': 'm.ximalaya.com',
            'Origin': 'https://m.ximalaya.com',
            'Referer': 'https://m.ximalaya.com/xmds-node-spa/apps/speed-growth-activities/finger-game/home',
        }

        data = '{"betAmount":200,"gesture":2}'

        response = requests.post('https://m.ximalaya.com/speed/web-earn/mora/action',
                                 headers=headers, cookies=cookies, data=data)
        result = response.json()
        print(result)
        result=result["data"]
        if not result:
            return
        if result["winFlag"] == 1:
            moraRecordId = result["moraRecordId"]
            data = {"betAmount": 200,
                    "moraRecordId": moraRecordId,
                    "signData": rsa_encrypt(f"{200}{moraRecordId}{uid}", pubkey_str),
                    }

            response = requests.post(
                'https://m.ximalaya.com/speed/web-earn/mora/doubleAward', headers=headers, cookies=cookies, data=json.dumps(data))
            print(response.text)
            time.sleep(2)


def account(cookies):
    print("\n【打印当前信息】")
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

    response = requests.get(
        'https://m.ximalaya.com/speed/web-earn/account/coin', headers=headers, cookies=cookies)
    result = response.json()
    print(result)
    print(f"""
当前剩余:{result["total"]/10000}
今日获得:{result["todayTotal"]/10000}
累计获得:{result["historyTotal"]/10000}

""")


def saveListenTime(cookies):
    headers = {
        'User-Agent': UserAgent,
        'Host': 'mobile.ximalaya.com',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    listentime = date_stamp
    print(listentime//60)
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

    response = requests.post('http://mobile.ximalaya.com/pizza-category/ball/saveListenTime',
                             headers=headers, cookies=cookies, data=data)
    print(response.text)


##################################################################



def main(cookies):
    print("#"*20)
    print("\n")
    listenData(cookies)
    saveListenTime(cookies)
    #card(cookies)
    hand(cookies)
    #reportTime(cookies)
    #getOmnipotentCard(cookies)
    #stage_(cookies)
    bubble(cookies)
    checkin(cookies)
    print("\n【答题】")
    ans_times = ans_getTimes(cookies)

    for i in range(ans_times["stamina"]):
        paperId, dateStr, lastTopicId = ans_start(cookies)
        ans_receive(cookies, paperId, lastTopicId, 1)
        time.sleep(1)
        ans_receive(cookies, paperId, lastTopicId, 2)
        time.sleep(1)

    if ans_times["remainingTimes"] > 0:
        print("[看视频回复体力]")
        ans_restore(cookies)
        for i in range(5):
            paperId, dateStr, lastTopicId = ans_start(cookies)
            ans_receive(cookies, paperId, lastTopicId, 1)
            time.sleep(1)
            ans_receive(cookies, paperId, lastTopicId, 2)
            time.sleep(1)

    lottery_info(cookies)

    print("\n")


for i in cookiesList:
    print(">>>>>>>>>【账号开始】")
    cookies = str2dict(i)
    uid = cookies["1&_token"].split("&")[0]
    uuid = cookies["XUM"]
    main(cookies)
    account(cookies)
