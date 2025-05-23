import os
import time
import openai
from abc import ABC, abstractmethod


class Responser(ABC):

    @abstractmethod
    def respond(self, system_info: str, user_prompt: str) -> str:
        pass


# class TurboResponser(Responser):
#     """ Openai LLM responser """

#     def __init__(self, model='gpt-3-turbo'):
#         """ environment information """
#         self.model = model
#         # openai.api_key = 'sk-hptadds0MqwHSpO4f3ZjQdZA6tGgflTK2Fb2c5ffkR36PdBw'
#         # openai.api_base = 'https://xiaoai.plus/v1'
#         openai.api_key = "sk-M14akbdYvKD8OWAv0e2cD978D2D84f47B801Dc3bE172B6F2"
#         openai.api_base = "http://vip.ooo.cool/v1"

#     def respond(self, system_info: str, user_prompt: str) -> str:

#         messages = [
#             {"role": "system", "content": system_info},
#             {"role": "user", "content": user_prompt}
#         ]
#         response = openai.ChatCompletion.create(
#             # model='gpt-4',
#             # model='gpt-3.5-turbo',
#             # model = "gpt-4o-mini-2024-07-18",
#             # model='gpt-4o',
#             # model='gpt-3.5-turbo-16k',
#             model = self.model,
#             temperature=0,
#             messages=messages
#         )
#         return response['choices'][0]['message']['content']

class TurboResponser(Responser):
    """ Openai LLM responser """

    def __init__(self, model='gpt-3-turbo'):
        """ environment information """
        # openai.api_key = os.environ.get("OPENAI_API_KEY")
        # openai.api_base = os.environ.get("OPENAI_API_BASE")
        # openai.api_key = 'sk-MfsGu5ILuHxYMuoSGYAbX0lwMMO2rnfjIqMZGxI0RgLaf89Y'
        # openai.api_base = 'https://www.blueshirtmap.com/v1'
        # openai.api_key = "sk-y78PUFWUEuN5ZmNx7826D16888134f398a872c7cC75dA722"
        # openai.api_base = "https://one.ooo.cool/v1"
        openai.api_key = "sk-tfxw7TpDIIkzwk6h58Bf444cD9B7480a8e04A9D51994C61a"
        openai.api_base = "https://one.ooo.cool/v1"
        self.model = model

    def respond(self, system_info: str, user_prompt: str) -> str:
        """
        respond to system_info and user prompt
        :param system_info: see in openai documentation
        :param user_prompt: see in openai documentation
        :return: response in form of string
        """
        messages = [
            {"role": "system", "content": system_info},
            {"role": "user", "content": user_prompt}
        ]
        response = openai.ChatCompletion.create(
            # model='gpt-4',
            model= self.model,
            # model = "gpt-4o-mini-2024-07-18",
            # model='gpt-4o',
            # model='gpt-3.5-turbo-16k',
            temperature=0,
            messages=messages
        )
        return response['choices'][0]['message']['content']

class GeminiResponser(Responser):
    """ Openai LLM responser """

    def __init__(self, model='gpt-3-turbo'):
        """ environment information """
        self.model = model
        openai.api_key = 'sk-hptadds0MqwHSpO4f3ZjQdZA6tGgflTK2Fb2c5ffkR36PdBw'
        openai.api_base = 'https://xiaoai.plus/v1'
        openai.api_key = "sk-tfxw7TpDIIkzwk6h58Bf444cD9B7480a8e04A9D51994C61a"
        openai.api_base = "https://one.ooo.cool/v1"

    def respond(self, system_info: str, user_prompt: str) -> str:

        messages = [
            {"role": "system", "content": system_info},
            {"role": "user", "content": user_prompt}
        ]
        response = openai.ChatCompletion.create(
            model = self.model,
            n=1,
            temperature=0.6,
            messages=messages
        )
        return response['choices'][0]['message']['content']

class DeepSeekResponser(Responser):
    """ Openai LLM responser """

    def __init__(self, model='gpt-3-turbo'):
        """ environment information """
        self.model = model
        openai.api_key = 'sk-hbsbzutooubnzifhooemtgznobyixupmtvytphtwxsjcvrmw'
        openai.api_base = 'https://api.siliconflow.cn/v1'

    def respond(self, system_info: str, user_prompt: str) -> str:

        messages = [
            {"role": "system", "content": system_info},
            {"role": "user", "content": user_prompt}
        ]
        response = openai.ChatCompletion.create(
            model = self.model,
            temperature=0,
            messages=messages
        )
        return response['choices'][0]['message']['content']


qus = """
A professor of logic had three students, and all three were extremely intelligent! One day, the professor posed a problem to them. He stuck a piece of paper on each of their foreheads and told them that each paper had a positive integer written on it, and the sum of two of the numbers was equal to the third! (Each person could see the other two numbers but not their own.) The professor asked the first student, "Can you guess your own number?" The answer was, "No." He then asked the second student, "No." The third student, "No." He asked the first student again, "No." The second student, "No." The third student: "I've figured it out, it's 144!" The professor smiled contentedly. How many possible combinations are there for the numbers of the other two students?
"""
if __name__ == '__main__':
    turbo_responser = DeepSeekResponser("Qwen/QwQ-32B")
    print(turbo_responser.respond(system_info="you are a hippie.",
                                  user_prompt=qus))
    # turbo_responser = TurboResponser("gpt-4o-mini-2024-07-18")
    # print(turbo_responser.respond(system_info="you are a hippie.",
    #                               user_prompt=f"fuck you"))
