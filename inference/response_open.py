import os
import time
import openai
from abc import ABC, abstractmethod
from vllm import LLM, SamplingParams

class Responser(ABC):

    @abstractmethod
    def respond(self, system_info: str, user_prompt: str) -> str:
        pass


class CodeLLama(Responser):
    def __init__(self, model='/home/jyhuang/.cache/modelscope/hub/AI-ModelScope/CodeLlama-13b-Instruct-hf/'):
        # 初始化 vLLM 推理引擎
        self.llm = LLM(model=model, 
                       max_model_len=4096, 
                       trust_remote_code=True)

    def respond(self, system_info: str, user_prompt: str) -> str:
        sampling_params = SamplingParams(temperature=0, max_tokens = 4096)
        prompts = system_info + user_prompt
        output = self.llm.generate(prompts, sampling_params)
        return output[0].outputs[0].text
    
class LLama3(Responser):
    # /home/jyhuang/.cache/modelscope/hub/LLM-Research/Meta-Llama-3___1-14B-Instruct/
    # /home/jyhuang/.cache/modelscope/hub/llm-research/meta-llama-3___1-8b-instruct/
    def __init__(self, model='/home/jyhuang/.cache/modelscope/hub/LLM-Research/Meta-Llama-3___1-14B-Instruct/'):
        # 初始化 vLLM 推理引擎
        self.llm = LLM(model=model, 
                       max_model_len=4096, 
                       trust_remote_code=True)

    def respond(self, system_info: str, user_prompt: str) -> str:
        sampling_params = SamplingParams(temperature=0, max_tokens = 4096)
        prompts = system_info + user_prompt
        output = self.llm.generate(prompts, sampling_params)
        return output[0].outputs[0].text

class CodeQwen(Responser):
    def __init__(self, model='/home/jyhuang/code/LLaMA-Factory-main/models/qwencoder7b_codefeedback'):
        # 初始化 vLLM 推理引擎
        self.llm = LLM(model=model, 
                       max_model_len=4096, 
                       trust_remote_code=True)

    def respond(self, system_info: str, user_prompt: str) -> str:
        sampling_params = SamplingParams(temperature=0, max_tokens = 4096)
        prompts = system_info + user_prompt + "<|im_end>\n <|im_start|>assistant"
        output = self.llm.generate(prompts, sampling_params)
        return output[0].outputs[0].text

class Mistral(Responser):
    def __init__(self, model='/home/jyhuang/.cache/modelscope/hub/LLM-Research/Mistral-14B-Instruct-v0___3/'):
        # 初始化 vLLM 推理引擎
        self.llm = LLM(model=model, 
                       max_model_len=4096, 
                       trust_remote_code=True)

    def respond(self, system_info: str, user_prompt: str) -> str:
        sampling_params = SamplingParams(temperature=0, max_tokens = 4096)
        prompts = system_info + user_prompt
        output = self.llm.generate(prompts, sampling_params)
        return output[0].outputs[0].text

class Deepseek(Responser):
    # /home/jyhuang/.cache/modelscope/hub/maple77/DeepSeek-Coder-V2-Lite-Instruct/
    # /home/jyhuang/.cache/modelscope/hub/deepseek-ai/deepseek-coder-6___7b-instruct/
    def __init__(self, model='/home/jyhuang/.cache/modelscope/hub/deepseek-ai/DeepSeek-R1-Distill-Qwen-14B/'):
        # 初始化 vLLM 推理引擎
        self.llm = LLM(model=model, 
                       max_model_len=4096, 
                       trust_remote_code=True)

    def respond(self, system_info: str, user_prompt: str) -> str:
        sampling_params = SamplingParams(temperature=0, max_tokens = 4096)
        prompts = system_info + user_prompt + f"### Response:\n\n"
        output = self.llm.generate(prompts, sampling_params)
        return output[0].outputs[0].text

if __name__ == '__main__':
    turbo_responser = CodeQwen()
    print(turbo_responser.respond(system_info="you are a python coder.",
                                  user_prompt=f"write a program to print 1-10."))
