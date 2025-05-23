from openai import OpenAI

url = 'https://api.siliconflow.cn/v1/'
api_key = 'sk-hbsbzutooubnzifhooemtgznobyixupmtvytphtwxsjcvrmw'

client = OpenAI(
    base_url=url,
    api_key=api_key
)

# 发送带有流式输出的请求
content = "请你设计一个代码问题, 然后推理解答"
reasoning_content=""
messages = [
    {"role": "user", "content": "奥运会的传奇名将有哪些？"}
]
response = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-R1",
    messages=messages,
    stream=True,  # 启用流式输出
    max_tokens=4096
)
# 逐步接收并处理响应
for chunk in response:
    if chunk.choices[0].delta.content:
        content += chunk.choices[0].delta.content
    if chunk.choices[0].delta.reasoning_content:
        reasoning_content += chunk.choices[0].delta.reasoning_content

# Round 2
messages.append({"role": "assistant", "content": content})
messages.append({'role': 'user', 'content': "继续"})
response = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-R1",
    messages=messages,
    stream=True
)