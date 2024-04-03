import csv

def read_csv_file(filename):
    """
    读取 CSV 文件并返回其中的数据。

    参数：
    filename：CSV 文件路径

    返回值：
    包含 CSV 文件数据的列表，每行数据作为一个子列表。
    """
    data = []
    with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            data.append(row)
    return data

def read_csv_column_as_strings(filename, column_index):
    """
    读取 CSV 文件中指定列的数据并返回每行数据作为一个字符串的列表。

    参数：
    filename：CSV 文件路径
    column_index：要读取的列的索引

    返回值：
    包含每行数据的字符串列表。
    """
    column_data = []
    with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if len(row) > column_index:
                column_data.append(row[column_index])
    return column_data