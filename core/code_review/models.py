from pydantic import BaseModel, Field
from typing import Optional, Sequence


class CodeBlock(BaseModel):
    """Represents a code block between two line numbers"""

    start_line: int = Field(
        ..., description="The start line of the function/method in the given code file"
    )
    end_line: int = Field(
        ..., description="The end line of the function/method in the given code file"
    )


class CodeBlocksCollection(BaseModel):
    """List of code blocks in a given code file"""

    items: Sequence[CodeBlock] = Field(..., description="List of code blocks")


class MethodInfo(CodeBlock):
    """Represents a method or a function in a programming language"""

    name: str = Field(..., description="The name of the function or the method")


class MethodInfoCollection(BaseModel):
    """List of methods in a given code file"""

    items: Sequence[MethodInfo] = Field(..., description="List of methods")


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
