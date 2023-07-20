import os
from app.reviewer.code_review_chain import CodeReviewChain
from dotenv import load_dotenv
from langchain.llms import AzureOpenAI
import unittest


class TestMyModule(unittest.TestCase):
    def test_when_csharp_method_given_with_issues_provides_valid_results(self):
        load_dotenv("../.env")
        deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        model_name = os.getenv("AZURE_OPENAI_MODEL_NAME")

        llm = AzureOpenAI(
            deployment_name=deployment_name,
            model_name=model_name,
        )
        code_block = ""
        with open("tests\\data\\method-UpdateOrderAsync.cs", "r") as file:
            code_block = file.read()

        chain = CodeReviewChain.from_llm(llm, verbose=True)
        result = chain.run({"input": code_block, "lang": "C#"})
        assert result is not None
