"""
openai==1.30.3
"""

from openai import OpenAI

client = OpenAI(api_key="sk-proj-RBgey2y5NjBlbYSH5mZbT3BlbkFJ36omKDnuBoGYFniuKD6W")

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

stream_mode()