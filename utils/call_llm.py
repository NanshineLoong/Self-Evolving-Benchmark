from openai import OpenAI
import zhipuai
import json
import requests
import time
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from config import opt

zhipuai_model_registry = ['chatglm_turbo']
openai_model_registry = ['chatgpt', 'gpt_4']

def get_openai_response(inputs_list, api_key, temp=0.0, max_tokens=256, logit_dict={}, model='chatgpt'):
    client = OpenAI(
        api_key=api_key
    )   
    all_messages = []
    if inputs_list[0] != "":
        all_messages.append({"role": "system", "content": inputs_list[0]})
    for i in range(1, len(inputs_list)):
        if i % 2 == 0:
            all_messages.append({"role": "assistant", "content": inputs_list[i]})
        else:
            all_messages.append({"role": "user", "content": inputs_list[i]})
    while True:
        try:
            if model == 'chatgpt':
                model = "gpt-3.5-turbo-1106"
            elif model == 'gpt_4':
                model = "gpt-4-1106-preview"
            completion = client.chat.completions.create(
                model=model,
                messages=all_messages,
                max_tokens=max_tokens,
                temperature=temp,
                logit_bias=logit_dict
            )
            break
        except Exception as e:
            sleep_time = 5
            print(e, f"Sleep {sleep_time} seconds.")
            time.sleep(sleep_time)
    return completion.choices[0].message.content

# chatglm_turbo
def invoke_zhipuai(prompt, api_key):
    zhipuai.api_key = api_key
    while True:
        try:
            response = zhipuai.model_api.invoke(
                model="chatglm_turbo",
                prompt=prompt,
                temperature=0.5,
            )
            break
        except Exception as e:
            sleep_time = 10
            print(e, f"Sleep {sleep_time} seconds.")
            time.sleep(sleep_time)
    return response['data']['choices'][0]['content'].strip('"').strip().replace('\\n', '\n')

def invoke_local_model(inputs_list, model_name, local_rul):
    raise NotImplementedError("The code for invoking local model is not implemented yet. Please implement it in the utils/call_llm.py file.")

def construct_mistral_string_prompt(input_list):
    input_string = ''
    input_string += '[INST]' + input_list[0] + '\n' + input_list[1]
    for i in range(2, len(input_list), 2):
        input_string += '[/INST]' + "Answer: " + input_list[i] + '\n\n' + '[INST]' + input_list[i + 1]
    input_string += '[/INST]'

    return input_string

def construct_string_prompt(input_list):
    input_string = ''
    input_string += input_list[0] + '\n'+ input_list[1]
    for i in range(2, len(input_list), 2):
        input_string += '\n' + "Answer: " + input_list[i] + '\n\n' + input_list[i + 1]
    input_string += '\nAnswer: '
    # print(input_string)
    return input_string

def get_completion(input_list, model, api_key, local_url=None):
    if model in openai_model_registry:
        if api_key['openai_api_key'] == '':
            raise ValueError("Please set the OpenAI API key in the config.py file.")  
        return get_openai_response(input_list, api_key['openai_api_key'], model=model)
    elif model in zhipuai_model_registry:
        if api_key['zhipuai_api_key'] == '':
            raise ValueError("Please set the Zhipuai API key in the config.py file.")
        input_string = construct_string_prompt(input_list)
        return invoke_zhipuai(input_string, api_key['zhipuai_api_key'])
    else:
        if local_url is not None:
            return invoke_local_model(input_list, model, local_url)
        else:
            raise ValueError("Not found the model in the registry. If it is a local model, please specify the local_url.")

if __name__ == '__main__':
    pass