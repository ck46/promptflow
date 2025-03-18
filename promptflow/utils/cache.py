"""
Caching functionality for PromptFlow.
"""

import os
import json
import time
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Union
import pickle
from pathlib import Path

from promptflow.core.prompt import Prompt
from promptflow.core.response import LLMResponse
from promptflow.utils.hashing import hash_prompt


class ResponseCache(ABC):
    """
    Abstract base class for response caches.
    """
    
    @abstractmethod
    def get(self, prompt: Prompt) -> Optional[LLMResponse]:
        """
        Get a cached response for a prompt.
        
        Args:
            prompt: The prompt to get a cached response for.
            
        Returns:
            The cached response, or None if not found.
        """
        pass
    
    @abstractmethod
    def set(self, prompt: Prompt, response: LLMResponse, ttl: Optional[int] = None) -> None:
        """
        Cache a response for a prompt.
        
        Args:
            prompt: The prompt to cache a response for.
            response: The response to cache.
            ttl: Time-to-live in seconds (optional).
        """
        pass
    
    @abstractmethod
    def invalidate(self, prompt: Optional[Prompt] = None) -> None:
        """
        Invalidate cached responses.
        
        Args:
            prompt: The prompt to invalidate. If None, invalidates all responses.
        """
        pass


class InMemoryCache(ResponseCache):
    """
    In-memory response cache.
    """
    
    def __init__(self):
        self.cache: Dict[str, Dict[str, Any]] = {}
        
    def get(self, prompt: Prompt) -> Optional[LLMResponse]:
        """
        Get a cached response for a prompt.
        
        Args:
            prompt: The prompt to get a cached response for.
            
        Returns:
            The cached response, or None if not found.
        """
        # Hash the prompt to get a cache key
        key = hash_prompt(prompt)
        
        # Check if the key exists in the cache
        if key not in self.cache:
            return None
            
        entry = self.cache[key]
        
        # Check if the entry has expired
        if "expires_at" in entry and entry["expires_at"] < time.time():
            # Remove the expired entry
            del self.cache[key]
            return None
            
        # Return the cached response
        return entry["response"]
    
    def set(self, prompt: Prompt, response: LLMResponse, ttl: Optional[int] = None) -> None:
        """
        Cache a response for a prompt.
        
        Args:
            prompt: The prompt to cache a response for.
            response: The response to cache.
            ttl: Time-to-live in seconds (optional).
        """
        # Hash the prompt to get a cache key
        key = hash_prompt(prompt)
        
        # Create a cache entry
        entry = {
            "response": response,
            "created_at": time.time()
        }
        
        # Add expiration time if TTL is provided
        if ttl is not None:
            entry["expires_at"] = time.time() + ttl
            
        # Add the entry to the cache
        self.cache[key] = entry
    
    def invalidate(self, prompt: Optional[Prompt] = None) -> None:
        """
        Invalidate cached responses.
        
        Args:
            prompt: The prompt to invalidate. If None, invalidates all responses.
        """
        if prompt is None:
            # Clear the entire cache
            self.cache.clear()
        else:
            # Remove a specific entry
            key = hash_prompt(prompt)
            if key in self.cache:
                del self.cache[key]


class FileCache(ResponseCache):
    """
    File-based response cache.
    """
    
    def __init__(self, cache_dir: str = ".promptflow_cache"):
        self.cache_dir = os.path.abspath(cache_dir)
        os.makedirs(self.cache_dir, exist_ok=True)
        
    def _get_cache_path(self, key: str) -> str:
        """Get the file path for a cache key."""
        # Use the first 2 characters of the hash as a subdirectory to avoid
        # too many files in a single directory
        subdir = key[:2]
        subdir_path = os.path.join(self.cache_dir, subdir)
        os.makedirs(subdir_path, exist_ok=True)
        
        return os.path.join(subdir_path, f"{key}.pkl")
        
    def get(self, prompt: Prompt) -> Optional[LLMResponse]:
        """
        Get a cached response for a prompt.
        
        Args:
            prompt: The prompt to get a cached response for.
            
        Returns:
            The cached response, or None if not found.
        """
        # Hash the prompt to get a cache key
        key = hash_prompt(prompt)
        cache_path = self._get_cache_path(key)
        
        # Check if the cache file exists
        if not os.path.exists(cache_path):
            return None
            
        try:
            # Load the cache entry
            with open(cache_path, "rb") as f:
                entry = pickle.load(f)
                
            # Check if the entry has expired
            if "expires_at" in entry and entry["expires_at"] < time.time():
                # Remove the expired entry
                os.remove(cache_path)
                return None
                
            # Return the cached response
            return entry["response"]
        except (IOError, pickle.PickleError):
            # If there's an error loading the cache, ignore it
            return None
    
    def set(self, prompt: Prompt, response: LLMResponse, ttl: Optional[int] = None) -> None:
        """
        Cache a response for a prompt.
        
        Args:
            prompt: The prompt to cache a response for.
            response: The response to cache.
            ttl: Time-to-live in seconds (optional).
        """
        # Hash the prompt to get a cache key
        key = hash_prompt(prompt)
        cache_path = self._get_cache_path(key)
        
        # Create a cache entry
        entry = {
            "response": response,
            "created_at": time.time()
        }
        
        # Add expiration time if TTL is provided
        if ttl is not None:
            entry["expires_at"] = time.time() + ttl
            
        # Save the cache entry
        try:
            with open(cache_path, "wb") as f:
                pickle.dump(entry, f)
        except (IOError, pickle.PickleError):
            # If there's an error saving the cache, ignore it
            pass
    
    def invalidate(self, prompt: Optional[Prompt] = None) -> None:
        """
        Invalidate cached responses.
        
        Args:
            prompt: The prompt to invalidate. If None, invalidates all responses.
        """
        if prompt is None:
            # Clear the entire cache directory
            for root, dirs, files in os.walk(self.cache_dir):
                for file in files:
                    if file.endswith(".pkl"):
                        os.remove(os.path.join(root, file))
        else:
            # Remove a specific entry
            key = hash_prompt(prompt)
            cache_path = self._get_cache_path(key)
            if os.path.exists(cache_path):
                os.remove(cache_path) 