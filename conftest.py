"""Configure module imports for pytest."""
import sys
import os

# Add project root to Python path for proper imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
