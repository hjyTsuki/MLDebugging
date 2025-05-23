import json

# 读取两个JSONL文件的数据
def load_jsonl(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [json.loads(line) for line in file]

# 合并数据
def merge_jsonl(file1_path, file2_path, output_file_path):
    data1 = load_jsonl(file1_path)
    data2 = load_jsonl(file2_path)

    # 使用一个字典按ID进行合并
    merged_data = {}
    
    for item in data1:
        merged_data[item['id']] = item
    
    for item in data2:
        merged_data[item['id']] = item

    # 将合并后的数据保存为新的jsonl文件
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for item in merged_data.values():
            file.write(json.dumps(item, ensure_ascii=False) + '\n')

# 文件路径
file2_path = './result/Qwen2.5-Coder-32B-Instruct-CoT.jsonl'
file1_path = './result/Qwen2.5-Coder-32B-Instruct-cot.jsonl'
output_file_path = 'merged_output.jsonl'

merge_jsonl(file1_path, file2_path, output_file_path)
print(f"合并完成，保存为: {output_file_path}")
