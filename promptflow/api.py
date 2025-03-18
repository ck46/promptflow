"""
High-level API for the PromptFlow library.
"""

import asyncio
import os
from typing import Dict, List, Optional, Any, Union, Callable

from promptflow.core.prompt import Prompt, PromptBuilder
from promptflow.core.template import PromptTemplate, MultiMessageTemplate
from promptflow.core.database import DBPromptRepo
from promptflow.core.strategy import (
    PromptStrategy, PromptSelector, ActivePromptStrategy, 
    FallbackPromptStrategy, LatestPromptStrategy
)
from promptflow.core.types import PromptCategory, PromptMetadata, MessageRole


class PromptFlow:
    """
    Main API for the PromptFlow library.
    """
    
    def __init__(self, db_url: Optional[str] = None):
        """
        Initialize the PromptFlow API.
        
        Args:
            db_url: Database URL. If None, uses SQLite in the current directory.
        """
        if db_url is None:
            # Use SQLite in the current directory by default
            db_url = f"sqlite://{os.getcwd()}/promptflow.db"
        
        self.repo = DBPromptRepo(db_url)
        self.selector = PromptSelector(self.repo)
    
    def _get_or_create_event_loop(self):
        """Get the current event loop or create a new one if it doesn't exist."""
        try:
            return asyncio.get_event_loop()
        except RuntimeError:
            # Create a new event loop if one doesn't exist in the current thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop
    
    def init(self):
        """Initialize the database."""
        loop = self._get_or_create_event_loop()
        loop.run_until_complete(self.repo.init())
    
    def close(self):
        """Close the database connection."""
        loop = self._get_or_create_event_loop()
        loop.run_until_complete(self.repo.close())
    
    def create_prompt(self) -> PromptBuilder:
        """
        Create a new prompt.
        
        Returns:
            A PromptBuilder for building the prompt. 
        
        Note:
            By default, prompts require at least one user message when built.
            To create a prompt without a user message, pass require_user_message=False
            to the build() method:
            
            ```
            prompt = flow.create_prompt().add_system("System instruction").build(require_user_message=False)
            ```
        """
        return PromptBuilder()
    
    def save_prompt(self, name: str, prompt: Prompt, version: Optional[str] = None, 
                   make_active: bool = True) -> str:
        """
        Save a prompt.
        
        Args:
            name: The name of the prompt.
            prompt: The prompt to save.
            version: Optional version to use. If None, a new version will be generated.
            make_active: Whether to make this version the active version.
            
        Returns:
            The version of the saved prompt.
        """
        loop = self._get_or_create_event_loop()
        version = loop.run_until_complete(self.repo.save_prompt(name, prompt, version))
        
        if make_active:
            loop.run_until_complete(self.repo.set_active(name, version))
            
        return version
    
    def get_prompt(self, name: str, version: Optional[str] = None) -> Optional[Prompt]:
        """
        Get a prompt.
        
        Args:
            name: The name of the prompt.
            version: Optional version to get. If None, gets the latest version.
            
        Returns:
            The prompt, or None if not found.
        """
        loop = self._get_or_create_event_loop()
        return loop.run_until_complete(self.repo.get_prompt(name, version))
    
    def get_active_prompt(self, name: str) -> Optional[Prompt]:
        """
        Get the active prompt for a name.
        
        Args:
            name: The name of the prompt.
            
        Returns:
            The active prompt, or None if not found.
        """
        loop = self._get_or_create_event_loop()
        return loop.run_until_complete(self.repo.get_active_prompt(name))
    
    def set_active(self, name: str, version: str) -> None:
        """
        Set a prompt as active.
        
        Args:
            name: The name of the prompt.
            version: The version to set as active.
        """
        loop = self._get_or_create_event_loop()
        loop.run_until_complete(self.repo.set_active(name, version))
    
    def set_fallback(self, name: str, version: str, fallback_for: str) -> None:
        """
        Set a prompt as a fallback for another prompt.
        
        Args:
            name: The name of the prompt.
            version: The version to set as a fallback.
            fallback_for: The name of the prompt this is a fallback for.
        """
        loop = self._get_or_create_event_loop()
        loop.run_until_complete(self.repo.set_fallback(name, version, fallback_for))
    
    def list_prompts(self, category: Optional[PromptCategory] = None) -> List[str]:
        """
        List all prompts.
        
        Args:
            category: Optional category to filter by.
            
        Returns:
            A list of prompt names.
        """
        loop = self._get_or_create_event_loop()
        return loop.run_until_complete(self.repo.list_prompts(category))
    
    def list_versions(self, name: str) -> List[str]:
        """
        List all versions of a prompt.
        
        Args:
            name: The name of the prompt.
            
        Returns:
            A list of versions.
        """
        loop = self._get_or_create_event_loop()
        return loop.run_until_complete(self.repo.list_versions(name))
    
    def select_prompt(self, name: str, strategy: Optional[PromptStrategy] = None, 
                     context: Dict[str, Any] = None) -> Optional[Prompt]:
        """
        Select a prompt using a strategy.
        
        Args:
            name: The name of the prompt.
            strategy: The strategy to use. If None, uses the default strategy.
            context: Additional context for prompt selection.
            
        Returns:
            The selected prompt, or None if not found.
        """
        loop = self._get_or_create_event_loop()
        return loop.run_until_complete(self.selector.select_prompt(name, strategy, context))
    
    def with_fallback(self, strategy: Optional[PromptStrategy] = None) -> FallbackPromptStrategy:
        """
        Create a strategy with fallback.
        
        Args:
            strategy: The primary strategy. If None, uses the active strategy.
            
        Returns:
            A strategy with fallback.
        """
        primary = strategy or self.selector.active_strategy
        return FallbackPromptStrategy(self.repo, primary)
    
    def template_from_string(self, template_str: str, variables: Dict[str, Any] = None) -> PromptTemplate:
        """
        Create a prompt template from a string.
        
        Args:
            template_str: The template string.
            variables: Optional default variables for the template.
            
        Returns:
            A PromptTemplate.
        """
        return PromptTemplate.from_string(template_str, variables)
    
    def template_from_file(self, file_path: str) -> PromptTemplate:
        """
        Create a prompt template from a file.
        
        Args:
            file_path: The path to the template file.
            
        Returns:
            A PromptTemplate.
        """
        return PromptTemplate.from_file(file_path)
    
    def multi_message_template_from_file(self, file_path: str, delimiter: str = "---") -> MultiMessageTemplate:
        """
        Create a multi-message template from a file.
        
        Args:
            file_path: The path to the template file.
            delimiter: The delimiter between messages.
            
        Returns:
            A MultiMessageTemplate.
        """
        return MultiMessageTemplate.from_file(file_path, delimiter)
    
    def create_ab_testing(self, prompt_variants: List[str], 
                        weights: Optional[List[float]] = None) -> PromptStrategy:
        """
        Create an A/B testing strategy.
        
        Args:
            prompt_variants: List of prompt names to test.
            weights: Optional weights for the variants.
            
        Returns:
            An A/B testing strategy.
        """
        return self.selector.create_ab_testing_strategy(prompt_variants, weights)
    
    def create_context_aware(self, context_key: str, 
                           prompt_mapping: Dict[Any, str]) -> PromptStrategy:
        """
        Create a context-aware strategy.
        
        Args:
            context_key: The key to look up in the context.
            prompt_mapping: A mapping from context values to prompt names.
            
        Returns:
            A context-aware strategy.
        """
        return self.selector.create_context_aware_strategy(context_key, prompt_mapping)
    
    def create_conditional(self, condition_fn: Callable[[Dict[str, Any]], bool], 
                         if_true: PromptStrategy, if_false: PromptStrategy) -> PromptStrategy:
        """
        Create a conditional strategy.
        
        Args:
            condition_fn: A function that takes the context and returns a boolean.
            if_true: The strategy to use if the condition is true.
            if_false: The strategy to use if the condition is false.
            
        Returns:
            A conditional strategy.
        """
        return self.selector.create_conditional_strategy(condition_fn, if_true, if_false)
    
    def category_prompts(self, category: PromptCategory) -> PromptStrategy:
        """
        Create a strategy that selects prompts in a category.
        
        Args:
            category: The category to filter by.
            
        Returns:
            A category-based strategy.
        """
        return self.selector.create_category_strategy(category)
    
    def update_stats(self, name: str, version: str, success: bool = True) -> None:
        """
        Update the stats for a prompt.
        
        Args:
            name: The name of the prompt.
            version: The version to update.
            success: Whether the prompt was used successfully.
        """
        loop = self._get_or_create_event_loop()
        loop.run_until_complete(self.repo.update_stats(name, version, success)) 