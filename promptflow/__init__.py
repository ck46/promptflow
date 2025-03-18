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

# Define UI availability flag without importing Streamlit
HAS_UI = False

# Define a function to get UI components only when needed
def get_ui_components():
    """Get UI components if streamlit is installed."""
    try:
        from promptflow.ui import run_streamlit_app
        return {"run_streamlit_app": run_streamlit_app}
    except ImportError:
        raise ImportError(
            "Streamlit is not installed. Install with 'pip install streamlit' "
            "or 'pip install promptflow[ui]' to use UI components."
        )

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
    
    # UI
    "HAS_UI",
    "get_ui_components",
] 