import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# --- DARK MODE TOGGLE ---
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

def toggle_dark_mode():
    st.session_state.dark_mode = not st.session_state.dark_mode

# Apply dark mode styling
if st.session_state.dark_mode:
    st.markdown("""
        <style>
        body, .stApp {
            background-color: #0d1117 !important;
        }
        .bubble-user {
            background-color: #0b8043;
            color: white;
            padding: 10px 15px;
            border-radius: 10px;
            margin: 5px;
            width: fit-content;
            margin-left: auto;
        }
        .bubble-bot {
            background-color: #30363d;
            color: #fff;
            padding: 10px 15px;
            border-radius: 10px;
            margin: 5px;
            width: fit-content;
            margin-right: auto;
        }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        .bubble-user {
            background-color: #dcf8c6;
            padding: 10px 15px;
            border-radius: 10px;
            margin: 5px;
            width: fit-content;
            margin-left: auto;
        }
        .bubble-bot {
            background-color: #ececec;
            padding: 10px 15px;
            border-radius: 10px;
            margin: 5px;
            width: fit-content;
            margin-right: auto;
        }
        </style>
    """, unsafe_allow_html=True)

# --- CHAT SESSION ---
if "gemini_chat" not in st.session_state:
    st.session_state.gemini_chat = client.chats.create(model="gemini-2.5-flash")

if "history" not in st.session_state:
    st.session_state.history = []

# --- UI ---
st.title("🤖 Gemini Chatbot")

# Dark mode button
st.button("🌓 Toggle Dark Mode", on_click=toggle_dark_mode)

# User input
user_input = st.text_input("You:")

if user_input:
    resp = st.session_state.gemini_chat.send_message(user_input)
    st.session_state.history.append({"user": user_input, "bot": resp.text})

# --- Display chat history with WhatsApp-style bubbles ---
st.markdown("### Chat History")
for chat in st.session_state.history:
    st.markdown(f"<div class='bubble-user'>🙋‍♂️ {chat['user']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='bubble-bot'>🤖 {chat['bot']}</div>", unsafe_allow_html=True)


