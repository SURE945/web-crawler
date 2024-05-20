from src import url_crawler
from src import file_reader
from src import log_printer
import sys

accounts_csv = 'D:\\web-crawler\\data\\accounts.csv'
accounts_test_csv = 'D:\\web-crawler\\data\\accounts_test.csv'
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
    csv_file = accounts_csv if flag == 'offical' else accounts_test_csv
    csv_data = file_reader.read_csv_file(csv_file)
    accounts = [row[0] for row in csv_data]

    for i in range(len(csv_data)):
        # 2. get accounts last date
        crawler_obj = url_crawler.crawler(accounts[i], flag)
        # 3. get articles
        crawler_obj.crawl(accounts[i], keywords, flag)
        # 4. print to pdf
        crawler_obj.in_pdf(flag)

if __name__ == '__main__':
    main()