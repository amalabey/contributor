import os
from langchain.chains.openai_functions import create_structured_output_chain
from langchain import PromptTemplate
from langchain.llms.base import BaseLLM
from app.reviewer.model import ReviewCommentCollection
from langchain.vectorstores.base import VectorStore


class CodeReviewPipeline:
    """Reviews a given code block and provides a list of comments"""
    def __init__(self, llm: BaseLLM, db: VectorStore):
        self.llm = llm
        self.db = db

    def execute(self,
                code_block: str,
                lang: str,
                verbose: bool = True):
        script_path = os.path.abspath(__file__)
        parent_directory = os.path.dirname(script_path)
        prompt_abs_path = os.path.join(parent_directory, "prompts", "review.txt")

        prompt = PromptTemplate.from_file(prompt_abs_path, ["input", "lang"])
        review_chain = create_structured_output_chain(ReviewCommentCollection,
                                                      self.llm,
                                                      prompt,
                                                      verbose=verbose)
        