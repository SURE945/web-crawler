#!/usr/bin/env python
# -*- coding: utf-8 -*-
import traceback
import requests
import csv
import random
import time
from src import pdf_print
from pprint import pprint

save_root = 'D:\\web-crawler\\res\\'
article_data  = []
__latest_date = []

class ArtInfo(object):
    def __init__(self, title, url, date):
        self.title = title
        self.url = url
        self.date = date

__session = requests.Session()
__headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}
__params = {
    "lang": "zh_CN",
    "f": "json",
}

cookie = "appmsglist_action_3915678078=card; RK=uQmp6z+tS/; ptcz=b81b78f64c1c6ebbefb28e5be19b795e7228f47e7f94cfa90cfbb8e19a50c1a6; pac_uid=0_e512eac24f90a; iip=0; pgv_pvid=6462161322; _qimei_uuid42=17b0e0a1e2f1007cc0eaa12740ee2e35efabe39a41; _qimei_fingerprint=cd838bb3f668d5a678cc7c3f05c52027; _qimei_q36=; _qimei_h38=8f9557bdc0eaa12740ee2e3502000000d17b0e; ua_id=hzpdFGya3ZJMGfJuAAAAAFHE1duewBS8PoBQDz7W-tM=; wxuin=11936855256056; data_bizuin=3915678078; bizuin=3915678078; data_ticket=FC6+Dw9fp8C/gZnG4hWG9cbPaj0ZkuKOzU9HlkCYanvuLNdlTES8K+7Kq9yIUO6T; rand_info=CAESIG8xEDNTEQcvQLdEE/4O+Ev9z/f/+Pmg3rVLKiKEZJG2; slave_bizuin=3915678078; slave_user=gh_d23bfd7b43a5; slave_sid=Qlp2U0N6U3lCdkRtWTRVbHN5Vll2S2EwcnFGdFNBU0FJWWhsaUo1eUJIWlVKbktWelVpTDZCcVEwUXNwOVRqSzk5cFpRdU1pN3VfOUtQOVQyQk51UWVQaE1hWDE1eTFjUWpNV1UzZ0dYblNEcGNQUzBadUpTU3N2a1BOSTB5dGRoOEF4V0ZwdUFCRk5kWTJI; _clck=3915678078|1|fkm|0; _clsk=5teb5w|1712110119848|6|1|mp.weixin.qq.com/weheat-agent/payload/record"
token = "1712078137"

def get_fakeid(nickname, begin=0, count=5):
    search_url = "https://mp.weixin.qq.com/cgi-bin/searchbiz"

    # 增加/更改请求参数
    params = {
    "action": "search_biz",
    "query": nickname,
    "begin": begin,
    "count": count,
    "ajax": "1",
    }
    __params.update(params)

    try:
        search_gzh_rsp = __session.get(search_url, headers=__headers, params=__params)
        rsp_list = search_gzh_rsp.json()["list"]
        # print(rsp_list)
        if rsp_list:
            return rsp_list[0].get('fakeid')
            return None
    except Exception as e:
        raise Exception(f'获取公众号{nickname}的fakeid失败，e={traceback.format_exc()}')

def contains_any_keyword(string, keywords):
    """
    判断字符串是否包含关键词集合中的任意一个。

    参数：
    string：要检查的字符串
    keywords：关键词集合

    返回值：
    如果字符串包含关键词集合中的任意一个，则返回 True，否则返回 False。
    """
    for keyword in keywords:
        if keyword in string:
            return True
    return False

def get_articles(nickname, date, flag, keywords, begin=0, count=5):
    __record_idx = 0
    for i in range(begin, count, 5):
        print("==第", (i / 5 + 1), "页==")
        art_url = "https://mp.weixin.qq.com/cgi-bin/appmsg"
        art_params = {
        "query": '',
        "begin": str(i * 5),
        "count": "5",
        "type": 9,
        "action": 'list_ex',
        }
        __params.update(art_params)

        try:
            rsp_data = __session.get(art_url, headers=__headers, params=__params)
            #pprint(rsp_data)
            if rsp_data:
                msg_json = rsp_data.json()
                #pprint(msg_json)

            if 'app_msg_list' in msg_json.keys():
                #result = [item.get('title') + ': ' + item.get('link') + ': ' + str(item.get('create_time')) for item in msg_json.get('app_msg_list') ]
                for item in msg_json.get('app_msg_list'):
                    if item.get('create_time') <= date:
                        return
                    if __record_idx == 0:
                        __latest_date.append(str(item.get('create_time')))
                        __record_idx = 1
                    if contains_any_keyword(item.get('title'), keywords):
                        result = ArtInfo(item.get('title'), item.get('link'), str(item.get('create_time')))
                        article_data.append(result)
                # return msg_json.get('app_msg_list')
            else:
                return []
        except Exception as e:
            raise Exception(f'获取公众号{nickname}的文章失败，e={traceback.format_exc()}')

        time.sleep(random.randint(1,10))
        if (flag == 'test'):
            in_csv("data\\" + nickname + ".csv")

def in_csv(title):
    with open(title, 'w', newline='',encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['date', 'title', 'url'])
        for info in article_data:
            writer.writerow([info.date, info.title, info.url])

def in_pdf(accounts):
    for info in article_data:
        pdf_print.print_url_to_pdf(info.url, save_root, info.title)
        time.sleep(5)

    # update dates
    headers = ['date', 'account']
    with open('data\\dates.csv', 'w', newline='',encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        accounts = accounts[1:]
        for row in zip(__latest_date, accounts):
            writer.writerow(row)

def crawl(nickname, keywords, date=1671546449, flag='offical'):
    __headers["Cookie"] = cookie
    __params["token"] = token

    fakeid = get_fakeid(nickname)
    print(nickname)
    __params["fakeid"] = fakeid

    get_articles(nickname, date, flag, keywords, 0, 10)