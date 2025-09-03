import requests
from typing import List, Dict
from duckduckgo_search import DDGS
import streamlit as st
from bs4 import BeautifulSoup
import time

class SearchAgent:
    def __init__(self):
        self.ddgs = DDGS()

    def search(self, query: str, category: str) -> List[Dict]:
        """Search for relevant documentation and tutorials"""

        # Enhance query based on category
        enhanced_query = self._enhance_query(query, category)

        try:
            # Search with DuckDuckGo
            results = self._search_duckduckgo(enhanced_query)

            # Filter and rank results
            filtered_results = self._filter_results(results, category)

            return filtered_results[:5]  # Return top 5 results

        except Exception as e:
            st.warning(f"Search error: {str(e)}. Using fallback documentation.")
            return self._get_fallback_results(category)

    def _enhance_query(self, query: str, category: str) -> str:
        """Enhance search query based on category"""

        category_terms = {
            "Unity": "Unity3D XR VR AR documentation tutorial",
            "Unreal": "Unreal Engine VR AR tutorial documentation",
            "Shader": "Unity shader HLSL tutorial documentation",
            "General": "AR VR development tutorial"
        }

        base_term = category_terms.get(category, "AR VR development")
        return f"{query} {base_term}"

    def _search_duckduckgo(self, query: str) -> List[Dict]:
        """Perform search using DuckDuckGo"""
        results = []

        try:
            # Use DuckDuckGo search
            ddg_results = self.ddgs.text(
                keywords=query,
                max_results=10,
                safesearch='moderate'
            )

            for result in ddg_results:
                results.append({
                    'title': result.get('title', ''),
                    'snippet': result.get('body', ''),
                    'url': result.get('href', ''),
                    'source': self._identify_source(result.get('href', ''))
                })

        except Exception as e:
            st.error(f"DuckDuckGo search failed: {str(e)}")

        return results

    def _identify_source(self, url: str) -> str:
        """Identify the source type of a URL"""
        if 'docs.unity3d.com' in url:
            return 'Unity Official'
        elif 'docs.unrealengine.com' in url:
            return 'Unreal Official'
        elif 'github.com' in url:
            return 'GitHub'
        elif 'stackoverflow.com' in url:
            return 'StackOverflow'
        elif 'youtube.com' in url or 'youtu.be' in url:
            return 'YouTube'
        else:
            return 'Web'

    def _filter_results(self, results: List[Dict], category: str) -> List[Dict]:
        """Filter and rank results based on relevance and quality"""

        # Priority sources for each category
        priority_sources = {
            'Unity': ['Unity Official', 'GitHub'],
            'Unreal': ['Unreal Official', 'GitHub'],
            'Shader': ['Unity Official', 'GitHub'],
            'General': ['Unity Official', 'Unreal Official', 'GitHub']
        }

        # Score results
        scored_results = []
        for result in results:
            score = self._calculate_score(result, category, priority_sources.get(category, []))
            scored_results.append((score, result))

        # Sort by score (descending)
        scored_results.sort(key=lambda x: x[0], reverse=True)

        # Return only the results (without scores)
        return [result for _, result in scored_results]

    def _calculate_score(self, result: Dict, category: str, priority_sources: List[str]) -> float:
        """Calculate relevance score for a search result"""
        score = 0.0

        # Source priority
        if result['source'] in priority_sources:
            score += 3.0
        elif result['source'] == 'StackOverflow':
            score += 2.0
        else:
            score += 1.0

        # Keyword matching in title and snippet
        text = (result['title'] + ' ' + result['snippet']).lower()

        category_keywords = {
            'Unity': ['unity', 'xr', 'vr', 'ar', 'c#'],
            'Unreal': ['unreal', 'ue4', 'ue5', 'vr', 'ar', 'c++'],
            'Shader': ['shader', 'hlsl', 'unity', 'material'],
            'General': ['vr', 'ar', 'xr', 'virtual reality']
        }

        keywords = category_keywords.get(category, [])
        for keyword in keywords:
            if keyword in text:
                score += 0.5

        # Penalize very short snippets
        if len(result['snippet']) < 50:
            score -= 1.0

        return score

    def _get_fallback_results(self, category: str) -> List[Dict]:
        """Provide fallback documentation links when search fails"""

        fallback_results = {
            'Unity': [
                {
                    'title': 'Unity XR Documentation',
                    'snippet': 'Official Unity XR development documentation covering VR and AR.',
                    'url': 'https://docs.unity3d.com/Manual/XR.html',
                    'source': 'Unity Official'
                },
                {
                    'title': 'XR Interaction Toolkit',
                    'snippet': 'Unity package for building VR and AR interactive experiences.',
                    'url': 'https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit@2.5/manual/',
                    'source': 'Unity Official'
                }
            ],
            'Unreal': [
                {
                    'title': 'Unreal Engine VR Development',
                    'snippet': 'Official documentation for VR development in Unreal Engine.',
                    'url': 'https://docs.unrealengine.com/5.3/en-US/vr-development-in-unreal-engine/',
                    'source': 'Unreal Official'
                }
            ],
            'Shader': [
                {
                    'title': 'Unity Shader Documentation',
                    'snippet': 'Complete guide to writing shaders in Unity using ShaderLab and HLSL.',
                    'url': 'https://docs.unity3d.com/Manual/Shaders.html',
                    'source': 'Unity Official'
                }
            ],
            'General': [
                {
                    'title': 'VR Development Best Practices',
                    'snippet': 'General guidelines and best practices for VR application development.',
                    'url': 'https://developer.oculus.com/documentation/unity/unity-conf-settings/',
                    'source': 'Web'
                }
            ]
        }

        return fallback_results.get(category, fallback_results['General'])
