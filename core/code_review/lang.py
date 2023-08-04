from abc import ABC, abstractmethod
import os
from core.code_review.models import CodeFileChange


class BaseLanguageDetector(ABC):
    @abstractmethod
    def detect_language(self, changed_file: CodeFileChange) -> str:
        raise NotImplementedError()


DEFAULT_LANG_MAP = {
    ".cs": "C#",
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".go": "Go",
    ".java": "Java",
    ".cpp": "C++",
    ".c": "C",
    ".h": "C",
    ".rs": "Rust",
    ".php": "PHP",
}


class LanguageDetector(BaseLanguageDetector):
    def detect_language(self, changed_file: CodeFileChange) -> str:
        file_extension = os.path.splitext(changed_file.path)[1].lower()
        return DEFAULT_LANG_MAP.get(file_extension, "Unknown")
