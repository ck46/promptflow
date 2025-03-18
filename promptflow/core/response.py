"""
Response classes for LLM providers.
"""

from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field

from promptflow.core.types import Message, PromptStats


class FunctionCall(BaseModel):
    """A function call made by the model."""
    name: str
    arguments: Dict[str, Any]


class LLMResponse(BaseModel):
    """
    A response from an LLM provider.
    """
    text: str
    model: Optional[str] = None
    provider: Optional[str] = None
    messages: Optional[List[Message]] = None
    stats: Optional[PromptStats] = None
    function_call: Optional[FunctionCall] = None
    chunks: Optional[List[str]] = None
    raw_response: Optional[Dict[str, Any]] = None
    
    def get_message(self) -> Message:
        """
        Get the response as a message.
        
        Returns:
            A Message object with the response.
        """
        from promptflow.core.types import MessageRole
        
        return Message(
            role=MessageRole.ASSISTANT,
            content=self.text
        )
    
    def update_stats(self, **kwargs) -> "LLMResponse":
        """
        Update the stats for the response.
        
        Args:
            **kwargs: The stats to update.
            
        Returns:
            The updated response.
        """
        if self.stats is None:
            self.stats = PromptStats()
            
        for key, value in kwargs.items():
            if hasattr(self.stats, key):
                setattr(self.stats, key, value)
                
        return self


class StreamingResponse:
    """
    A streaming response from an LLM provider.
    """
    def __init__(self, model: Optional[str] = None, provider: Optional[str] = None):
        self.text = ""
        self.chunks: List[str] = []
        self.model = model
        self.provider = provider
        self.stats = PromptStats()
        self.done = False
        
    def add_chunk(self, chunk: str) -> None:
        """
        Add a chunk to the response.
        
        Args:
            chunk: The chunk to add.
        """
        self.chunks.append(chunk)
        self.text += chunk
        
    def to_response(self) -> LLMResponse:
        """
        Convert the streaming response to a regular response.
        
        Returns:
            An LLMResponse object.
        """
        return LLMResponse(
            text=self.text,
            model=self.model,
            provider=self.provider,
            stats=self.stats,
            chunks=self.chunks
        ) 