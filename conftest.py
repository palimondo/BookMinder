"""Configure module imports for pytest."""

import os
import sys

# Add project root to Python path for proper imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
