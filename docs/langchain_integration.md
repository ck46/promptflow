# Using EvolutePrompt with LangChain

This guide explains how to integrate EvolutePrompt's prompt management capabilities with LangChain's ecosystem.

## Overview

[LangChain](https://langchain.com) is a popular framework for developing applications powered by language models. It provides a standard interface for chains, prompt templates, and various tools. EvolutePrompt complements LangChain by adding robust prompt management capabilities:

- Version control for prompts
- Activation strategies (A/B testing, fallbacks)
- Categorization and metadata
- Storage and retrieval

By combining these libraries, you can leverage EvolutePrompt's prompt management while utilizing LangChain's extensive ecosystem of components.

## Installation

First, make sure you have both packages installed:

```bash
pip install evoluteprompt langchain
```

## Basic Integration

The simplest way to use EvolutePrompt with LangChain is to create and manage your prompts with EvolutePrompt, then convert them for use with LangChain components.

### Converting EvolutePrompt Prompts to LangChain Format

Here's how to convert a EvolutePrompt prompt to LangChain format:

```python
# Import required components
from EvolutePrompt.api import EvolutePrompt
from langchain.schema import HumanMessage, SystemMessage, AIMessage

# Initialize EvolutePrompt
flow = EvolutePrompt()
flow.init()

# Create or retrieve a prompt
prompt = flow.get_prompt("my_prompt")

# Convert to LangChain format
def EvolutePrompt_to_langchain_messages(pf_prompt):
    """Convert EvolutePrompt messages to LangChain messages."""
    lc_messages = []
    
    for msg in pf_prompt.messages:
        content = msg.content
        if msg.role.value == "system":
            lc_messages.append(SystemMessage(content=content))
        elif msg.role.value == "user":
            lc_messages.append(HumanMessage(content=content))
        elif msg.role.value == "assistant":
            lc_messages.append(AIMessage(content=content))
    
    return lc_messages

# Use with LangChain
lc_messages = EvolutePrompt_to_langchain_messages(prompt)
```

### Converting EvolutePrompt Templates to LangChain PromptTemplates

EvolutePrompt and LangChain both have template mechanisms with different syntax. Here's how to convert between them:

```python
from langchain.prompts import PromptTemplate as LangChainPromptTemplate

# Create a EvolutePrompt template
pf_template = flow.template_from_string(
    "Please explain {{topic}} in {{style}} language.",
    variables={"topic": "quantum computing", "style": "simple"}
)

# Convert to LangChain format
def EvolutePrompt_template_to_langchain(pf_template):
    """Convert a EvolutePrompt template to a LangChain PromptTemplate."""
    # Extract variables
    variables = list(pf_template.variables.keys())
    
    # Get the template string
    template_str = pf_template.template
    
    # Replace EvolutePrompt variable syntax with LangChain syntax
    for var in variables:
        template_str = template_str.replace(f"{{{{" + var + "}}}}", f"{{{var}}}")
    
    # Create LangChain PromptTemplate
    return LangChainPromptTemplate.from_template(template_str)

# Convert and use
lc_template = EvolutePrompt_template_to_langchain(pf_template)
```

## Advanced Integration

### Using Version-Controlled Prompts

One of EvolutePrompt's key features is prompt versioning. Here's how to use it with LangChain:

```python
# Create multiple versions of a prompt
for i in range(3):
    temp_builder = flow.create_prompt()
    temp_builder.add_system(f"You are a helpful assistant. Version {i+1}")
    temp_builder.add_user("Explain {concept} to me.")
    temp_prompt = temp_builder.build()
    
    # Save with versioning
    flow.save_prompt("versioned_prompt", temp_prompt)

# List all versions
versions = flow.list_versions("versioned_prompt")

# Set the active version
flow.set_active("versioned_prompt", versions[-1])

# Use the active version in LangChain
active_prompt = flow.get_active_prompt("versioned_prompt")
lc_messages = EvolutePrompt_to_langchain_messages(active_prompt)

# Use with a LangChain model
from langchain.chat_models import ChatOpenAI
llm = ChatOpenAI()
result = llm.generate([lc_messages])
```

### Using EvolutePrompt Strategies with LangChain

EvolutePrompt provides several strategies for prompt selection. Here's how to use them with LangChain:

#### A/B Testing

```python
# Create A/B testing strategy
ab_strategy = flow.create_ab_testing(
    prompt_variants=["prompt_a", "prompt_b"],
    weights=[0.7, 0.3]
)

# Get prompt using strategy
selected_prompt = flow.select_prompt("fallback_id", strategy=ab_strategy)
lc_messages = EvolutePrompt_to_langchain_messages(selected_prompt)

# Use with LangChain
result = llm.generate([lc_messages])
```

#### Fallback Strategy

```python
# Set up a fallback relationship
flow.set_fallback("fallback_prompt", fallback_version, "main_prompt")

# Use the fallback strategy
strategy = flow.with_fallback()
selected_prompt = flow.select_prompt("main_prompt", strategy=strategy)
lc_messages = EvolutePrompt_to_langchain_messages(selected_prompt)
```

#### Context-Aware Selection

```python
# Create context-aware strategy
context_strategy = flow.create_context_aware(
    context_key="language",
    prompt_mapping={
        "en": "english_prompt",
        "es": "spanish_prompt",
        "fr": "french_prompt"
    }
)

# Get prompt using context
selected_prompt = flow.select_prompt(
    "default_prompt", 
    strategy=context_strategy,
    context={"language": "es"}
)
lc_messages = EvolutePrompt_to_langchain_messages(selected_prompt)
```

## Using EvolutePrompt with LangChain Chains

You can use EvolutePrompt prompts in LangChain chains:

```python
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI

# Get a template from EvolutePrompt
pf_template = flow.get_prompt_template("my_template")
lc_template = EvolutePrompt_template_to_langchain(pf_template)

# Create a chain
llm = ChatOpenAI()
chain = LLMChain(llm=llm, prompt=lc_template)

# Run the chain
response = chain.run(topic="quantum computing", style="simple")
```

## Complete Example

For a complete working example, see the [LangChain integration example](../examples/langchain_integration.py) in the examples directory.

## Best Practices

1. **Use EvolutePrompt for prompt management** - Let EvolutePrompt handle versioning, storage, and selection strategies.
2. **Use LangChain for orchestration** - Use LangChain for chains, agents, and tools that combine multiple components.
3. **Keep conversion utilities in a central place** - Create helper functions for converting between EvolutePrompt and LangChain formats.
4. **Leverage both ecosystems** - Use EvolutePrompt's UI for prompt management and LangChain's ecosystem for application development.

## Related Resources

- [LangChain Documentation](https://python.langchain.com/en/latest/)
- [EvolutePrompt Core Concepts](./core_concepts.md)
- [Getting Started with EvolutePrompt](./getting_started.md) 