import streamlit as st
import json
from datetime import datetime
from typing import Dict, Any

def render_sidebar():
    """Render the sidebar with configuration and info"""
    with st.sidebar:
        st.header("⚙️ Configuration")

        st.markdown("---")

        st.header("📚 Quick Links")
        st.markdown("""
        **Unity:**
        - [XR Toolkit Docs](https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit@2.5/manual/)
        - [Unity VR Best Practices](https://docs.unity3d.com/Manual/VROverview.html)

        **Unreal:**
        - [UE5 VR Development](https://docs.unrealengine.com/5.3/en-US/vr-development-in-unreal-engine/)
        - [UE5 AR Development](https://docs.unrealengine.com/5.3/en-US/ar-development-in-unreal-engine/)

        **General:**
        - [WebXR Standards](https://immersiveweb.dev/)
        - [OpenXR Specification](https://www.khronos.org/openxr/)
        """)

        st.markdown("---")

        st.header("🚀 Setup Guide")
        with st.expander("How to set up CodeXR"):
            st.markdown("""
            **Option 1: Ollama (Recommended)**
            1. Download from [ollama.ai](https://ollama.ai)
            2. Run: `ollama pull codellama:7b-code`
            3. Select "Ollama (Local)" above

            **Option 2: Hugging Face**
            1. Create account at [huggingface.co](https://huggingface.co)
            2. Get free API token
            3. Select "Hugging Face (Online)"

            **Option 3: Demo Mode**
            - Works immediately with sample responses
            - Perfect for testing the UI
            """)

        st.markdown("---")
        st.caption("CodeXR v1.0 - Built with ❤️ for AR/VR developers")

def render_response(response: Dict[Any, Any], query: str):
    """Render the structured response from the LLM"""

    st.success("✅ Solution Generated!")

    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["📋 Solution", "💻 Code", "📄 Raw JSON"])

    with tab1:
        render_solution_tab(response, query)

    with tab2:
        render_code_tab(response)

    with tab3:
        render_json_tab(response)

def render_solution_tab(response: Dict[Any, Any], query: str):
    """Render the main solution tab"""

    # Header
    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader(f"Solution for: {query}")

    with col2:
        difficulty = response.get('difficulty', 'Medium')
        difficulty_colors = {
            'Easy': '🟢',
            'Medium': '🟡',
            'Hard': '🔴'
        }

        color = difficulty_colors.get(difficulty, '🟡')
        st.metric("Difficulty", f"{color} {difficulty}")

    # Estimated time
    estimated_time = response.get('estimated_time', 'Unknown')
    st.info(f"⏱️ **Estimated Time:** {estimated_time}")

    # Subtasks
    st.subheader("📝 Step-by-Step Guide")
    subtasks = response.get('subtasks', [])

    for i, subtask in enumerate(subtasks, 1):
        with st.container():
            st.markdown(f"""
            <div class="subtask">
                <strong>Step {i}:</strong> {subtask}
            </div>
            """, unsafe_allow_html=True)

    # Best Practices
    best_practices = response.get('best_practices', [])
    if best_practices:
        st.subheader("💡 Best Practices & Tips")
        for practice in best_practices:
            st.info(f"💡 {practice}")

    # Documentation Links
    doc_links = response.get('documentation_links', [])
    if doc_links:
        st.subheader("📖 Documentation Links")
        for link in doc_links:
            if link.startswith('http'):
                st.markdown(f"- [{link}]({link})")
            else:
                st.markdown(f"- {link}")

def render_code_tab(response: Dict[Any, Any]):
    """Render the code snippet tab"""

    code_snippet = response.get('code_snippet', '// No code snippet available')

    st.subheader("💻 Ready-to-Use Code")

    # Determine language for syntax highlighting
    language = determine_code_language(code_snippet)

    st.code(code_snippet, language=language)

    # Copy button (simulated)
    if st.button("📋 Copy Code", use_container_width=True):
        st.success("Code copied to clipboard! (In a real app, this would work)")

def render_json_tab(response: Dict[Any, Any]):
    """Render the raw JSON response tab"""

    st.subheader("📄 Raw JSON Response")
    st.caption("This structured format can be used for further processing or integration")

    # Pretty print JSON
    json_str = json.dumps(response, indent=2)
    st.code(json_str, language='json')

def determine_code_language(code: str) -> str:
    """Determine programming language for syntax highlighting"""
    code_lower = code.lower()

    if any(keyword in code_lower for keyword in ['using unityengine', 'monobehaviour', 'gameobject']):
        return 'csharp'
    elif any(keyword in code_lower for keyword in ['#include', 'uclass', 'uproperty']):
        return 'cpp'
    elif any(keyword in code_lower for keyword in ['shader', 'hlsl', 'vertex', 'fragment']):
        return 'hlsl'
    elif 'javascript' in code_lower or 'js' in code_lower:
        return 'javascript'
    elif 'python' in code_lower:
        return 'python'
    else:
        return 'text'
