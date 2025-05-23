from response import  DeepSeekR1, DeepSeekResponser, Responser, TurboResponser
import os
import json
import time
from prompt.base_prompt import BUG_PROMPT, BUG_PROMPT_CoT
import re

def jsonl_to_dict(file_path, id_key='id'):
    result_dict = {}

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            item = json.loads(line.strip())
            key = item.get(id_key)
            if key is not None:
                result_dict[key] = item

    return result_dict

def load_data():
    with open("./MLDebug.jsonl", 'r', encoding='utf-8') as file:
        data_list = [json.loads(line) for line in file]
        return data_list

def find_last_python_code_block(text):
    code_blocks = re.findall(r'```python(.*?)```', text, re.DOTALL)

    if code_blocks:
        return code_blocks[-1]
    return ""

class BugGenerator(object):

    def __init__(self, responser):
        self.responser = responser

    def repair_bug(self, code: str) -> tuple[str, str]:
        """
        ask gpt-4 to generate a buggy python code
        :param code: the target code
        :return: buggy code
        """
        response = self.responser.respond(system_info=BUG_PROMPT_CoT, user_prompt=code)

        code = find_last_python_code_block(response)

        return code

from tqdm import tqdm

model_type = "Qwen/QwQ-32B"
if __name__ == '__main__':

    """ test """
    responser = DeepSeekResponser(model_type)
    # responser = TurboResponser(model_type)
    # responser = DeepSeekR1()
    agent = BugGenerator(responser)
    result_dict = jsonl_to_dict("/home/jyhuang/code/MLDebug/inference/result/QwQ-32B-cot.jsonl")
    ml_dataset = load_data()
    for item in tqdm(ml_dataset):
        instruct = item["instruct_prompt"]
        code = item["bug_code"]

        if item["ID"] in result_dict.keys() and result_dict[item["ID"]]["code_repair"] != "":
            continue

        attempts = 0
        while attempts < 10:
            try:
                input_message = "<instruct>\n" + instruct + "\n</instruct>" +"<bug_code>\n" + code + "\n</bug_code>"
                bug_repair = agent.repair_bug(input_message)
                break
            except Exception as e:
                print(e)
                time.sleep(2)
                attempts += 1
        if attempts >= 10:
            continue
        bug_dict = {
            "id": item["ID"],
            "code_repair":bug_repair,
            "test_case": item["test_case"],
            "category": item["category"]
        }
        with open(f"/home/jyhuang/code/MLDebug/inference/result/QwQ-32B-cot-2.jsonl", 'a+') as file:
            file.write(json.dumps(bug_dict)+"\n")
            file.flush()
            file.close()


