# Getting Started

This guide will help you get started with PromptFlow, explaining the basic usage and concepts.

## Installation

You can install PromptFlow via pip:

```bash
pip install promptflow
```

Or with Poetry:

```bash
poetry add promptflow
```

## Basic Usage

### Setting up a Provider

First, you need to set up a provider for the LLM you want to use. PromptFlow currently supports OpenAI, Anthropic, and Hugging Face.

```python
from promptflow.integrations import OpenAIProvider

# Create a provider
provider = OpenAIProvider(
    api_key="YOUR_API_KEY",
    model="gpt-3.5-turbo"  # Optional, defaults to gpt-3.5-turbo
)
```

### Creating a Prompt

You can create a prompt using the PromptBuilder:

```python
from promptflow import PromptBuilder

# Create a prompt
prompt = PromptBuilder()\
    .add_system("You are a helpful assistant.")\
    .add_user("What is the capital of France?")\
    .build()
```

### Completing a Prompt

Once you have a provider and a prompt, you can complete the prompt:

```python
# Complete the prompt
response = provider.complete(prompt)

# Print the response
print(response.text)
```

### Streaming Responses

You can also stream responses:

```python
# Function to process each chunk
def process_chunk(chunk):
    print(chunk, end="", flush=True)

# Stream the response
provider.stream(prompt, callback=process_chunk)
```

## Using Templates

Templates allow you to reuse prompts with different variables:

```python
from promptflow import PromptTemplate

# Create a template
template = PromptTemplate("""
You are a {{ role }} assistant. Please answer the following question:

Question: {{ question }}

Keep your answer {{ style }}.
""")

# Render the template with specific values
prompt = template.to_prompt(
    role="technical",
    question="What is Python?",
    style="concise"
)

# Complete the prompt
response = provider.complete(prompt)
```

## Version Control

PromptFlow includes a version control system for prompts:

```python
from promptflow import PromptRepo

# Create a repository
repo = PromptRepo("./prompts")

# Create a prompt
prompt = repo.create_prompt("greeting")
prompt.add_system("You are a friendly assistant.")
prompt.add_user("Say hello to the user.")

# Save the prompt
repo.save_prompt("greeting", prompt, message="Initial greeting prompt")

# Retrieve a specific version
prompt = repo.get_prompt("greeting", version="0.1.0")
```

## Next Steps

- Check out the [Core Concepts](./core_concepts.md) to understand the fundamental concepts in PromptFlow.
- Explore the [Examples](./examples/index.md) to see more complex usage scenarios.
- Read the [API Reference](./api_reference/index.md) for detailed information about the API. 