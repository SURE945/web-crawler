#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import json
import time
from datetime import date
import requests

__art_infos = []

'''
日期：2024年2月23日
公众号ID：java-tech
公众号：Java实用技术手册
声明：本文仅供技术研究，请勿用于非法采集，后果自负。
'''
class ArtInfo(object):
    """
    文章信息：包括日期、标题、题图、链接
    """

    def __init__(self, pub_date, json_info):
        self.pub_date = pub_date
        self.title = json_info.get('title')
        self.cover = json_info.get('cover')
        self.content_url = json_info.get('content_url')


def get_history(offset=0, count=10, continue_flag=True):
    biz = 'MzUxMjAwNjM2MA=='  #你的biz
    uin = 'MjM4MDAxMzQxMQ=='  #你的uin
    key = 'cba1c122413701d685ae2ea8eb713e874673a2c27f4715a4e5a2324718c92e248a48b1f26c292643f4d59869302fe4f83b7ebb2bf8ca699fa0b4cda7540f0d078497ed7beb2cd00ae23f9e9171baaab775cc7ca804c488b35c2203c6e43c796354511f2c39810ed47be04eb6d5fe1f0744290ebd6255bce50c5d14975b76fdd6'  #你的key
    # pass_ticket = 'tS1eMbmDmdNLrZP5/55e6BrLg9TWDuGOFkOXYPIXM8N1SWkZbAEGALDh6kaMQO/GPFT1emxuf j0Rnxxlq iUw=='

    url = f'https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz={biz}&f=json&offset={offset}&count={count}&is_ok=1&scene=124&uin={uin}&key={key}'
    res = requests.get(url)
    #print(res.json())
    js = res.json()
    # print(js.get('general_msg_list').get('list'))
    general_msg_list_str = js.get('general_msg_list')
    msg_list_json = json.loads(general_msg_list_str)
    art_list = msg_list_json.get('list')
    for art in art_list:
        get_art_info(art)

    # can_msg_continue 是用来判断是否可以继续获取文章的
    if js.get('can_msg_continue') and continue_flag:
        offset = offset + count
        print(f'===继续获取下一页,offset={offset}')
        time.sleep(10)  # 防封
        get_history(offset, 10, True) # 测试一次就不继续

    else:
        print('结束，没有更多文章。')


def get_art_info(json_art_info):
    comm_msg_info = json_art_info.get('comm_msg_info')

    # 获取发文时间
    datetime_ms = comm_msg_info.get('datetime')
    pub_datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(datetime_ms))
    #print('pub_datetime=', pub_datetime)
    pub_date = str(date.fromtimestamp(datetime_ms))
    info = json_art_info.get('app_msg_ext_info')
    if info:
        # 头条消息
        art_info0 = ArtInfo(pub_date, info)
        # art_info0.parse(info)
        #print('头条：', art_info0.__dict__)
        __art_infos.append(art_info0)

        # 次消息
        multi_item_list = info.get('multi_app_msg_item_list')
        if multi_item_list:
            for item in multi_item_list:
                art_info = ArtInfo(pub_date, item)
                #print('次头条：', art_info.__dict__)
                __art_infos.append(art_info)
                # break


def save_art_info(art_infos):
    with open('art_infos.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['pub_date', 'title', 'cover', 'content_url'])
        for info in art_infos:
            writer.writerow([info.pub_date, info.title, info.cover, info.content_url])


def main():
    get_history()
    save_art_info(__art_infos)


if __name__ == '__main__':
    main()

