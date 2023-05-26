import json
from pprint import pprint

import openai

messages = {}

file = open('config.json', 'r')
config = json.load(file)

openai.api_key = config['api_key']


def update(username: str, messages, role, content):
    if username not in messages:
        messages[username] = [{"role": role, "content": content}]
    else:
        messages[username].append({"role": role, "content": content})
    #pprint(messages)


def resp(content: str, username: str, model_="gpt-3.5-turbo"):
    update(username, messages, "user", content)
    response = openai.ChatCompletion.create(
        model=model_,
        messages=messages[username]
    )
    update(username, messages, "assistant", response["choices"][0]["message"]["content"])
    return response


def reset():
    messages.clear()
    #print(messages)
