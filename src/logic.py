from src.utils.llm.openai_assistant import (
    retrieve_assistant, create_thread, delete_thread, create_message_in_thread, run_assistant, get_chat_history
)
from src.utils.prompt import get_prompt

def select_assistant(name):
    """
    Retrieves an assistant by name and returns its ID.

    Args:
        name (str): The name of the assistant.

    Returns:
        str: The ID of the assistant.
    """
    assistant = retrieve_assistant(name=name)
    return assistant.id

def start_chat():
    """
    Starts a new chat session by creating a thread and returns its ID.

    Returns:
        str: The ID of the newly created thread.
    """
    return create_thread().id

def clear_chat(thread_id):
    """
    Clears the chat by deleting the specified thread.

    Parameters:
        thread_id (int): The ID of the thread to be deleted.

    Returns:
        Response of API
    """
    return delete_thread(thread_id)

def send_message(
    user_message,
    assistant_id,
    thread_id,
    instructions=None,
    max_completion_tokens=None,
    max_prompt_tokens=None,
    tools=None,
    model=None,
):
    """
    Sends a user message to the assistant in a specified thread and runs the assistant with optional parameters.

    Args:
        user_message (str): The message from the user to be sent to the assistant.
        assistant_id (str): The ID of the assistant to run.
        thread_id (str): The ID of the thread in which the message will be sent and the assistant will be run.
        instructions (str, optional): Additional instructions for the assistant.
        max_completion_tokens (int, optional): The maximum number of tokens the assistant can generate.
        max_prompt_tokens (int, optional): The maximum number of tokens the assistant can consume.
        tools (list, optional): A list of tools to use for the assistant.
        model (str, optional): The model to use for the assistant.

    Returns:
        Chat history list.
    """
    # Create Message in Thread
    create_message_in_thread(thread_id=thread_id, role="user", content=user_message)

    # Prepare arguments for run_assistant
    run_assistant_args = {
        "thread_id": thread_id,
        "assistant_id": assistant_id,
    }

    # Add optional parameters if provided
    if instructions is not None:
        run_assistant_args["instructions"] = instructions
    if max_completion_tokens is not None:
        run_assistant_args["max_completion_tokens"] = max_completion_tokens
    if max_prompt_tokens is not None:
        run_assistant_args["max_prompt_tokens"] = max_prompt_tokens
    if tools is not None:
        run_assistant_args["tools"] = tools
    if model is not None:
        run_assistant_args["model"] = model

    # Run Assistant
    run = run_assistant(**run_assistant_args)
    chat_history = get_chat_history(run=run, thread_id=thread_id)
    return chat_history
