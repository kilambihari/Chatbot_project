import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

# Create Gemini client once
if "client" not in st.session_state:
    st.session_state.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Create chat session once
if "chat" not in st.session_state:
    st.session_state.chat = st.session_state.client.chats.create(model="gemini-2.5-flash")

# Store conversation history
if "history" not in st.session_state:
    st.session_state.history = []

# Default theme
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False


# --------------------------
# 👉 DARK MODE TOGGLE
# --------------------------
def toggle_dark_mode():
    st.session_state.dark_mode = not st.session_state.dark_mode

st.checkbox("🌙 Dark Mode", value=st.session_state.dark_mode, on_change=toggle_dark_mode)


# --------------------------
# 👉 APPLY THEME (CSS)
# --------------------------
if st.session_state.dark_mode:
    st.markdown(
        """
        <style>
        body { background-color: #0d1117 !important; color: white !important; }

        /* Input box fix */
        input[type="text"] {
            background-color: #1f2937 !important;
            color: #ffffff !important;
            border: 1px solid #555 !important;
        }

        .stTextInput label {
            color: white !important;
            font-weight: 600;
        }

        /* WhatsApp Bubbles */
        .user-bubble {
            background: #005c4b;
            color: white;
            padding: 10px 14px;
            border-radius: 14px;
            max-width: 70%;
            margin-left: auto;
            margin-bottom: 8px;
        }
        .bot-bubble {
            background: #202c33;
            color: white;
            padding: 10px 14px;
            border-radius: 14px;
            max-width: 70%;
            margin-right: auto;
            margin-bottom: 8px;
        }
        </style>
        """, unsafe_allow_html=True)
else:
    st.markdown(
        """
        <style>
        /* Light mode bubbles */
        .user-bubble {
            background: #d1f4e4;
            color: black;
            padding: 10px 14px;
            border-radius: 14px;
            max-width: 70%;
            margin-left: auto;
            margin-bottom: 8px;
        }
        .bot-bubble {
            background: #f0f0f0;
            color: black;
            padding: 10px 14px;
            border-radius: 14px;
            max-width: 70%;
            margin-right: auto;
            margin-bottom: 8px;
        }

        input[type="text"] {
            color: black !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


st.title("🤖 Gemini Chatbot")


# --------------------------
# 👉 CLEAR HISTORY BUTTON
# --------------------------
if st.button("🗑️ Clear Chat History"):
    st.session_state.history = []
    st.session_state.chat = st.session_state.client.chats.create(model="gemini-2.5-flash")
    st.success("Chat history cleared!")


# --------------------------
# 👉 USER INPUT
# --------------------------
user_input = st.text_input("You:", key="input_box")

if user_input:
    try:
        resp = st.session_state.chat.send_message(user_input)
        bot_msg = resp.text

        st.session_state.history.append({"user": user_input, "bot": bot_msg})

        # Clear input box after sending
        st.session_state.input_box = ""

    except Exception as e:
        st.error(f"Error: {str(e)}")


# --------------------------
# 👉 DISPLAY CHAT HISTORY
# --------------------------
for chat in st.session_state.history:
    st.markdown(f"<div class='user-bubble'>{chat['user']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='bot-bubble'>{chat['bot']}</div>", unsafe_allow_html=True)
