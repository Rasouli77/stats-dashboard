import os
from openai import OpenAI
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()

AI_API_KEY = os.environ.get('AI_API_KEY')

client = OpenAI(api_key=AI_API_KEY, base_url="https://api.deepseek.com")

def ai_give_answers(messages, temperature, max_tokens=2048, stream=False):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=stream
    )
    return response

messages = [
    {"role": "system", "content": "You are a data analyst who speaks in Persian"},
    {"role": "user", "content": "Hi"}
]

response = ai_give_answers(messages, 1)
print(response.choices[0].message.content)