from response import  DeepSeekResponser, Responser, TurboResponser
import os
import json
import time
from prompt.base_prompt import BUG_PROMPT, BUG_PROMPT_Reasoning

def load_data():
    with open("./MLDebug.jsonl", 'r', encoding='utf-8') as file:
        data_list = [json.loads(line) for line in file]
        return data_list

import re

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
        response = self.responser.respond(system_info=BUG_PROMPT_Reasoning, user_prompt=code)

        return find_last_python_code_block(response)

from tqdm import tqdm
# model_type='gpt-4'
# model='gpt-3.5-turbo',
# model = "gpt-4o-mini-2024-07-18",
# model='gpt-4o',
# model='gpt-3.5-turbo-16k',
# model_type = "gpt-4o-mini-2024-07-18"
# model_type='gpt-4o'
# model_type='gpt-3.5-turbo'
# model_type = "claude-3-5-sonnet-20241022"
model_type = "gemini-1.5-pro-latest"
model_type = "deepseek-ai/DeepSeek-R1"
model_type = "Qwen/Qwen2.5-Coder-32B-Instruct"
model_type = "Qwen/QwQ-32B-Preview"
model_type = "deepseek-ai/DeepSeek-R1-Distill-Llama-70B"
model_type = "deepseek-ai/DeepSeek-R1-Distill-Llama-8B"
model_type = "deepseek-ai/DeepSeek-R1-Distill-Llama-70B"
model_type = "Qwen/QwQ-32B"
# model_type = "meta-llama/Meta-Llama-3.1-70B-Instruct"
if __name__ == '__main__':

    """ test """
    responser = DeepSeekResponser(model_type)
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
        with open(f"./result/{model_type.replace('deepseek-ai/', '')}.jsonl", 'a+') as file:
            file.write(json.dumps(bug_dict)+"\n")
            file.flush()
            file.close()


