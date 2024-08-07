#!/usr/bin/env python
# -*- coding: utf-8 -*-
import traceback
import requests
import csv
import random
import time
from . import pdf_printer
from . import log_printer
from pprint import pprint
import re
import os

class ArtInfo(object):
    def __init__(self, title, url, date):
        self.title = title
        self.url = url
        self.date = date

class crawler:
    def __init__(self, nickname, theme, flag, cookie, token, check_ariticle_num, max_article_num):
        self.article_data  = []
        self.__headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
        self.save_root = 'D:\\web-crawler\\res\\' + theme + '\\'
        self.__latest_date = []
        self.check_article_num = check_ariticle_num
        self.max_article_num = max_article_num
        self.cookie = cookie
        self.token  = token
        self.__session = requests.Session()
        self.__params = {
            "lang": "zh_CN",
            "f": "json",
        }
        self.__theme = theme
        if (flag == 'official'):
            self.last_date = self.check_and_modify_csv("data\\" + self.__theme + "\\test\\" + nickname + ".csv")
        else:
            self.last_date = self.check_and_modify_csv("data\\" + self.__theme + "\\test\\test.csv")

    def check_and_modify_csv(self, file_path):
        default_date = '1671546449'
        # 检查文件是否存在
        if not os.path.exists(file_path):
            # 文件不存在，创建并写入第一行
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                first_row = ['date', 'title', 'url']
                writer.writerow(first_row)
            # print(f"文件 '{file_path}' 不存在，已创建并写入第一行：{first_row}")
            return default_date
        else:
            # 文件存在，读取内容
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                rows = list(reader)

            # 判断文件中的行数
            if len(rows) == 1:
                # print("文件存在，且只有一行，不进行操作。")
                return default_date
            elif len(rows) > 1:
                # 获取最后一行的第一列
                last_row_first_column = rows[-1][0]
                # print(f"文件存在，最后一行的第一列的值是：{last_row_first_column}")
                return last_row_first_column

    def get_fakeid(self, nickname, begin=0, count=5):
        search_url = "https://mp.weixin.qq.com/cgi-bin/searchbiz"
        # 增加/更改请求参数
        params = {
        "action": "search_biz",
        "query": nickname,
        "begin": begin,
        "count": count,
        "ajax": "1",
        }
        self.__params.update(params)
        try:
            search_gzh_rsp = self.__session.get(search_url, headers=self.__headers, params=self.__params)
            rsp_list = search_gzh_rsp.json()["list"]
            # print(rsp_list)
            if rsp_list:
                return rsp_list[0].get('fakeid')
                return None
        except Exception as e:
            raise Exception(f'获取公众号{nickname}的fakeid失败，e={traceback.format_exc()}')

    def contains_any_keyword(self, string, keywords):
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

    def get_articles(self, nickname, date, flag, keywords, begin=0, count=5):
        __article_num  = 0

        for i in range(begin, count, 5):
            __end = False
            self.local_print((i / 5 + 1), end='', flush=True)
            art_url = "https://mp.weixin.qq.com/cgi-bin/appmsg"
            art_params = {
            "query": '',
            "begin": str(i * 5),
            "count": "5",
            "type": 9,
            "action": 'list_ex',
            }
            self.__params.update(art_params)

            try:
                while not __end:
                    rsp_data = self.__session.get(art_url, headers=self.__headers, params=self.__params)
                    if rsp_data:
                        msg_json = rsp_data.json()
                        if 'app_msg_list' in msg_json.keys():
                            self.local_print(',', end=' ', flush=True)
                            for item in msg_json.get('app_msg_list'):
                                # 还没找到上限，先到了时间
                                if item.get('create_time') <= date:
                                    reversed_list = list(reversed(self.article_data))
                                    if flag=='official':
                                        self.in_csv("data\\" + self.__theme + "\\test\\" + nickname + ".csv", reversed_list)
                                    else:
                                        self.in_csv("data\\" + self.__theme + "\\test\\test.csv", reversed_list)
                                    self.local_print("end")
                                    return
                                #print(item.get('title'))
                                if self.contains_any_keyword(item.get('title'), keywords):
                                    result = ArtInfo(item.get('title'), item.get('link'), str(item.get('create_time')))
                                    self.article_data.append(result)
                                    __article_num = __article_num + 1
                                if __article_num >= self.max_article_num:
                                    break
                        else:
                            reversed_list = list(reversed(self.article_data))
                            if flag=='official':
                                self.in_csv("data\\" + self.__theme + "\\test\\" + nickname + ".csv", reversed_list)
                            else:
                                self.in_csv("data\\" + self.__theme + "\\test\\test.csv", reversed_list)
                            self.local_print("访问被限制, end")
                            return
                    __end = True
            except Exception as e:
                raise Exception(f'获取公众号{nickname}的文章失败，e={traceback.format_exc()}')

            time.sleep(random.randint(1,10))
        reversed_list = list(reversed(self.article_data))
        if flag=='official':
            self.in_csv("data\\" + self.__theme + "\\test\\" + nickname + ".csv", reversed_list)
        else:
            self.in_csv("data\\" + self.__theme + "\\test\\test.csv", reversed_list)
        self.local_print("end")

    def in_csv(self, title, data_set):
        with open(title, 'a', newline='',encoding='utf-8') as f:
            writer = csv.writer(f)
            #writer.writerow(['date', 'title', 'url'])
            for info in data_set:
                writer.writerow([info.date, info.title, info.url])

    def in_pdf(self, flag):
        if (flag == 'official'):
            for info in self.article_data:
                pdf_printer.print_url_to_pdf(info.url, self.save_root, info.title)
                time.sleep(5)

    def local_print(self, content, end='\n', flush=True):
        print(content, end=end, flush=flush)
        log_printer.append_to_file(content, end=end, flush=flush)

    def crawl(self, nickname, keywords, flag=''):
        self.__headers["Cookie"] = self.cookie
        self.__params["token"] = self.token

        fakeid = self.get_fakeid(nickname)
        self.local_print(nickname, end='...', flush=True)
        self.__params["fakeid"] = fakeid

        self.get_articles(nickname, int(self.last_date), flag, keywords, 0, self.check_article_num)
