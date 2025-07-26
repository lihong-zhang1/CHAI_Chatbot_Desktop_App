"""
CHAI API Client - handles talking to the AI service.

Does the HTTP requests to CHAI's API and handles responses.
Includes retry logic because network requests can be flaky.
Runs in background threads so the UI doesn't freeze.
"""

import json
import logging
import requests
from datetime import datetime
from typing import List, Dict, Optional, Tuple, Callable
from dataclasses import dataclass, asdict
from PyQt5.QtCore import QThread, pyqtSignal

from config import config

# Configure elegant logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class ChatMessage:
    """Immutable representation of a chat message."""
    sender: str
    message: str
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary for API consumption."""
        return {"sender": self.sender, "message": self.message}


@dataclass
class ChatRequest:
    """Structured chat request with validation."""
    user_message: str
    chat_history: List[ChatMessage]
    bot_name: str = None
    user_name: str = None
    custom_prompt: str = None
    
    def __post_init__(self):
        self.bot_name = self.bot_name or config.ui.BOT_NAME
        self.user_name = self.user_name or config.ui.USER_NAME
        self.custom_prompt = self.custom_prompt or config.safety_prompt
    
    def to_payload(self) -> Dict:
        """Convert to API payload format."""
        return {
            "memory": "",
            "prompt": self.custom_prompt,
            "bot_name": self.bot_name,
            "user_name": self.user_name,
            "chat_history": [msg.to_dict() for msg in self.chat_history]
        }


class APIClient:
    """Elegant CHAI API client with robust error handling."""
    
    def __init__(self):
        self.session = self._create_session()
    
    def _create_session(self) -> requests.Session:
        """Create a robust HTTP session with retry strategy."""
        session = requests.Session()
        
        # Configure retry strategy for resilience
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry
        
        retry_strategy = Retry(
            total=2,  # Reduce retries for faster failure
            backoff_factor=0.5,
            status_forcelist=[429, 502, 503, 504],  # Don't retry on 500
            method_whitelist=["POST"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def send_message(self, request: ChatRequest) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Send message to CHAI API with elegant error handling.
        
        Returns:
            Tuple[success: bool, response: Optional[str], error: Optional[str]]
        """
        try:
            logger.info(f"Sending request for {request.bot_name}")
            
            response = self.session.post(
                config.api.BASE_URL,
                headers=config.api_headers,
                json=request.to_payload(),
                timeout=config.api.TIMEOUT
            )
            
            response.raise_for_status()
            
            # Parse response with fallback
            try:
                data = response.json()
                message = data.get("model_output", "No response")
            except json.JSONDecodeError:
                message = response.text.strip()
            
            logger.info("Successfully received response")
            return True, message, None
            
        except requests.exceptions.Timeout:
            error = "Request timed out. Please try again."
            logger.error(error)
            return False, None, error
            
        except requests.exceptions.ConnectionError:
            error = "Connection failed. Check your internet connection."
            logger.error(error)
            return False, None, error
            
        except requests.exceptions.HTTPError as e:
            error = f"HTTP Error: {e}"
            logger.error(error)
            return False, None, error
            
        except Exception as e:
            error = f"Unexpected error: {str(e)}"
            logger.error(error)
            return False, None, error


class AsyncAPIWorker(QThread):
    """Asynchronous worker for non-blocking API calls."""
    
    # Elegant signal definitions
    response_ready = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    progress_update = pyqtSignal(int)
    
    def __init__(self, request: ChatRequest):
        super().__init__()
        self.request = request
        self.client = APIClient()
    
    def run(self):
        """Execute API request in background thread."""
        try:
            self.progress_update.emit(20)
            
            success, response, error = self.client.send_message(self.request)
            
            self.progress_update.emit(80)
            
            if success:
                self.progress_update.emit(100)
                self.response_ready.emit(response)
            else:
                self.error_occurred.emit(f"❌ {error}")
                
        except Exception as e:
            self.error_occurred.emit(f"❌ Unexpected error: {str(e)}")


# Convenience factory function
def create_chat_request(
    user_message: str,
    chat_history: List[Dict[str, str]] = None
) -> ChatRequest:
    """Factory function to create a chat request from simple inputs."""
    history = []
    if chat_history:
        history = [
            ChatMessage(sender=msg["sender"], message=msg["message"])
            for msg in chat_history
        ]
    
    return ChatRequest(
        user_message=user_message,
        chat_history=history
    )