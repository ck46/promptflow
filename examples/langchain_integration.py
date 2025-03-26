"""
Example of using PromptFlow with LangChain.

This example demonstrates how to integrate PromptFlow's prompt management capabilities
with LangChain's components.
"""

import os
from typing import Dict, Any

# Import PromptFlow components
from evoluteprompt.api import EvolutePrompt
from evoluteprompt.core.types import PromptCategory

# Import LangChain components
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate as LangChainPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

# Initialize PromptFlow
flow = EvolutePrompt()
flow.init()

# 1. Basic Integration: Using a PromptFlow prompt template with LangChain

# First, create and save a prompt in PromptFlow
prompt_builder = flow.create_prompt()
prompt_builder.add_system("You are a helpful assistant specialized in {domain}.")
prompt_builder.add_user("Tell me about {topic} in about {word_count} words.")
prompt = prompt_builder.build()

# Add metadata
prompt.update_metadata(
    description="A flexible domain-specific information request",
    tags=["template", "information", "langchain"],
    category=PromptCategory.QA,
    is_active=True
)

# Save the prompt
prompt_id = "langchain_domain_query"
version = flow.save_prompt(prompt_id, prompt)
print(f"Saved prompt version: {version}")

# Retrieve the prompt for use with LangChain
retrieved_prompt = flow.get_prompt(prompt_id)

# Convert PromptFlow prompt to LangChain format
def promptflow_to_langchain_messages(pf_prompt):
    """Convert PromptFlow messages to LangChain messages."""
    lc_messages = []
    
    for msg in pf_prompt.messages:
        content = msg.content
        if msg.role.value == "system":
            lc_messages.append(SystemMessage(content=content))
        elif msg.role.value == "user":
            lc_messages.append(HumanMessage(content=content))
        # Add other message types as needed
    
    return lc_messages

# 2. Using PromptFlow templates with LangChain

# Create a template in PromptFlow
pf_template = flow.template_from_string(
    "Please summarize this article about {{topic}} in {{format}} format.",
    variables={"topic": "artificial intelligence", "format": "bullet points"}
)

# Convert PromptFlow template to LangChain PromptTemplate
def promptflow_template_to_langchain(pf_template):
    """Convert a PromptFlow template to a LangChain PromptTemplate."""
    # Extract variables from PromptFlow template
    variables = list(pf_template.variables.keys())
    
    # Get the template string
    template_str = pf_template.template
    
    # Replace PromptFlow variable syntax with LangChain syntax
    for var in variables:
        template_str = template_str.replace(f"{{{{" + var + "}}}}", f"{{{var}}}")
    
    # Create LangChain PromptTemplate
    return LangChainPromptTemplate.from_template(template_str)

# Convert our template
lc_template = promptflow_template_to_langchain(pf_template)
print(f"LangChain template: {lc_template.template}")

# 3. Using PromptFlow with LangChain chains

# Initialize LangChain LLM
openai_api_key = os.environ.get("OPENAI_API_KEY", "your-api-key-here")
llm = ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo", api_key=openai_api_key)

# Create a LangChain chain using our converted template
chain = LLMChain(llm=llm, prompt=lc_template)

# Run the chain
response = chain.run(topic="quantum computing", format="simple paragraph")
print(f"Chain response: {response}")

# 4. Advanced: Version-Controlled Prompts with LangChain

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
print(f"Available versions: {versions}")

# Set the active version
flow.set_active("versioned_prompt", versions[-1])

# Use the active version in LangChain
active_prompt = flow.get_active_prompt("versioned_prompt")
lc_messages = promptflow_to_langchain_messages(active_prompt)

# Use with LangChain
result = llm.generate([lc_messages])
print(f"Result using active version: {result.generations[0][0].text}")

# 5. Using PromptFlow strategies with LangChain

# Create A/B testing strategy
ab_strategy = flow.create_ab_testing(
    prompt_variants=["langchain_domain_query", "versioned_prompt"],
    weights=[0.7, 0.3]
)

# Get prompt using strategy
selected_prompt = flow.select_prompt("fallback_id", strategy=ab_strategy)
lc_messages = promptflow_to_langchain_messages(selected_prompt)

# Use with LangChain
result = llm.generate([lc_messages])
print(f"Result using A/B testing strategy: {result.generations[0][0].text}")

# Clean up
flow.close() 