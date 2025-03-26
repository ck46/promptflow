# Poetry Package Management Guide

## Updating Package Version

Update version using Poetry's built-in version command:
```bash
poetry version patch  # for patch version increment (0.0.x)
poetry version minor  # for minor version increment (0.x.0)
poetry version major  # for major version increment (x.0.0)
```

Or specify exact version:
```bash
poetry version 1.2.3
```

## Building the Package

Build your package:
```bash
poetry build
```

This creates distributions in the `dist/` directory.

## Publishing to PyPI

### First-time Setup

1. Create an account on PyPI (https://pypi.org)

2. Configure Poetry with your PyPI credentials:
```bash
poetry config pypi-token.pypi your-token-here
```

### Publishing

Publish to PyPI:
```bash
poetry publish
```

To build and publish in one command:
```bash
poetry publish --build
```

### Testing Before Publishing

1. Configure TestPyPI:
```bash
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry config pypi-token.testpypi your-test-token-here
```

2. Publish to TestPyPI:
```bash
poetry publish -r testpypi
```

## Upgrading an Installed Package

Update dependencies in your project:
```bash
poetry update
```

Update a specific package:
```bash
poetry update package-name
```

## Managing Dependencies

Add a new dependency:
```bash
poetry add package-name
```

Add a development dependency:
```bash
poetry add --group dev package-name
```

Remove a dependency:
```bash
poetry remove package-name
```

## Best Practices

1. Keep your `pyproject.toml` organized and clean
2. Use `poetry.lock` for deterministic builds (commit this file)
3. Update dependencies regularly with `poetry update`
4. Test your package before publishing:
```bash
poetry install  # Install your package in development mode
poetry run pytest  # Run your tests
```

## Common Issues

1. **Lock file conflicts**: Resolve with `poetry lock --no-update`
2. **Authentication errors**: Verify your PyPI token is correctly configured
3. **Build errors**: Check your `pyproject.toml` configuration
4. **Version conflicts**: Ensure version bumps are appropriate

## Example `pyproject.toml`

```toml:pyproject.toml
[tool.poetry]
name = "your-package"
version = "1.0.0"
description = "Your package description"
authors = ["Your Name <your.email@example.com>"]
readme = "README.md"
packages = [{include = "your_package"}]

[tool.poetry.dependencies]
python = "^3.8"

[tool.poetry.group.dev.dependencies]
pytest = "^7.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

## Quick Reference

```bash
# Version management
poetry version patch

# Build
poetry build

# Publish
poetry publish --build

# Install in development
poetry install

# Update dependencies
poetry update

# Run commands in virtual environment
poetry run python script.py
poetry run pytest
```