"""
Example of basic PromptFlow usage.
"""

import asyncio
from promptflow.api import PromptFlow
from promptflow.core.types import PromptCategory, MessageRole

# Initialize the PromptFlow API
flow = PromptFlow()
flow.init()

# Create a simple prompt
prompt_builder = flow.create_prompt()
prompt_builder.add_system("You are a helpful assistant.")
prompt_builder.add_user("What is the capital of France?")
prompt = prompt_builder.build()

# Set some metadata
prompt.update_metadata(
    description="A simple prompt asking about the capital of France",
    tags=["geography", "test"],
    category=PromptCategory.QA,
    is_active=True
)

# Save the prompt
version = flow.save_prompt("capital_question", prompt)
print(f"Saved prompt version: {version}")

# Create a fallback prompt
fallback_builder = flow.create_prompt()
fallback_builder.add_system("You are a helpful assistant. If you don't know the answer, just say so.")
fallback_builder.add_user("What is the capital of France?")
fallback_prompt = fallback_builder.build()

# Set metadata for the fallback
fallback_prompt.update_metadata(
    description="Fallback prompt for capital questions",
    tags=["geography", "fallback"],
    category=PromptCategory.QA,
    is_fallback=True
)

# Save the fallback prompt
fallback_version = flow.save_prompt("capital_fallback", fallback_prompt)
print(f"Saved fallback prompt version: {fallback_version}")

# Set the fallback relationship
flow.set_fallback("capital_fallback", fallback_version, "capital_question")

# Retrieve the prompt
retrieved_prompt = flow.get_prompt("capital_question")
print(f"Retrieved prompt: {retrieved_prompt.messages[0].content}")

# Create a prompt template
template = flow.template_from_string(
    "What is the capital of {{country}}?",
    variables={"country": "France"}
)

# Render the template
rendered = template.render()
print(f"Rendered template: {rendered}")

# Convert to a prompt
template_prompt = template.to_prompt()
print(f"Template prompt: {template_prompt.messages[0].content}")

# Save the template prompt
template_version = flow.save_prompt("capital_template", template_prompt)
print(f"Saved template prompt version: {template_version}")

# List all prompts
prompts = flow.list_prompts()
print(f"All prompts: {prompts}")

# List prompts by category
qa_prompts = flow.list_prompts(category=PromptCategory.QA)
print(f"QA prompts: {qa_prompts}")

# Use the fallback strategy
strategy = flow.with_fallback()
selected_prompt = flow.select_prompt("capital_question", strategy=strategy)
print(f"Selected prompt: {selected_prompt.messages[0].content}")

# Clean up
flow.close() 