from difflib import Differ
from typing import Iterator
from semantic_kernel.skill_definition import (
    sk_function,
    sk_function_context_parameter,
)
from semantic_kernel.orchestration.sk_context import SKContext
from skills.Reviewer.model import (
    CodeBlock,
    CodeBlocksCollection,
    MethodInfoCollection,
)


class ReviewerPlugin:
    @sk_function(
        description="Returns changed method blocks based on a list of start and end line numbers",
        name="get_changed_methods",
    )
    @sk_function_context_parameter(
        name="methods",
        description="List of methods names and corresponding start and end line numbers",
    )
    @sk_function_context_parameter(
        name="changed_blocks",
        description="List of start and end line numbers of changed blocks",
    )
    def get_changed_methods(self, context: SKContext) -> str:
        methods = MethodInfoCollection.model_validate_json(context["methods"])
        blocks = CodeBlocksCollection.model_validate_json(context["changed_blocks"])
        changed_methods = list()

        for method in methods.items:
            if any(
                blk.end_line >= method.start_line and blk.start_line <= method.end_line
                for blk in blocks.items
            ):
                changed_methods.append(method)

        return MethodInfoCollection(items=changed_methods).model_dump_json()

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
    def get_changed_blocks(self, context: SKContext) -> str:
        from_source = context["from_source"]
        to_source = context["to_source"]
        changed_blocks = [
            CodeBlock(start_line=blk[0], end_line=blk[1])
            for blk in self._get_changed_blocks(from_source, to_source)
        ]
        return CodeBlocksCollection(items=changed_blocks).model_dump_json()

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
