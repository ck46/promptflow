"""
Tests for the PromptTemplate classes.
"""

import os
import tempfile

import pytest

from promptflow.core.template import MultiMessageTemplate, PromptTemplate
from promptflow.core.types import MessageRole


def test_prompt_template_render():
    """Test rendering a prompt template."""
    # Create a template
    template = PromptTemplate.from_string(
        """
You are a {{ role }} assistant. Please answer the following question:

Question: {{ question }}

Keep your answer {{ style }}.
    """
    )

    # Render the template
    rendered = template.render(role="technical", question="What is Python?", style="concise")

    # Check that variables were properly substituted
    assert "technical assistant" in rendered
    assert "Question: What is Python?" in rendered
    assert "Keep your answer concise" in rendered


def test_prompt_template_to_prompt():
    """Test converting a template to a prompt."""
    # Create a template
    template = PromptTemplate.from_string("Hello, my name is {{ name }}.")

    # Convert the template to a prompt
    prompt = template.to_prompt(role=MessageRole.USER, name="Alice")

    # Check that the prompt was created correctly
    assert len(prompt.messages) == 1
    assert prompt.messages[0].role == MessageRole.USER
    assert prompt.messages[0].content == "Hello, my name is Alice."


def test_prompt_template_default_variables():
    """Test template with default variables."""
    # Create a template with default variables
    template = PromptTemplate.from_string(
        "Hello, my name is {{ name }}. I am {{ age }} years old.",
        variables={"name": "Bob", "age": 30},
    )

    # Render with default variables
    rendered1 = template.render()
    assert "Hello, my name is Bob. I am 30 years old." == rendered1

    # Override default variables
    rendered2 = template.render(name="Alice", age=25)
    assert "Hello, my name is Alice. I am 25 years old." == rendered2

    # Override only some variables
    rendered3 = template.render(name="Charlie")
    assert "Hello, my name is Charlie. I am 30 years old." == rendered3


def test_multi_message_template():
    """Test the MultiMessageTemplate class."""
    # Create a template
    template = MultiMessageTemplate(
        system_template="You are a {{ role }} assistant.",
        user_templates=["What is {{ topic }}?", "Why is {{ topic }} important?"],
        assistant_templates=["{{ topic }} is a programming language."],
        variables={"role": "helpful", "topic": "Python"},
    )

    # Render the template
    messages = template.render()

    # Check that the messages were rendered correctly
    assert len(messages) == 4
    assert messages[0]["role"] == "system"
    assert messages[0]["content"] == "You are a helpful assistant."
    assert messages[1]["role"] == "user"
    assert messages[1]["content"] == "What is Python?"
    assert messages[2]["role"] == "assistant"
    assert messages[2]["content"] == "Python is a programming language."
    assert messages[3]["role"] == "user"
    assert messages[3]["content"] == "Why is Python important?"

    # Convert to a prompt
    prompt = template.to_prompt()
    assert len(prompt.messages) == 4


def test_multi_message_template_from_file():
    """Test creating a MultiMessageTemplate from a file."""
    # Create a temporary file with template content
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write(
            """system
You are a {{ role }} assistant.
---
user
What is {{ topic }}?
---
assistant
{{ topic }} is a programming language.
---
user
Why is {{ topic }} important?
"""
        )
        file_path = f.name

    try:
        # Create a template from the file
        template = MultiMessageTemplate.from_file(file_path)

        # Render the template
        messages = template.render(role="helpful", topic="Python")

        # Check that the messages were rendered correctly
        assert len(messages) == 4
        assert messages[0]["role"] == "system"
        assert messages[0]["content"] == "You are a helpful assistant."
        assert messages[1]["role"] == "user"
        assert messages[1]["content"] == "What is Python?"
        assert messages[2]["role"] == "assistant"
        assert messages[2]["content"] == "Python is a programming language."
        assert messages[3]["role"] == "user"
        assert messages[3]["content"] == "Why is Python important?"
    finally:
        # Clean up the temporary file
        os.unlink(file_path)


def test_prompt_template_without_user_message():
    """Test converting a template to a prompt without a user message."""
    # Create a template
    template = PromptTemplate.from_string("You should respond in a friendly tone.")

    # Convert the template to a system prompt without requiring a user message
    prompt = template.to_prompt(role=MessageRole.SYSTEM, require_user_message=False)

    # Check that the prompt was created correctly with only a system message
    assert len(prompt.messages) == 1
    assert prompt.messages[0].role == MessageRole.SYSTEM
    assert prompt.messages[0].content == "You should respond in a friendly tone."

    # Using the default require_user_message=True with a SYSTEM message fails
    with pytest.raises(ValueError, match="Prompt must contain at least " "one user message"):
        template.to_prompt(role=MessageRole.SYSTEM)
