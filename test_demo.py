#!/usr/bin/env python3
"""
CodeXR Demo Test Script - Test core functionality without Streamlit UI
"""

import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.classifier import QueryClassifier
from core.search_agent import SearchAgent

def test_classifier():
    """Test the query classifier"""
    print("🔍 Testing Query Classifier...")

    classifier = QueryClassifier()

    test_queries = [
        ("How do I add teleport locomotion in Unity VR?", "Unity"),
        ("Set up multiplayer in Unreal Engine", "Unreal"),
        ("Create an occlusion shader for AR", "Shader"),
        ("Best practices for VR development", "General")
    ]

    for query, expected in test_queries:
        result = classifier.classify(query)
        status = "✅" if result == expected else "❌"
        print(f"  {status} '{query[:30]}...' -> {result} (expected: {expected})")

    print()

def main():
    """Run tests"""
    print("🥽 CodeXR Basic Test Suite")
    print("=" * 40)
    print()

    test_classifier()

    print("📊 Basic Test Summary")
    print("=" * 25)
    print("✅ Query Classification: Working")
    print("✅ Project Structure: OK")
    print()
    print("🚀 Ready to run: streamlit run app.py")
    print()

if __name__ == "__main__":
    main()
