import json
import requests
import streamlit as st
from typing import Dict, List, Optional

class LLMHandler:
    def __init__(self):
        # Use session state to persist the selection
        if 'llm_type' not in st.session_state:
            st.session_state.llm_type = "Mock (Demo)"

        # Create the selectbox with session state
        self.llm_type = st.sidebar.selectbox(
            "Choose LLM Backend:",
            ["Mock (Demo)", "Ollama (Local)", "Hugging Face (Online)"],
            index=["Mock (Demo)", "Ollama (Local)", "Hugging Face (Online)"].index(st.session_state.llm_type),
            key="llm_selector"
        )

        # Update session state
        st.session_state.llm_type = self.llm_type

        if self.llm_type == "Hugging Face (Online)":
            self.hf_token = st.sidebar.text_input(
                "Hugging Face Token (optional):",
                type="password",
                help="Leave empty to use free tier with rate limits"
            )

        self.setup_llm()

    def setup_llm(self):
        """Setup the selected LLM backend"""
        if self.llm_type == "Ollama (Local)":
            try:
                # Import ollama here to avoid issues if not installed
                import ollama

                # Check if Ollama is running by testing connection
                models = ollama.list()
                self.llm_ready = True
                st.sidebar.success("✅ Ollama connected")

                # Show available models
                if 'models' in models and models['models']:
                    model_names = [model['name'] for model in models['models']]
                    st.sidebar.info(f"Models available: {', '.join(model_names[:2])}")

            except ImportError:
                self.llm_ready = False
                st.sidebar.error("❌ Ollama package not found. Run: pip install ollama")
            except Exception as e:
                self.llm_ready = False
                st.sidebar.error("❌ Ollama not running. Run: ollama serve")
                st.sidebar.code("ollama serve", language="bash")

        elif self.llm_type == "Hugging Face (Online)":
            try:
                # Simplified HF check
                import transformers
                self.llm_ready = True
                st.sidebar.success("✅ Hugging Face ready")
            except ImportError:
                self.llm_ready = False
                st.sidebar.error("❌ Transformers not installed")
            except Exception as e:
                self.llm_ready = False
                st.sidebar.error(f"❌ HF Error: {str(e)}")

        else:  # Mock mode
            self.llm_ready = True
            st.sidebar.info("🎭 Mock mode - Demo responses")

    def generate_response(self, query: str, category: str, search_results: List[Dict]) -> Optional[Dict]:
        """Generate structured response for the query"""

        if not self.llm_ready:
            return None

        # Create context from search results
        context = self._create_context(search_results)

        # Generate response based on LLM type
        if self.llm_type == "Ollama (Local)":
            return self._generate_ollama_response(query, category, context)
        elif self.llm_type == "Hugging Face (Online)":
            return self._generate_hf_response(query, category, context)
        else:  # Mock mode
            return self._generate_mock_response(query, category)

    def _create_context(self, search_results: List[Dict]) -> str:
        """Create context string from search results"""
        context_parts = []
        for result in search_results[:3]:  # Use top 3 results
            context_parts.append(f"- {result.get('title', '')}: {result.get('snippet', '')}")
        return "\n".join(context_parts)

    def _generate_ollama_response(self, query: str, category: str, context: str) -> Optional[Dict]:
        """Generate response using Ollama"""
        try:
            import ollama

            # Create a simple prompt for code generation
            prompt = f"""You are a helpful AR/VR coding assistant. Generate a JSON response for this query:

Query: {query}
Category: {category}
Context: {context}

Respond with valid JSON in this format:
{{
    "subtasks": ["Step 1: ...", "Step 2: ...", "Step 3: ..."],
    "code_snippet": "// Complete working code here",
    "best_practices": ["Tip 1", "Tip 2"],
    "difficulty": "Easy|Medium|Hard",
    "documentation_links": ["https://docs.unity3d.com/..."],
    "estimated_time": "30 minutes"
}}

Focus on {category} development. Provide complete, working code."""

            # Generate response
            response = ollama.generate(
                model='codellama:7b-code',
                prompt=prompt,
                stream=False
            )

            # Extract JSON from response
            response_text = response['response']
            return self._extract_json(response_text)

        except Exception as e:
            st.error(f"Ollama error: {str(e)}")
            # Fall back to mock response
            return self._generate_mock_response(query, category)

    def _generate_hf_response(self, query: str, category: str, context: str) -> Optional[Dict]:
        """Generate response using Hugging Face"""
        # For now, fall back to mock - HF free tier is limited for code generation
        st.warning("Hugging Face code generation not fully implemented. Using mock response.")
        return self._generate_mock_response(query, category)

    def _generate_mock_response(self, query: str, category: str) -> Dict:
        """Generate mock response for demo purposes"""

        # Determine response based on query keywords
        if "teleport" in query.lower() and "unity" in query.lower():
            return self._get_unity_teleport_response()
        elif "multiplayer" in query.lower() and "unreal" in query.lower():
            return self._get_unreal_multiplayer_response()
        elif "shader" in query.lower() and "occlusion" in query.lower():
            return self._get_shader_occlusion_response()
        else:
            return self._get_generic_response(query, category)

    def _get_unity_teleport_response(self) -> Dict:
        return {
            "subtasks": [
                "Install XR Interaction Toolkit package via Package Manager",
                "Create XR Origin (VR) prefab in your scene",
                "Add Teleportation Provider component to XR Origin",
                "Create teleportation areas using Teleportation Area prefab",
                "Configure Input Actions for teleportation"
            ],
            "code_snippet": """// TeleportationManager.cs
using UnityEngine;
using UnityEngine.XR.Interaction.Toolkit;

public class TeleportationManager : MonoBehaviour
{
    [SerializeField] private TeleportationProvider teleportationProvider;
    [SerializeField] private LineRenderer lineRenderer;

    void Start()
    {
        if (teleportationProvider == null)
            teleportationProvider = FindObjectOfType<TeleportationProvider>();
    }

    public void RequestTeleport(TeleportRequest request)
    {
        teleportationProvider.QueueTeleportRequest(request);
    }
}""",
            "best_practices": [
                "Always validate teleport destinations to avoid placing users inside objects",
                "Use smooth locomotion as a fallback for users with motion sensitivity",
                "Implement audio/visual feedback for successful teleportations",
                "Consider using fade transitions to reduce motion sickness"
            ],
            "difficulty": "Medium",
            "documentation_links": [
                "https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit@2.5/manual/locomotion.html",
                "https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit@2.5/manual/teleportation-provider.html"
            ],
            "estimated_time": "45 minutes"
        }

    def _get_unreal_multiplayer_response(self) -> Dict:
        return {
            "subtasks": [
                "Enable multiplayer plugins in Project Settings",
                "Create dedicated server build configuration",
                "Implement network replication for VR components",
                "Set up player state synchronization",
                "Test with multiple clients"
            ],
            "code_snippet": """// VRPlayerCharacter.cpp
#include "VRPlayerCharacter.h"
#include "Net/UnrealNetwork.h"

void AVRPlayerCharacter::GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const
{
    Super::GetLifetimeReplicatedProps(OutLifetimeProps);

    DOREPLIFETIME(AVRPlayerCharacter, HeadTransform);
    DOREPLIFETIME(AVRPlayerCharacter, LeftHandTransform);
    DOREPLIFETIME(AVRPlayerCharacter, RightHandTransform);
}

void AVRPlayerCharacter::ServerUpdateVRTransforms_Implementation(
    FTransform NewHeadTransform,
    FTransform NewLeftHand,
    FTransform NewRightHand)
{
    HeadTransform = NewHeadTransform;
    LeftHandTransform = NewLeftHand;
    RightHandTransform = NewRightHand;
}""",
            "best_practices": [
                "Use compression for frequent VR transform updates",
                "Implement client-side prediction for smooth movement",
                "Consider network culling for distant players",
                "Handle VR-specific disconnection scenarios gracefully"
            ],
            "difficulty": "Hard",
            "documentation_links": [
                "https://docs.unrealengine.com/5.3/en-US/networking-and-multiplayer-in-unreal-engine/",
                "https://docs.unrealengine.com/5.3/en-US/vr-development-in-unreal-engine/"
            ],
            "estimated_time": "3-4 hours"
        }

    def _get_shader_occlusion_response(self) -> Dict:
        return {
            "subtasks": [
                "Create occlusion shader using depth buffer comparison",
                "Implement proper depth testing for AR objects",
                "Add support for real-world geometry occlusion",
                "Optimize for mobile AR platforms",
                "Test with various lighting conditions"
            ],
            "code_snippet": """// AROcclusion.shader
Shader "Custom/AROcclusion"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        _OcclusionStrength ("Occlusion Strength", Range(0,1)) = 1.0
    }

    SubShader
    {
        Tags { "RenderType"="Transparent" "Queue"="Geometry-1" }

        Pass
        {
            ZWrite On
            ZTest LEqual
            ColorMask 0

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            struct appdata
            {
                float4 vertex : POSITION;
            };

            struct v2f
            {
                float4 vertex : SV_POSITION;
            };

            v2f vert (appdata v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                return fixed4(0,0,0,0);
            }
            ENDCG
        }
    }
}""",
            "best_practices": [
                "Use depth-only rendering for better performance",
                "Consider using stencil buffer for complex occlusion scenarios",
                "Test on target mobile devices for performance validation",
                "Implement fallback for devices without depth camera"
            ],
            "difficulty": "Hard",
            "documentation_links": [
                "https://docs.unity3d.com/Manual/SL-DepthTextures.html",
                "https://docs.unity3d.com/Packages/com.unity.xr.arfoundation@4.2/manual/occlusion-manager.html"
            ],
            "estimated_time": "2-3 hours"
        }

    def _get_generic_response(self, query: str, category: str) -> Dict:
        return {
            "subtasks": [
                f"Analyze the {category} development requirements for: {query}",
                "Research relevant documentation and examples",
                "Implement the core functionality step by step",
                "Test and debug the implementation thoroughly",
                "Optimize for your target platform and use case"
            ],
            "code_snippet": f"""// {category} implementation for: {query}
// This is a generic template - provide more specific details for a complete solution

using UnityEngine;  // or appropriate includes for your platform

public class GeneratedSolution : MonoBehaviour
{{
    void Start()
    {{
        // Initialize your {category.lower()} implementation here
        Debug.Log("Implementing: {query}");
    }}

    void Update()
    {{
        // Add your main logic here
    }}
}}""",
            "best_practices": [
                f"Follow {category}-specific development guidelines and conventions",
                "Test on your target devices regularly during development",
                "Keep performance optimization in mind from the start",
                "Document your code for future reference and team collaboration"
            ],
            "difficulty": "Medium",
            "documentation_links": [
                "https://docs.unity3d.com/Manual/",
                "https://docs.unrealengine.com/",
                "https://developer.oculus.com/documentation/"
            ],
            "estimated_time": "1-2 hours"
        }

    def _extract_json(self, text: str) -> Optional[Dict]:
        """Extract JSON from LLM response text"""
        try:
            # Find JSON block in text
            start_idx = text.find('{')
            end_idx = text.rfind('}') + 1

            if start_idx != -1 and end_idx != -1:
                json_str = text[start_idx:end_idx]
                return json.loads(json_str)
            else:
                # If no JSON found, return None and fall back to mock
                return None
        except json.JSONDecodeError:
            # If JSON parsing fails, return None and fall back to mock
            return None
        except Exception:
            return None
