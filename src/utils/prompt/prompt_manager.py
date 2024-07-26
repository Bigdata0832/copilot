import sqlite3
from .prompt_template import PromptTemplate


class PromptManager:
    def __init__(self, db_path="prompt.db"):
        """
        Initializes a new instance of the PromptManager class.

        Args:
            db_path (str, optional): The path to the database file. Defaults to 'prompt.db'.

        Returns:
            None
        """
        self.db_path = db_path

    def add_prompt(self, name: str, prompt: PromptTemplate):
        """
        Adds or replaces a prompt in the database with the given name and template string.

        Args:
            name (str): The name of the prompt.
            prompt (PromptTemplate): The prompt template to be added or replaced.

        Returns:
            None
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO prompts (name, template_str)
                VALUES (?, ?)
            """,
                (name, prompt.template_str),
            )
            conn.commit()

    def get_prompt(self, name: str) -> PromptTemplate:
        """
        Retrieves a prompt template from the database by its name.

        Args:
            name (str): The name of the prompt template to retrieve.

        Returns:
            PromptTemplate: The retrieved prompt template, or None if no template with the given name exists.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT template_str FROM prompts WHERE name = ?", (name,))
            row = cursor.fetchone()
            if row:
                return PromptTemplate(template_str=row[0])
            return None

    def remove_prompt(self, name: str):
        """
        Removes a prompt from the database by its name.

        Args:
            name (str): The name of the prompt to be removed.

        Returns:
            None
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM prompts WHERE name = ?", (name,))
            conn.commit()

    def list_prompts(self) -> list:
        """
        Retrieves a list of prompt names from the database.

        Returns:
            list: A list of prompt names.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM prompts")
            return [row[0] for row in cursor.fetchall()]
