from backend.app.services.chat_service import ask_chat
import sys
import os

# Add project root to path so imports work
sys.path.append(os.getcwd())

print("Testing Chat with Groq...")
try:
    response = ask_chat("Hola, cómo estás?")
    print(f"Success! Response: {response}")
except Exception as e:
    print(f"Error: {e}")
