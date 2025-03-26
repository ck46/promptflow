# EvolutePrompt Documentation

Welcome to the documentation for EvolutePrompt, a comprehensive prompt management library for Large Language Models (LLMs).

## Overview

EvolutePrompt is designed to simplify the process of creating, managing, versioning, and deploying prompts for LLMs. It provides a set of tools and abstractions to make working with prompts more systematic and efficient.

## Key Features

- **Prompt Version Control**: Track changes to prompts over time ([examples](./examples/version_control.md))
- **Experimentation & Analytics**: Compare prompt performance with metrics ([examples](./examples/experimentation.md))
- **Prompt Templates and Variables**: Reuse and parameterize prompts ([examples](./examples/templates.md))
- **Caching**: Optional response caching for efficiency ([examples](./examples/caching.md))
- **Prompt Auditing & Testing**: Built-in testing framework ([examples](./examples/testing.md))
- **Safety and Alignment Checks**: Filter prompts for ethical constraints ([examples](./examples/safety.md))
- **Extensible Plugin System**: Support for various LLM providers (OpenAI, Anthropic, Hugging Face) ([examples](./examples/plugins.md))
- **LangChain Integration**: Compatibility with the LangChain framework ([examples](./examples/langchain.md))

## Installation

```bash
pip install evoluteprompt
```

Or with Poetry:

```bash
poetry add evoluteprompt
```

## Quick Start

```python
from evoluteprompt import PromptBuilder, LLMProvider
from evoluteprompt.integrations import OpenAIProvider

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
- [Examples](./examples/): Detailed examples of all features
  - [Version Control](./examples/version_control.md)
  - [Experimentation & Analytics](./examples/experimentation.md)
  - [Templates & Variables](./examples/templates.md)
  - [Caching](./examples/caching.md)
  - [Testing](./examples/testing.md)
  - [Safety & Alignment](./examples/safety.md)
  - [Plugin System](./examples/plugins.md)
  - [LangChain Integration](./examples/langchain.md)
- [API Reference](./api_reference/index.md): Detailed API documentation
- [Contributing](./contributing.md): How to contribute to the project 