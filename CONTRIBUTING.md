# Contributing to PromptFlow

Thank you for your interest in contributing to PromptFlow! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to abide by our code of conduct. Please be respectful and considerate of others.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue on GitHub with the following information:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior and actual behavior
- Any additional context (screenshots, error messages, etc.)

### Suggesting Features

We welcome feature suggestions! Please create an issue on GitHub with:
- A clear, descriptive title
- A detailed description of the proposed feature
- Any relevant examples or use cases
- Potential implementation details (if applicable)

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Setup

1. Clone the repository
```bash
git clone https://github.com/yourusername/promptflow.git
cd promptflow
```

2. Install dependencies
```bash
poetry install
```

3. Activate the virtual environment
```bash
poetry shell
```

4. Run tests
```bash
pytest
```

## Coding Standards

- Follow PEP 8 style guidelines
- Write docstrings for all functions, classes, and modules
- Include type hints where appropriate
- Write tests for new features and bug fixes

## Commit Message Guidelines

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters
- Reference issues and pull requests liberally after the first line

## License

By contributing to PromptFlow, you agree that your contributions will be licensed under the project's MIT License. 