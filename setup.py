"""Setup script for the BookMinder package."""

from setuptools import setup, find_packages

setup(
    name="bookminder",
    version="0.1.0",
    packages=find_packages(),
    python_requires=">=3.9",
    extras_require={
        "dev": [
            "pytest",
            "pytest-describe",
            "pytest-spec",
            "pytest-cov",
            "black",
            "flake8",
            "mypy",
            "pre-commit",
        ],
    },
)
