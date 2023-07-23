from abc import ABC, abstractmethod
import os
from langchain.llms.base import BaseLLM
from langchain import LLMChain, PromptTemplate
from core.code_review.models import MethodInfoCollection


class BaseSyntaxProvider(ABC):
    """Base class for syntax providers"""

    @abstractmethod
    def get_method_blocks(self, code_contents: str, lang: str) -> MethodInfoCollection:
        """Returns a list of method/function blocks in the given code file contents"""
        raise NotImplementedError()


class SyntaxProvider(BaseSyntaxProvider):
    """Provides syntax information for a given code file"""

    def __init__(self, llm: BaseLLM, verbose: bool = False) -> None:
        self.llm = llm
        self.verbose = verbose

    """Returns a list of method/function blocks in the given code file contents"""

    def get_method_blocks(self, code_contents: str, lang: str) -> MethodInfoCollection:
        script_path = os.path.abspath(__file__)
        parent_directory = os.path.dirname(script_path)
        prompt_abs_path = os.path.join(parent_directory, "prompts", "get-methods.txt")

        prompt = PromptTemplate.from_file(prompt_abs_path, ["input", "lang"])
        chain = LLMChain(llm=self.llm, prompt=prompt, verbose=self.verbose)
        result = chain.run({"input": code_contents, "lang": lang})
        return MethodInfoCollection.parse_raw(result)
