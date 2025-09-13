# Stateful ChatBot with Auto-Persistence

A minimal, streamlined chatbot implementation using Google's Gemini Flash API with automatic session persistence, user profiles, and conversation memory.

## Features

- ✅ **Automatic Session Persistence** - No manual save/load needed
- ✅ **User Profiles** - Remembers name and preferences
- ✅ **Conversation Memory** - Maintains context across sessions
- ✅ **Auto-Summarization** - Compresses long conversations
- ✅ **Minimal Dependencies** - Only 2 packages required
- ✅ **Single File** - Everything in one clean script

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install google-generativeai python-dotenv
   ```

2. **Set up API key**:
   ```bash
   echo "GOOGLE_API_KEY=your_api_key_here" > .env
   ```

3. **Run the chatbot**:
   ```bash
   python streamlined_chatbot.py
   ```

## Usage

### Commands
- `set_user <id>` - Set current user
- `update_profile name=<name>,interest=<topic>` - Update profile
- `quit` - Exit

### Example Session
```
You: set_user john123
User set to: john123

You: update_profile name=John,interest=AI
Profile updated

You: Hi, I'm John and I love machine learning
Bot: Hello John! I'd be happy to help you learn about ML...

You: quit

# Later - restart app
python streamlined_chatbot.py
🔄 Loaded session for user: john123

You: What's my name?
Bot: Your name is John.
```

## How It Works

- **Auto-Save**: Sessions are automatically saved after every interaction
- **Auto-Load**: Previous sessions are automatically restored on startup
- **Memory Management**: Keeps last 50 messages, summarizes when needed
- **Context Awareness**: Uses user profile info in conversations

## Files

- `streamlined_chatbot.py` - Main chatbot (single file)
- `requirements_minimal.txt` - Minimal dependencies
- `chatbot_session.json` - Auto-generated session file
- `.env` - Your API key (create this)

## Session Persistence

The chatbot automatically:
- Saves your session to `chatbot_session.json`
- Loads your session when you restart
- Remembers your name, preferences, and conversation history
- Compresses long conversations to save space

No manual intervention needed - just start chatting!

## Requirements

- Python 3.7+
- Google API key
- Only 2 packages: `google-generativeai`, `python-dotenv`

## License

MIT License - feel free to use and modify!