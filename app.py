import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Set page title and layout
st.set_page_config(page_title="Startup Chatbot", layout="centered")

# Inject custom CSS
st.markdown("""
    <style>
    h1 { text-align: center; color: #000000; }
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    .user-bubble, .bot-bubble {
        padding: 12px 18px;
        border-radius: 18px;
        max-width: 80%;
        word-wrap: break-word;
        font-size: 16px;
        line-height: 1.5;
        color: white;
    }
    .user-container {
        display: flex;
        justify-content: flex-end;
    }
    .user-bubble {
        background-color: #0078FF;
        text-align: right;
    }
    .bot-container {
        display: flex;
        justify-content: flex-start;
    }
    .bot-bubble {
        background-color: #2F2F2F;
        text-align: left;
    }
    </style>
""", unsafe_allow_html=True)

# App Title
st.title("Startup Chatbot")

# Load API key securely
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Initialize model and chat history
if "chat" not in st.session_state:
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    st.session_state.chat = model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display message bubbles
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'''
            <div class="chat-container">
                <div class="user-container">
                    <div class="user-bubble">{msg["text"]}</div>
                </div>
            </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown(f'''
            <div class="chat-container">
                <div class="bot-container">
                    <div class="bot-bubble">{msg["text"]}</div>
                </div>
            </div>
        ''', unsafe_allow_html=True)

# Chat input
prompt = st.chat_input("Say something...")
if prompt:
    st.session_state.messages.append({"role": "user", "text": prompt})

    with st.spinner("Model is thinking..."):
        response = st.session_state.chat.send_message(prompt)
        output = response.text
        st.session_state.messages.append({"role": "assistant", "text": output})

    st.rerun()
