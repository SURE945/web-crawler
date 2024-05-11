#!/usr/bin/env python
# -*- coding: utf-8 -*-
import traceback
import requests
import csv
import random
import time
from src import new_printer
from pprint import pprint
import re

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

cookie = "RK=DRnpuR+GVf; ptcz=4de7f31efbd92a74738ca320fc7d0c73f5cb056b476a3c606c9735325d28bdf3; ua_id=xsUB8PowLcEhzJswAAAAAFlkeAAzDyRPbmf33bfylWg=; wxuin=13167235767384; mm_lang=zh_CN; rewardsn=; wxtokenkey=777; _clck=1168l8z|1|flo|0; uuid=5d6eed864a7ab2c9b0893d46cdeb0b7e; rand_info=CAESIDyw4djzOvTSJH0RnhtUxu3hnHigv6Fr5bcu+nWYKCqg; slave_bizuin=3915678078; data_bizuin=3915678078; bizuin=3915678078; data_ticket=iS7amOaLG/TdtkVHKvaI0zJ/fVGTVvldegzK23K9VmWLPCwih/jOIBeEoQBvcTOQ; slave_sid=aHYwaVNuWjl2UGh0SlViQ2Q2dkE4TkljM1J0RDdRSHZ2RmE2ekRLcDJzZFZZZkZidHNxc09POFBMOEo5Tl9KX2pmNlRLTzF6MTUxQWQ0Y0c5cHdEMmZwenZHekNrMlQ3SDhYWlJRM21JUnFyRUZ0Mzl3T3lBeWhsZlpRUEs1YUhiU3AzME5wWDN5ZzJEdmFE; slave_user=gh_d23bfd7b43a5; xid=c237f56f2f93ed95721cc804bb59a0f9; _clsk=1yepdjy|1715411747549|2|1|mp.weixin.qq.com/weheat-agent/payload/record"
token  = "577787959"

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
        pattern = re.compile(keyword)
        if pattern.search(string):
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
        new_printer.print_url_to_pdf(info.url, save_root, info.title)
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