"""
Configuration for CHAI Friend.

Keeps all the settings in one place so they're easy to find and change.
Learned this the hard way after having magic numbers scattered everywhere.
"""

import os
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class APIConfig:
    """API configuration settings."""
    BASE_URL: str = "http://guanaco-submitter.guanaco-backend.k2.chaiverse.com/endpoints/onsite/chat"
    API_KEY: str = "Bearer CR_14d43f2bf78b4b0590c2a8b87f354746"
    TIMEOUT: int = 30
    MAX_RETRIES: int = 3


@dataclass
class UIConfig:
    """User interface configuration."""
    # Window settings
    MIN_WIDTH: int = 380
    MIN_HEIGHT: int = 600
    DEFAULT_WIDTH: int = 450
    DEFAULT_HEIGHT: int = 750
    
    # Chat settings
    BOT_NAME: str = "CHAI Friend"
    USER_NAME: str = "You"
    
    # Files
    HISTORY_FILE: str = "chat_history.json"
    SETTINGS_FILE: str = "settings.json"


@dataclass
class StyleConfig:
    """Styling configuration for consistent theming."""
    # Color palette
    PRIMARY_GRADIENT = """
        qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 rgba(255, 255, 255, 0.9),
            stop:0.3 rgba(200, 150, 255, 0.8),
            stop:1.0 rgba(178, 77, 197, 0.9))
    """
    
    BACKGROUND_GRADIENT = """
        qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 rgba(30, 30, 50, 1.0),
            stop:0.3 rgba(20, 20, 40, 1.0),
            stop:0.7 rgba(15, 15, 30, 1.0),
            stop:1.0 rgba(10, 10, 20, 1.0))
    """
    
    AI_BUBBLE_COLOR = "rgba(30, 30, 30, 0.9)"
    FONT_FAMILY = "Arial, sans-serif"


class AppConfig:
    """Main application configuration."""
    
    def __init__(self):
        self.api = APIConfig()
        self.ui = UIConfig()
        self.style = StyleConfig()
        
        # Safety prompt for responsible AI interaction
        self.safety_prompt = (
            "This conversation must be family friendly. Avoid using profanity, "
            "or being rude. Be courteous and use language which is appropriate "
            "for any audience. Avoid NSFW content. ###"
        )
    
    @property
    def api_headers(self) -> Dict[str, str]:
        """Get API headers for requests."""
        return {"Authorization": self.api.API_KEY}
    
    def get_file_path(self, filename: str) -> str:
        """Get full path for application files."""
        return os.path.join(os.path.dirname(__file__), filename)


# Global configuration instance
config = AppConfig()