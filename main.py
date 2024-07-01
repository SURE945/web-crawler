from src import url_crawler
from src import file_reader
from src import log_printer
from src import json_parser
import sys

def main():
    # 0. check parameters
    if len(sys.argv) != 2:
        print("param error! please input test or offical")
        return
    flag = sys.argv[1]
    if (flag != 'test' and flag != 'official'):
        print("param error! please input test or offical")
        return

    parsed_data = json_parser.parse_json_file("config.json")
    theme = parsed_data["theme"]
    cookie = parsed_data["cookie"]
    token = parsed_data["token"]
    check_article_num = parsed_data["check_article_num"]
    max_article_num = parsed_data["max_article_num"]
    accounts_csv      = 'D:\\web-crawler\\data\\' + theme + '\\accounts.csv'
    accounts_test_csv = 'D:\\web-crawler\\data\\' + theme + '\\accounts_test.csv'
    keywords_csv      = 'D:\\web-crawler\\data\\' + theme + '\\keywords.csv'

    # 1. initialize
    log_printer.initialize_file()
    keywords = file_reader.read_csv_column_as_strings(keywords_csv, 0)
    csv_file = accounts_csv if flag == 'official' else accounts_test_csv
    csv_data = file_reader.read_csv_file(csv_file)
    accounts = [row[0] for row in csv_data]

    for i in range(len(csv_data)):
        # 2. get accounts last date
        crawler_obj = url_crawler.crawler(accounts[i], theme, flag, cookie, token, check_article_num, max_article_num)
        # 3. get articles
        crawler_obj.crawl(accounts[i], keywords, flag)
        # 4. print to pdf
        crawler_obj.in_pdf(flag)

if __name__ == '__main__':
    main()