from abc import ABC, abstractmethod
from difflib import Differ
from typing import Iterator
from core.shared.models import (
    CodeBlock,
    CodeBlocksCollection,
    MethodInfoCollection,
)


class BaseChangesetProvider(ABC):
    """Base class for changeset providers"""

    """ Compares current code with previous and
    returns a list of changed blocks of code"""

    @abstractmethod
    def get_changed_blocks(
        self, current_code: str, previous_code: str | None
    ) -> CodeBlocksCollection:
        pass

    """ Get changed methods from a list of methods and a list of changed blocks of code"""

    @abstractmethod
    def get_changed_methods(
        self, methods: MethodInfoCollection, changed_blocks: CodeBlocksCollection
    ) -> MethodInfoCollection:
        pass


class ChangesetProvider(BaseChangesetProvider):
    def get_changed_methods(
        self, methods: MethodInfoCollection, changed_blocks: CodeBlocksCollection
    ) -> MethodInfoCollection:
        changed_methods = list()
        for method in methods.items:
            if any(
                blk.end_line >= method.start_line and blk.start_line <= method.end_line
                for blk in changed_blocks.items
            ):
                changed_methods.append(method)

        return MethodInfoCollection(items=changed_methods)

    def get_changed_blocks(
        self, current_code: str, previous_code: str | None
    ) -> CodeBlocksCollection:
        changed_blocks = [
            CodeBlock(start_line=blk[0], end_line=blk[1])
            for blk in self._get_changed_blocks(previous_code, current_code)
        ]
        return CodeBlocksCollection(items=changed_blocks)

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
                index = changed_line_num
                continue
            elif changed_line_num > index:
                yield (blockStart, changed_line_num)
                blockStart = 0
        if blockStart > 0:
            yield (blockStart, index)
