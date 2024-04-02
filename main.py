import crawler

def main():
    print("java-tech")
    biz = 'MzUxMjAwNjM2MA=='
    uin = 'MjM4MDAxMzQxMQ=='
    key = '7d521e321d0bd8f8c7fd2bb7c3d8a69e81e51193b1fd1844497fe9c9a2cc62b2f8d1750312b6ea44076ace848866a203c8e3152b772005181abdbeeedc2e15001df3e403d314d15b61a2b915176c6c0cc16acb0ce8cdccf71845ed628a6930aae1a2c505ef1fd805b2d9f4af42e1903fa2192aec7751f46d0e43bccd969f7915'
    crawler.get_history(biz, uin, key)
    print("java-tech")
    biz = 'MzUxMjAwNjM2MA=='
    uin = 'MjM4MDAxMzQxMQ=='
    key = '7d521e321d0bd8f8c7fd2bb7c3d8a69e81e51193b1fd1844497fe9c9a2cc62b2f8d1750312b6ea44076ace848866a203c8e3152b772005181abdbeeedc2e15001df3e403d314d15b61a2b915176c6c0cc16acb0ce8cdccf71845ed628a6930aae1a2c505ef1fd805b2d9f4af42e1903fa2192aec7751f46d0e43bccd969f7915'
    crawler.get_history(biz, uin, key)
    crawler.save_art_info()


if __name__ == '__main__':
    main()