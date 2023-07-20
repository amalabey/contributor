from typing import List
from langchain import LLMChain
from langchain.base_language import BaseLanguageModel
from app.reviewer.prompts import get_review_prompt
from app.reviewer.model import ReviewComment
from langchain.chains.openai_functions import create_structured_output_chain


def create_review_chain(llm: BaseLanguageModel, code: str, lang: str) -> LLMChain:
    prompt = get_review_prompt(code, lang)
    chain = create_structured_output_chain(List[ReviewComment], llm, prompt, verbose=True)
    return chain
