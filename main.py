import crawler
import csv

date_str = "2023-04-12"
dates = []

def readfile():
    with open('D:\\web-crawler\\dates.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        global dates
        dates = [row['date'] for row in reader]   # weight 同列的数据

def info():
    print("java-tech")
    biz = 'MzUxMjAwNjM2MA=='
    uin = 'MjM4MDAxMzQxMQ=='
    key = '00e58c2b456c255bfe94d58ae8edbc243fa895da07257498b16a05359fbe9401bc1a1019f7d24d84299a08bdb284fb3cd2c20e26828a10a6d655006f5696c58a737325fc952692828bdb5a6848af36ad6bfee0c6ff1b701230d4b5608e726c663d871533a725104fa53c76b96bfda00b85affbccc4afb6d77ef843a62eba2104'
    crawler.get_history(biz, uin, key, dates[0], 1)
    print("java-tech2")
    biz = 'Mzg3MTUxOTk2OQ=='
    uin = 'MjM4MDAxMzQxMQ=='
    key = '2b21e5c6d92d765ea48bf3680315eaf80c6e661934a1f36ce9591745750989934ab4e38fcc4b2cab80d1373253f61b885ff0ff98c089cdea77bfe434f6e3d4898e61ff120b827c9d41b891a972255b237f72b8267607f1e53291eaa00e6100a7ceaf15dc65d021ca53c29103a449372ebfaa188a6411d7c4163fe9c9340c56dd'
    crawler.get_history(biz, uin, key, dates[1], 2)

def main():
    readfile()
    info()
    crawler.save_art_info()

if __name__ == '__main__':
    main()