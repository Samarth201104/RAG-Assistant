"""
Chat Page
Premium ChatGPT-like interface for document Q&A
"""

import streamlit as st
from typing import List, Dict, Optional
from datetime import datetime
from components.header import render_page_title
from components.chat_message import (
    render_chat_message,
    render_typing_indicator,
    render_empty_chat,
)
from services.api_client import api_client
from utils.session import (
    get_chat_history,
    add_chat_message,
    reset_chat_history,
    set_error,
)


def chat_page() -> None:
    """Render the chat interface page."""
    render_page_title("Research Chat", "💬")
    
    # Chat container
    chat_container = st.container()
    
    # Input area
    with st.container():
        render_chat_input()
    
    # Render chat history
    with chat_container:
        render_chat_history()
    
    # Sidebar options
    with st.sidebar:
        render_chat_options()


def render_chat_history() -> None:
    """Render the complete chat history."""
    chat_history = get_chat_history()
    
    if not chat_history:
        render_empty_chat()
        return
    
    for message in chat_history:
        role = message.get("role", "user")
        content = message.get("content", "")
        timestamp = message.get("timestamp", "")
        metadata = message.get("metadata", {})
        sources = metadata.get("sources", [])
        
        render_chat_message(
            role=role,
            content=content,
            timestamp=timestamp,
            metadata=metadata,
            sources=sources,
        )


def render_chat_input() -> None:
    """Render the chat input area."""
    # Style the input area
    st.markdown("""
    <style>
        .chat-input-container {
            position: fixed;
            bottom: 0;
            left: var(--sidebar-width);
            right: 0;
            background: linear-gradient(180deg, transparent, var(--bg-primary) 50%);
            padding: var(--space-lg) var(--space-xl) var(--space-xl);
            z-index: 100;
        }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([6, 1])
    
    with col1:
        user_input = st.text_area(
            "Ask a question about your documents...",
            placeholder="Ask anything about your research documents...",
            label_visibility="collapsed",
            key="chat_input",
            height=100,
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        send_button = st.button("📤 Send", use_container_width=True, type="primary")
        if st.button("🗑️ Clear", use_container_width=True):
            reset_chat_history()
            st.rerun()
    
    # Handle send
    if send_button and user_input.strip():
        handle_send_message(user_input.strip())


def handle_send_message(message: str) -> None:
    """
    Handle sending a chat message.
    
    Args:
        message: User message text
    """
    # Add user message
    add_chat_message("user", message)
    
    # Show typing indicator
    with st.chat_message("assistant"):
        render_typing_indicator()
    
    # Get AI response
    response = api_client.send_message(
        message=message,
        chat_history=get_chat_history()[:-1],  # Exclude current message
        temperature=st.session_state.get("temperature", 0.7),
        max_tokens=st.session_state.get("max_tokens", 2048),
    )
    
    if response:
        ai_content = response.get("response", "")
        sources = response.get("sources", [])
        
        add_chat_message(
            "assistant",
            ai_content,
            metadata={"sources": sources},
        )
    else:
        set_error("Failed to get response from AI")
    
    # Clear input and rerun
    st.session_state.chat_input = ""
    st.rerun()


def render_chat_options() -> None:
    """Render chat options in sidebar."""
    st.markdown("### ⚙️ Chat Settings")
    
    # Temperature
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.get("temperature", 0.7),
        step=0.1,
        help="Higher values make output more creative, lower values more focused",
    )
    st.session_state.temperature = temperature
    
    # Max tokens
    max_tokens = st.number_input(
        "Max Tokens",
        min_value=256,
        max_value=4096,
        value=st.session_state.get("max_tokens", 2048),
        step=256,
    )
    st.session_state.max_tokens = max_tokens
    
    st.markdown("---")
    
    # Chat history info
    chat_history = get_chat_history()
    st.markdown(f"**Messages:** {len(chat_history)}")
    
    if st.button("🧹 Clear Chat History", use_container_width=True):
        reset_chat_history()
        st.rerun()