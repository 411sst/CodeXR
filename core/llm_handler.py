import json
import requests
import streamlit as st
from typing import Dict, List, Optional
import ollama
from transformers import pipeline

class LLMHandler:
    def __init__(self):
        self.llm_type = st.sidebar.selectbox(
            "Choose LLM Backend:",
            ["Ollama (Local)", "Hugging Face (Online)", "Mock (Demo)"],
            index=2  # Default to Mock for quick testing
        )

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
                # Check if Ollama is running
                ollama.list()
                self.llm_ready = True
                st.sidebar.success("✅ Ollama connected")
            except:
                self.llm_ready = False
                st.sidebar.error("❌ Ollama not found. Install from ollama.ai")

        elif self.llm_type == "Hugging Face (Online)":
            try:
                # Use a free code generation model
                self.hf_pipeline = pipeline(
                    "text-generation",
                    model="microsoft/DialoGPT-medium",
                    max_length=1000
                )
                self.llm_ready = True
                st.sidebar.success("✅ Hugging Face ready")
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

        # Generate prompt
        prompt = self._create_prompt(query, category, context)

        # Get response based on LLM type
        if self.llm_type == "Ollama (Local)":
            return self._generate_ollama_response(prompt)
        elif self.llm_type == "Hugging Face (Online)":
            return self._generate_hf_response(prompt)
        else:  # Mock mode
            return self._generate_mock_response(query, category)

    def _create_context(self, search_results: List[Dict]) -> str:
        """Create context string from search results"""
        context_parts = []
        for result in search_results[:3]:  # Use top 3 results
            context_parts.append(f"- {result.get('title', '')}: {result.get('snippet', '')}")
        return "\n".join(context_parts)

    def _create_prompt(self, query: str, category: str, context: str) -> str:
        """Create the main prompt for the LLM"""
        return f"""
You are CodeXR, an expert AR/VR coding assistant. Generate a structured JSON response for this developer query.

Query: {query}
Category: {category}
Context from documentation:
{context}

Generate a JSON response with this exact structure:
{{
    "subtasks": [
        "Step 1: Clear action item",
        "Step 2: Another action item",
        "Step 3: Final step"
    ],
    "code_snippet": "// Ready-to-paste code\\nusing UnityEngine;\\n// ... complete code here",
    "best_practices": [
        "Important tip 1",
        "Common pitfall to avoid"
    ],
    "difficulty": "Easy|Medium|Hard",
    "documentation_links": [
        "https://docs.unity3d.com/...",
        "https://docs.unrealengine.com/..."
    ],
    "estimated_time": "30 minutes"
}}

Focus on {category} development. Provide complete, working code snippets.
"""

    def _generate_ollama_response(self, prompt: str) -> Optional[Dict]:
        """Generate response using Ollama"""
        try:
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
            return None

    def _generate_hf_response(self, prompt: str) -> Optional[Dict]:
        """Generate response using Hugging Face"""
        try:
            # For demo purposes, we'll use a simpler approach
            # In production, you'd want to use a proper code generation model
            response = self.hf_pipeline(prompt, max_length=500, num_return_sequences=1)
            response_text = response[0]['generated_text']

            # For HF free tier, we might need to parse differently
            return self._extract_json(response_text)

        except Exception as e:
            st.error(f"Hugging Face error: {str(e)}")
            return None

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
                f"Analyze the {category} development requirements",
                "Research relevant documentation and examples",
                "Implement the core functionality",
                "Test and debug the implementation",
                "Optimize for your target platform"
            ],
            "code_snippet": f"// {category} implementation for: {query}\n// This is a generic template\n// Please provide more specific details for a complete solution",
            "best_practices": [
                "Follow platform-specific development guidelines",
                "Test on your target devices regularly",
                "Keep performance optimization in mind from the start"
            ],
            "difficulty": "Medium",
            "documentation_links": [
                f"https://docs.unity3d.com/Manual/",
                f"https://docs.unrealengine.com/"
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
                return None
        except:
            return None
