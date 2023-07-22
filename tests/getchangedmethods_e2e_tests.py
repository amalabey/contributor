import unittest
from semantic_kernel.orchestration.context_variables import ContextVariables
from helpers import get_kernel
from skills.Reviewer.model import (
    CodeBlock,
    CodeBlocksCollection,
    MethodInfo,
    MethodInfoCollection,
)
from skills.Reviewer.plugin import ReviewerPlugin


class TestGetChangedMethods(unittest.TestCase):
    def test_when_two_versions_with_changes_returns_correct_changed_methods(
        self,
    ):
        kernel = get_kernel()
        skill = kernel.import_skill(ReviewerPlugin(), "ReviewerPlugin")
        getchangedmethods_func = skill["get_changed_methods"]

        changed_blocks = CodeBlocksCollection(
            items=[
                CodeBlock(start_line=48, end_line=49),
                CodeBlock(start_line=50, end_line=54),
            ]
        )
        methods = MethodInfoCollection(
            items=[
                MethodInfo(name="AddItemToBasket", start_line=23, end_line=30),
                MethodInfo(name="DeleteBasketAsync", start_line=32, end_line=36),
                MethodInfo(name="GetBasketItemCountAsync", start_line=38, end_line=57),
                MethodInfo(name="SetQuantities", start_line=59, end_line=74),
                MethodInfo(name="TransferBasketAsync", start_line=76, end_line=85),
            ]
        )
        context_variables = ContextVariables(
            variables={
                "changed_blocks": changed_blocks.model_dump_json(),
                "methods": methods.model_dump_json(),
            }
        )

        result = getchangedmethods_func.invoke(variables=context_variables)
        changed_methods = MethodInfoCollection.model_validate_json(result.result)
        assert changed_methods is not None
        assert len(changed_methods.items) > 0
