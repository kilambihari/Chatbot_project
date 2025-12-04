from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Create chat once
chat = client.chats.create(model="gemini-2.5-flash")

# Send user message — no need to manually build full history
resp = chat.send_message("What is India?")
print("Bot:", resp.text)
