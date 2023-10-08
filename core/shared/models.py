from pydantic import BaseModel, Field
from typing import Sequence


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
