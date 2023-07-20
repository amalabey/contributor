import os
from langchain import LLMChain, PromptTemplate
from langchain.llms.base import BaseLLM
from app.reviewer.model import ReviewCommentCollection
from langchain.chains.openai_functions import create_structured_output_chain


class CodeReviewChain:
    """Reviews a given code block and provides a list of comments"""
    @classmethod
    def from_llm(cls, llm: BaseLLM, verbose: bool = True) -> LLMChain:
        script_path = os.path.abspath(__file__)
        parent_directory = os.path.dirname(script_path)
        prompt_abs_path = os.path.join(parent_directory, "prompts", "review.txt")
        prompt = PromptTemplate.from_file(prompt_abs_path, ["input", "lang"])
        chain = create_structured_output_chain(ReviewCommentCollection, llm, prompt, verbose=True)
        return chain
