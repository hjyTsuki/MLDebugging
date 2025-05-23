import random

from response import Responser, TurboResponser
import os
import json
import time
from prompt.few_shots_prompt import SAMPLES_PROMPT

def load_data():
    with open("/home/jyhuang/code/MLDebug/inference/MLDebug.jsonl", 'r', encoding='utf-8') as file:
        data_list = [json.loads(line) for line in file]
        return data_list


def get_sample(data, curr_id, num_of_samples, mode: str = "random"):
    sample_set = set()
    sample_set.add(curr_id)
    count = 0
    if mode == "random":
        data_len = len(data)
        max_try = 100
        while count < num_of_samples and max_try > 0:
            pos = random.randint(0, data_len - 1)
            if pos not in sample_set and pos != curr_id:
                sample_set.add(pos)
                count += 1
            max_try -= 1
    elif mode == "category":
        import pickle
        samples = []
        with open('/home/jyhuang/code/MLDebug/inference/category_dict.pkl', 'rb') as file:
            category_dict = pickle.load(file)
        for k, v in category_dict.items():
            if k in data[curr_id]["category"]:
                samples += v

        if len(samples) == 0:
            return ""
        data_len = len(samples)
        max_try = 100
        while count < num_of_samples and max_try > 0:
            pos = random.randint(0, data_len - 1)
            if pos not in sample_set and pos != curr_id:
                sample_set.add(samples[pos])
                count += 1
            max_try -= 1
    elif mode == "lib":
        return
    samples_str = ""
    a = 1
    sample_set.remove(curr_id)
    for i in sample_set:
        item = data[i]
        samples_str += f"====Sample{a}====\n"
        samples_str += f"Inputs:\n"
        samples_str += "<instruct>\n" + item["instruct_prompt"] + "\n</instruct>\n"
        samples_str += "<bug_code>\n" + item["bug_code"] + "\n</bug_code>\n"
        samples_str += f"Outputs:\n"
        samples_str += "<bug_description>\n" + item["bug_description"] + "\n</bug_description>\n"
        samples_str += "<corrected_code>\n" + item["code_prompt"] + item["golden_code"] + "\n</corrected_code>\n"
        a += 1
    return samples_str

class BugGenerator(object):

    def __init__(self, responser):
        self.responser = responser

    def repair_bug(self, code: str, samples) -> tuple[str, str]:
        """
        ask gpt-4 to generate a buggy python code
        :param code: the target code
        :return: buggy code
        """
        response = self.responser.respond(system_info=SAMPLES_PROMPT.format(samples), user_prompt=code)

        code_head = response.find('<corrected_code>') + len('<corrected_code>')
        code_end = response.find('</corrected_code>')
        code = response[code_head:code_end]

        return code

from tqdm import tqdm
model_type = "gpt-4o-mini-2024-07-18"
import sys
num_of_sample = 1
# # 获取所有命令行参数
arguments = sys.argv
num_of_sample = int(arguments[1])
print(num_of_sample)
if __name__ == '__main__':

    """ test """
    # responser = DeepSeekResponser(model_type)
    responser = TurboResponser(model_type)
    agent = BugGenerator(responser)
    ml_dataset = load_data()
    i = 0
    for item in tqdm(ml_dataset):
        instruct = item["instruct_prompt"]
        code = item["bug_code"]
        sample_str = get_sample(ml_dataset, i, num_of_sample)
        attempts = 0
        while attempts < 10:
            try:
                input_message = "<instruct>\n" + instruct + "\n</instruct>" +"<bug_code>\n" + code + "\n</bug_code>"
                bug_repair = agent.repair_bug(input_message, sample_str)
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
        with open(f"./fewshots_result/{model_type}-random-{num_of_sample}.jsonl", 'a+') as file:
            file.write(json.dumps(bug_dict)+"\n")
            file.flush()
            file.close()
        i+=1