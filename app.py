import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

# Load env vars
load_dotenv()

# Page title
st.title("🤖 Gemini Chatbot")

# -------------------------
# Session State
# -------------------------
if "history" not in st.session_state:
    st.session_state.history = []     # Store chat messages only

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False


# -------------------------
# Function to generate response
# -------------------------
def generate_gemini_response(prompt):

    # Recreate fresh client each time
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    # Convert history to Gemini input format
    messages = []
    for h in st.session_state.history:
        messages.append({"role": "user", "content": h["user"]})
        messages.append({"role": "model", "content": h["bot"]})

    # Append new user message
    messages.append({"role": "user", "content": prompt})

    # Generate response
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages
    )

    return response.text


# -------------------------
# Buttons
# -------------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("🌓 Toggle Dark Mode"):
        st.session_state.dark_mode = not st.session_state.dark_mode

with col2:
    if st.button("🗑️ Clear History"):
        st.session_state.history = []


# -------------------------
# User Input
# -------------------------
user_input = st.text_input("You:")

if user_input:
    bot_reply = generate_gemini_response(user_input)

    # Save to history
    st.session_state.history.append({
        "user": user_input,
        "bot": bot_reply
    })


# -------------------------
# Display Chat History
# -------------------------
st.markdown("### Chat History")

for chat in st.session_state.history:
    st.markdown(f"**You:** {chat['user']}")
    st.markdown(f"**Bot:** {chat['bot']}")
