import os
from langchain import PromptTemplate


def get_review_prompt(input: str, lang: str) -> str:
    script_path = os.path.abspath(__file__)
    parent_directory = os.path.dirname(script_path)
    prompt_abs_path = os.path.join(parent_directory, "review.txt")

    prompt = PromptTemplate.from_file(prompt_abs_path, ["input", "lang"])
    prompt.format(input=input, lang=lang)
    return prompt
