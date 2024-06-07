import json

def parse_json_file(file_path):
    try:
        # 打开并读取 JSON 文件
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        # print("解析成功!")
        # print("解析的数据为：")
        # print(data)
        return data
    except FileNotFoundError:
        print(f"文件未找到: {file_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"解析 JSON 时出错: {e}")
        return None

'''
# 示例文件路径
json_file_path = 'data.json'

# 调用解析函数
parsed_data = parse_json_file(json_file_path)

# 如果解析成功，可以进一步处理数据
if parsed_data:
    print("Name:", parsed_data["name"])
    print("Age:", parsed_data["age"])
    print("City:", parsed_data["city"])
    print("Children:")
    for child in parsed_data["children"]:
        print(f"  - {child['name']}, {child['age']} years old")
'''
