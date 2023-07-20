from typing import Optional
from pydantic import BaseModel, Field


class ReviewComment(BaseModel):
    """Represents a code review comment"""
    suggestion: str = Field(..., description="Feedback suggestion for the given code")
    example: Optional[str] = Field(..., description="Example code in markdown format to show the suggestion")
