"""
Example of running the PromptFlow UI.
"""

import os
import sys
from pathlib import Path

# Add the parent directory to the path so we can import promptflow
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import streamlit
except ImportError:
    print(
        "Streamlit is not installed. "
        "Please install it with 'pip install streamlit'."
    )
    sys.exit(1)

from promptflow.ui import run_streamlit_app

if __name__ == "__main__":
    # Run the Streamlit app
    run_streamlit_app() 