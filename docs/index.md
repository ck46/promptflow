# PromptFlow Documentation

Welcome to the documentation for PromptFlow, a comprehensive prompt management library for Large Language Models (LLMs).

## Overview

PromptFlow is designed to simplify the process of creating, managing, versioning, and deploying prompts for LLMs. It provides a set of tools and abstractions to make working with prompts more systematic and efficient.

## Key Features

- **Prompt Version Control**: Track changes to prompts over time
- **Experimentation & Analytics**: Compare prompt performance with metrics
- **Prompt Templates and Variables**: Reuse and parameterize prompts
- **Caching**: Optional response caching for efficiency
- **Prompt Auditing & Testing**: Built-in testing framework
- **Safety and Alignment Checks**: Filter prompts for ethical constraints
- **Extensible Plugin System**: Support for various LLM providers (OpenAI, Anthropic, Hugging Face)

## Installation

```bash
pip install promptflow
```

Or with Poetry:

```bash
poetry add promptflow
```

## Quick Start

```python
from promptflow import PromptBuilder, LLMProvider
from promptflow.integrations import OpenAIProvider

# Create a provider
provider = OpenAIProvider(api_key="YOUR_API_KEY")

# Create a simple prompt
prompt = PromptBuilder()\
    .add_system("You are a helpful assistant.")\
    .add_user("What is the capital of France?")\
    .build()

# Send the prompt to the LLM
response = provider.complete(prompt)
print(response.text)
```

## Documentation Sections

- [Getting Started](./getting_started.md): Basic introduction to the library
- [Core Concepts](./core_concepts.md): Understanding the fundamental concepts
- [API Reference](./api_reference/index.md): Detailed API documentation
- [Examples](./examples/index.md): Various usage examples
- [Contributing](./contributing.md): How to contribute to the project 