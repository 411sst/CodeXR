import streamlit as st
import json
from datetime import datetime
import sys
import os

# Add the core module to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

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
        color: #1f2937 !important;
    }
    .subtask strong {
        color: #1f2937 !important;
    }
    .difficulty-easy { color: #28a745 !important; }
    .difficulty-medium { color: #ffc107 !important; }
    .difficulty-hard { color: #dc3545 !important; }

    /* Fix white text issues */
    .stMarkdown p {
        color: #1f2937 !important;
    }
    div[data-testid="stMarkdownContainer"] p {
        color: #1f2937 !important;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'search_agent' not in st.session_state:
        st.session_state.search_agent = SearchAgent()
    if 'classifier' not in st.session_state:
        st.session_state.classifier = QueryClassifier()
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Initialize LLM selection states
    if 'use_mock' not in st.session_state:
        st.session_state.use_mock = True
        st.session_state.use_ollama = False
        st.session_state.use_huggingface = False

def create_llm_sidebar():
    """Create stable LLM selection sidebar with checkboxes"""

    with st.sidebar:
        st.header("⚙️ LLM Configuration")

        st.subheader("Select AI Backend:")

        # Checkbox options
        use_mock = st.checkbox(
            "🎭 Mock (Demo Mode)",
            value=st.session_state.use_mock,
            help="Instant responses with pre-written examples"
        )

        use_ollama = st.checkbox(
            "🤖 Ollama (Local AI)",
            value=st.session_state.use_ollama,
            help="Real AI running locally on your machine"
        )

        use_hf = st.checkbox(
            "🌐 Hugging Face (Online)",
            value=st.session_state.use_huggingface,
            help="Online AI with free tier (limited)"
        )

        # Ensure only one is selected (radio button behavior)
        if use_mock and (st.session_state.use_ollama or st.session_state.use_huggingface):
            st.session_state.use_ollama = False
            st.session_state.use_huggingface = False
            st.rerun()

        if use_ollama and (st.session_state.use_mock or st.session_state.use_huggingface):
            st.session_state.use_mock = False
            st.session_state.use_huggingface = False
            st.rerun()

        if use_hf and (st.session_state.use_mock or st.session_state.use_ollama):
            st.session_state.use_mock = False
            st.session_state.use_ollama = False
            st.rerun()

        # If none selected, default to mock
        if not (use_mock or use_ollama or use_hf):
            st.session_state.use_mock = True
            use_mock = True

        # Update session state
        st.session_state.use_mock = use_mock
        st.session_state.use_ollama = use_ollama
        st.session_state.use_huggingface = use_hf

        st.markdown("---")

        # Show status based on selection
        if use_mock:
            selected_llm = "Mock (Demo)"
            st.info("🎭 **Active:** Demo Mode")
            st.caption("• Instant responses\n• Pre-written examples\n• Perfect for testing UI")
            llm_ready = True

        elif use_ollama:
            selected_llm = "Ollama (Local)"
            llm_ready = check_ollama_status()

        elif use_hf:
            selected_llm = "Hugging Face (Online)"
            llm_ready = check_huggingface_status()

        else:
            selected_llm = "Mock (Demo)"
            llm_ready = True

        # Additional sidebar content
        render_sidebar_links()

        return selected_llm, llm_ready

def check_ollama_status():
    """Check Ollama connection and show status"""
    try:
        import ollama
        models = ollama.list()

        st.success("✅ **Ollama Connected**")

        if 'models' in models and models['models']:
            model_names = [model['name'] for model in models['models']]
            st.info(f"📦 **Models:** {', '.join(model_names[:2])}")

            # Show which model will be used
            if any('codellama' in name for name in model_names):
                st.caption("🚀 Using: codellama:7b-code")
            else:
                st.warning("⚠️ codellama:7b-code not found")
                st.code("ollama pull codellama:7b-code", language="bash")
        else:
            st.warning("⚠️ No models found")
            st.code("ollama pull codellama:7b-code", language="bash")

        st.caption("• Real AI responses\n• 10-30 second generation time\n• Runs locally on your PC")
        return True

    except ImportError:
        st.error("❌ **Ollama not installed**")
        st.code("pip install ollama", language="bash")
        return False

    except Exception as e:
        st.error("❌ **Ollama not running**")
        st.code("ollama serve", language="bash")
        st.caption(f"Error: {str(e)[:50]}...")
        return False

def check_huggingface_status():
    """Check Hugging Face status"""
    hf_token = st.text_input(
        "🔑 HF Token (optional):",
        type="password",
        help="Get free token from huggingface.co"
    )

    st.warning("⚠️ **Limited Implementation**")
    st.caption("• Falls back to Mock responses\n• Free tier has rate limits\n• Full HF integration coming soon")

    return True

def render_sidebar_links():
    """Render documentation links in sidebar"""
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
    st.caption("CodeXR v1.0 - Built with ❤️ for AR/VR developers")

def generate_response_unified(query: str, category: str, search_results: list, llm_type: str, llm_ready: bool):
    """Unified response generation"""

    if not llm_ready:
        st.error("❌ LLM backend not ready. Check sidebar configuration.")
        return None

    if llm_type == "Ollama (Local)":
        return generate_ollama_response(query, category, search_results)
    elif llm_type == "Hugging Face (Online)":
        st.warning("🔄 Hugging Face not fully implemented, using Mock response")
        return generate_mock_response(query, category)
    else:  # Mock mode
        return generate_mock_response(query, category)

def generate_ollama_response(query: str, category: str, search_results: list):
    """Generate response using Ollama"""
    try:
        import ollama

        # Create context from search results
        context = ""
        if search_results:
            context = "\n".join([f"- {r.get('title', '')}: {r.get('snippet', '')}" for r in search_results[:3]])

        prompt = f"""You are CodeXR, an expert AR/VR coding assistant. Generate a structured response for this developer query.

Query: {query}
Category: {category}
Context from documentation: {context}

Respond with valid JSON in this exact format:
{{
    "subtasks": [
        "Step 1: Specific actionable task",
        "Step 2: Another clear step",
        "Step 3: Final implementation step"
    ],
    "code_snippet": "// Complete, working code that developers can copy-paste\\n// Include necessary imports and full implementation",
    "best_practices": [
        "Important tip for {category} development",
        "Common pitfall to avoid"
    ],
    "difficulty": "Easy|Medium|Hard",
    "documentation_links": [
        "https://docs.unity3d.com/relevant-link",
        "https://docs.unrealengine.com/relevant-link"
    ],
    "estimated_time": "X minutes/hours"
}}

Focus on {category} development. Provide complete, production-ready code."""

        with st.spinner("🤖 Ollama is generating response..."):
            response = ollama.generate(
                model='codellama:7b-code',
                prompt=prompt,
                stream=False
            )

        response_text = response['response']

        # Try to extract JSON
        try:
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1

            if start_idx != -1 and end_idx != -1:
                json_str = response_text[start_idx:end_idx]
                parsed_response = json.loads(json_str)

                # Validate required fields
                required_fields = ['subtasks', 'code_snippet', 'best_practices', 'difficulty', 'estimated_time']
                if all(field in parsed_response for field in required_fields):
                    return parsed_response

        except json.JSONDecodeError:
            pass

        # If JSON parsing fails, create structured response from raw text
        st.warning("🔄 Ollama response couldn't be parsed as JSON, using fallback format")

        return {
            "subtasks": [
                f"Implement the core {category} functionality for: {query}",
                "Test the implementation on your target platform",
                "Debug and optimize for performance"
            ],
            "code_snippet": f"// Ollama generated response:\n{response_text[:500]}...",
            "best_practices": [
                "Follow platform-specific guidelines",
                "Test thoroughly on target devices"
            ],
            "difficulty": "Medium",
            "documentation_links": ["https://docs.unity3d.com/", "https://docs.unrealengine.com/"],
            "estimated_time": "1-2 hours"
        }

    except Exception as e:
        st.error(f"Ollama error: {str(e)}")
        st.info("🔄 Falling back to Mock response")
        return generate_mock_response(query, category)

def generate_mock_response(query: str, category: str):
    """Generate mock response based on query keywords"""

    query_lower = query.lower()

    # Unity VR Teleport
    if "teleport" in query_lower and "unity" in query_lower:
        return {
            "subtasks": [
                "Install XR Interaction Toolkit package via Package Manager",
                "Create XR Origin (VR) prefab in your scene",
                "Add Teleportation Provider component to XR Origin",
                "Create teleportation areas using Teleportation Area prefab",
                "Configure Input Actions for teleportation gestures"
            ],
            "code_snippet": """// TeleportationManager.cs
using UnityEngine;
using UnityEngine.XR.Interaction.Toolkit;

public class TeleportationManager : MonoBehaviour
{
    [SerializeField] private TeleportationProvider teleportationProvider;
    [SerializeField] private LineRenderer teleportLine;
    [SerializeField] private GameObject teleportReticle;

    void Start()
    {
        if (teleportationProvider == null)
            teleportationProvider = FindObjectOfType<TeleportationProvider>();

        if (teleportLine == null)
            teleportLine = GetComponent<LineRenderer>();
    }

    public void StartTeleport()
    {
        teleportLine.enabled = true;
        teleportReticle.SetActive(true);
    }

    public void EndTeleport(Vector3 destination)
    {
        TeleportRequest request = new TeleportRequest()
        {
            destinationPosition = destination,
            matchOrientation = MatchOrientation.TargetUp
        };

        teleportationProvider.QueueTeleportRequest(request);
        teleportLine.enabled = false;
        teleportReticle.SetActive(false);
    }
}""",
            "best_practices": [
                "Always validate teleport destinations to prevent users from teleporting inside objects",
                "Provide smooth locomotion as an alternative for users sensitive to teleportation",
                "Add audio and visual feedback to make teleportation feel responsive",
                "Use fade-to-black transitions to reduce motion sickness during teleportation"
            ],
            "difficulty": "Medium",
            "documentation_links": [
                "https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit@2.5/manual/locomotion.html",
                "https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit@2.5/manual/teleportation-provider.html"
            ],
            "estimated_time": "45-60 minutes"
        }

    # Unreal Multiplayer
    elif "multiplayer" in query_lower and "unreal" in query_lower:
        return {
            "subtasks": [
                "Enable Online Subsystem and Steam/EOS plugins in Project Settings",
                "Create GameMode and GameState classes with replication support",
                "Implement VR character with networked hand/head tracking",
                "Set up dedicated server build configuration",
                "Test multiplayer functionality with multiple clients"
            ],
            "code_snippet": """// VRMultiplayerCharacter.cpp
#include "VRMultiplayerCharacter.h"
#include "Net/UnrealNetwork.h"
#include "Components/CapsuleComponent.h"
#include "Camera/CameraComponent.h"

AVRMultiplayerCharacter::AVRMultiplayerCharacter()
{
    PrimaryActorTick.bCanEverTick = true;
    bReplicates = true;
    SetReplicateMovement(true);

    // VR Camera setup
    VRCamera = CreateDefaultSubobject<UCameraComponent>(TEXT("VR Camera"));
    VRCamera->SetupAttachment(RootComponent);
}

void AVRMultiplayerCharacter::GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const
{
    Super::GetLifetimeReplicatedProps(OutLifetimeProps);

    DOREPLIFETIME(AVRMultiplayerCharacter, HeadTransform);
    DOREPLIFETIME(AVRMultiplayerCharacter, LeftHandTransform);
    DOREPLIFETIME(AVRMultiplayerCharacter, RightHandTransform);
    DOREPLIFETIME(AVRMultiplayerCharacter, PlayerName);
}

void AVRMultiplayerCharacter::ServerUpdateVRTransforms_Implementation(
    FTransform NewHeadTransform,
    FTransform NewLeftHandTransform,
    FTransform NewRightHandTransform)
{
    HeadTransform = NewHeadTransform;
    LeftHandTransform = NewLeftHandTransform;
    RightHandTransform = NewRightHandTransform;
}

bool AVRMultiplayerCharacter::ServerUpdateVRTransforms_Validate(
    FTransform NewHeadTransform,
    FTransform NewLeftHandTransform,
    FTransform NewRightHandTransform)
{
    return true;
}""",
            "best_practices": [
                "Use transform compression to reduce bandwidth for frequent VR updates",
                "Implement client-side prediction for smooth VR movement",
                "Consider network culling for distant players to optimize performance",
                "Handle VR-specific disconnect scenarios gracefully (headset removal, etc.)"
            ],
            "difficulty": "Hard",
            "documentation_links": [
                "https://docs.unrealengine.com/5.3/en-US/networking-and-multiplayer-in-unreal-engine/",
                "https://docs.unrealengine.com/5.3/en-US/vr-development-in-unreal-engine/"
            ],
            "estimated_time": "3-5 hours"
        }

    # AR Occlusion Shader
    elif "shader" in query_lower and "occlusion" in query_lower:
        return {
            "subtasks": [
                "Create new shader using Unity's Shader Graph or write HLSL manually",
                "Implement depth buffer comparison for real-world occlusion",
                "Add support for AR Foundation's occlusion manager",
                "Optimize shader for mobile AR platforms (iOS/Android)",
                "Test occlusion accuracy with various lighting conditions"
            ],
            "code_snippet": """// AROcclusion.shader
Shader "Custom/AROcclusion"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        _OcclusionStrength ("Occlusion Strength", Range(0,1)) = 1.0
        _DepthSensitivity ("Depth Sensitivity", Range(0.001, 0.1)) = 0.01
    }

    SubShader
    {
        Tags {
            "RenderType"="Transparent"
            "Queue"="Geometry-1"
            "RenderPipeline" = "UniversalPipeline"
        }

        Pass
        {
            Name "AROcclusion"
            ZWrite On
            ZTest LEqual
            ColorMask 0
            Cull Off

            HLSLPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #pragma multi_compile_local _ _USE_DEPTH_TEXTURE

            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/DeclareDepthTexture.hlsl"

            struct Attributes
            {
                float4 positionOS : POSITION;
                float2 uv : TEXCOORD0;
            };

            struct Varyings
            {
                float4 positionHCS : SV_POSITION;
                float2 uv : TEXCOORD0;
                float4 screenPos : TEXCOORD1;
            };

            TEXTURE2D(_MainTex);
            SAMPLER(sampler_MainTex);

            float _OcclusionStrength;
            float _DepthSensitivity;

            Varyings vert(Attributes input)
            {
                Varyings output;
                output.positionHCS = TransformObjectToHClip(input.positionOS.xyz);
                output.uv = input.uv;
                output.screenPos = ComputeScreenPos(output.positionHCS);
                return output;
            }

            half4 frag(Varyings input) : SV_Target
            {
                float2 screenUV = input.screenPos.xy / input.screenPos.w;
                float sceneDepth = SampleSceneDepth(screenUV);
                float fragmentDepth = input.positionHCS.z;

                // Compare depths for occlusion
                float depthDiff = sceneDepth - fragmentDepth;
                float occlusion = step(_DepthSensitivity, depthDiff);

                return half4(0, 0, 0, occlusion * _OcclusionStrength);
            }
            ENDHLSL
        }
    }
}""",
            "best_practices": [
                "Use depth-only rendering passes for optimal mobile performance",
                "Consider using stencil buffer for complex multi-object occlusion",
                "Test thoroughly on target mobile devices to ensure acceptable frame rates",
                "Implement graceful fallbacks for devices without depth camera support"
            ],
            "difficulty": "Hard",
            "documentation_links": [
                "https://docs.unity3d.com/Manual/SL-DepthTextures.html",
                "https://docs.unity3d.com/Packages/com.unity.xr.arfoundation@4.2/manual/occlusion-manager.html"
            ],
            "estimated_time": "2-4 hours"
        }

    # Generic response for other queries
    else:
        return {
            "subtasks": [
                f"Research {category} development best practices for: {query}",
                f"Set up the basic {category} project structure and dependencies",
                f"Implement the core functionality step by step",
                f"Test the implementation on your target platform",
                f"Debug, optimize, and document your solution"
            ],
            "code_snippet": f"""// {category} Implementation Template
// Query: {query}

using UnityEngine;  // or #include for Unreal/C++

public class GeneratedSolution : MonoBehaviour
{{
    [Header("{category} Configuration")]
    [SerializeField] private GameObject targetObject;
    [SerializeField] private float processingSpeed = 1.0f;

    private void Start()
    {{
        InitializeSystem();
        Debug.Log("Starting {category} implementation for: {query}");
    }}

    private void InitializeSystem()
    {{
        // TODO: Implement your {category.lower()} logic here
        // This is a template - customize based on your specific needs
    }}

    private void Update()
    {{
        // TODO: Add your main processing loop here
        ProcessMainLogic();
    }}

    private void ProcessMainLogic()
    {{
        // Add your specific implementation here
    }}
}}""",
            "best_practices": [
                f"Follow {category}-specific coding standards and naming conventions",
                "Test frequently on your target hardware during development",
                "Profile performance early and optimize critical code paths",
                "Document your code thoroughly for future maintenance and team collaboration",
                "Use version control to track changes and enable rollback if needed"
            ],
            "difficulty": "Medium",
            "documentation_links": [
                "https://docs.unity3d.com/Manual/",
                "https://docs.unrealengine.com/5.3/en-US/",
                "https://developer.oculus.com/documentation/",
                "https://developers.google.com/ar"
            ],
            "estimated_time": "1-3 hours"
        }

def main():
    initialize_session_state()

    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🥽 CodeXR - AR/VR Coding Assistant</h1>
        <p>Your AI-powered companion for Unity, Unreal Engine, and Shader development</p>
    </div>
    """, unsafe_allow_html=True)

    # Create LLM sidebar and get selection
    selected_llm, llm_ready = create_llm_sidebar()

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
            if st.button("🎮 Unity VR Teleport", use_container_width=True):
                st.session_state.demo_query = "How do I add teleport locomotion in Unity VR?"

        with col_demo2:
            if st.button("🌐 Unreal Multiplayer", use_container_width=True):
                st.session_state.demo_query = "How do I set up multiplayer in Unreal VR?"

        with col_demo3:
            if st.button("🔮 AR Occlusion Shader", use_container_width=True):
                st.session_state.demo_query = "Which shader works best for AR occlusion?"

        # Use demo query if selected
        if 'demo_query' in st.session_state:
            query = st.session_state.demo_query
            del st.session_state.demo_query

        # Process query
        if st.button("🚀 Generate Solution", type="primary", use_container_width=True):
            if query.strip():
                process_query(query, selected_llm, llm_ready)
            else:
                st.warning("Please enter a query or try one of the demo scenarios!")

    with col2:
        st.subheader("📊 Query Analysis")

        if query:
            # Classify query
            category = st.session_state.classifier.classify(query)
            st.info(f"**Category:** {category}")

            difficulty = estimate_difficulty(query)
            difficulty_colors = {
                "Easy": "🟢 Easy",
                "Medium": "🟡 Medium",
                "Hard": "🔴 Hard"
            }

            st.metric("Difficulty", difficulty_colors.get(difficulty, "🟡 Medium"))

            # Show selected LLM
            st.metric("AI Backend", selected_llm)

            if llm_ready:
                st.success("✅ Ready to generate")
            else:
                st.error("❌ Backend not ready")

def process_query(query, selected_llm, llm_ready):
    """Process the user query and generate response"""

    with st.spinner("🔍 Analyzing your query..."):
        try:
            # Step 1: Classify query
            category = st.session_state.classifier.classify(query)

            # Step 2: Search for relevant documentation
            st.info("🌐 Searching for relevant documentation...")
            search_results = st.session_state.search_agent.search(query, category)

            # Step 3: Generate structured response
            if selected_llm == "Mock (Demo)":
                st.info("🎭 Generating demo response...")
            else:
                st.info(f"🤖 Generating response with {selected_llm}...")

            response = generate_response_unified(query, category, search_results, selected_llm, llm_ready)

            # Step 4: Render response
            if response:
                render_response(response, query)

                # Add to chat history
                st.session_state.chat_history.append({
                    'timestamp': datetime.now(),
                    'query': query,
                    'category': category,
                    'llm_type': selected_llm,
                    'response': response
                })
            else:
                st.error("Sorry, I couldn't generate a response. Please check your LLM configuration.")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.info("Please check your LLM configuration in the sidebar.")

def estimate_difficulty(query):
    """Simple difficulty estimation based on keywords"""
    easy_keywords = ['basic', 'simple', 'how to', 'tutorial', 'beginner', 'start']
    hard_keywords = ['multiplayer', 'networking', 'optimization', 'advanced', 'performance', 'complex', 'shader']

    query_lower = query.lower()

    if any(keyword in query_lower for keyword in hard_keywords):
        return "Hard"
    elif any(keyword in query_lower for keyword in easy_keywords):
        return "Easy"
    else:
        return "Medium"

if __name__ == "__main__":
    main()
