import json
import unittest
from semantic_kernel.orchestration.context_variables import ContextVariables
from helpers import get_kernel, get_skill


class TestReviewMethod(unittest.TestCase):
    def test_when_csharp_method_given_with_issues_returns_results_as_valid_json(self):
        kernel = get_kernel()
        skill = get_skill(kernel, "Reviewer")
        review_function = skill["ReviewMethod"]
        with open("tests/data/method-UpdateOrderAsync.cs", "+r") as file:
            code_block = file.read()
        context_variables = ContextVariables(
            content=code_block, variables={"lang": "C#"}
        )

        result = review_function(variables=context_variables)

        review_comments_payload = result.result
        review_comments = json.loads(review_comments_payload, strict=False)
        self.assertTrue(len(review_comments) > 0)
