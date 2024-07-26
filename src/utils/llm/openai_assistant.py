import os
from dotenv import load_dotenv
from openai import OpenAI


class LLMAssistant:
    def __init__(self, model="gpt-4o-mini"):
        """
        Initializes an instance of the LLMAssistant class.

        Args:
            model (str, optional): The model to use for the assistant. Defaults to "gpt-4o-mini".
        """
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model

    def create_assistant(
        self,
        name,
        description=None,
        instructions=None,
        temperature=1,
        file_search=False,
        code_interpreter=False,
    ):
        """
        Creates an assistant with the given name, description, instructions, temperature, file search, and code interpreter settings.

        Args:
            name (str): The name of the assistant.
            description (str, optional): The description of the assistant. Defaults to None.
            instructions (str, optional): The instructions for the assistant. Defaults to None.
            temperature (float, optional): The temperature for the assistant. Defaults to 1.
            file_search (bool, optional): Whether to enable file search for the assistant. Defaults to False.
            code_interpreter (bool, optional): Whether to enable code interpreter for the assistant. Defaults to False.

        Returns:
            openai.api_resources.beta.assistants.Assistant: The assistant object representing the created assistant.
        """
        tools = []
        if file_search:
            tools.append({"type": "file_search"})
        if code_interpreter:
            tools.append({"type": "code_interpreter"})

        assistant = self.client.beta.assistants.create(
            name=name,
            model=self.model,
            instructions=instructions,
            description=description,
            temperature=temperature,
            tools=tools,
        )
        return assistant

    def list_assistants(self):
        """
        Retrieves a list of assistants from the OpenAI API.

        Returns:
            list: A list of assistant objects representing the retrieved assistants.
        """
        assistants = self.client.beta.assistants.list(order="desc", limit="20")
        return assistants.data

    def retrieve_assistant(self, name):
        """
        Retrieves an assistant by name.

        Parameters:
            name (str): The name of the assistant to retrieve.

        Returns:
            Assistant or None: The assistant object if found, None otherwise.
        """
        assistants = self.list_assistants()
        for assistant in assistants:
            if assistant.name == name:
                return assistant
        return None

    def delete_assistant(self, assistant_id):
        """
        Deletes an assistant by its ID.

        Args:
            assistant_id (str): The ID of the assistant to delete.

        Returns:
            Response: The response object representing the deletion result.
        """
        response = self.client.beta.assistants.delete(assistant_id)
        return response

    def create_thread(self, messages=None):
        """
        Create a thread with optional messages.

        Parameters:
            messages (list, optional): A list of dictionaries representing the messages in the thread.
            Each dictionary should have the keys 'role' and 'content'. Defaults to None.

        Returns:
            dict: The created thread.
        """
        thread = self.client.beta.threads.create(messages=messages)
        return thread

    def delete_thread(self, thread_id):
        """
        Deletes a thread with the given thread ID.

        Args:
            thread_id (str): The ID of the thread to be deleted.

        Returns:
            Response: The response object representing the deletion result.
        """
        response = self.client.beta.threads.delete(thread_id)
        return response

    def create_message_in_thread(self, thread_id, role, content):
        """
        Creates a message in a thread with the given thread ID, role, and content.

        Args:
            thread_id (str): The ID of the thread to create the message in.
            role (str): The role of the message sender.
            content (str): The content of the message.
        """
        _ = self.client.beta.threads.messages.create(
            thread_id=thread_id, role=role, content=content
        )

    def run_assistant(
        self,
        thread_id,
        assistant_id,
        instructions=None,
        max_completion_tokens=None,
        max_prompt_tokens=None,
        tools=None,
        model=None,
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
            model (str, optional): The model to use for the assistant. Defaults to None.

        Returns:
            openai.api_resources.beta.threads.runs.Run: The run object representing the assistant's execution.
        """
        if model is None:
            model = self.model
        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=thread_id,
            assistant_id=assistant_id,
            instructions=instructions,
            max_completion_tokens=max_completion_tokens,
            max_prompt_tokens=max_prompt_tokens,
            tools=tools,
            model=model,
        )
        return run

    def get_chat_history(self, run, thread_id):
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
            messages = self.client.beta.threads.messages.list(thread_id=thread_id)
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
    # Define class
    obj = LLMAssistant()
    # Create assistant
    new_assistant = obj.create_assistant(
        name="拿破崙",
        description="拿破崙克隆人",
        instructions="你是拿破崙，縱橫沙場的法國將軍，一代英豪，語調沈著而穩重，凌厲的語氣，時刻警惕著對方",
        temperature=0.7,
    )

    # List Assistants
    a = obj.list_assistants()
    print(a)

    # Retrieve Assistant
    assistant = obj.retrieve_assistant("拿破崙")
    print(assistant.id)

    # Delete Assistant
    obj.delete_assistant(assistant.id)

    # Create Thread
    thread = obj.create_thread(messages=[{"role": "user", "content": "Hello"}])
    print(thread.id)

    # Delete Thread
    obj.delete_thread(thread.id)

    # Create Message in Thread
    obj.create_message_in_thread(thread_id=thread.id, role="user", content="你誰啊")

    # Run Assistant
    run = obj.run_assistant(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )
    print(run)

    # Get Chat History
    chat_history = obj.get_chat_history(run=run, thread_id=thread.id)
    print(chat_history)
