import new_crawler
import csv
import sys

dates = []

def readfile():
    with open('D:\\web-crawler\\dates.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        global dates
        dates = [row['date'] for row in reader]

def main():
    if len(sys.argv) != 2:
        print("param error! please input test or offical")
        return
    flag = sys.argv[1]
    if (flag != 'test' and flag != 'offical'):
        print("param error! please input test or offical")
        return
    readfile()
    new_crawler.crawl("国际太空", int(dates[0]), flag)
    #new_crawler.crawl("Java实用技术手册", int(dates[1]))
    if (flag == 'offical'):
        new_crawler.in_pdf()

if __name__ == '__main__':
    main()