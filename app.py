import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

# ---------------------------------------
# DARK MODE CONFIG
# ---------------------------------------
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# Apply theme CSS
def apply_theme():
    if st.session_state.dark_mode:
        st.markdown(
            """
            <style>

            /* Page background */
            body, .stApp {
                background-color: #0d0d0d !important;
                color: #ffffff !important;
            }

            /* Input box text */
            input[type="text"] {
                color: #ffffff !important;
            }

            /* Chat bubbles */
            .user-bubble {
                background-color: #005c4b;
                color: white;
                padding: 10px;
                margin: 5px;
                border-radius: 12px;
                width: fit-content;
                max-width: 80%;
            }

            .bot-bubble {
                background-color: #262d31;
                color: white;
                padding: 10px;
                margin: 5px;
                border-radius: 12px;
                width: fit-content;
                max-width: 80%;
            }

            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <style>

            /* Light mode background */
            body, .stApp {
                background-color: #ffffff !important;
                color: #000000 !important;
            }

            /* Input box text */
            input[type="text"] {
                color: #000000 !important;
            }

            /* Chat bubbles */
            .user-bubble {
                background-color: #dcf8c6;
                color: black;
                padding: 10px;
                margin: 5px;
                border-radius: 12px;
                width: fit-content;
                max-width: 80%;
            }

            .bot-bubble {
                background-color: #f1f0f0;
                color: black;
                padding: 10px;
                margin: 5px;
                border-radius: 12px;
                width: fit-content;
                max-width: 80%;
            }

            </style>
            """,
            unsafe_allow_html=True
        )


apply_theme()


# ---------------------------------------
# GEMINI CLIENT + CHAT SESSION
# ---------------------------------------
if "client" not in st.session_state:
    st.session_state.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

if "chat" not in st.session_state:
    st.session_state.chat = st.session_state.client.chats.create(model="gemini-2.5-flash")

if "history" not in st.session_state:
    st.session_state.history = []


# ---------------------------------------
# HEADER + BUTTONS
# ---------------------------------------
st.title("🤖 Gemini Chatbot")

col1, col2 = st.columns(2)

with col1:
    if st.button("🌓 Toggle Dark Mode"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

with col2:
    if st.button("🗑️ Clear Chat History"):
        st.session_state.history = []
        st.session_state.chat = st.session_state.client.chats.create(model="gemini-2.5-flash")
        st.success("Chat history cleared!")


# ---------------------------------------
# USER INPUT
# ---------------------------------------
user_input = st.text_input("You:")

if user_input:
    try:
        resp = st.session_state.chat.send_message(user_input)
        bot_msg = resp.text

        st.session_state.history.append({"user": user_input, "bot": bot_msg})

    except Exception as e:
        st.error(f"Error: {str(e)}")


# ---------------------------------------
# DISPLAY CHAT HISTORY (WhatsApp Style)
# ---------------------------------------
for msg in st.session_state.history:
    st.markdown(f"<div class='user-bubble'>👤 {msg['user']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='bot-bubble'>🤖 {msg['bot']}</div>", unsafe_allow_html=True)
