import json
import unittest
from semantic_kernel.orchestration.context_variables import ContextVariables
from helpers import get_kernel
from skills.Reviewer.plugin import ReviewerPlugin


class TestGetChangedMethods(unittest.TestCase):
    def test_when_two_versions_with_changes_returns_correct_changed_methods(
        self,
    ):
        kernel = get_kernel()
        skill = kernel.import_skill(ReviewerPlugin(), "ReviewerPlugin")
        getchangedmethods_func = skill["get_changed_methods"]

        changed_methods = "[[48, 49], [50, 54]]"
        methods = '[{"name":"AddItemToBasket", "start":23,"end":30},{"name":"DeleteBasketAsync", "start":32,"end":36},{"name":"GetBasketItemCountAsync", "start":38,"end":57},{"name":"SetQuantities", "start":59,"end":74},{"name":"TransferBasketAsync", "start":76,"end":85}]'
        context_variables = ContextVariables(
            variables={
                "changed_blocks": json.dumps(changed_methods),
                "methods": json.dumps(methods),
            }
        )

        result = getchangedmethods_func.invoke(variables=context_variables)
        changed_methods = json.loads(result.result)
        assert changed_methods is not None
