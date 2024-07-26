class PromptTemplate:
    def __init__(self, template_str: str):
        """
        Initializes a new instance of the `PromptTemplate` class.

        Args:
            template_str (str): The template string to be stored in the `template_str` attribute.

        Returns:
            None
        """
        self.template_str = template_str

    def format(self, **kwargs) -> str:
        """
        Formats the template string with the given keyword arguments.

        Args:
            **kwargs: The keyword arguments to be used for formatting the template string.

        Returns:
            str: The formatted template string.
        """
        return self.template_str.format(**kwargs)
