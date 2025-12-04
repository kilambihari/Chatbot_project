import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    st.error("Set GEMINI_API_KEY in .env")
    st.stop()

client = genai.Client(api_key=API_KEY)

# Initialize chat session (one per Streamlit session)
if "chat_obj" not in st.session_state:
    st.session_state.chat_obj = client.chats.create(model="gemini-2.5-flash")

st.title("🤖 Gemini Chatbot")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("You:")

if user_input:
    chat = st.session_state.chat_obj
    try:
        resp = chat.send_message(user_input)
        bot_reply = resp.text
    except Exception as e:
        bot_reply = f"Error: {e}"

    st.session_state.history.append({"user": user_input, "bot": bot_reply})

for turn in st.session_state.history:
    st.markdown(f"**You:** {turn['user']}")
    st.markdown(f"**Bot:** {turn['bot']}")
