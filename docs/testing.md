# Testing PromptFlow

This guide provides instructions for testing the PromptFlow library.

## Prerequisites

Before running tests, ensure you have the development dependencies installed:

```bash
# Using Poetry (recommended)
poetry install --with dev

# Using pip
pip install -e ".[dev]"
```

The development dependencies include:
- pytest: For running tests
- pytest-cov: For generating test coverage reports
- flake8: For linting
- black: For code formatting
- isort: For import sorting
- mypy: For type checking

If you're missing any dependencies (for example, if you get an error about `--cov` being an unrecognized argument), install them using:

```bash
poetry add --group dev pytest-cov
```

## Running Tests

PromptFlow uses pytest for testing. You can run the entire test suite with:

```bash
# Using Poetry
poetry run pytest

# Directly with pytest if you have it installed
pytest
```

### Running Specific Tests

To run a specific test file:

```bash
poetry run pytest tests/core/test_prompt.py
```

To run a specific test function:

```bash
poetry run pytest tests/core/test_prompt.py::test_prompt_builder
```

### Verbose Output

For more detailed output, use the `-v` or `-vv` flag:

```bash
poetry run pytest -v
```

### Test Coverage

To see test coverage reports:

```bash
poetry run pytest --cov=promptflow
```

For a detailed HTML coverage report:

```bash
poetry run pytest --cov=promptflow --cov-report=html
```

This will generate a report in the `htmlcov` directory. Open the `index.html` file in your browser to view it.

## Integration Tests

Integration tests verify the interaction between different components of the PromptFlow library. These tests may require internet connectivity if they interact with external LLM providers.

To run only integration tests:

```bash
poetry run pytest tests/test_integration.py
```

## Writing Tests

When contributing to PromptFlow, please follow these guidelines for writing tests:

1. **Test Organization**: Place unit tests in the appropriate directory under `tests/` corresponding to the module being tested.

2. **Naming Conventions**: 
   - Test files should be named `test_*.py`
   - Test functions should be named `test_*`
   - Test classes should be named `Test*`

3. **Test Documentation**: Each test function should have a docstring describing what is being tested.

4. **Assertions**: Use pytest's assertion mechanisms rather than the `unittest` style assertions.

5. **Mocking**: When testing components that interact with external services, use `unittest.mock` to mock those interactions.

### Example Test

Here's an example of a well-structured test:

```python
def test_prompt_builder():
    """Test creating a prompt using PromptBuilder."""
    # Create a prompt using the builder
    builder = PromptBuilder()
    builder.add_system("You are a helpful assistant.")
    builder.add_user("What is the capital of France?")

    # Build the prompt
    prompt = builder.build()

    # Check that the prompt has the expected messages
    assert len(prompt.messages) == 2
    assert prompt.messages[0].role == MessageRole.SYSTEM
    assert prompt.messages[0].content == "You are a helpful assistant."
    assert prompt.messages[1].role == MessageRole.USER
    assert prompt.messages[1].content == "What is the capital of France?"
```

## Debugging Tests

For debugging tests, you can use the `--pdb` flag to drop into the Python debugger on test failure:

```bash
poetry run pytest --pdb
```

You can also use the `-s` flag to see print statements and other output:

```bash
poetry run pytest -s
```

## Continuous Integration

PromptFlow uses GitHub Actions for continuous integration. The test suite is automatically run on push to the main branch and on pull requests.

To see the current CI configuration, check the `.github/workflows/ci.yml` file. 