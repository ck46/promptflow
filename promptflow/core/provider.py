"""
Abstract base class for LLM providers.
"""

from abc import ABC, abstractmethod
import time
from typing import Dict, Any, Optional, List, Union, Callable

from promptflow.core.prompt import Prompt
from promptflow.core.response import LLMResponse


class LLMProvider(ABC):
    """
    Abstract base class for LLM providers (OpenAI, Anthropic, Hugging Face, etc.).
    """
    
    def __init__(self, api_key: Optional[str] = None, **kwargs):
        """
        Initialize the provider.
        
        Args:
            api_key: The API key for the provider.
            **kwargs: Additional provider-specific arguments.
        """
        self.api_key = api_key
        self.config = kwargs
        
    @abstractmethod
    async def complete_async(self, prompt: Prompt) -> LLMResponse:
        """
        Complete a prompt asynchronously.
        
        Args:
            prompt: The prompt to complete.
            
        Returns:
            The response from the LLM.
        """
        pass
    
    def complete(self, prompt: Prompt) -> LLMResponse:
        """
        Complete a prompt synchronously.
        
        Args:
            prompt: The prompt to complete.
            
        Returns:
            The response from the LLM.
        """
        import asyncio
        
        # Get or create an event loop
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
        # Run the async method in the event loop
        start_time = time.time()
        response = loop.run_until_complete(self.complete_async(prompt))
        end_time = time.time()
        
        # Calculate latency
        if response.stats is None:
            response.stats = {}
        response.stats["latency_ms"] = (end_time - start_time) * 1000
        
        return response
    
    @abstractmethod
    async def stream_async(self, prompt: Prompt) -> LLMResponse:
        """
        Stream a response to a prompt asynchronously.
        
        Args:
            prompt: The prompt to complete.
            
        Returns:
            The streaming response from the LLM.
        """
        pass
    
    def stream(self, prompt: Prompt, callback: Optional[Callable[[str], None]] = None) -> LLMResponse:
        """
        Stream a response to a prompt synchronously.
        
        Args:
            prompt: The prompt to complete.
            callback: A function to call with each chunk of text.
            
        Returns:
            The final response from the LLM.
        """
        import asyncio
        
        # Get or create an event loop
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        async def _stream_with_callback():
            response = await self.stream_async(prompt)
            
            if callback and hasattr(response, "chunks"):
                for chunk in response.chunks:
                    callback(chunk)
                    
            return response
        
        # Run the async method in the event loop
        start_time = time.time()
        response = loop.run_until_complete(_stream_with_callback())
        end_time = time.time()
        
        # Calculate latency
        if response.stats is None:
            response.stats = {}
        response.stats["latency_ms"] = (end_time - start_time) * 1000
        
        return response 