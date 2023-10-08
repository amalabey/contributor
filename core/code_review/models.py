from pydantic import BaseModel, Field
from typing import Optional, Sequence


class ReviewComment(BaseModel):
    """Represents a code review comment"""

    comment: str = Field(..., description="Review comment for the given code")
    line: int = Field(..., description="Line number in the given method")
    example: Optional[str] = Field(..., description="Example code in markdown format")


class ReviewCommentsCollection(BaseModel):
    """List of review comments for a given code file"""

    items: Sequence[ReviewComment] = Field(..., description="List of review comments")


class CodeFileChange(BaseModel):
    """Represents code file changes"""

    path: str = Field(..., description="Repository relative path to the code file")
    contents: str = Field(..., description="Code file contents to be reviewed")
    is_new_file: bool = Field(..., description="Was this file newly added")
    original_contents: Optional[str] = Field(
        default=None, description="Previous version of the code file"
    )
