from difflib import Differ
from typing import Iterator, List
from semantic_kernel.skill_definition import (
    sk_function,
    sk_function_context_parameter,
)
from semantic_kernel.orchestration.sk_context import SKContext


class GetChangedBlocks:
    @sk_function(
        description="Returns a list of changed blocks based on a list of start and end line numbers",
        name="get_changed_blocks",
    )
    @sk_function_context_parameter(
        name="from_source",
        description="From source code for the comparison",
    )
    @sk_function_context_parameter(
        name="to_source",
        description="To source code for the comparison",
    )
    def get_changed_blocks(self, context: SKContext) -> List[tuple[int, int]]:
        from_source = context.get_parameter_value("from_source")
        to_source = context.get_parameter_value("to_source")
        changed_blocks = list(self._get_changed_blocks(from_source, to_source))
        return changed_blocks

    def _get_changed_lines(self, source: str, target: str) -> Iterator[int]:
        differ = Differ()
        diffs = differ.compare(source.splitlines(True), target.splitlines(True))
        lineNum = 0
        for line in diffs:
            code = line[:2]
            if code in ("  ", "+ "):
                lineNum += 1
            if code == "+ ":
                yield lineNum

    def _get_changed_blocks(
        self, source: str, target: str
    ) -> Iterator[tuple[int, int]]:
        index = 0
        blockStart = 0
        for changed_line_num in self._get_changed_lines(source, target):
            index += 1
            if blockStart == 0:
                blockStart = changed_line_num
                continue
            elif changed_line_num > index:
                yield (blockStart, changed_line_num)
                blockStart = 0
            index = changed_line_num
        if blockStart > 0:
            yield (blockStart, index)
