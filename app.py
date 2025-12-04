import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

# Load env
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# -------------------------
# SESSION STATES
# -------------------------
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

if "history" not in st.session_state:
    st.session_state.history = []

if "gemini_chat" not in st.session_state:
    st.session_state.gemini_chat = client.chats.create(model="gemini-2.5-flash")

# -------------------------
# FUNCTIONS
# -------------------------
def toggle_dark_mode():
    st.session_state.dark_mode = not st.session_state.dark_mode

def clear_history():
    st.session_state.history = []

# -------------------------
# STYLING
# -------------------------
if st.session_state.dark_mode:
    st.markdown("""
        <style>
        body, .stApp {
            background-color: #0d1117 !important;
            color: white !important;
        }

        /* Make text glow */
        .glow-text {
            color: #ffffff !important;
            text-shadow: 0 0 8px #00eaff, 0 0 12px #00eaff;
        }

        /* User bubble */
        .bubble-user {
            background-color: #0b8043;
            color: white !important;
            padding: 12px 16px;
            border-radius: 12px;
            margin: 8px;
            width: fit-content;
            margin-left: auto;
            font-size: 16px;
            text-shadow: 0 0 5px black;
        }

        /* Bot bubble */
        .bubble-bot {
            background-color: #30363d;
            color: #e5e5e5 !important;
            padding: 12px 16px;
            border-radius: 12px;
            margin: 8px;
            width: fit-content;
            margin-right: auto;
            font-size: 16px;
            text-shadow: 0 0 6px #00eaff;
        }

        input {
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
        <style>
        .bubble-user {
            background-color: #dcf8c6;
            padding: 12px 16px;
            border-radius: 12px;
            margin: 8px;
            width: fit-content;
            margin-left: auto;
            font-size: 16px;
        }
        .bubble-bot {
            background-color: #ececec;
            padding: 12px 16px;
            border-radius: 12px;
            margin: 8px;
            width: fit-content;
            margin-right: auto;
            font-size: 16px;
        }
        </style>
    """, unsafe_allow_html=True)

# -------------------------
# UI
# -------------------------
st.title("🤖 Gemini Chatbot")

col1, col2 = st.columns(2)
with col1:
    st.button("🌓 Toggle Dark Mode", on_click=toggle_dark_mode)
with col2:
    st.button("🗑️ Clear Chat", on_click=clear_history)

user_input = st.text_input("You:", key="input_box")

if user_input:
    resp = st.session_state.gemini_chat.send_message(user_input)
    st.session_state.history.append({"user": user_input, "bot": resp.text})

# -------------------------
# CHAT HISTORY
# -------------------------
st.markdown("### <span class='glow-text'>Chat History</span>", unsafe_allow_html=True)

for chat in st.session_state.history:
    st.markdown(f"<div class='bubble-user'>🙋‍♂️ {chat['user']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='bubble-bot'>🤖 {chat['bot']}</div>", unsafe_allow_html=True)




