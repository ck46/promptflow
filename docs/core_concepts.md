# Core Concepts

This document explains the core concepts and components of the EvolutePrompt library.

## Prompts

In EvolutePrompt, a prompt is a structured collection of messages that are sent to a language model. A prompt consists of one or more messages, each with a role (system, user, assistant, or function) and content.

### Message Roles

- **System**: Instructions or context for the model
- **User**: Input from the user
- **Assistant**: Responses from the model
- **Function**: Function calls or results

### Prompt Builder

The PromptBuilder provides a fluent API for constructing prompts:

```python
from evoluteprompt import PromptBuilder

prompt = PromptBuilder()\
    .add_system("You are a helpful assistant.")\
    .add_user("What is the capital of France?")\
    .build()
```

## Templates

Templates allow you to parameterize prompts with variables. EvolutePrompt uses Jinja2 for templating.

```python
from evoluteprompt import PromptTemplate

template = PromptTemplate("""
You are a {{ role }} assistant. Please answer the following question:

Question: {{ question }}

Keep your answer {{ style }}.
""")

prompt = template.to_prompt(
    role="technical",
    question="What is Python?",
    style="concise"
)
```

## Providers

Providers are abstraction layers for different LLM APIs. They handle the communication with the API and convert between EvolutePrompt's internal representation and the API's format.

```python
from evoluteprompt.integrations import OpenAIProvider

provider = OpenAIProvider(
    api_key="YOUR_API_KEY",
    model="gpt-3.5-turbo"
)

response = provider.complete(prompt)
```

## Responses

Responses from LLMs are wrapped in a LLMResponse object that includes:

- The response text
- Statistics (token counts, latency)
- Provider-specific information
- Raw response data

```python
response = provider.complete(prompt)

print(response.text)  # The response text
print(response.stats.total_tokens)  # Token usage
```

## Version Control

The PromptRepo system provides version control for prompts:

```python
from evoluteprompt import PromptRepo

repo = PromptRepo("./prompts")

# Create and save a prompt
prompt = repo.create_prompt("greeting")
prompt.add_system("You are a friendly assistant.")
repo.save_prompt("greeting", prompt)

# Get a specific version
prompt_v1 = repo.get_prompt("greeting", version="0.1.0")

# Compare versions
diff = repo.compare_versions("greeting", "0.1.0", "0.2.0")
```

## Prompt Filters

Filters provide safety and alignment checks for prompts:

```python
from evoluteprompt.prompt_filters import KeywordFilter, RegexFilter, FilterPipeline

# Create filters
keyword_filter = KeywordFilter(
    keywords=["hack", "illegal", "bomb"],
    name="HarmfulContentFilter"
)

personal_info_filter = RegexFilter(
    patterns=[r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b"],  # Phone number
    name="PersonalInfoFilter"
)

# Create a pipeline
pipeline = FilterPipeline([keyword_filter, personal_info_filter])

# Check a prompt
result = pipeline.check(prompt)
if result.passed:
    # Prompt is safe
    response = provider.complete(prompt)
else:
    # Prompt failed safety check
    print(f"Prompt failed safety check: {result.reason}")
```

## Caching

EvolutePrompt includes caching to avoid redundant API calls:

```python
from evoluteprompt.utils import InMemoryCache, FileCache

# Create a cache
cache = InMemoryCache()  # Or: cache = FileCache("./cache")

# Check if response is in cache
cached_response = cache.get(prompt)
if cached_response:
    print("Using cached response")
    response = cached_response
else:
    # Get response from provider
    response = provider.complete(prompt)
    
    # Cache the response
    cache.set(prompt, response, ttl=3600)  # Cache for 1 hour
``` 