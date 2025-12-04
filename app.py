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

st.title("🤖 Gemini Chatbot")


# --------------------------
# 👉 CLEAR HISTORY BUTTON
# --------------------------
if st.button("🗑️ Clear Chat History"):
    st.session_state.history = []              # clear history
    st.session_state.chat = st.session_state.client.chats.create(model="gemini-2.5-flash")  # new chat
    st.success("Chat history cleared!")


# --------------------------
# 👉 USER INPUT
# --------------------------
user_input = st.text_input("You:")

if user_input:
    try:
        resp = st.session_state.chat.send_message(user_input)
        bot_msg = resp.text

        # Save in history
        st.session_state.history.append(
            {"user": user_input, "bot": bot_msg}
        )

    except Exception as e:
        st.error(f"Error: {str(e)}")


# --------------------------
# 👉 DISPLAY HISTORY
# --------------------------
for chat in st.session_state.history:
    st.markdown(f"**You:** {chat['user']}")
    st.markdown(f"**Bot:** {chat['bot']}")
    st.markdown("---")
