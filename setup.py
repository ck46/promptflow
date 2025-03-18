"""
Setup script for PromptFlow.
"""

from setuptools import setup, find_packages

# Read version from package
with open("promptflow/__init__.py", "r") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"\'')
            break

# Read description from README
with open("README.md", "r") as f:
    long_description = f.read()

# Core dependencies
core_deps = [
    "pydantic>=1.9.0,<2.0.0",
    "jinja2>=3.0.0",
    "semver>=2.13.0",
]

# Database dependencies
db_deps = [
    "tortoise-orm>=0.19.0",
    "aiosqlite>=0.17.0",
]

# API dependencies
api_deps = [
    "fastapi>=0.68.0",
    "uvicorn>=0.15.0",
]

# UI dependencies
ui_deps = [
    "streamlit>=1.22.0",
]

setup(
    name="promptflow",
    version=version,
    description="A comprehensive prompt management library for Large Language Models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="PromptFlow Team",
    author_email="info@promptflow.com",
    url="https://github.com/promptflow/promptflow",
    packages=find_packages(),
    include_package_data=True,
    install_requires=core_deps + db_deps,
    extras_require={
        "api": api_deps,
        "ui": ui_deps,
        "all": api_deps + ui_deps,
    },
    entry_points={
        "console_scripts": [
            "promptflow=promptflow.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
) 