from typing import List
from core.code_review.models import CodeFileChange


class PullRequestBuilder:
    def __init__(self):
        self._codefilechanges = []

    def with_code_file(
        self, file_path: str, prev_version_path: str = None
    ) -> "PullRequestBuilder":
        with open(file_path, "r") as file:
            current_code = file.read()
        is_new_file = False
        if prev_version_path:
            with open(prev_version_path, "r") as file:
                previous_code = file.read()
        else:
            previous_code = None
            is_new_file = True
        code_file_change = CodeFileChange(
            path=file_path,
            contents=current_code,
            original_contents=previous_code,
            is_new_file=is_new_file,
        )
        self._codefilechanges.append(code_file_change)
        return self

    def build(self) -> List[CodeFileChange]:
        return self._codefilechanges
