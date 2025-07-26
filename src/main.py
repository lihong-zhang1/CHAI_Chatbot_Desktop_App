#!/usr/bin/env python3
"""
CHAI Friend - AI Chat Desktop App

A desktop chat application for talking with AI. Built with PyQt5.
Focuses on clean UI and smooth user experience.

Started as a learning project but turned out pretty nice.
"""

import sys
import json
import logging
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QScrollArea, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

from config import config
from styles import Theme
from components import ChatBubble, InputArea, QuickReplySection
from api_client import AsyncAPIWorker, create_chat_request, ChatMessage

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChatWindow(QWidget):
    """Main chat window with modern design and smooth interactions."""
    
    def __init__(self):
        super().__init__()
        self.chat_history: List[Dict[str, str]] = []
        self.api_worker: Optional[AsyncAPIWorker] = None
        self.thinking_bubble: Optional[QWidget] = None
        self.is_waiting_for_reply = False
        
        self._setup_window()
        self._create_ui()
        self._load_history_silently()
    
    def _setup_window(self):
        """Configure the main window properties."""
        self.setWindowTitle("CHAI Friend")
        self.setMinimumSize(config.ui.MIN_WIDTH, config.ui.MIN_HEIGHT)
        self.resize(config.ui.DEFAULT_WIDTH, config.ui.DEFAULT_HEIGHT)
        self.setStyleSheet(Theme.get_main_window_style())
    
    def _create_ui(self):
        """Create the user interface layout."""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header = self._create_header()
        main_layout.addWidget(header)
        
        # Content area
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(16, 20, 16, 20)
        content_layout.setSpacing(20)
        
        # Chat area
        self.chat_scroll = self._create_chat_area()
        content_layout.addWidget(self.chat_scroll, 1)
        
        # Input area
        self.input_area = InputArea(self)
        content_layout.addWidget(self.input_area)
        
        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)
        
        # Initialize with welcome message and quick replies
        self._add_welcome_message()
        self._add_quick_replies()
    
    def _create_header(self) -> QWidget:
        """Create the modern header with title and controls."""
        header = QWidget()
        header.setFixedHeight(80)
        header.setStyleSheet(Theme.get_header_style())
        
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Close button
        close_btn = QPushButton("×")
        close_btn.setFixedSize(40, 40)
        close_btn.setStyleSheet(f"""
            QPushButton {{
                {Theme.get_button_style()}
                font-size: 20px;
            }}
        """)
        close_btn.clicked.connect(self.close)
        
        # Title section
        title_layout = self._create_title_section()
        
        # Settings button
        settings_btn = QPushButton("⚙️")
        settings_btn.setFixedSize(40, 40)
        settings_btn.setStyleSheet(f"""
            QPushButton {{
                {Theme.get_button_style(primary=False)}
                font-size: 16px;
            }}
        """)
        settings_btn.clicked.connect(self._show_settings)
        
        layout.addWidget(close_btn)
        layout.addLayout(title_layout, 1)
        layout.addWidget(settings_btn)
        
        header.setLayout(layout)
        return header
    
    def _create_title_section(self) -> QVBoxLayout:
        """Create the centered title section."""
        title_layout = QVBoxLayout()
        title_layout.setSpacing(2)
        
        # Icon and title row
        title_row = QHBoxLayout()
        
        # App icon
        icon = QLabel("✨")
        icon.setStyleSheet(f"""
            QLabel {{
                {config.style.PRIMARY_GRADIENT.replace('background:', 'background:')}
                border-radius: 8px;
                padding: 2px 6px;
                font-size: 12px;
                color: white;
            }}
        """)
        
        # Title
        title = QLabel("CHAI Friend")
        title.setStyleSheet("color: white; font-size: 18px; font-weight: 600; background: transparent;")
        title.setAlignment(Qt.AlignCenter)
        
        title_row.addWidget(icon)
        title_row.addWidget(title)
        title_row.addStretch()
        
        # Subtitle
        subtitle = QLabel("Your AI Chat Companion")
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 13px; background: transparent;")
        subtitle.setAlignment(Qt.AlignCenter)
        
        title_layout.addLayout(title_row)
        title_layout.addWidget(subtitle)
        
        return title_layout
    
    def _create_chat_area(self) -> QScrollArea:
        """Create the scrollable chat area."""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
        """)
        
        self.chat_widget = QWidget()
        self.chat_widget.setStyleSheet("background: transparent;")
        self.chat_layout = QVBoxLayout()
        self.chat_layout.setSpacing(16)
        self.chat_layout.setContentsMargins(0, 20, 0, 20)
        self.chat_layout.addStretch(1)
        self.chat_widget.setLayout(self.chat_layout)
        scroll.setWidget(self.chat_widget)
        
        return scroll
    
    def _add_welcome_message(self):
        """Add the initial welcome message."""
        welcome_msg = (
            "Hello! I'm CHAI Friend, your AI companion. I'm here to chat "
            "with you about anything you'd like to discuss. How are you doing today?"
        )
        self._add_message(config.ui.BOT_NAME, welcome_msg, is_ai=True)
    
    def _add_quick_replies(self):
        """Add quick reply section."""
        quick_replies = QuickReplySection(self)
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, quick_replies)
    
    def _add_message(
        self, 
        sender: str, 
        message: str, 
        is_ai: bool, 
        timestamp: Optional[datetime] = None
    ) -> QWidget:
        """Add a message to the chat with proper alignment."""
        bubble = ChatBubble(sender, message, is_ai, timestamp)
        
        # Create container for proper 2:1 alignment
        container = QWidget()
        container.setStyleSheet("background: transparent;")
        container_layout = QHBoxLayout()
        container_layout.setContentsMargins(0, 0, 0, 0)
        
        if is_ai:
            # AI message: 2/3 width, left-aligned
            container_layout.addWidget(bubble, 2)
            container_layout.addStretch(1)
        else:
            # User message: 2/3 width, right-aligned
            container_layout.addStretch(1)
            container_layout.addWidget(bubble, 2)
        
        container.setLayout(container_layout)
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, container)
        
        # Auto-scroll to bottom
        QTimer.singleShot(100, self._scroll_to_bottom)
        
        return bubble
    
    def _scroll_to_bottom(self):
        """Smoothly scroll to the bottom of the chat."""
        scrollbar = self.chat_scroll.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def send_message(self):
        """Send user message and get AI response."""
        if self.is_waiting_for_reply:
            return
        
        user_text = self.input_area.input_field.toPlainText().strip()
        if not user_text:
            return
        
        # Clear input and add user message
        self.input_area.input_field.clear()
        self.input_area._adjust_height()
        
        timestamp = datetime.now()
        self._add_message(config.ui.USER_NAME, user_text, is_ai=False, timestamp=timestamp)
        
        # Save to history
        self.chat_history.append({
            "sender": config.ui.USER_NAME,
            "message": user_text,
            "timestamp": timestamp.isoformat()
        })
        
        # Show thinking indicator
        self._show_thinking_indicator()
        
        # Send to AI
        self._send_to_ai()
    
    def _show_thinking_indicator(self):
        """Show AI thinking indicator."""
        self.thinking_bubble = self._add_message(config.ui.BOT_NAME, "🤔 Thinking...", is_ai=True)
        self.input_area.send_btn.setEnabled(False)
        self.is_waiting_for_reply = True
    
    def _send_to_ai(self):
        """Send message to AI in background thread."""
        request = create_chat_request(
            user_message=self.chat_history[-1]["message"],
            chat_history=self.chat_history[:-1]  # Exclude the current message
        )
        
        self.api_worker = AsyncAPIWorker(request)
        self.api_worker.response_ready.connect(self._handle_ai_response)
        self.api_worker.error_occurred.connect(self._handle_ai_error)
        self.api_worker.finished.connect(self._on_ai_finished)
        self.api_worker.start()
    
    def _handle_ai_response(self, response: str):
        """Handle successful AI response."""
        self._remove_thinking_indicator()
        
        timestamp = datetime.now()
        self._add_message(config.ui.BOT_NAME, response, is_ai=True, timestamp=timestamp)
        
        # Save to history
        self.chat_history.append({
            "sender": config.ui.BOT_NAME,
            "message": response,
            "timestamp": timestamp.isoformat()
        })
        
        self._save_history()
    
    def _handle_ai_error(self, error: str):
        """Handle AI response error."""
        self._remove_thinking_indicator()
        self._add_message(config.ui.BOT_NAME, error, is_ai=True)
    
    def _remove_thinking_indicator(self):
        """Remove the thinking indicator."""
        if self.thinking_bubble:
            self.thinking_bubble.setParent(None)
            self.thinking_bubble = None
    
    def _on_ai_finished(self):
        """Re-enable UI after AI response."""
        self.input_area.send_btn.setEnabled(True)
        self.is_waiting_for_reply = False
    
    def _load_history_silently(self):
        """Load chat history for AI context without displaying."""
        history_file = Path(config.ui.HISTORY_FILE)
        
        try:
            if history_file.exists():
                with open(history_file, 'r', encoding='utf-8') as f:
                    self.chat_history = json.load(f)
                logger.info(f"Loaded {len(self.chat_history)} messages for AI context")
            else:
                self.chat_history = []
        except Exception as e:
            logger.error(f"Failed to load history: {e}")
            self.chat_history = []
    
    def _save_history(self):
        """Save chat history to file."""
        history_file = Path(config.ui.HISTORY_FILE)
        
        try:
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(self.chat_history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save history: {e}")
    
    def _show_settings(self):
        """Show settings dialog."""
        msg = QMessageBox()
        msg.setWindowTitle("Settings")
        msg.setText(
            "Settings panel coming soon!\n\n"
            "Available actions:\n"
            "• Clear current session\n"
            "• Export conversation\n"
            "• Change theme\n\n"
            "Note: Chat history is saved for AI context but hidden from view."
        )
        msg.exec_()


def main():
    """Main application entry point."""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("CHAI Friend")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("AI Studio")
    app.setQuitOnLastWindowClosed(True)
    
    # Create and show main window
    window = ChatWindow()
    window.show()
    
    # Start event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()