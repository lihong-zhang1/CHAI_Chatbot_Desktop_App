"""
Tests for configuration management.

Quick tests to make sure our config system works as expected.
Nothing fancy, just the basics.
"""

import unittest
import os
from config import config, APIConfig, UIConfig, StyleConfig


class TestConfiguration(unittest.TestCase):
    """Test the config classes work properly."""
    
    def test_api_config_defaults(self):
        """Check API config has sensible defaults."""
        api_config = APIConfig()
        
        self.assertIsNotNone(api_config.BASE_URL)
        self.assertIn("http", api_config.BASE_URL.lower())
        self.assertEqual(api_config.TIMEOUT, 30)
        self.assertEqual(api_config.MAX_RETRIES, 3)
    
    def test_ui_config_window_sizes(self):
        """Make sure window sizes are reasonable."""
        ui_config = UIConfig()
        
        # Window shouldn't be tiny or massive
        self.assertGreater(ui_config.MIN_WIDTH, 300)
        self.assertGreater(ui_config.MIN_HEIGHT, 500)
        self.assertLess(ui_config.DEFAULT_WIDTH, 1000)
        self.assertLess(ui_config.DEFAULT_HEIGHT, 1000)
    
    def test_ui_config_names(self):
        """Check bot and user names are set."""
        ui_config = UIConfig()
        
        self.assertIsNotNone(ui_config.BOT_NAME)
        self.assertIsNotNone(ui_config.USER_NAME)
        self.assertNotEqual(ui_config.BOT_NAME, "")
        self.assertNotEqual(ui_config.USER_NAME, "")
    
    def test_style_config_has_gradients(self):
        """Style config should have gradient definitions."""
        style_config = StyleConfig()
        
        self.assertIn("qlineargradient", style_config.PRIMARY_GRADIENT)
        self.assertIn("qlineargradient", style_config.BACKGROUND_GRADIENT)
        self.assertIsNotNone(style_config.AI_BUBBLE_COLOR)
    
    def test_global_config_instance(self):
        """Global config should be properly initialized."""
        self.assertIsNotNone(config.api)
        self.assertIsNotNone(config.ui)
        self.assertIsNotNone(config.style)
        
        # Should have API headers
        headers = config.api_headers
        self.assertIn("Authorization", headers)
    
    def test_file_path_generation(self):
        """File path generation should work."""
        test_filename = "test.json"
        path = config.get_file_path(test_filename)
        
        self.assertIn(test_filename, path)
        # Path should exist or be constructable
        self.assertIsNotNone(path)


if __name__ == '__main__':
    unittest.main()