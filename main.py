from src import url_crawler
from src import file_reader
from src import log_printer
import sys

dates_csv = 'D:\\web-crawler\\data\\dates.csv'
dates_test_csv = 'D:\\web-crawler\\data\\dates_test.csv'
keywords_csv = 'D:\\web-crawler\\data\\keywords.csv'

def main():
    # 0. check parameters
    if len(sys.argv) != 2:
        print("param error! please input test or offical")
        return
    flag = sys.argv[1]
    if (flag != 'test' and flag != 'offical'):
        print("param error! please input test or offical")
        return

    # 1. initialize
    log_printer.initialize_file()
    keywords = file_reader.read_csv_column_as_strings(keywords_csv, 0)
    csv_file = dates_csv if flag == 'offical' else dates_test_csv
    csv_data = file_reader.read_csv_file(csv_file)
    dates = [row[0] for row in csv_data]
    accounts = [row[1] for row in csv_data]

    # 2. get articles
    for i in range(len(csv_data)):
        if (i != 0):
            url_crawler.crawl(accounts[i], keywords, int(dates[i]), flag)

    # 3. print to pdf
    url_crawler.in_pdf(flag)

    # 4. update memory
    url_crawler.update_dates(accounts, flag)

if __name__ == '__main__':
    main()