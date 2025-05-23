import json
import multiprocessing
import os
import sys
import types
import unittest
import time
from typing import Tuple

import numpy as np

from check_utils import safe_environment, create_tempdir, reliability_guard, swallow_io, time_limit

PASS = "pass"
FAIL = "fail"
TIMEOUT = "timeout"

_SUCCESS = 0
_FAILED = 1
_TIMEOUT = 2
_UNKNOWN = 3

_mapping = {_SUCCESS: PASS, _FAILED: FAIL, _TIMEOUT: TIMEOUT, _UNKNOWN: None}

def get_jsonl_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
            data_list = [json.loads(line) for line in file]
            return data_list

def unsafe_execute(
        code: str,
        test_code: str,
        timeout: float,
        max_as_limit: float,
        max_data_limit: float,
        max_stack_limit: float,
        stat,  # Value
        details,  # Array
):
    with safe_environment(), create_tempdir():
        # These system calls are needed when cleaning up tempdir.
        import os
        import shutil
        import builtins

        rmtree = shutil.rmtree
        rmdir = os.rmdir
        chdir = os.chdir
        # Disable functionalities that can make destructive changes to the test.
        reliability_guard(max_as_limit, max_data_limit, max_stack_limit)
        module_name = "__test__"
        new_module = types.ModuleType(module_name)
        # Set necessary attributes for the module
        new_module.__dict__.update({
            '__builtins__': builtins,
            '__file__': f"{module_name}.py",
            '__package__': None,
            '__doc__': None,
            'sys': sys,
            'os': os,
            'environ': os.environ,
        })

        try:
            full_code = code + "\n" + test_code

            with swallow_io():
                exec(compile(full_code, f"{module_name}.py", 'exec'), new_module.__dict__)
                sys.modules[module_name] = new_module
                TestCases = getattr(new_module, 'TestCases')
                loader = unittest.TestLoader()
                suite = loader.loadTestsFromTestCase(TestCases)
                test_result = unittest.TestResult()
                start_time = time.time()
                with time_limit(timeout):
                    suite.run(test_result)

            issues = test_result.failures + test_result.errors
            for test, trace in issues:
                details[test.id().split(".")[-1]] = trace
            stat.value = _SUCCESS
        except BaseException as e:
            details["ALL"] = str(e)
            stat.value = _FAILED
        # Needed for cleaning up.
        shutil.rmtree = rmtree
        os.rmdir = rmdir
        os.chdir = chdir



def untrusted_check(
        code: str,
        test_code: str,
        max_as_limit: int = 30 * 1024,
        max_data_limit: int = 30 * 1024,
        max_stack_limit: int = 10,
        min_time_limit: float = 10,
        gt_time_limit: float = 60
) -> Tuple[str, np.ndarray]:
    min_time_limit = max(min_time_limit, gt_time_limit)
    timeout = max(os.getenv("BIGCODEBENCH_TIMEOUT_PER_TASK", 10), min_time_limit) + 1
    # shared memory objects
    stat = multiprocessing.Value("i", _UNKNOWN)
    manager = multiprocessing.Manager()
    details = manager.dict()

    p = multiprocessing.Process(
        target=unsafe_execute,
        args=(
            code,
            test_code,
            timeout,
            max_as_limit,
            max_data_limit,
            max_stack_limit,
            stat,
            details,
        ),
    )
    p.start()
    p.join(timeout=timeout + 1)
    if p.is_alive():
        p.terminate()
        time.sleep(0.1)
    if p.is_alive():
        p.kill()
        time.sleep(0.1)

    stat = _mapping[stat.value]
    # convert details to a dict
    details = dict(details)

    if not stat:
        stat = TIMEOUT
    if stat == PASS:
        if details:
            stat = FAIL

    return stat, details

model_type = "gpt-4o-mini-2024-07-18"
# model_type='gpt-40.4'
# model_type='gpt-3.5-turbo'
# model_type = "claude-3-5-sonnet-20241022-test_case-feedback-t0"
# model_type='LLama3.1-8b'
# model_type = "CodeQwen-14B"
# model_type = "gpt-3.5-turbo-test_case-feedback"
# model_type = "Mistral-7b"
# model_type = "gemini-1.5-pro-latestt0.6"
# model_type='Deepseek-Coder-14b'
model_type = "R1"
# arguments = sys.argv
# model_type = arguments[1]

from tqdm import tqdm
def main():
    # results = get_jsonl_file(f"/home/jyhuang/code/MLDebug/inference/fewshots_result/{model_type}.jsonl")
    # results = get_jsonl_file(f"/home/jyhuang/code/MLDebug/inference/result/{model_type}.jsonl")
    results = get_jsonl_file("/home/jyhuang/code/MLDebug/inference/result/DeepSeek-R1-cot.jsonl")
    category_dict = {
    "Type Mismatch":{"all":0, "pass":0},
    "Data Transfer Issues":{"all":0, "pass":0},
    "Function Parameter Errors":{"all":0, "pass":0},
    "Parameter Configuration Errors":{"all":0, "pass":0},
    "Function Misuse":{"all":0, "pass":0},
    "Requirement Misunderstanding":{"all":0, "pass":0},
    "Import Errors":{"all":0, "pass":0}
    }
    eval_result = {}
    right_count = 0

    for item in tqdm(results):
        code = item["code_repair"]
        test_code = item["test_case"]
        stat, details = untrusted_check(code, test_code)
        eval_result[item["id"]] = {
            "stat": stat,
            # "details": details
        }
        if stat == PASS:
            right_count += 1
        for k, pass_count in category_dict.items():
            if k in item["category"]:
                pass_count["all"] += 1
                if stat == PASS:
                    pass_count["pass"] += 1
    print(model_type)
    print(f"pass rate {(right_count / len(results)):.2%}")
    for k, v in category_dict.items():
        if v['all'] == 0:
            continue  
        print(f"{k}: {v['pass'] / v['all']}")
    
    with open(f"./model_result/{model_type}_result.jsonl", "w") as f:
        f.write(json.dumps(eval_result))



if __name__ == "__main__":
    main()
