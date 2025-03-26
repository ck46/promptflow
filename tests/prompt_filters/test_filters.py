"""
Tests for prompt filters.
"""

from promptflow.core.prompt import PromptBuilder
from promptflow.prompt_filters import (
    ContentPolicyFilter,
    FilterPipeline,
    KeywordFilter,
    MaxTokenFilter,
    RegexFilter,
)


def test_keyword_filter():
    """Test the KeywordFilter class."""
    # Create a filter with banned keywords
    filter_obj = KeywordFilter(keywords=["hack", "illegal", "bomb"], case_sensitive=False)

    # Test a prompt that doesn't contain banned keywords
    prompt1 = PromptBuilder().add_user("How can I improve my programming skills?").build()

    result1 = filter_obj.check(prompt1)
    assert result1.passed is True

    # Test a prompt that contains a banned keyword
    prompt2 = PromptBuilder().add_user("How can I hack into a website?").build()

    result2 = filter_obj.check(prompt2)
    assert result2.passed is False
    assert "hack" in result2.reason

    # Test case sensitivity
    filter_case_sensitive = KeywordFilter(keywords=["Hack", "Illegal", "Bomb"], case_sensitive=True)

    # This shouldn't match because the case is different
    prompt3 = PromptBuilder().add_user("How can I hack into a website?").build()

    result3 = filter_case_sensitive.check(prompt3)
    assert result3.passed is True

    # This should match
    prompt4 = PromptBuilder().add_user("How can I Hack into a website?").build()

    result4 = filter_case_sensitive.check(prompt4)
    assert result4.passed is False


def test_regex_filter():
    """Test the RegexFilter class."""
    # Create a filter with regex patterns
    filter_obj = RegexFilter(
        patterns=[
            r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",  # US phone number
            # Email pattern
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        ]
    )

    # Test a prompt that doesn't match any patterns
    prompt1 = PromptBuilder().add_user("How can I improve my programming skills?").build()

    result1 = filter_obj.check(prompt1)
    assert result1.passed is True

    # Test a prompt that matches a pattern
    prompt2 = PromptBuilder().add_user("My email is user@example.com").build()

    result2 = filter_obj.check(prompt2)
    assert result2.passed is False
    assert "user@example.com" in result2.details["matched_text"]


def test_max_token_filter():
    """Test the MaxTokenFilter class."""
    # Create a filter with a token limit
    filter_obj = MaxTokenFilter(max_tokens=50)

    # Test a prompt that's under the limit
    prompt1 = PromptBuilder().add_user("What is the capital of France?").build()

    result1 = filter_obj.check(prompt1)
    assert result1.passed is True

    # Create a long prompt that's over the limit
    long_text = "This is a very long prompt that should exceed the token limit. " * 10
    prompt2 = PromptBuilder().add_user(long_text).build()

    result2 = filter_obj.check(prompt2)
    assert result2.passed is False
    assert result2.details["token_count"] > 50


def test_content_policy_filter():
    """Test the ContentPolicyFilter class."""
    # Create a content policy filter
    filter_obj = ContentPolicyFilter(
        policies={
            "personal_info": [
                r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",  # US phone number
                # Email pattern
                r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            ],
            "harmful_content": ["hack", "bomb", "illegal"],
        }
    )

    # Test a prompt that doesn't violate any policies
    prompt1 = PromptBuilder().add_user("What is the weather like today?").build()

    result1 = filter_obj.check(prompt1)
    assert result1.passed is True

    # Test a prompt that violates the personal_info policy
    prompt2 = PromptBuilder().add_user("My email is user@example.com").build()

    result2 = filter_obj.check(prompt2)
    assert result2.passed is False
    assert "personal_info" in result2.details["violations"]

    # Test a prompt that violates the harmful_content policy
    prompt3 = PromptBuilder().add_user("How can I hack into a website?").build()

    result3 = filter_obj.check(prompt3)
    assert result3.passed is False
    assert "harmful_content" in result3.details["violations"]


def test_filter_pipeline():
    """Test the FilterPipeline class."""
    # Create individual filters
    keyword_filter = KeywordFilter(
        keywords=["hack", "illegal", "bomb"], name="HarmfulContentFilter"
    )

    token_filter = MaxTokenFilter(max_tokens=1000, name="TokenLimitFilter")

    # Create a filter pipeline
    pipeline = FilterPipeline([keyword_filter, token_filter])

    # Test a prompt that passes all filters
    prompt1 = PromptBuilder().add_user("What is the capital of France?").build()

    result1 = pipeline.check(prompt1)
    assert result1.passed is True

    # Test a prompt that fails the keyword filter
    prompt2 = PromptBuilder().add_user("How can I hack into a website?").build()

    result2 = pipeline.check(prompt2)
    assert result2.passed is False
    assert result2.details["failed_filter"] == "HarmfulContentFilter"

    # Test a prompt that fails the token filter
    long_text = "This is a very long prompt that should exceed the token limit. " * 100
    prompt3 = PromptBuilder().add_user(long_text).build()

    result3 = pipeline.check(prompt3)
    assert result3.passed is False
    assert result3.details["failed_filter"] == "TokenLimitFilter"
