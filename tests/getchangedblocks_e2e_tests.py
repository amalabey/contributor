import json
import unittest
from semantic_kernel.orchestration.context_variables import ContextVariables
from helpers import get_kernel
from skills.Reviewer.ReviewerPlugin import ReviewerPlugin


class TestGetChangedBlocks(unittest.TestCase):
    def test_when_two_versions_with_changes_returns_correct_changed_blocks(
        self,
    ):
        kernel = get_kernel()
        skill = kernel.import_skill(ReviewerPlugin(), "ReviewerPlugin")
        getchangedblocks_func = skill["get_changed_blocks"]

        with open("tests/data/full-BasketService-v1.cs", "+r") as file:
            from_code_file = file.read()
        with open("tests/data/full-BasketService-v2.cs", "+r") as file:
            to_code_file = file.read()
        context_variables = ContextVariables(
            variables={"from_source": from_code_file, "to_source": to_code_file}
        )

        result = getchangedblocks_func.invoke(variables=context_variables)
        changed_blocks = json.loads(result.result)
        assert changed_blocks is not None
