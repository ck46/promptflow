# Prompt Templates and Variables Examples

Learn how to create reusable prompt templates and work with variables in EvolutePrompt.

## Basic Templates

```python
from evoluteprompt import PromptTemplate, Variable

# Create a simple template
template = PromptTemplate("""
You are a {role} specialized in {field}.
Help the user with their {topic} question: {question}
""")

# Use the template with different variables
prompt = template.format(
    role="professional tutor",
    field="mathematics",
    topic="calculus",
    question="What is the derivative of e^x?"
)

# Create a template with default values
math_tutor = PromptTemplate(
    template="""
    You are a math tutor helping with {topic}.
    Question: {question}
    Provide a step-by-step solution.
    """,
    defaults={
        "topic": "general mathematics"
    }
)
```

## Advanced Template Features

```python
# Template with conditional blocks
complex_template = PromptTemplate("""
You are a {role} assistant.
{% if expertise %}
Your areas of expertise include: {expertise}
{% endif %}
{% if context %}
Consider this context: {context}
{% endif %}
User question: {question}
""")

# Template with loops
list_template = PromptTemplate("""
Consider the following points:
{% for point in points %}
- {point}
{% endfor %}
Provide a summary of these points.
""")

# Using the templates
prompt = complex_template.format(
    role="technical",
    expertise=["Python", "Machine Learning", "Data Science"],
    context="Working on a data analysis project",
    question="How do I implement cross-validation?"
)

summary_prompt = list_template.format(
    points=[
        "AI is transforming industries",
        "Machine learning requires quality data",
        "Ethics in AI is crucial"
    ]
)
```

## Template Management

```python
from evoluteprompt import TemplateManager

# Initialize template manager
manager = TemplateManager()

# Register templates
manager.register("math_tutor", math_tutor)
manager.register("technical_support", support_template)

# Get template by name
template = manager.get_template("math_tutor")

# List all templates
all_templates = manager.list_templates()

# Template versioning
manager.register("customer_service", template, version="2.0")
latest_version = manager.get_latest_version("customer_service")
```

## Variable Validation and Types

```python
from evoluteprompt import Variable, TemplateValidator

# Define variables with types and validation
variables = {
    "temperature": Variable(float, min_value=0.0, max_value=1.0),
    "max_tokens": Variable(int, min_value=1),
    "model": Variable(str, choices=["gpt-3.5-turbo", "gpt-4"]),
    "tags": Variable(list, max_length=5)
}

# Create template with validation
validated_template = PromptTemplate(
    template="Generate a {temperature} response with {max_tokens} tokens using {model}",
    variables=variables
)

# Validation will raise error if values are invalid
try:
    prompt = validated_template.format(
        temperature=1.5,  # Will raise error (> max_value)
        max_tokens=100,
        model="gpt-3.5-turbo"
    )
except ValueError as e:
    print(f"Validation error: {e}")
``` 