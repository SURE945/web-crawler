def append_to_file(content, end="\n", flush=True):
    with open("log.txt", "a", encoding="utf-8") as file:
        print(content, end=end, flush=flush, file=file)

def initialize_file():
    with open("log.txt", "w", encoding="utf-8") as file:
        file.write("")  # 清空文件内容
