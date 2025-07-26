#!/usr/bin/env python3
"""
Test runner for CHAI Friend.

Just a simple way to run all our tests at once.
Could use pytest but keeping it simple with unittest for now.
"""

import unittest
import sys
import os

# Add src directory to path so we can import our modules
current_dir = os.path.dirname(__file__)
src_dir = os.path.join(os.path.dirname(current_dir), 'src')
sys.path.insert(0, src_dir)


def run_all_tests():
    """Run all test modules."""
    # Discover and run tests
    loader = unittest.TestLoader()
    suite = loader.discover('.', pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code based on results
    return 0 if result.wasSuccessful() else 1


def run_specific_test(test_module):
    """Run a specific test module."""
    try:
        # Import the test module
        module = __import__(test_module)
        
        # Load tests from module
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromModule(module)
        
        # Run tests
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        return 0 if result.wasSuccessful() else 1
        
    except ImportError as e:
        print(f"Error importing test module {test_module}: {e}")
        return 1


if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Run specific test
        test_name = sys.argv[1]
        if not test_name.startswith('test_'):
            test_name = f'test_{test_name}'
        if not test_name.endswith('.py'):
            test_name = test_name.replace('.py', '')
        
        print(f"Running tests for: {test_name}")
        exit_code = run_specific_test(test_name)
    else:
        # Run all tests
        print("Running all tests...")
        exit_code = run_all_tests()
    
    sys.exit(exit_code)