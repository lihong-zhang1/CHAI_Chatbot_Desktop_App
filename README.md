# CHAI Friend - AI Chat Companion

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A desktop chat application for having conversations with CHAI AI Model[https://www.chai-research.com/]. 

## Getting Started

### What you'll need

- Python 3.7+ 
- A system that can run PyQt5 (Windows, macOS, or Linux)

### Installation

1. **Get the code**
   ```bash
   git clone https://github.com/lihong-zhang1/CHAI_Chatbot_Desktop_App
   cd CHAI_Chatbot_Desktop_App
   ```

2. **Install what it needs**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run it**
   ```bash
   python run.py
   ```

The app should open up, and you can start chatting right away as below.
<img width="736" height="786" alt="Screenshot 2025-07-26 at 12 07 08 PM" src="https://github.com/user-attachments/assets/a63153ae-21f1-49f1-979c-be8a5d2c6909" />

## Using it

Just type in the text box at the bottom and hit Enter to send. Shift+Enter if you want to add a new line without sending.

There are some quick-start buttons when you first open the app - just click them to send common greetings.

### Text formatting
Basic markdown works:
- `**bold**` makes **bold** text
- `*italic*` makes *italic* text  
- Backticks for `code`
- Some text emojis get converted: `:)` becomes 😊, `<3` becomes ❤️

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

## Key parts of Codes

### Chat Messages
The `ChatBubble` class handles displaying messages. AI messages show up on the left with a sparkle icon, user messages on the right. It processes basic markdown formatting and converts text emojis to actual emojis.

### API Client
Handles all the communication with CHAI's servers. Runs in a background thread so the UI doesn't freeze while waiting for responses. Has retry logic in case the network is flaky.

## Customizing it

### Colors and styling
Check out `styles.py`. The main purple gradient is defined in `PRIMARY_GRADIENT`. You can change the colors there and it'll update throughout the app.

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

## License

MIT License - see [LICENSE](LICENSE) file.

---

Built with Python and PyQt5. Thanks to CHAI for the AI API.
