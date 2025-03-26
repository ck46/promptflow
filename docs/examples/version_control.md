# Prompt Version Control Examples

This guide demonstrates how to use EvolutePrompt's version control features to track and manage your prompts.

## Basic Version Control

```python
from evoluteprompt import PromptVersion, PromptRepository

# Initialize a prompt repository
repo = PromptRepository("my_prompts")

# Create and save a prompt version
prompt = PromptBuilder()\
    .add_system("You are a helpful assistant specialized in science.")\
    .add_user("Explain quantum entanglement.")\
    .build()

# Save the prompt with a version tag
version = PromptVersion(
    prompt=prompt,
    version="v1.0",
    description="Initial science tutor prompt"
)
repo.save_version(version)

# Retrieve a specific version
v1_prompt = repo.get_version("v1.0")

# List all versions
versions = repo.list_versions()
```

## Working with Prompt History

```python
# Get prompt history
history = repo.get_history("science_tutor")

# Compare versions
diff = repo.compare_versions("v1.0", "v2.0")

# Revert to previous version
repo.revert("science_tutor", "v1.0")

# Create a branch for experimentation
repo.create_branch("experimental_prompts")
repo.switch_branch("experimental_prompts")
```

## Version Metadata and Tags

```python
# Add metadata to versions
version = PromptVersion(
    prompt=prompt,
    version="v1.1",
    description="Improved science explanations",
    metadata={
        "author": "Jane Doe",
        "performance_score": 0.95,
        "use_case": "education"
    }
)

# Tag specific versions
repo.add_tag("v1.1", "production-ready")

# Find versions by tag
prod_versions = repo.find_by_tag("production-ready")
``` 