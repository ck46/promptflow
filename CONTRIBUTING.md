# Contributing to PromptFlow

Thank you for your interest in contributing to PromptFlow! This document provides guidelines for contributing to the project.

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally: `git clone https://github.com/ck46/promptflow.git`
3. Install development dependencies: `poetry install --with dev`
4. Create a branch for your contribution: `git checkout -b feature/your-feature-name`

## Development Workflow

1. Make your changes in your feature branch
2. Add tests for your changes
3. Run tests to ensure they pass: `poetry run pytest`
4. Check code style: `poetry run black promptflow tests`
5. Check imports: `poetry run isort promptflow tests`
6. Run type checking: `poetry run mypy promptflow`
7. Commit your changes: `git commit -m "Add your meaningful commit message"`
8. Push to your fork: `git push origin feature/your-feature-name`
9. Create a Pull Request from your fork to the main repository

## Testing

All contributions must include appropriate tests. Please refer to the [Testing Documentation](docs/testing.md) for details on how to write and run tests for PromptFlow.

## Pull Request Process

1. Update the README.md and documentation with details of changes to the interface, if applicable
2. Make sure all tests pass in the CI pipeline
3. The PR will be merged once it receives approval from maintainers

## Coding Standards

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Write docstrings for all modules, classes, and functions
- Add type hints to function signatures
- Keep functions small and focused on a single responsibility
- Use black and isort for formatting code

## Documentation

- Update documentation when changing functionality
- Use clear and consistent language
- Include examples when appropriate
- Documentation is in Markdown format

## Reporting Bugs

When reporting bugs, please include:

- A clear and descriptive title
- A detailed description of the bug
- Steps to reproduce the behavior
- Expected behavior
- Actual behavior
- Environment information (OS, Python version, etc.)

## Feature Requests

Feature requests are welcome. Please provide:

- A clear and descriptive title
- A detailed description of the proposed feature
- Any relevant examples or use cases
- If possible, a description of how you would implement the feature

## Questions?

If you have any questions about contributing, please open an issue with your question.

Thank you for contributing to PromptFlow! 