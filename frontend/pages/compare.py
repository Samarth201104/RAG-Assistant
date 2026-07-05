"""
Compare Page
Premium document comparison interface
"""

import streamlit as st
from typing import Dict, List
from components.header import render_page_title
from components.loading import render_loading_state
from services.api_client import api_client
from utils.session import set_error
from utils.helpers import truncate_text


def compare_page() -> None:
    """Render the document comparison page."""
    render_page_title("Document Comparison", "⚖️")
    
    # Get documents
    documents = api_client.list_documents("research_documents")
    
    if not documents or len(documents) < 2:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">📚</div>
            <h3>Need at least 2 documents to compare</h3>
            <p>Upload more documents to use the comparison feature</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Document selection
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📄 Document A")
        doc_a = select_document(documents, "a")
    
    with col2:
        st.markdown("### 📄 Document B")
        doc_b = select_document(documents, "b")
    
    # Compare button
    if st.button("🔍 Compare Documents", type="primary", use_container_width=True):
        if doc_a and doc_b:
            if doc_a == doc_b:
                st.warning("Please select different documents to compare")
                return
            handle_compare([doc_a, doc_b])
        else:
            st.warning("Please select both documents")


def select_document(documents: List[Dict], key: str) -> str:
    """
    Render document selection dropdown.
    
    Args:
        documents: List of document dictionaries
        key: Unique key for this selector
        
    Returns:
        Selected document ID
    """
    doc_options = {doc["id"]: doc["filename"] for doc in documents}
    selected = st.selectbox(
        "Select document",
        options=list(doc_options.keys()),
        format_func=lambda x: truncate_text(doc_options[x], 40),
        key=f"doc_{key}",
    )
    
    # Show document preview
    if selected:
        doc = next((d for d in documents if d["id"] == selected), None)
        if doc:
            st.markdown(f"""
            <div style="
                padding: var(--space-md);
                background: var(--bg-secondary);
                border-radius: var(--radius-md);
                border-left: 3px solid var(--accent-blue);
                font-size: var(--text-sm);
                color: var(--text-secondary);
            ">
                <strong>Size:</strong> {doc.get('size', 0) / 1024:.1f} KB<br>
                <strong>Uploaded:</strong> {doc.get('uploaded_at', 'N/A')[:10]}
            </div>
            """, unsafe_allow_html=True)
    
    return selected


def handle_compare(document_ids: List[str]) -> None:
    """
    Handle document comparison.
    
    Args:
        document_ids: List of two document IDs
    """
    with st.spinner(""):
        render_loading_state("comparing")
    
    response = api_client.compare_documents(document_ids)
    
    if response:
        render_comparison_results(response)
    else:
        set_error("Failed to compare documents")


def render_comparison_results(comparison: Dict) -> None:
    """
    Render comparison results.
    
    Args:
        comparison: Comparison data dictionary
    """
    st.markdown("## 📊 Comparison Results")
    
    # Similarity score
    similarity = comparison.get("similarity_score", 0)
    similarity_pct = f"{similarity:.1%}"
    
    st.markdown(f"""
    <div style="text-align: center; margin: var(--space-xl) 0;">
        <div style="font-size: var(--text-lg); color: var(--text-secondary); margin-bottom: var(--space-sm);">
            Similarity Score
        </div>
        <div style="font-size: var(--text-4xl); font-weight: 700; 
                    background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            {similarity_pct}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Two-column comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📄 Document A")
        render_comparison_panel(comparison.get("doc_a", {}), "a")
    
    with col2:
        st.markdown("### 📄 Document B")
        render_comparison_panel(comparison.get("doc_b", {}), "b")
    
    # Differences section
    st.markdown("---")
    st.markdown("### 🔍 Key Differences")
    
    differences = comparison.get("differences", [])
    if differences:
        for i, diff in enumerate(differences, 1):
            st.markdown(f"""
            <div style="
                padding: var(--space-md);
                background: var(--bg-secondary);
                border-radius: var(--radius-md);
                border-left: 4px solid var(--accent-purple);
                margin-bottom: var(--space-sm);
            ">
                <strong>Difference {i}:</strong> {diff}
            </div>
            """, unsafe_allow_html=True)
    
    # Conclusion
    if comparison.get("conclusion"):
        st.markdown("---")
        st.markdown("### 💡 Conclusion")
        st.markdown(f"""
        <div style="
            padding: var(--space-lg);
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(139, 92, 246, 0.1));
            border: 1px solid var(--border-accent);
            border-radius: var(--radius-lg);
        ">
            {comparison['conclusion']}
        </div>
        """, unsafe_allow_html=True)


def render_comparison_panel(doc_data: Dict, key: str) -> None:
    """
    Render a single document comparison panel.
    
    Args:
        doc_data: Document comparison data
        key: Unique key for this panel
    """
    # Pros
    st.markdown("**✅ Strengths**")
    for pro in doc_data.get("pros", []):
        st.markdown(f"- {pro}")
    
    # Cons
    st.markdown("**⚠️ Limitations**")
    for con in doc_data.get("cons", []):
        st.markdown(f"- {con}")
    
    # Topics
    st.markdown("**🏷️ Key Topics**")
    topics = doc_data.get("topics", [])
    if topics:
        topic_html = " ".join([
            f'<span style="padding: 2px 10px; background: var(--bg-tertiary); '
            f'border-radius: var(--radius-full); font-size: var(--text-xs); '
            f'color: var(--text-secondary); border: 1px solid var(--border-primary);">'
            f'{topic}</span>'
            for topic in topics
        ])
        st.markdown(topic_html, unsafe_allow_html=True)