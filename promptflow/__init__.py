"""
PromptFlow: A comprehensive prompt management library for Large Language Models.
"""

__version__ = "0.1.0"

from promptflow.core.prompt import Prompt, PromptBuilder
from promptflow.core.template import PromptTemplate, MultiMessageTemplate
from promptflow.core.repository import PromptRepo
from promptflow.core.provider import LLMProvider
from promptflow.core.response import LLMResponse
from promptflow.core.database import DBPromptRepo
from promptflow.core.strategy import (
    PromptStrategy, ActivePromptStrategy, FallbackPromptStrategy, 
    LatestPromptStrategy, ConditionalPromptStrategy, ABTestingPromptStrategy,
    ContextAwarePromptStrategy, CategoryPromptStrategy, PromptSelector
)
from promptflow.core.types import (
    MessageRole, Message, PromptMetadata, PromptParameters, 
    PromptStats, PromptCategory
)
from promptflow.api import PromptFlow

# Import UI components if streamlit is installed
try:
    import streamlit
    from promptflow.ui import run_streamlit_app
    HAS_UI = True
except ImportError:
    HAS_UI = False

__all__ = [
    # Core classes
    "Prompt", 
    "PromptBuilder", 
    "PromptTemplate", 
    "MultiMessageTemplate", 
    "PromptRepo",
    "LLMProvider",
    "LLMResponse",
    
    # Database
    "DBPromptRepo",
    
    # Strategies
    "PromptStrategy",
    "ActivePromptStrategy",
    "FallbackPromptStrategy",
    "LatestPromptStrategy",
    "ConditionalPromptStrategy",
    "ABTestingPromptStrategy",
    "ContextAwarePromptStrategy",
    "CategoryPromptStrategy",
    "PromptSelector",
    
    # Types
    "MessageRole",
    "Message",
    "PromptMetadata",
    "PromptParameters",
    "PromptStats",
    "PromptCategory",
    
    # High-level API
    "PromptFlow",
]

# Add UI components if available
if HAS_UI:
    __all__.extend(["run_streamlit_app"]) 