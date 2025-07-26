"""
API client tests.

Testing the CHAI API client functionality. Had to mock the actual API calls
since we don't want to spam their servers during testing.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import json
from api_client import (
    ChatMessage, ChatRequest, APIClient, AsyncAPIWorker, 
    create_chat_request
)


class TestChatMessage(unittest.TestCase):
    """Test the ChatMessage class."""
    
    def test_message_creation(self):
        """Basic message creation should work."""
        msg = ChatMessage("user", "hello there")
        
        self.assertEqual(msg.sender, "user")
        self.assertEqual(msg.message, "hello there")
        self.assertIsNotNone(msg.timestamp)
    
    def test_message_to_dict(self):
        """Converting to dict should work for API calls."""
        msg = ChatMessage("bot", "hi back")
        result = msg.to_dict()
        
        self.assertEqual(result["sender"], "bot")
        self.assertEqual(result["message"], "hi back")
        # timestamp shouldn't be in API dict
        self.assertNotIn("timestamp", result)


class TestChatRequest(unittest.TestCase):
    """Test chat request building."""
    
    def test_basic_request_creation(self):
        """Creating a basic request should work."""
        messages = [ChatMessage("user", "test")]
        request = ChatRequest("new message", messages)
        
        self.assertEqual(request.user_message, "new message")
        self.assertEqual(len(request.chat_history), 1)
        # Should use defaults for optional fields
        self.assertIsNotNone(request.bot_name)
        self.assertIsNotNone(request.user_name)
    
    def test_request_to_payload(self):
        """Payload generation should have right format."""
        messages = [ChatMessage("user", "hello")]
        request = ChatRequest("hi", messages)
        payload = request.to_payload()
        
        # Check required fields are there
        self.assertIn("memory", payload)
        self.assertIn("prompt", payload)
        self.assertIn("bot_name", payload)
        self.assertIn("user_name", payload)
        self.assertIn("chat_history", payload)
        
        # History should be list of dicts
        self.assertIsInstance(payload["chat_history"], list)
        if len(payload["chat_history"]) > 0:
            self.assertIsInstance(payload["chat_history"][0], dict)


class TestAPIClient(unittest.TestCase):
    """Test the main API client."""
    
    def setUp(self):
        """Set up test client."""
        self.client = APIClient()
    
    @patch('api_client.requests.Session.post')
    def test_successful_api_call(self, mock_post):
        """Test successful API response handling."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"model_output": "test response"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Create test request
        request = ChatRequest("test", [])
        success, response, error = self.client.send_message(request)
        
        self.assertTrue(success)
        self.assertEqual(response, "test response")
        self.assertIsNone(error)
    
    @patch('api_client.requests.Session.post')
    def test_api_error_handling(self, mock_post):
        """Test API error scenarios."""
        # Mock failed response
        mock_post.side_effect = Exception("Network error")
        
        request = ChatRequest("test", [])
        success, response, error = self.client.send_message(request)
        
        self.assertFalse(success)
        self.assertIsNone(response)
        self.assertIsNotNone(error)
        self.assertIn("error", error.lower())
    
    @patch('api_client.requests.Session.post')
    def test_json_fallback(self, mock_post):
        """Test fallback when JSON parsing fails."""
        # Mock response with invalid JSON
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = json.JSONDecodeError("bad json", "", 0)
        mock_response.text = "plain text response"
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        request = ChatRequest("test", [])
        success, response, error = self.client.send_message(request)
        
        self.assertTrue(success)
        self.assertEqual(response, "plain text response")


class TestFactoryFunction(unittest.TestCase):
    """Test the convenience factory function."""
    
    def test_create_request_no_history(self):
        """Creating request without history should work."""
        request = create_chat_request("hello")
        
        self.assertEqual(request.user_message, "hello")
        self.assertEqual(len(request.chat_history), 0)
    
    def test_create_request_with_history(self):
        """Creating request with history should work."""
        history = [
            {"sender": "user", "message": "hi"},
            {"sender": "bot", "message": "hello"}
        ]
        request = create_chat_request("how are you?", history)
        
        self.assertEqual(request.user_message, "how are you?")
        self.assertEqual(len(request.chat_history), 2)
        
        # Check history conversion
        self.assertEqual(request.chat_history[0].sender, "user")
        self.assertEqual(request.chat_history[1].message, "hello")


# Note: AsyncAPIWorker tests would need QApplication setup for PyQt testing
# Skipping those for now since they're more complex to test properly

if __name__ == '__main__':
    unittest.main()