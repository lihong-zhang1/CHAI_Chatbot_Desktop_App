"""
UI styling for CHAI Friend.

All the colors and CSS-style stuff in one place. 
Makes it easier to keep the theme consistent and change colors later.
"""

from config import config


class Theme:
    """Centralized theme management for consistent styling."""
    
    @staticmethod
    def get_main_window_style() -> str:
        """Get main window styling."""
        return f"""
            QWidget {{
                background: {config.style.BACKGROUND_GRADIENT};
                color: white;
                font-family: '{config.style.FONT_FAMILY}';
            }}
        """
    
    @staticmethod
    def get_header_style() -> str:
        """Get header styling."""
        return """
            QWidget {
                background: rgba(0, 0, 0, 0.2);
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }
        """
    
    @staticmethod
    def get_ai_bubble_style() -> str:
        """Get AI message bubble styling."""
        return f"""
            QFrame {{
                background: {config.style.AI_BUBBLE_COLOR};
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                margin: 8px;
            }}
        """
    
    @staticmethod
    def get_user_bubble_style() -> str:
        """Get user message bubble styling."""
        return f"""
            QFrame {{
                background: {config.style.PRIMARY_GRADIENT};
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.3);
                margin: 8px;
            }}
        """
    
    @staticmethod
    def get_input_area_style() -> str:
        """Get input area styling."""
        return """
            QFrame {
                background: rgba(0, 0, 0, 0.3);
                border-radius: 25px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
        """
    
    @staticmethod
    def get_button_style(primary: bool = True) -> str:
        """Get button styling."""
        if primary:
            return f"""
                QPushButton {{
                    background: {config.style.PRIMARY_GRADIENT};
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 20px;
                    color: white;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(255, 255, 255, 1.0),
                        stop:0.3 rgba(220, 170, 255, 0.9),
                        stop:1.0 rgba(198, 97, 217, 1.0));
                }}
            """
        else:
            return """
                QPushButton {
                    background: rgba(255, 255, 255, 0.1);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 20px;
                    color: white;
                }
                QPushButton:hover {
                    background: rgba(255, 255, 255, 0.2);
                }
            """
    
    @staticmethod
    def get_avatar_style() -> str:
        """Get avatar styling."""
        return f"""
            QLabel {{
                background: {config.style.PRIMARY_GRADIENT};
                border-radius: 20px;
                font-size: 20px;
                color: white;
            }}
        """
    
    @staticmethod
    def get_quick_reply_style() -> str:
        """Get quick reply button styling."""
        return f"""
            QPushButton {{
                background: {config.style.PRIMARY_GRADIENT.replace('0.9', '0.7').replace('0.8', '0.6')};
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 15px;
                color: white;
                font-size: 12px;
                padding: 8px 12px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 255, 255, 0.9),
                    stop:0.3 rgba(220, 170, 255, 0.8),
                    stop:1.0 rgba(198, 97, 217, 0.9));
            }}
        """