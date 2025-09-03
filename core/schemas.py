from pydantic import BaseModel, Field
from typing import List

class CodeXRResponse(BaseModel):
    subtasks: List[str] = Field(..., description="List of step-by-step subtasks")
    code_snippet: str = Field(..., description="Ready-to-paste code snippet")
    best_practices: List[str] = Field(..., description="Best practices and tips")
    difficulty: str = Field(..., description="Difficulty level: Easy, Medium, or Hard")
    documentation_links: List[str] = Field(..., description="Relevant documentation URLs")
    estimated_time: str = Field(..., description="Estimated time to complete")
