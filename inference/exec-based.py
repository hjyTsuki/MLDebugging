from response import  Responser, TurboResponser, GPT4Responser
import os
import json
import time
from prompt.base_prompt import BUG_PROMPT, RUNTIME_PROMPT, RUNTIME_PROMPT_RUN, RUNTIME_PROMPT_TEST

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
        response = self.responser.respond(system_info=RUNTIME_PROMPT_TEST, user_prompt=code)

        code_head = response.find('<corrected_code>') + len('<corrected_code>')
        code_end = response.find('</corrected_code>')
        code = response[code_head:code_end]

        return code

from tqdm import tqdm
# model_type='gpt-4'
# model_type ='gpt-3.5-turbo'
# model = "gpt-4o-mini-2024-07-18",
# model='gpt-4o',
# model='gpt-3.5-turbo-16k',
# model_type = "gpt-4o-mini-2024-07-18"
# model_type='gpt-4o'
# model_type='gpt-3.5-turbo'
model_type = "claude-3-5-sonnet-20241022"
# model_type = "gemini-1.5-pro-latest"
if __name__ == '__main__':

    """ test """
    responser = TurboResponser(model_type)
    agent = BugGenerator(responser)
    ml_dataset = load_data()
    # print('only runtime feedback')
    for item in tqdm(ml_dataset):
        instruct = item["instruct_prompt"]
        code = item["bug_code"]
        test_case = item["test_case"]
        feedback = item["runtime_feedback"]

        attempts = 0
        while attempts < 10:
            try:
                input_message = "<instruct>\n" + instruct + "\n</instruct>" +"<bug_code>\n" + code + "\n</bug_code>"
                input_message += f"<test_case>\n {test_case} \n <test_case>"
                # input_message += f"<runtime_feedback>\n {feedback} \n</runtime_feedback>"
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
        with open(f"./result/{model_type}-test_case-t0.jsonl", 'a+') as file:
            file.write(json.dumps(bug_dict)+"\n")
            file.flush()
            file.close()


