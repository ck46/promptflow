"""
Command-line interface for PromptFlow.
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path


def run_ui():
    """Run the Streamlit UI."""
    # Get the path to the streamlit_app.py file
    app_path = Path(__file__).parent / "ui" / "streamlit_app.py"
    
    # Run streamlit
    cmd = [sys.executable, "-m", "streamlit", "run", str(app_path), "--server.headless", "true"]
    subprocess.run(cmd)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="PromptFlow CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # UI command
    ui_parser = subparsers.add_parser("ui", help="Run the PromptFlow UI")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Run the appropriate command
    if args.command == "ui":
        run_ui()
    else:
        parser.print_help()


if __name__ == "__main__":
    main() 