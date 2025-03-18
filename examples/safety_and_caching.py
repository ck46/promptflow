"""
Example demonstrating prompt filters and caching in PromptFlow.
"""

import os
import time
from dotenv import load_dotenv

from promptflow import PromptBuilder
from promptflow.integrations import OpenAIProvider
from promptflow.prompt_filters import (
    KeywordFilter,
    RegexFilter,
    MaxTokenFilter,
    ContentPolicyFilter,
    FilterPipeline
)
from promptflow.utils import InMemoryCache, FileCache

# Load environment variables from .env file (if it exists)
load_dotenv()


def setup_provider_with_cache():
    """Create an OpenAI provider with caching enabled."""
    # Create a provider
    provider = OpenAIProvider(
        api_key=os.environ.get("OPENAI_API_KEY"),
        model="gpt-3.5-turbo"
    )
    
    # Create a cache
    cache = InMemoryCache()
    # Alternative: cache = FileCache(".promptflow_cache")
    
    # Wrap the provider's complete method to use caching
    original_complete = provider.complete
    
    def cached_complete(prompt, **kwargs):
        # Check if the response is in the cache
        cached_response = cache.get(prompt)
        if cached_response:
            print("Using cached response")
            return cached_response
            
        # Get a new response from the provider
        print("Making API call")
        response = original_complete(prompt, **kwargs)
        
        # Cache the response (with a 1-hour TTL)
        cache.set(prompt, response, ttl=3600)
        
        return response
        
    # Replace the complete method with our cached version
    provider.complete = cached_complete
    
    return provider


def setup_content_policy():
    """Create a content policy filter pipeline."""
    # Create individual filters
    harmful_content_filter = KeywordFilter(
        keywords=[
            "hack", "crack", "illegal", "bomb", "weapon", "fraud",
            "steal", "murder", "terrorist", "suicide"
        ],
        name="HarmfulContentFilter"
    )
    
    personal_info_filter = RegexFilter(
        patterns=[
            r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",  # US phone number
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # Email
            r"\b(?:\d{4}[ -]?){3}\d{4}\b",  # Credit card number
            r"\b\d{3}[ -]?\d{2}[ -]?\d{4}\b",  # SSN
        ],
        name="PersonalInfoFilter"
    )
    
    token_limit_filter = MaxTokenFilter(
        max_tokens=1000,
        name="TokenLimitFilter"
    )
    
    # Create a filter pipeline
    return FilterPipeline([
        harmful_content_filter,
        personal_info_filter,
        token_limit_filter
    ])


def example_content_policy():
    """Example of using content policy filters."""
    print("\n=== Content Policy Example ===")
    
    # Set up provider
    provider = setup_provider_with_cache()
    
    # Set up content policy
    content_policy = setup_content_policy()
    
    # Create various prompts
    prompts = [
        PromptBuilder().add_user("What is the capital of France?").build(),
        PromptBuilder().add_user("How can I hack into a website?").build(),
        PromptBuilder().add_user("My email is user@example.com").build(),
        PromptBuilder().add_user("My phone number is 123-456-7890").build(),
    ]
    
    # Check each prompt against the content policy
    for i, prompt in enumerate(prompts):
        print(f"\nPrompt {i+1}: {prompt.messages[0].content}")
        
        # Check the prompt against the content policy
        result = content_policy.check(prompt)
        
        if result.passed:
            print("Prompt passed content policy check")
            response = provider.complete(prompt)
            print(f"Response: {response.text}")
        else:
            print(f"Prompt failed content policy check: {result.reason}")
            if "failed_filter" in result.details:
                print(f"Failed filter: {result.details['failed_filter']}")


def example_caching():
    """Example of using response caching."""
    print("\n=== Caching Example ===")
    
    # Set up provider with caching
    provider = setup_provider_with_cache()
    
    # Create a prompt
    prompt = PromptBuilder()\
        .add_system("You are a helpful assistant.")\
        .add_user("What is the capital of France?")\
        .build()
    
    # First request should make an API call
    print("\nFirst request:")
    response1 = provider.complete(prompt)
    print(f"Response: {response1.text}")
    
    # Second request with the same prompt should use the cache
    print("\nSecond request (should use cache):")
    response2 = provider.complete(prompt)
    print(f"Response: {response2.text}")
    
    # Modify the prompt
    modified_prompt = PromptBuilder()\
        .add_system("You are a helpful assistant.")\
        .add_user("What is the capital of Italy?")\
        .build()
    
    # Request with a different prompt should make a new API call
    print("\nRequest with different prompt:")
    response3 = provider.complete(modified_prompt)
    print(f"Response: {response3.text}")


if __name__ == "__main__":
    example_content_policy()
    example_caching() 