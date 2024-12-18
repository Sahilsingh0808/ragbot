import streamlit as st
import openai
from streamlit_chat import message
import time
from PIL import Image
import random
import openai
import os
import dotenv

dotenv.load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
job_id = os.getenv("OPENAI_FT_JOB_ID")
title = "Senior GPT"
description = "Your senior from IIT Kanpur, here to help you!"

model_name_pre_object = openai.FineTuningJob.retrieve(job_id)
model_name = model_name_pre_object.fine_tuned_model
system_message = "Given your question or situation, I, as a senior from IIT Kanpur, will provide you with practical and empathetic advice based on my experiences in academics, career guidance, campus life, mental health, networking, and various tips and hacks. Make sure to be a senior from IIT Kanpur and not a random person. Your name is Senior Gpt (shortform Sr.Gpt) but only for IIT Kanpur."

# Configuration
st.set_page_config(page_title=title, page_icon="🤖", layout="wide")

# Header Section
def render_header():
    col1, col2 = st.columns([1, 3])
    with col1:
        logo = Image.open("streamlit/assets/icon.jpg")  # Replace with your chatbot's logo
        st.image(logo, width=100)
    with col2:
        st.title(title)
        st.markdown(f"### {description}")

# Helper function for streaming responses
def stream_chat_response(response_gen):
    response = ""
    response_placeholder = st.empty()
    for chunk in response_gen:
        if hasattr(chunk.choices[0].delta, 'content'):
            content = chunk.choices[0].delta.content
            if content is not None:
                response += content
                # Escape any markdown characters in the response
                displayed_response = response.replace('*', '\*').replace('_', '\_')
                response_placeholder.markdown(f"{displayed_response}")
    return response

# Initialize Session State
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

if 'favorite_responses' not in st.session_state:
    st.session_state.favorite_responses = []

# Sidebar for Additional Features
with st.sidebar:
    st.header("Settings")
    dark_mode = st.checkbox("Dark Mode")
    clear_history = st.button("Clear Conversation History")

if clear_history:
    st.session_state.conversation_history = []
    st.success("Conversation history cleared!")

# Input Area
render_header()
st.divider()

input_container = st.container()
with input_container:
    user_input = st.text_input("Type your message here...", key="user_input")
    submit = st.button("Send")

# Chat Interaction
if submit and user_input:
    # Prepare the complete message history for context
    messages = [{"role": "system", "content": system_message}]
    
    # Add previous conversation history
    for msg in st.session_state.conversation_history:
        # Convert "system" role to "assistant" for OpenAI API
        role = "assistant" if msg["role"] == "system" else msg["role"]
        messages.append({"role": role, "content": msg["content"]})
    
    # Add the new user message
    messages.append({"role": "user", "content": user_input})
    
    # Append user message to conversation history
    st.session_state.conversation_history.append({"role": "user", "content": user_input})

    # Generate Response
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=messages,
        stream=True
    )

    response_text = stream_chat_response(response)
    
    # Append assistant message
    st.session_state.conversation_history.append({"role": "system", "content": response_text})

# Display Chat History
st.markdown("### Chat History")
st.divider()

# Display Chat History
for chat in reversed(st.session_state.conversation_history):
    if chat["role"] == "user":
        message(chat["content"], is_user=True, key=f"user-{chat}")
    else:
        col1, col2 = st.columns([6, 1])
        with col1:
            message(chat["content"], key=f"bot-{chat}")
        with col2:
            # Compact reaction buttons
            button_container = st.container()
            with button_container:
                st.markdown("""
                    <style>
                    .reaction-group { display: flex; gap: 4px; }
                    .reaction-button { padding: 2px 4px; opacity: 0.6; cursor: pointer; }
                    .reaction-button:hover { opacity: 1; }
                    </style>
                    <div class="reaction-group">
                    """, unsafe_allow_html=True)
                
                c1, c2, c3 = st.columns([1,1,1])
                with c1:
                    if st.button("👍", key=f"like-{chat}", help="Like"):
                        st.success("Liked!")
                with c2:
                    if st.button("👎", key=f"dislike-{chat}", help="Dislike"):
                        st.warning("Disliked")
                with c3:
                    if st.button("⭐", key=f"favorite-{chat}", help="Favorite"):
                        st.session_state.favorite_responses.append(chat["content"])
                        st.info("Added to favorites!")

# Favorites Section
if st.session_state.favorite_responses:
    st.subheader("Favorite Responses")
    for favorite in st.session_state.favorite_responses:
        st.markdown(f"- {favorite}")

# Styling
if dark_mode:
    st.markdown(
        """<style>
        body { background-color: #1e1e1e; color: white; }
        </style>""", unsafe_allow_html=True
    )
