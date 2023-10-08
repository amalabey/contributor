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