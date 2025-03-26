"""
Tests for the Prompt and PromptBuilder classes.
"""

import pytest

from evoluteprompt.core.prompt import Prompt, PromptBuilder
from evoluteprompt.core.types import MessageRole


def test_prompt_builder():
    """Test creating a prompt using PromptBuilder."""
    # Create a prompt using the builder
    builder = PromptBuilder()
    builder.add_system("You are a helpful assistant.")
    builder.add_user("What is the capital of France?")

    # Build the prompt
    prompt = builder.build()

    # Check that the prompt has the expected messages
    assert len(prompt.messages) == 2
    assert prompt.messages[0].role == MessageRole.SYSTEM
    assert prompt.messages[0].content == "You are a helpful assistant."
    assert prompt.messages[1].role == MessageRole.USER
    assert prompt.messages[1].content == "What is the capital of France?"


def test_prompt_add_messages():
    """Test adding messages to an existing prompt."""
    # Create an empty prompt
    prompt = Prompt(messages=[])

    # Add messages
    prompt.add_system("You are a helpful assistant.")
    prompt.add_user("What is the capital of France?")
    prompt.add_assistant("The capital of France is Paris.")

    # Check that the prompt has the expected messages
    assert len(prompt.messages) == 3
    assert prompt.messages[0].role == MessageRole.SYSTEM
    assert prompt.messages[0].content == "You are a helpful assistant."
    assert prompt.messages[1].role == MessageRole.USER
    assert prompt.messages[1].content == "What is the capital of France?"
    assert prompt.messages[2].role == MessageRole.ASSISTANT
    assert prompt.messages[2].content == "The capital of France is Paris."


def test_prompt_serialization():
    """Test serializing and deserializing a prompt."""
    # Create a prompt
    builder = PromptBuilder()
    builder.add_system("You are a helpful assistant.")
    builder.add_user("What is the capital of France?")
    prompt = builder.build()

    # Serialize the prompt to JSON
    json_str = prompt.to_json()

    # Deserialize the prompt from JSON
    prompt2 = Prompt.from_json(json_str)

    # Check that the prompts are equivalent
    assert len(prompt.messages) == len(prompt2.messages)
    assert prompt.messages[0].role == prompt2.messages[0].role
    assert prompt.messages[0].content == prompt2.messages[0].content
    assert prompt.messages[1].role == prompt2.messages[1].role
    assert prompt.messages[1].content == prompt2.messages[1].content


def test_prompt_parameters():
    """Test setting parameters on a prompt."""
    # Create a prompt
    prompt = PromptBuilder().build()

    # Set parameters
    prompt.set_parameters(temperature=0.7, max_tokens=100, top_p=0.9)

    # Check that the parameters were set correctly
    assert prompt.parameters is not None
    assert prompt.parameters.temperature == 0.7
    assert prompt.parameters.max_tokens == 100
    assert prompt.parameters.top_p == 0.9


def test_prompt_function_definition():
    """Test adding a function definition to a prompt."""
    # Create a prompt
    prompt = PromptBuilder().build()

    # Add a function definition
    prompt.add_function_definition(
        name="get_weather",
        description="Get the weather for a location",
        parameters={
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": ("The city and state, e.g. San Francisco, CA"),
                }
            },
            "required": ["location"],
        },
    )

    # Check that the function definition was added correctly
    assert prompt.parameters is not None
    assert prompt.parameters.functions is not None
    assert len(prompt.parameters.functions) == 1
    assert prompt.parameters.functions[0].name == "get_weather"
    assert prompt.parameters.functions[0].description == "Get the weather for a location"
    assert "location" in prompt.parameters.functions[0].parameters["properties"]


def test_prompt_without_user_message():
    """Test creating a prompt without a user message."""
    # Create a prompt with only system message
    builder = PromptBuilder()
    builder.add_system("You are a helpful assistant.")

    # This should work now since user message is optional
    prompt = builder.build(require_user_message=False)

    # Check that the prompt has only the system message
    assert len(prompt.messages) == 1
    assert prompt.messages[0].role == MessageRole.SYSTEM
    assert prompt.messages[0].content == "You are a helpful assistant."

    # But if we require a user message, it should fail
    with pytest.raises(ValueError, match="Prompt must contain at least one user message"):
        builder.build(require_user_message=True)
