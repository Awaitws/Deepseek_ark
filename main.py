import os
from openai import OpenAI
from configparser import ConfigParser
from volcenginesdkarkruntime import Ark

# 读取ini文件信息
conf = ConfigParser()
conf.read('data/conf.ini')

# 创建客户端对象
client = OpenAI(
    api_key = conf['data']['ARK_API_KEY'], 
    base_url = "https://ark.cn-beijing.volces.com/api/v3",
    )

# 创建流式对话
def chat(messages,model):
    user_input = input()
    print('思考中...\n')
    messages_str = ''
    answer_f = []
    answer_f_l = []
    messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model = conf['data'][model],
        messages = messages,
        stream = True
    )
    for chunk in response:
        if not chunk.choices:
            continue
        print(chunk.choices[0].delta.content, end = '')
        messages_str += chunk.choices[0].delta.content
        answer_f_l.append(chunk.choices[0].delta)
    answer_f = answer_f_l[0]
    answer_f.content = messages_str
    messages.append(answer_f)
    print()
    return messages

model_c = eval(input('选择你想要使用的大模型:\n\
1.Deepseek-R1 671B\n\
2.Deepseek-R1 32B\n\
3.Deepseek-R1 7B\n\
4.Deepseek-V3\n\
5.豆包pro 128k\n\
键入数字并回车:'))
model_list = ['model_dsr1','model_dsr1_32','model_dsr1_7','model_dsv3','model_doubaopro128']
model = model_list[model_c - 1]
message = []
print('User:')
m = chat(message,model)
while True:
    print('User:')
    m = chat(m,model)