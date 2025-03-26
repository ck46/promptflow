"""
PromptFlow: A comprehensive prompt management library for Large Language Models.
"""

__version__ = "0.1.0"

from promptflow.api import PromptFlow
from promptflow.core.database import DBPromptRepo
from promptflow.core.prompt import Prompt, PromptBuilder
from promptflow.core.provider import LLMProvider
from promptflow.core.repository import PromptRepo
from promptflow.core.response import LLMResponse
from promptflow.core.strategy import (
    ABTestingPromptStrategy,
    ActivePromptStrategy,
    CategoryPromptStrategy,
    ConditionalPromptStrategy,
    ContextAwarePromptStrategy,
    FallbackPromptStrategy,
    LatestPromptStrategy,
    PromptSelector,
    PromptStrategy,
)
from promptflow.core.template import MultiMessageTemplate, PromptTemplate
from promptflow.core.types import (
    Message,
    MessageRole,
    PromptCategory,
    PromptMetadata,
    PromptParameters,
    PromptStats,
)

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
