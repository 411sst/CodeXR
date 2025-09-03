class QueryClassifier:
    def __init__(self):
        self.unity_keywords = [
            'unity', 'c#', 'gameobject', 'transform', 'monobehaviour',
            'prefab', 'scene', 'xr toolkit', 'oculus', 'vive'
        ]

        self.unreal_keywords = [
            'unreal', 'ue4', 'ue5', 'c++', 'blueprint', 'pawn', 'actor',
            'component', 'world', 'level', 'steam vr', 'oculus'
        ]

        self.shader_keywords = [
            'shader', 'hlsl', 'material', 'vertex', 'fragment', 'surface',
            'lighting', 'texture', 'uv', 'normal', 'glsl'
        ]

    def classify(self, query: str) -> str:
        """Classify query into Unity, Unreal, Shader, or General"""
        query_lower = query.lower()

        unity_score = sum(1 for keyword in self.unity_keywords if keyword in query_lower)
        unreal_score = sum(1 for keyword in self.unreal_keywords if keyword in query_lower)
        shader_score = sum(1 for keyword in self.shader_keywords if keyword in query_lower)

        # Determine category based on highest score
        scores = {
            'Unity': unity_score,
            'Unreal': unreal_score,
            'Shader': shader_score
        }

        max_category = max(scores, key=scores.get)
        max_score = scores[max_category]

        # Return the category with highest score, or General if no clear winner
        return max_category if max_score > 0 else 'General'
