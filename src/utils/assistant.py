import os

from dotenv import load_dotenv
from openai import OpenAI

# Settings
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def hello(name):
    return f"Hello {name}!"

# Adjust
def create_assistant(name, description=None, instructions=None, temperature=1, model="gpt-4o"):
    """Create an assistant

    Args:
        name (str): name of assistant
        description (str): To describe the assistant's information. Defaults to None.
        instructions (str): Like the system to instruct ai. Defaults to None.
        temperature (int): Adjust ai response. Defaults to 1.
        model (str, optional): Model gpt-4-turbo, gpt-4, gpt-3.5-turbo, gpt-3.5-turbo-16k. Defaults to "gpt-4o".

    Returns:
        class: Assistant object
    """
    assistant = client.beta.assistants.create(
        name=name,
        model=model,
        instructions=instructions,
        description=description,
        temperature=temperature,
        # tools=[
        #     {"type": "file_search"},
        #     {"type": "code_interpreter"}
        # ],
    )
    return assistant

def list_assistant():
    my_assistants = client.beta.assistants.list(
        order="desc",
        limit="20",
    )
    return my_assistants.data

def retrive_assistant(assistant_id):
    assistant = client.beta.assistants.retrieve(assistant_id)
    return assistant

def delete_assistant(assistant_id):
    response = client.beta.assistants.delete(assistant_id)
    return response


# Operate
def create_thread(messages=None):
    """Create a thread to chat
    messages = [{"role": "user","content": "推薦幾個AI技術給我"},...]
    """
    thread = client.beta.threads.create(messages=messages)
    return thread

def delete_thread(thread_id):
    response = client.beta.threads.delete(thread_id)
    print(response)

def create_messages_to_thread(thread_id, role, content):
    _ = client.beta.threads.messages.create(
        thread_id=thread_id,
        role=role,
        content=content
    )

def run_assistant(thread_id, assistant_id, instructions=None, max_completion_tokens=None, max_prompt_tokens=None, tools=None):
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions=instructions,
        max_completion_tokens=max_completion_tokens,
        max_prompt_tokens=max_prompt_tokens,
        tools=tools,
    )
    return run

def get_chat_history(run, thread_id):
    if run.status == 'completed': 
        messages = client.beta.threads.messages.list(
            thread_id=thread_id
        )
        data = messages.data
        chat_history = []
        for message in data:
            role = message.role
            text_content = message.content[0].text.value
            chat_history.append(f"{role}: {text_content}")
        chat_history.reverse()
        return chat_history
    else:
        print(run.status)
        return []

if __name__ == "__main__":
    # Create
    # assistant = create_assistant(name="KEYPO Copilot", description="你是個做輿情分析的專家，協助使用者進行輿情分析", instructions="除了輿情分析的話題，其他都拒絕回答")
    # print(assistant)
    # thread = create_thread()
    # print(thread)

    # Operate
    # assistants = list_assistant()
    assistant_id = "asst_Q0aogQUlR5PkLuBB6Hmh6mk5"
    thread_id = "thread_3BlDvnPAXyUEVto9TWhHwqJr"

    # Do
    create_messages_to_thread(thread_id=thread_id, role="user", content="告訴我為何天氣如此棒")
    run = run_assistant(thread_id=thread_id, assistant_id=assistant_id)
    print(run)
    chat_history = get_chat_history(run=run, thread_id=thread_id)
    print(chat_history)
