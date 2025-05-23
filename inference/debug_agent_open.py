from response_open import CodeQwen, Deepseek, Mistral
from response_open import  Responser, CodeLLama
import os
import json
import time
from prompt.base_prompt import BUG_PROMPT, BUG_PROMPT_Reasoning

import re

def find_last_python_code_block(text):
    code_blocks = re.findall(r'```python(.*?)```', text, re.DOTALL)

    if code_blocks:
        return code_blocks[-1]
    return ""

def load_data():
    with open("./MLDebug.jsonl", 'r', encoding='utf-8') as file:
        data_list = [json.loads(line) for line in file]
        return data_list

class BugGenerator(object):

    def __init__(self, responser):
        self.responser = responser

    def repair_bug(self, code: str) -> tuple[str, str]:
        """
        ask gpt-4 to generate a buggy python code
        :param code: the target code
        :return: buggy code
        """
        response = self.responser.respond(system_info=BUG_PROMPT, user_prompt=code)
        
        code_head = response.find('<corrected_code>') + len('<corrected_code>')
        code_end = response.find('</corrected_code>')
        code = response[code_head:code_end]
        return code

        # return find_last_python_code_block(response)

from tqdm import tqdm

if __name__ == '__main__':

    """ test """
    # model_type='CodeQwen-32B'
    # responser = CodeQwen()
    # model_type='Mistral-14b'
    # responser = Mistral()
    model_type='QwenCoder7B-codefeedback'
    responser = CodeQwen()
    agent = BugGenerator(responser)
    ml_dataset = load_data()
    for item in tqdm(ml_dataset):
        instruct = item["instruct_prompt"]
        code = item["bug_code"]

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
        with open(f"./result/{model_type}.jsonl", 'a+') as file:
            file.write(json.dumps(bug_dict)+"\n")
            file.flush()
            file.close()


