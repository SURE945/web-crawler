import crawler

date_str = "2023-04-12"

def info():
    print("java-tech")
    biz = 'MzUxMjAwNjM2MA=='
    uin = 'MjM4MDAxMzQxMQ=='
    key = '7d521e321d0bd8f88e8a10f964d585b19acfbee5c498bc320bd3a1eb70b2ea1a5ccd4b4d2eb56808ef700d0155501a40ce3919f3b8f346f5b84b23b0528672613ab7b823f2f8d7f92a175a34640c31c6155e0062bcfd18c104f353666cfcfb7876e55b96e6189e9fe976b1954347ac51e79bff05cc2060a233bf5e0d8c1646ed'
    crawler.get_history(biz, uin, key, date_str, 1)
    print("java-tech")
    biz = 'MzUxMjAwNjM2MA=='
    uin = 'MjM4MDAxMzQxMQ=='
    key = '7d521e321d0bd8f88e8a10f964d585b19acfbee5c498bc320bd3a1eb70b2ea1a5ccd4b4d2eb56808ef700d0155501a40ce3919f3b8f346f5b84b23b0528672613ab7b823f2f8d7f92a175a34640c31c6155e0062bcfd18c104f353666cfcfb7876e55b96e6189e9fe976b1954347ac51e79bff05cc2060a233bf5e0d8c1646ed'
    crawler.get_history(biz, uin, key, date_str, 2)

def main():
    info()
    crawler.save_art_info()

if __name__ == '__main__':
    main()