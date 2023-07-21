import os
from app.reviewer.model import ReviewCommentCollection
from app.reviewer.code_review_chain import CodeReviewChain
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
import unittest

DEFAULT_TEMPERATURE = 0.0


class TestCodeReviewChain(unittest.TestCase):
    def test_when_csharp_method_given_with_issues_provides_results_as_valid_json(self):
        load_dotenv("../.env")
        db_path = ".db"
        model_name = os.getenv("MODEL_NAME")

        llm = ChatOpenAI(model_name=model_name,
                         temperature=DEFAULT_TEMPERATURE)
        code_block = ""
        with open("tests/data/method-UpdateOrderAsync.cs", "r") as file:
            code_block = file.read()

        chain = CodeReviewChain.from_llm(llm, db_path=db_path, verbose=True)
        response = chain.run({"input": code_block, "lang": "C#"})
        comments = ReviewCommentCollection.parse_obj(response)
        assert comments is not None
