import os
import openai

try:
    from keys import *
except:
    API_KEY = input("OpenAI Key: ")

openai.api_key = API_KEY

def fetch(call):
    prompt = "I am a Spanish student and you are my tutor. I am going to speak in spanish to you and I would like you to critique my grammar."
    prompt += call
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[" Student:", " AI:"]
    )

    return response['choices'][0]['text'].strip()

