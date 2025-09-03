import streamlit as st
import json
from datetime import datetime
import sys
import os

# Add the core module to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.llm_handler import LLMHandler
from core.search_agent import SearchAgent
from core.classifier import QueryClassifier
from ui.components import render_response, render_sidebar

# Page config
st.set_page_config(
    page_title="CodeXR - AR/VR Coding Assistant",
    page_icon="🥽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .subtask {
        background-color: #f0f2f6;
        padding: 0.8rem;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
        border-radius: 4px;
        color: #1f2937 !important;  /* Force dark text */
    }
    .difficulty-easy { color: #28a745 !important; }
    .difficulty-medium { color: #ffc107 !important; }
    .difficulty-hard { color: #dc3545 !important; }

    /* Fix white text issues */
    .stMarkdown p {
        color: #1f2937 !important;
    }

    /* Ensure step text is visible */
    .subtask strong {
        color: #1f2937 !important;
    }

    /* Fix any remaining white text */
    div[data-testid="stMarkdownContainer"] p {
        color: #1f2937 !important;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'llm_handler' not in st.session_state:
        st.session_state.llm_handler = LLMHandler()
    if 'search_agent' not in st.session_state:
        st.session_state.search_agent = SearchAgent()
    if 'classifier' not in st.session_state:
        st.session_state.classifier = QueryClassifier()
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

def main():
    initialize_session_state()

    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🥽 CodeXR - AR/VR Coding Assistant</h1>
        <p>Your AI-powered companion for Unity, Unreal Engine, and Shader development</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar
    render_sidebar()

    # Main interface
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("What would you like to build?")

        # Query input
        query = st.text_area(
            "Describe your AR/VR development task:",
            height=100,
            placeholder="e.g., How do I add teleport locomotion in Unity VR?"
        )

        # Demo buttons
        st.subheader("🎯 Try Demo Scenarios")
        col_demo1, col_demo2, col_demo3 = st.columns(3)

        with col_demo1:
            if st.button("Unity VR Teleport", use_container_width=True):
                query = "How do I add teleport locomotion in Unity VR?"

        with col_demo2:
            if st.button("Unreal Multiplayer", use_container_width=True):
                query = "How do I set up multiplayer in Unreal VR?"

        with col_demo3:
            if st.button("AR Occlusion Shader", use_container_width=True):
                query = "Which shader works best for AR occlusion?"

        # Process query
        if st.button("🚀 Generate Solution", type="primary", use_container_width=True):
            if query.strip():
                process_query(query)
            else:
                st.warning("Please enter a query or try one of the demo scenarios!")

    with col2:
        st.subheader("📊 Query Info")
        if query:
            # Classify query
            category = st.session_state.classifier.classify(query)
            st.info(f"**Category:** {category}")

            difficulty = estimate_difficulty(query)
            difficulty_color = {
                "Easy": "difficulty-easy",
                "Medium": "difficulty-medium",
                "Hard": "difficulty-hard"
            }.get(difficulty, "")

            st.markdown(f'**Estimated Difficulty:** <span class="{difficulty_color}">{difficulty}</span>',
                       unsafe_allow_html=True)

def process_query(query):
    """Process the user query and generate response"""
    with st.spinner("🔍 Analyzing your query..."):
        try:
            # Step 1: Classify query
            category = st.session_state.classifier.classify(query)

            # Step 2: Search for relevant documentation
            st.info("🌐 Searching for relevant documentation...")
            search_results = st.session_state.search_agent.search(query, category)

            # Step 3: Generate structured response
            st.info("🤖 Generating structured solution...")
            response = st.session_state.llm_handler.generate_response(
                query, category, search_results
            )

            # Step 4: Render response
            if response:
                render_response(response, query)

                # Add to chat history
                st.session_state.chat_history.append({
                    'timestamp': datetime.now(),
                    'query': query,
                    'category': category,
                    'response': response
                })
            else:
                st.error("Sorry, I couldn't generate a response. Please try again!")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.info("This might be due to LLM setup. Check the sidebar for configuration options.")

def estimate_difficulty(query):
    """Simple difficulty estimation based on keywords"""
    easy_keywords = ['basic', 'simple', 'how to', 'tutorial', 'beginner']
    hard_keywords = ['multiplayer', 'networking', 'optimization', 'advanced', 'performance', 'complex']

    query_lower = query.lower()

    if any(keyword in query_lower for keyword in hard_keywords):
        return "Hard"
    elif any(keyword in query_lower for keyword in easy_keywords):
        return "Easy"
    else:
        return "Medium"

if __name__ == "__main__":
    main()
