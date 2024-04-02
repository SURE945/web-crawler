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
    key = '17e9c66386b120bbe7e99346a4ac32052c50e053ed778619c174c26a8df99c26d426bac396b589418602801c0fe8deb668123da0e32d52eb6e065f69015c83549282e951130fc9ed94775984b9082393abff7fa688490c65fb424b87043dca62835d17530c8457a6892d39703f0ac3dc3ead6f8dd6f6dd4b466da71f2b252ed2'
    crawler.get_history(biz, uin, key, dates[0], 1)
    print("java-tech2")
    biz = 'MzUxMjAwNjM2MA=='
    uin = 'MjM4MDAxMzQxMQ=='
    key = '17e9c66386b120bbe7e99346a4ac32052c50e053ed778619c174c26a8df99c26d426bac396b589418602801c0fe8deb668123da0e32d52eb6e065f69015c83549282e951130fc9ed94775984b9082393abff7fa688490c65fb424b87043dca62835d17530c8457a6892d39703f0ac3dc3ead6f8dd6f6dd4b466da71f2b252ed2'
    crawler.get_history(biz, uin, key, dates[1], 2)

def main():
    readfile()
    info()
    crawler.save_art_info()

if __name__ == '__main__':
    main()