"""
Tests for the cache functionality.
"""

import shutil
import tempfile
import time
from unittest.mock import MagicMock

from promptflow.core.prompt import PromptBuilder
from promptflow.core.response import LLMResponse
from promptflow.utils import FileCache, InMemoryCache, hash_prompt


def test_hash_prompt():
    """Test hashing a prompt."""
    # Create two identical prompts
    prompt1 = (
        PromptBuilder()
        .add_system("You are a helpful assistant.")
        .add_user("What is the capital of France?")
        .build()
    )

    prompt2 = (
        PromptBuilder()
        .add_system("You are a helpful assistant.")
        .add_user("What is the capital of France?")
        .build()
    )

    # The hashes should be identical
    assert hash_prompt(prompt1) == hash_prompt(prompt2)

    # Create a different prompt
    prompt3 = (
        PromptBuilder()
        .add_system("You are a helpful assistant.")
        .add_user("What is the capital of Spain?")
        .build()
    )

    # The hash should be different
    assert hash_prompt(prompt1) != hash_prompt(prompt3)

    # Test that parameters are included in the hash
    prompt1.set_parameters(temperature=0.7)
    prompt2.set_parameters(temperature=0.8)

    # The hashes should now be different
    assert hash_prompt(prompt1) != hash_prompt(prompt2)

    # Test without including parameters
    assert hash_prompt(prompt1, include_parameters=False) == hash_prompt(
        prompt2, include_parameters=False
    )


def test_in_memory_cache():
    """Test the InMemoryCache class."""
    # Create a cache
    cache = InMemoryCache()

    # Create a prompt
    prompt = (
        PromptBuilder()
        .add_system("You are a helpful assistant.")
        .add_user("What is the capital of France?")
        .build()
    )

    # Initially, the cache should be empty
    assert cache.get(prompt) is None

    # Create a mock response
    response = MagicMock(spec=LLMResponse)
    response.text = "The capital of France is Paris."

    # Cache the response
    cache.set(prompt, response)

    # Retrieve the response from the cache
    cached_response = cache.get(prompt)
    assert cached_response is response
    assert cached_response.text == "The capital of France is Paris."

    # Test TTL expiration
    prompt2 = PromptBuilder().add_user("What is the capital of Spain?").build()

    response2 = MagicMock(spec=LLMResponse)
    response2.text = "The capital of Spain is Madrid."

    # Cache with a very short TTL
    cache.set(prompt2, response2, ttl=0.1)

    # Should be in the cache initially
    assert cache.get(prompt2) is response2

    # Wait for TTL to expire
    time.sleep(0.2)

    # Should be removed from the cache
    assert cache.get(prompt2) is None

    # Test invalidation
    cache.invalidate(prompt)
    assert cache.get(prompt) is None

    # Test invalidating all
    cache.set(prompt, response)
    cache.invalidate()
    assert cache.get(prompt) is None


def test_file_cache():
    """Test the FileCache class."""
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()

    try:
        # Create a cache
        cache = FileCache(temp_dir)

        # Create a prompt
        prompt = (
            PromptBuilder()
            .add_system("You are a helpful assistant.")
            .add_user("What is the capital of France?")
            .build()
        )

        # Initially, the cache should be empty
        assert cache.get(prompt) is None

        # Create a proper LLMResponse object instead of a mock
        response = LLMResponse(
            text="The capital of France is Paris.",
            model="test-model",
            provider="test-provider"
        )

        # Cache the response
        cache.set(prompt, response)

        # Retrieve the response from the cache
        cached_response = cache.get(prompt)
        assert cached_response is not None
        assert cached_response.text == "The capital of France is Paris."

        # Test invalidation
        cache.invalidate(prompt)
        assert cache.get(prompt) is None

        # Test invalidating all
        cache.set(prompt, response)
        cache.invalidate()
        assert cache.get(prompt) is None

    finally:
        # Clean up the temporary directory
        shutil.rmtree(temp_dir)
