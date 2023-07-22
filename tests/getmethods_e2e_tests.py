import json
import unittest
from semantic_kernel.orchestration.context_variables import ContextVariables
from helpers import get_kernel, get_skill


class TestReviewMethod(unittest.TestCase):
    def test_when_csharp_class_given_with_multiple_methods_returns_results_as_valid_json(
        self,
    ):
        kernel = get_kernel()
        skill = get_skill(kernel, "Reviewer")
        getmethods_func = skill["GetMethods"]
        with open("tests/data/full-BasketService.cs", "+r") as file:
            code_block = file.read()
        context_variables = ContextVariables(
            content=code_block, variables={"lang": "C#"}
        )

        result = getmethods_func(variables=context_variables)

        methods_payload = result.result
        methods = json.loads(methods_payload, strict=False)
        self.assertTrue(len(methods) > 0)
