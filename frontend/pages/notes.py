"""
Notes Page
Premium study notes generation and export
"""

import streamlit as st
from typing import Dict, List
from components.header import render_page_title
from components.loading import render_loading_state
from services.api_client import api_client
from utils.session import set_error, set_success
from utils.helpers import truncate_text
import base64


def notes_page() -> None:
    """Render the notes generation page."""
    render_page_title("Study Notes Generator", "📚")
    
    # Document selection
    documents = api_client.list_documents("research_documents")
    
    if not documents:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">📭</div>
            <h3>No Documents Available</h3>
            <p>Upload documents to generate study notes</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Selection interface
    st.markdown("### Select Documents for Notes")
    
    selected_ids = []
    cols = st.columns(2)
    
    for i, doc in enumerate(documents):
        with cols[i % 2]:
            if st.checkbox(
                doc.get("filename", "Unknown"),
                key=f"note_doc_{i}",
                value=True,
            ):
                selected_ids.append(doc.get("id"))
    
    # Notes type
    notes_type = st.selectbox(
        "Notes Format",
        ["study_notes", "bullet_points", "detailed_analysis", "flashcards"],
        format_func=lambda x: {
            "study_notes": "📝 Study Notes",
            "bullet_points": "🔹 Bullet Points",
            "detailed_analysis": "📊 Detailed Analysis",
            "flashcards": "🃏 Flashcards",
        }.get(x, x),
    )
    
    # Generate button
    if st.button("🎓 Generate Notes", type="primary", use_container_width=True):
        if not selected_ids:
            st.warning("Please select at least one document")
            return
        
        handle_generate_notes(selected_ids, notes_type)


def handle_generate_notes(document_ids: List[str], notes_type: str) -> None:
    """
    Handle notes generation.
    
    Args:
        document_ids: List of document IDs
        notes_type: Type of notes to generate
    """
    with st.spinner(""):
        render_loading_state("notes")
    
    response = api_client.generate_notes(document_ids, notes_type)
    
    if response:
        render_notes_results(response, notes_type)
    else:
        set_error("Failed to generate notes")


def render_notes_results(notes_data: Dict, notes_type: str) -> None:
    """
    Render generated notes with export options.
    
    Args:
        notes_data: Notes data dictionary
        notes_type: Type of notes generated
    """
    st.markdown("## 📚 Generated Notes")
    
    # Notes content
    content = notes_data.get("content", "")
    
    # Render in markdown container
    st.markdown(f"""
    <div class="markdown-content">
        {content}
    </div>
    
    <style>
        .markdown-content {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-primary);
            border-radius: var(--radius-lg);
            padding: var(--space-xl);
            line-height: 1.8;
        }}
        
        .markdown-content h1 {{ 
            font-size: var(--text-3xl);
            color: var(--text-primary);
            border-bottom: 2px solid var(--border-accent);
            padding-bottom: var(--space-sm);
        }}
        
        .markdown-content h2 {{
            font-size: var(--text-2xl);
            color: var(--text-primary);
        }}
        
        .markdown-content h3 {{
            font-size: var(--text-xl);
            color: var(--accent-blue);
        }}
        
        .markdown-content ul, .markdown-content ol {{
            padding-left: var(--space-xl);
        }}
        
        .markdown-content blockquote {{
            border-left: 4px solid var(--accent-purple);
            padding-left: var(--space-md);
            color: var(--text-secondary);
            font-style: italic;
            background: var(--bg-tertiary);
            padding: var(--space-md);
            border-radius: var(--radius-sm);
        }}
        
        .markdown-content code {{
            background: var(--bg-primary);
            padding: 2px 6px;
            border-radius: var(--radius-sm);
            font-family: var(--font-mono);
            font-size: var(--text-sm);
        }}
        
        .markdown-content pre {{
            background: var(--bg-primary);
            padding: var(--space-md);
            border-radius: var(--radius-md);
            overflow-x: auto;
            border: 1px solid var(--border-primary);
        }}
        
        .markdown-content table {{
            width: 100%;
            border-collapse: collapse;
            margin: var(--space-md) 0;
        }}
        
        .markdown-content th {{
            background: var(--bg-tertiary);
            padding: var(--space-sm) var(--space-md);
            text-align: left;
            font-weight: 600;
            border-bottom: 2px solid var(--border-primary);
        }}
        
        .markdown-content td {{
            padding: var(--space-sm) var(--space-md);
            border-bottom: 1px solid var(--border-primary);
        }}
    </style>
    """, unsafe_allow_html=True)
    
    # Export section
    st.markdown("---")
    st.markdown("### 📥 Export Options")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📋 Copy", use_container_width=True):
            st.success("Notes copied to clipboard!")
    
    with col2:
        st.download_button(
            "📝 Markdown",
            data=content,
            file_name="study_notes.md",
            mime="text/markdown",
            use_container_width=True,
        )
    
    with col3:
        if st.button("📄 PDF", use_container_width=True):
            handle_export(content, "pdf")
    
    with col4:
        if st.button("📘 DOCX", use_container_width=True):
            handle_export(content, "docx")


def handle_export(content: str, format_type: str) -> None:
    """
    Handle notes export.
    
    Args:
        content: Notes content
        format_type: Export format
    """
    result = api_client.export_notes(content, format_type)
    
    if result:
        set_success(f"Notes exported as {format_type.upper()}")
        # Trigger download (implement based on response)
    else:
        set_error(f"Failed to export as {format_type.upper()}")