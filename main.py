import crawler

def main():
    print("java-tech")
    biz = 'MzUxMjAwNjM2MA=='
    uin = 'MjM4MDAxMzQxMQ=='
    key = 'cba1c122413701d62b24e7a0d21679a0639c52ac8eefcb94eb16a4af70a145540b641b8a6c10a724e4442b19e080fc1d0666114eb0fa42b40f3178fcd2298aa95eaee3aeedfec8cd7aa0bd6c947bfb0a3db39b3dbd7cadfe6ff32b0154c0cc742c50f28f19f292c2f92610ff11eb1d03764fac9100103638a05d118751f05861'
    crawler.get_history(biz, uin, key)
    print("java-tech")
    biz = 'MzUxMjAwNjM2MA=='
    uin = 'MjM4MDAxMzQxMQ=='
    key = 'cba1c122413701d62b24e7a0d21679a0639c52ac8eefcb94eb16a4af70a145540b641b8a6c10a724e4442b19e080fc1d0666114eb0fa42b40f3178fcd2298aa95eaee3aeedfec8cd7aa0bd6c947bfb0a3db39b3dbd7cadfe6ff32b0154c0cc742c50f28f19f292c2f92610ff11eb1d03764fac9100103638a05d118751f05861'
    crawler.get_history(biz, uin, key)
    crawler.save_art_info()


if __name__ == '__main__':
    main()