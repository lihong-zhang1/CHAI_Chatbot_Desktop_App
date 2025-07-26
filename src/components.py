"""
UI Components for CHAI Friend Chat Application.

This module contains reusable, well-designed UI components that demonstrate
clean architecture and separation of concerns.
"""

import re
from datetime import datetime
from typing import Optional, Callable
from PyQt5.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QTextEdit, QWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from config import config
from styles import Theme


class MessageProcessor:
    """Elegant message processing with markdown and emoji support."""
    
    @staticmethod
    def process_text(text: str) -> str:
        """Process markdown formatting and emojis in text."""
        # Apply markdown formatting
        text = MessageProcessor._apply_markdown(text)
        
        # Convert emoji patterns
        text = MessageProcessor._convert_emojis(text)
        
        # Handle line breaks
        text = text.replace('\n', '<br>')
        
        return text
    
    @staticmethod
    def _apply_markdown(text: str) -> str:
        """Apply basic markdown formatting."""
        # Bold text **text** -> <b>text</b>
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        
        # Italic text *text* -> <i>text</i>
        text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
        
        # Code blocks `code` -> styled code
        text = re.sub(
            r'`(.*?)`', 
            r'<span style="background-color: rgba(100,100,100,0.3); '
            r'padding: 2px 4px; border-radius: 3px; font-family: monospace;">\1</span>', 
            text
        )
        
        return text
    
    @staticmethod
    def _convert_emojis(text: str) -> str:
        """Convert text patterns to emojis."""
        emoji_patterns = {
            ':)': '😊', ':-)': '😊', ':(': '😢', ':-(': '😢',
            ':D': '😄', ':-D': '😄', ':P': '😛', ':-P': '😛',
            ';)': '😉', ';-)': '😉', ':o': '😮', ':-o': '😮',
            '<3': '❤️', '</3': '💔', ':*': '😘', ':-*': '😘'
        }
        
        for pattern, emoji in emoji_patterns.items():
            text = text.replace(pattern, emoji)
        
        return text


class ChatBubble(QFrame):
    """Elegant chat bubble component with modern styling."""
    
    def __init__(
        self, 
        sender: str, 
        message: str, 
        is_ai: bool, 
        timestamp: Optional[datetime] = None
    ):
        super().__init__()
        self.sender = sender
        self.message = message
        self.is_ai = is_ai
        self.timestamp = timestamp or datetime.now()
        
        self._setup_styling()
        self._create_layout()
    
    def _setup_styling(self):
        """Apply appropriate styling based on sender type."""
        if self.is_ai:
            self.setStyleSheet(Theme.get_ai_bubble_style())
        else:
            self.setStyleSheet(Theme.get_user_bubble_style())
    
    def _create_layout(self):
        """Create the bubble layout with header and content."""
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(8)
        
        # Create header
        header = self._create_header()
        layout.addLayout(header)
        
        # Create message content
        content = self._create_content()
        layout.addWidget(content)
        
        # Add action buttons for AI messages
        if self.is_ai and not self.message.startswith("🤔"):
            actions = self._create_action_buttons()
            layout.addLayout(actions)
        
        self.setLayout(layout)
    
    def _create_header(self) -> QHBoxLayout:
        """Create the message header with avatar, name, and timestamp."""
        header_layout = QHBoxLayout()
        
        if self.is_ai:
            return self._create_ai_header(header_layout)
        else:
            return self._create_user_header(header_layout)
    
    def _create_ai_header(self, layout: QHBoxLayout) -> QHBoxLayout:
        """Create header for AI messages."""
        # AI avatar
        avatar = QLabel("✨")
        avatar.setFixedSize(40, 40)
        avatar.setAlignment(Qt.AlignCenter)
        avatar.setStyleSheet(Theme.get_avatar_style())
        
        # Name and timestamp section
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)
        
        # Name and time in same row
        name_time_layout = QHBoxLayout()
        name_time_layout.setSpacing(8)
        
        name_label = QLabel(self.sender)
        name_label.setStyleSheet("color: white; font-size: 16px; font-weight: 600; background: transparent;")
        
        time_label = QLabel(self.timestamp.strftime('%H:%M'))
        time_label.setStyleSheet("color: rgba(255, 255, 255, 0.6); font-size: 11px; background: transparent;")
        
        name_time_layout.addWidget(name_label)
        name_time_layout.addWidget(time_label)
        name_time_layout.addStretch()
        
        # Subtitle
        subtitle = QLabel("AI Companion")
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 12px; background: transparent;")
        
        info_layout.addLayout(name_time_layout)
        info_layout.addWidget(subtitle)
        
        layout.addWidget(avatar)
        layout.addLayout(info_layout)
        layout.addStretch()
        
        return layout
    
    def _create_user_header(self, layout: QHBoxLayout) -> QHBoxLayout:
        """Create header for user messages."""
        layout.addStretch()
        
        # User info (right-aligned, no avatar)
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)
        
        # Name and time layout
        name_time_layout = QHBoxLayout()
        name_time_layout.addStretch()
        
        time_label = QLabel(self.timestamp.strftime('%H:%M'))
        time_label.setStyleSheet("color: rgba(255, 255, 255, 0.9); font-size: 11px; background: transparent;")
        
        name_label = QLabel(self.sender)
        name_label.setStyleSheet("color: white; font-size: 14px; font-weight: 600; background: transparent;")
        
        name_time_layout.addWidget(time_label)
        name_time_layout.addWidget(name_label)
        
        info_layout.addLayout(name_time_layout)
        layout.addLayout(info_layout)
        
        return layout
    
    def _create_content(self) -> QLabel:
        """Create the message content with formatting."""
        processed_message = MessageProcessor.process_text(self.message)
        
        content_label = QLabel(processed_message)
        content_label.setWordWrap(True)
        content_label.setFont(QFont(config.style.FONT_FAMILY.split(',')[0], 15))
        content_label.setStyleSheet("""
            color: white; 
            line-height: 1.5; 
            background: transparent;
            padding: 8px 0px;
        """)
        content_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        
        return content_label
    
    def _create_action_buttons(self) -> QHBoxLayout:
        """Create action buttons for AI messages."""
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(8)
        actions_layout.setContentsMargins(0, 8, 0, 0)
        
        actions = [
            ("👍", "Like"),
            ("📋", "Copy"),
            ("🔄", "Regenerate"),
            ("🔊", "Read aloud")
        ]
        
        for icon, tooltip in actions:
            btn = QPushButton(icon)
            btn.setToolTip(tooltip)
            btn.setFixedSize(32, 32)
            btn.setStyleSheet("""
                QPushButton {
                    background: rgba(255, 255, 255, 0.1);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 16px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background: rgba(255, 255, 255, 0.2);
                }
            """)
            actions_layout.addWidget(btn)
        
        actions_layout.addStretch()
        return actions_layout


class InputArea(QFrame):
    """Modern input area with auto-resize and keyboard shortcuts."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the input area UI."""
        self.setStyleSheet(Theme.get_input_area_style())
        
        layout = QHBoxLayout()
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)
        
        # Create input field
        self.input_field = self._create_input_field()
        
        # Create action buttons
        voice_btn = self._create_voice_button()
        self.send_btn = self._create_send_button()
        
        layout.addWidget(self.input_field, 1)
        layout.addWidget(voice_btn)
        layout.addWidget(self.send_btn)
        
        self.setLayout(layout)
        
        # Setup event handlers
        self._setup_event_handlers()
    
    def _create_input_field(self) -> QTextEdit:
        """Create the main input text field."""
        field = QTextEdit()
        field.setPlaceholderText("Send message...")
        field.setMaximumHeight(120)
        field.setMinimumHeight(44)
        field.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        field.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        field.setStyleSheet(f"""
            QTextEdit {{
                background: transparent;
                border: none;
                color: white;
                font-size: 16px;
                font-family: '{config.style.FONT_FAMILY}';
                padding: 8px 0px;
            }}
            QTextEdit::placeholder {{
                color: rgba(255, 255, 255, 0.5);
            }}
        """)
        return field
    
    def _create_voice_button(self) -> QPushButton:
        """Create the voice input button."""
        btn = QPushButton("🎤")
        btn.setFixedSize(40, 40)
        btn.setToolTip("Voice input")
        btn.setStyleSheet(f"""
            QPushButton {{
                background: rgba(233, 30, 133, 0.8);
                border: none;
                border-radius: 20px;
                color: white;
                font-size: 18px;
            }}
            QPushButton:hover {{
                background: rgba(233, 30, 133, 1.0);
            }}
        """)
        return btn
    
    def _create_send_button(self) -> QPushButton:
        """Create the send message button."""
        btn = QPushButton("→")
        btn.setFixedSize(40, 40)
        btn.setToolTip("Send message")
        btn.setStyleSheet(f"""
            QPushButton {{
                {Theme.get_button_style().replace('border-radius: 20px', 'border-radius: 20px').replace('font-weight: bold;', 'font-weight: bold; font-size: 20px;')}
            }}
            QPushButton:disabled {{
                background: rgba(100, 100, 100, 0.5);
                color: rgba(255, 255, 255, 0.3);
            }}
        """)
        return btn
    
    def _setup_event_handlers(self):
        """Setup event handlers for input functionality."""
        # Auto-resize functionality
        self.input_field.textChanged.connect(self._adjust_height)
        
        # Connect send button
        if self.parent_window:
            self.send_btn.clicked.connect(self.parent_window.send_message)
            self.input_field.keyPressEvent = self._handle_key_press
    
    def _adjust_height(self):
        """Auto-adjust input height based on content."""
        doc = self.input_field.document()
        doc.setTextWidth(self.input_field.viewport().width())
        height = doc.size().height() + 16
        height = max(44, min(120, int(height)))
        self.input_field.setFixedHeight(height)
    
    def _handle_key_press(self, event):
        """Handle keyboard shortcuts."""
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            if event.modifiers() == Qt.ShiftModifier:
                QTextEdit.keyPressEvent(self.input_field, event)
            else:
                if self.parent_window:
                    self.parent_window.send_message()
        else:
            QTextEdit.keyPressEvent(self.input_field, event)


class QuickReplySection(QWidget):
    """Quick reply buttons for common chat starters."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the quick reply section."""
        self.setStyleSheet("background: transparent;")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 8, 16, 8)
        layout.setSpacing(8)
        
        # Title
        title = QLabel("Quick Start")
        title.setStyleSheet("""
            color: rgba(255, 255, 255, 0.7); 
            font-size: 14px; 
            font-weight: 600;
            background: transparent;
            padding: 8px 0px;
        """)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(8)
        
        quick_replies = [
            "👋 Hello",
            "😊 How are you?",
            "🤔 What's new?",
            "💬 Let's chat"
        ]
        
        for reply_text in quick_replies:
            btn = QPushButton(reply_text)
            btn.setStyleSheet(Theme.get_quick_reply_style())
            btn.clicked.connect(
                lambda checked, text=reply_text: self._send_quick_reply(text)
            )
            buttons_layout.addWidget(btn)
        
        layout.addWidget(title)
        layout.addLayout(buttons_layout)
        self.setLayout(layout)
    
    def _send_quick_reply(self, reply_text: str):
        """Send a quick reply message."""
        if self.parent_window:
            # Extract the text part after the emoji
            clean_text = reply_text.split(' ', 1)[1] if ' ' in reply_text else reply_text
            self.parent_window.input_area.input_field.setPlainText(clean_text)
            self.parent_window.send_message()