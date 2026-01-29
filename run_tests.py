"""
Test runner script for CyberBooks application
Run all tests with: python run_tests.py
"""

import unittest
import sys
import os

# Add the parent directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Discover and run all tests
if __name__ == '__main__':
    # Create test loader
    loader = unittest.TestLoader()
    
    # Discover tests in tests directory
    start_dir = 'tests'
    suite = loader.discover(start_dir, pattern='test*.py')
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with proper code
    sys.exit(0 if result.wasSuccessful() else 1)
