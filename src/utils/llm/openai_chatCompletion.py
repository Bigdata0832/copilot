"""
openai==1.30.3
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def stream_mode():
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "你是一個AI助手"},
            {"role": "user", "content": "哈囉"}
        ],
        stream=True
    )

    for chunk in completion:
        print(chunk.choices[0].delta.content,end="")

if __name__ == "__main__":
    stream_mode()