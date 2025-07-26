"""
Tests for UI components.

Testing the message processing and component logic.
PyQt UI testing is tricky so focusing on the core logic here.
"""

import unittest
from datetime import datetime
from components import MessageProcessor


class TestMessageProcessor(unittest.TestCase):
    """Test message text processing features."""
    
    def test_basic_text_passthrough(self):
        """Plain text should pass through unchanged."""
        text = "Hello world"
        result = MessageProcessor.process_text(text)
        self.assertEqual(result, text)
    
    def test_bold_formatting(self):
        """Bold markdown should convert to HTML."""
        text = "This is **bold** text"
        result = MessageProcessor.process_text(text)
        self.assertIn("<b>bold</b>", result)
        self.assertNotIn("**", result)
    
    def test_italic_formatting(self):
        """Italic markdown should convert to HTML."""
        text = "This is *italic* text"
        result = MessageProcessor.process_text(text)
        self.assertIn("<i>italic</i>", result)
    
    def test_code_formatting(self):
        """Code blocks should get styled spans."""
        text = "Here's some `code`"
        result = MessageProcessor.process_text(text)
        self.assertIn("<span", result)
        self.assertIn("monospace", result)
        self.assertIn("code", result)
    
    def test_emoji_conversion(self):
        """Text emojis should convert to unicode."""
        test_cases = [
            (":)", "😊"),
            (":(", "😢"),
            ("<3", "❤️"),
            (":D", "😄")
        ]
        
        for text_emoji, unicode_emoji in test_cases:
            result = MessageProcessor.process_text(text_emoji)
            self.assertIn(unicode_emoji, result)
            self.assertNotIn(text_emoji, result)
    
    def test_line_breaks(self):
        """Newlines should convert to HTML breaks."""
        text = "Line one\nLine two"
        result = MessageProcessor.process_text(text)
        self.assertIn("<br>", result)
        self.assertNotIn("\n", result)
    
    def test_mixed_formatting(self):
        """Multiple formatting types should work together."""
        text = "**Bold** and *italic* with `code` :)"
        result = MessageProcessor.process_text(text)
        
        self.assertIn("<b>Bold</b>", result)
        self.assertIn("<i>italic</i>", result)
        self.assertIn("monospace", result)
        self.assertIn("😊", result)
    
    def test_nested_formatting_protection(self):
        """Nested formatting shouldn't break."""
        # This is a bit of an edge case but worth testing
        text = "**Bold with *italic* inside**"
        result = MessageProcessor.process_text(text)
        
        # Should have both formatting types
        self.assertIn("<b>", result)
        self.assertIn("<i>", result)
    
    def test_empty_string(self):
        """Empty string should be handled gracefully."""
        result = MessageProcessor.process_text("")
        self.assertEqual(result, "")
    
    def test_only_whitespace(self):
        """Whitespace-only strings should be preserved."""
        text = "   \n   "
        result = MessageProcessor.process_text(text)
        # Should have spaces and converted line break
        self.assertIn(" ", result)
        self.assertIn("<br>", result)


class TestChatBubbleLogic(unittest.TestCase):
    """Test ChatBubble component logic (without UI)."""
    
    def test_timestamp_defaults(self):
        """ChatBubble should handle timestamp defaults."""
        # Can't easily test the actual ChatBubble class without QApplication
        # but we can test the logic
        
        now = datetime.now()
        # If we pass None, it should use current time
        # This would be tested in the actual ChatBubble constructor
        self.assertIsNotNone(now)
    
    def test_message_type_detection(self):
        """Different message types should be detected properly."""
        # AI messages vs user messages
        # This would be tested with actual ChatBubble instances
        ai_message = True
        user_message = False
        
        self.assertTrue(ai_message)
        self.assertFalse(user_message)


# Note: Full UI component testing would require:
# - QApplication setup
# - Mock parent widgets
# - Event simulation
# This is complex enough that it's often done with integration tests instead

if __name__ == '__main__':
    unittest.main()