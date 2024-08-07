import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def chat_completion(messages, model="gpt-4o-mini", temperature=0):
    """
    Generates a chat completion using the OpenAI Chat API.

    Args:
        messages (list): The input prompt try to generate completions.
        model (str, optional): The name of the model to use for completion. Defaults to "gpt-4o-mini".
        temperature (float, optional): The temperature value for generating the completion. Defaults to 0.

    Returns:
        dict: The completion response from the Chat API.
    """
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    print(f"Prompt:{response.usage.prompt_tokens}, Completion:{response.usage.completion_tokens}")

    return response.choices[0].message.content


if __name__ == "__main__":
    resp = chat_completion(
        system_prompt="你只會說不要吵，無論使用者問什麼",
        user_prompt="你是誰",
        model="gpt-4o",
        temperature=0.8,
    )
    print(resp)
