import os

from dotenv import load_dotenv
from openai import OpenAI

# Settings
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Adjust
def create_assistant(
    name, description=None, instructions=None, temperature=1, model="gpt-4o"
):
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
    """
    Retrieves a list of assistants from the OpenAI API.

    Returns:
        list: A list of assistant objects representing the assistants.
    """
    my_assistants = client.beta.assistants.list(
        order="desc",
        limit="20",
    )
    return my_assistants.data


def retrive_assistant(assistant_id):
    """
    Retrieve an assistant by its ID.

    Args:
        assistant_id (str): The ID of the assistant to retrieve.

    Returns:
        dict: The assistant object representing the assistant with the given ID.
    """
    assistant = client.beta.assistants.retrieve(assistant_id)
    return assistant


def delete_assistant(assistant_id):
    response = client.beta.assistants.delete(assistant_id)
    return response


# Operate
def create_thread(messages=None):
    """
    Create a thread to chat.

    Args:
        messages (list, optional): A list of dictionaries representing the messages in the thread.
        Each dictionary should have the keys 'role' and 'content'. Defaults to None.
        messages = [{"role": "user","content": "推薦幾個AI技術給我"},...]

    Returns:
        dict: The created thread.
    """
    thread = client.beta.threads.create(messages=messages)
    return thread


def delete_thread(thread_id):
    """
    Deletes a thread with the given thread ID.

    Parameters:
        thread_id (str): The ID of the thread to be deleted.

    Returns:
        None
    """
    response = client.beta.threads.delete(thread_id)
    print(response)


def create_messages_to_thread(thread_id, role, content):
    """
    Create a message in a thread with the given thread ID, role, and content.

    Args:
        thread_id (str): The ID of the thread to create the message in.
        role (str): The role of the message sender.
        content (str): The content of the message.

    Returns:
        None
    """
    _ = client.beta.threads.messages.create(
        thread_id=thread_id, role=role, content=content
    )


def run_assistant(
    thread_id,
    assistant_id,
    instructions=None,
    max_completion_tokens=None,
    max_prompt_tokens=None,
    tools=None,
):
    """
    Runs an assistant in a thread with the given thread ID, assistant ID, and optional parameters.

    Args:
        thread_id (str): The ID of the thread to run the assistant in.
        assistant_id (str): The ID of the assistant to run.
        instructions (str, optional): Additional instructions for the assistant. Defaults to None.
        max_completion_tokens (int, optional): The maximum number of tokens the assistant can generate. Defaults to None.
        max_prompt_tokens (int, optional): The maximum number of tokens the assistant can consume. Defaults to None.
        tools (list, optional): A list of tools to use for the assistant. Defaults to None.

    Returns:
        openai.api_resources.beta.threads.runs.Run: The run object representing the assistant's execution.
    """
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
    """
    Retrieves the chat history from a completed run.

    Args:
        run (openai.api_resources.beta.threads.runs.Run): The run object representing the completed assistant execution.
        thread_id (str): The ID of the thread to retrieve the chat history from.

    Returns:
        list: A list of strings representing the chat history. Each string is in the format "role: text_content".
        If the run is not completed, an empty list is returned.
    """
    if run.status == "completed":
        messages = client.beta.threads.messages.list(thread_id=thread_id)
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
    # assistant = create_assistant(
    #     name="KEYPO Copilot",
    #     description="你是個做輿情分析的專家，協助使用者進行輿情分析",
    #     instructions="除了輿情分析的話題，其他都拒絕回答"
    # )
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
