from typing import List, Optional
from pydantic import BaseModel, Field


class ReviewComment(BaseModel):
    """Represents a code review comment"""
    suggestion: str = Field(..., description="Feedback suggestion for the given code")
    example: Optional[str] = Field(..., description="Example code in markdown format to show the suggestion")


class ReviewCommentCollection(BaseModel):
    """Represents a collection of code review comments"""
    results: List[ReviewComment] = Field(..., description="List of review comments")
