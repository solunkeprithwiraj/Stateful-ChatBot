#!/usr/bin/env python3
"""
Streamlined Stateful Chatbot with Auto-Persistence
- Single file with minimal dependencies
- Automatic session saving/loading
- User profiles and memory
- Conversation summarization
"""

import os
import json
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

class Chatbot:
    def __init__(self):
        # Configure Google AI
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("Please set GOOGLE_API_KEY in your .env file")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Data storage
        self.user_profiles = {}
        self.current_user = None
        self.conversation_history = []
        self.session_file = "chatbot_session.json"
        
        # Auto-load existing session
        self._load_session()
    
    def _load_session(self):
        """Load session automatically"""
        try:
            if os.path.exists(self.session_file):
                with open(self.session_file, 'r') as f:
                    data = json.load(f)
                
                self.user_profiles = data.get("profiles", {})
                self.current_user = data.get("current_user")
                self.conversation_history = data.get("history", [])
                
                if self.current_user:
                    print(f"🔄 Loaded session for user: {self.current_user}")
        except Exception as e:
            print(f"⚠️ Could not load session: {e}")
    
    def _save_session(self):
        """Save session automatically"""
        try:
            data = {
                "profiles": self.user_profiles,
                "current_user": self.current_user,
                "history": self.conversation_history[-50:],  # Keep last 50 messages
                "last_saved": datetime.now().isoformat()
            }
            
            with open(self.session_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            print(f"⚠️ Save failed: {e}")
    
    def set_user(self, user_id):
        """Set current user"""
        self.current_user = user_id
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {
                "name": None,
                "preferences": {}
            }
        self._save_session()
        print(f"User set to: {user_id}")
    
    def update_profile(self, name=None, **preferences):
        """Update user profile"""
        if not self.current_user:
            print("No user set")
            return
        
        if name:
            self.user_profiles[self.current_user]["name"] = name
        if preferences:
            self.user_profiles[self.current_user]["preferences"].update(preferences)
        
        self._save_session()
        print("Profile updated")
    
    def _get_context(self):
        """Get user context for conversation"""
        if not self.current_user or self.current_user not in self.user_profiles:
            return ""
        
        profile = self.user_profiles[self.current_user]
        context = ""
        
        if profile["name"]:
            context += f"User's name: {profile['name']}. "
        
        if profile["preferences"]:
            prefs = ", ".join([f"{k}: {v}" for k, v in profile["preferences"].items()])
            context += f"Preferences: {prefs}. "
        
        return context
    
    def _summarize_if_needed(self):
        """Summarize conversation if it gets too long"""
        if len(self.conversation_history) < 20:
            return
        
        try:
            # Get recent conversation
            recent = self.conversation_history[-15:]
            conversation_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in recent])
            
            # Create summary
            summary_prompt = f"""
            Summarize this conversation in 2 sentences, focusing on:
            - Key topics discussed
            - Important user information
            
            Conversation:
            {conversation_text}
            
            Summary:
            """
            
            summary = self.model.generate_content(summary_prompt)
            
            # Replace old history with summary
            self.conversation_history = [
                {"role": "system", "content": f"Previous conversation summary: {summary.text}"},
                *self.conversation_history[-5:]  # Keep last 5 messages
            ]
            
            print(f"[System] Conversation summarized")
            
        except Exception as e:
            print(f"[System] Summarization error: {e}")
    
    def chat(self, message):
        """Main chat function"""
        try:
            # Get user context
            context = self._get_context()
            
            # Build conversation history
            history_text = ""
            for msg in self.conversation_history[-10:]:  # Last 10 messages
                history_text += f"{msg['role'].title()}: {msg['content']}\n"
            
            # Create prompt
            prompt = f"{history_text}{context}Human: {message}\nAssistant:"
            
            # Get response
            response = self.model.generate_content(prompt)
            response_text = response.text
            
            # Store conversation
            self.conversation_history.extend([
                {"role": "human", "content": message, "timestamp": datetime.now().isoformat()},
                {"role": "assistant", "content": response_text, "timestamp": datetime.now().isoformat()}
            ])
            
            # Summarize if needed
            self._summarize_if_needed()
            
            # Auto-save
            self._save_session()
            
            return response_text
            
        except Exception as e:
            return f"Error: {str(e)}"

def main():
    chatbot = Chatbot()
    
    print("🤖 Stateful Chatbot with Auto-Persistence")
    print("Commands: 'set_user <id>', 'update_profile name=<name>', 'quit'")
    print("-" * 60)
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Goodbye!")
            break
        
        # Handle commands
        if user_input.startswith('set_user '):
            user_id = user_input.split(' ', 1)[1]
            chatbot.set_user(user_id)
            continue
        
        elif user_input.startswith('update_profile '):
            params = user_input.split(' ', 1)[1]
            kwargs = {}
            for param in params.split(','):
                if '=' in param:
                    key, value = param.strip().split('=', 1)
                    kwargs[key] = value
            chatbot.update_profile(**kwargs)
            continue
        
        # Regular chat
        response = chatbot.chat(user_input)
        print(f"Bot: {response}")

if __name__ == "__main__":
    main()
