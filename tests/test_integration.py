"""
Integration tests for the PromptFlow library.
"""

from unittest.mock import MagicMock, patch

import pytest

from promptflow import PromptBuilder
from promptflow.core.response import LLMResponse
from promptflow.core.types import PromptStats
from promptflow.integrations import OpenAIProvider
from promptflow.prompt_filters import FilterPipeline, KeywordFilter, MaxTokenFilter
from promptflow.utils import InMemoryCache


class TestIntegration:
    """Integration tests for PromptFlow components."""

    def test_provider_with_filters_and_cache(self):
        """Test using a provider with filters and cache."""
        # Create a mock provider
        provider = MagicMock(spec=OpenAIProvider)

        # Mock the complete method to return a fixed response
        mock_response = LLMResponse(
            text="The capital of France is Paris.",
            stats=PromptStats(
                prompt_tokens=20, completion_tokens=10, total_tokens=30, latency_ms=500
            ),
            provider="mock",
            model="mock-model",
            raw_response={"choices": [{"message": {"content": "The capital of France is Paris."}}]},
        )
        provider.complete.return_value = mock_response

        # Create a filter pipeline
        keyword_filter = KeywordFilter(
            keywords=["hack", "illegal", "bomb"], name="HarmfulContentFilter"
        )

        token_filter = MaxTokenFilter(max_tokens=1000, name="TokenLimitFilter")

        pipeline = FilterPipeline([keyword_filter, token_filter])

        # Create a cache
        cache = InMemoryCache()

        # Create a prompt that should pass the filters
        prompt1 = (
            PromptBuilder()
            .add_system("You are a helpful assistant.")
            .add_user("What is the capital of France?")
            .build()
        )

        # Check filters and get response
        filter_result = pipeline.check(prompt1)
        assert filter_result.passed is True

        # Get response
        response = provider.complete(prompt1)
        assert response.text == "The capital of France is Paris."

        # Cache the response
        cache.set(prompt1, response)

        # Verify the response is in the cache
        cached_response = cache.get(prompt1)
        assert cached_response is not None
        assert cached_response.text == "The capital of France is Paris."

        # Create a prompt that should fail the filters
        prompt2 = (
            PromptBuilder()
            .add_system("You are a helpful assistant.")
            .add_user("How can I hack into a website?")
            .build()
        )

        # Check filters
        filter_result = pipeline.check(prompt2)
        assert filter_result.passed is False
        assert filter_result.details["failed_filter"] == "HarmfulContentFilter"
