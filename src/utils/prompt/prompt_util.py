"""
Get a prompt from the prompt manager based on the given prompt name.

Args:
    prompt (str): The name of the prompt to retrieve.
    name (str, optional): The name parameter to be used in the prompt template. Defaults to "".

Raises:
    ValueError: If the prompt name is not found in the prompt manager.
    KeyError: If the prompt template does not contain the name parameter.

Returns:
    str: The formatted prompt string.

Example:
    from utils.prompt import get_prompt, list_prompts

    # List All Prompts
    prompts = list_prompts()
    print(prompts)

    # Use Normal Prompt
    init_prompt = get_prompt(prompt="init")
    print(init_prompt)

    # Use Template Prompt
    hello_prompt = get_prompt(prompt="hello", name="Lucien")
    print(hello_prompt)
"""
from .prompt_data import PROMPTS

def get_prompt(prompt: str, **kwargs) -> str:
    """
    Retrieves and formats a prompt template by its name if it contains format placeholders.

    Args:
        prompt (str): The name of the prompt template to retrieve.
        **kwargs: The keyword arguments to be used for formatting the template string.

    Returns:
        str: The formatted prompt template.

    Raises:
        ValueError: If no template with the given name exists.
        KeyError: If the template contains placeholders but required parameters are missing.
    """
    template = PROMPTS.get(prompt)
    if template is None:
        raise ValueError(f"Prompt '{prompt}' not found.")

    try:
        formatted_template = template.format(**kwargs)
        return formatted_template
    except KeyError as e:
        missing_keys = e.args[0]
        raise KeyError(f"Missing parameters for prompt '{prompt}': {missing_keys}")

def list_prompts() -> list:
    """
    Retrieves a list of prompt names.

    Returns:
        list: A list of prompt names.
    """
    return list(PROMPTS.keys())
