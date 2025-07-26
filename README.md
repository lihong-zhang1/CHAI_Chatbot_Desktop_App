# CHAI Friend - AI Chat Companion

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A modern desktop chat application for having conversations with AI. Built with PyQt5 and designed with a clean, intuitive interface.

## Features

- **Modern UI**: Clean purple-themed interface with gradient effects
- **AI Chat**: Powered by CHAI's language model for natural conversations  
- **Resizable Window**: Drag to resize, works well on different screen sizes
- **Quick Start**: Pre-made conversation starters to get going quickly
- **Rich Text**: Basic markdown formatting and emoji support
- **Chat History**: Remembers previous conversations for context
- **Smooth Experience**: Non-blocking UI with background API calls

## Getting Started

### What you'll need

- Python 3.7+ 
- A system that can run PyQt5 (Windows, macOS, or Linux)

### Installation

1. **Get the code**
   ```bash
   git clone <your-repo-url>
   cd CHAI-Friend
   ```

2. **Install what it needs**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run it**
   ```bash
   python run.py
   ```

The app should open up and you can start chatting right away.

## How it's organized

The code is split into logical pieces to keep things manageable:

```
├── src/             # Source code
│   ├── main.py      # Main app window and startup
│   ├── config.py    # Settings and configuration 
│   ├── styles.py    # UI colors and styling
│   ├── components.py # Chat bubbles and input areas
│   └── api_client.py # Handles talking to the AI API
├── tests/           # Unit tests
├── docs/            # Documentation and guides
├── run.py           # Main launcher script
└── requirements.txt # Dependencies
```

I tried to keep each file focused on one thing. The main app doesn't need to know about API details, and the UI components don't need to worry about configuration. Makes it easier to change things later.

## Key parts

### Chat Messages
The `ChatBubble` class handles displaying messages. AI messages show up on the left with a sparkle icon, user messages on the right. It processes basic markdown formatting and converts text emojis to actual emojis.

### Input Area  
The text input at the bottom auto-resizes as you type. Enter sends the message, Shift+Enter adds a new line. There's also a voice button (not implemented yet) and the send button.

### API Client
Handles all the communication with CHAI's servers. Runs in a background thread so the UI doesn't freeze while waiting for responses. Has retry logic in case the network is flaky.

## Customizing it

### Colors and styling
Want different colors? Check out `styles.py`. The main purple gradient is defined in `PRIMARY_GRADIENT`. You can change the colors there and it'll update throughout the app.

### Settings
The `config.py` file has the main settings like window size, bot name, and API endpoints. Pretty straightforward to modify if you need to.

## Using it

Just type in the text box at the bottom and hit Enter to send. Shift+Enter if you want to add a new line without sending.

There are some quick-start buttons when you first open the app - just click them to send common greetings.

### Text formatting
Basic markdown works:
- `**bold**` makes **bold** text
- `*italic*` makes *italic* text  
- Backticks for `code`
- Some text emojis get converted: `:)` becomes 😊, `<3` becomes ❤️

## Development stuff

### Testing
There are unit tests you can run:
```bash
python tests/test_runner.py
```

To run the app in development mode, just:
```bash
python run.py
```

Check the console output if something goes wrong - there's logging to help debug issues.

### Code style
I tried to follow standard Python practices. Used type hints where it made sense, kept functions focused, and documented the trickier parts.

## Contributing

Feel free to open issues or submit pull requests if you find bugs or want to add features. The code is organized to make it easy to extend.

## License

MIT License - see [LICENSE](LICENSE) file.

---

Built with Python and PyQt5. Thanks to CHAI for the AI API.