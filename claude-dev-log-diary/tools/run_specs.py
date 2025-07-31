#!/usr/bin/env python3
"""
Simple test runner for explore_session characterization tests.
Run from the tools directory: python run_tests.py
"""
import sys
import os

# Add the tools directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run tests
import pytest

if __name__ == "__main__":
    # Run with pytest but use standard naming
    pytest.main([
        "specs/",
        "-v",
        "--tb=short",
        "--no-header",
        "-p", "no:cacheprovider",  # Disable .pytest_cache
        "--override-ini=python_files=*_spec.py",
        "--override-ini=python_classes=describe_*", 
        "--override-ini=python_functions=it_*"
    ])