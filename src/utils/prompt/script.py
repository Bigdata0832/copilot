import sqlite3


def create_database(db_path="prompt.db"):
    """
    Creates a database table named 'prompts' if it does not already exist in the specified database file.

    Args:
        db_path (str): The path to the database file. Defaults to 'prompt.db'.

    Returns:
        None
    """
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS prompts (
            name TEXT PRIMARY KEY,
            template_str TEXT
        )
    """
    )

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_database()
    print("Database created successfully.")
