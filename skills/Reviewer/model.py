from pydantic import BaseModel, Field
from typing import Optional, Sequence


class ReviewComment(BaseModel):
    """Represents a code review comment"""

    suggestion: str = Field(..., description="Review comment for the given code")
    example: Optional[str] = Field(..., description="Example code in markdown format")


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
