## KEYPO COPILOT


## Prompt

How to use `PromptTemplate` and `PromptManager`?

### Creating a PromptTemplate

Instantiate `PromptTemplate` with a template string:

```python
from prompt import PromptTemplate

# Create a PromptTemplate instance
greeting_template = PromptTemplate("Hello, {name}!")
```

### Managing Prompts with PromptManager

Use `PromptManager` to add, retrieve, list, and remove prompts.

#### Adding a Prompt

```python
from prompt import PromptManager

# Create PromptManager instance
manager = PromptManager()

# Add the template to the manager
manager.add_prompt("greeting", greeting_template)
```

#### Getting a Prompt

```python
# Get the template from the manager
template = manager.get_prompt("greeting")
if template:
    formatted_text = template.format(name="Alice")
    print(formatted_text)  # Output: Hello, Alice!
```

#### Listing All Prompts

```python
# List all prompt names
print(manager.list_prompts())  # Output: ['greeting']
```

#### Removing a Prompt

```python
# Remove the template from the manager
manager.remove_prompt("greeting")

# Verify removal
print(manager.list_prompts())  # Output: []
```
