import unittest
from core.code_review.changeset import ChangesetProvider
from core.code_review.syntax import SyntaxProvider
from tests.helpers import get_model


class CodeReviewTests(unittest.TestCase):
    def test_get_method_blocks_when_csharp_code_returns_all_methods(self):
        model = get_model()
        syntax_provider = SyntaxProvider(model, verbose=True)
        with open("tests/data/BasketService.cs", "r") as file:
            code_file_contents = file.read()
        methods = syntax_provider.get_method_blocks(code_file_contents, "C#")
        self.assertEqual(len(methods.items), 5)

    def test_get_changed_blocks_when_csharp_code_returns_changed_blocks(self):
        with open("tests/data/BasketService.cs", "r") as file:
            current_code = file.read()
        with open("tests/data/BasketService-previous.cs", "r") as file:
            previous_code = file.read()

        changeset_provider = ChangesetProvider()
        blocks = changeset_provider.get_changed_blocks(previous_code, current_code)
        self.assertGreater(len(blocks.items), 0)

    def test_get_changed_methods_when_csharp_code_returns_changed_methods(self):
        with open("tests/data/BasketService.cs", "r") as file:
            current_code = file.read()
        with open("tests/data/BasketService-previous.cs", "r") as file:
            previous_code = file.read()
        model = get_model()
        syntax_provider = SyntaxProvider(model, verbose=True)
        methods = syntax_provider.get_method_blocks(current_code, "C#")
        changeset_provider = ChangesetProvider()
        blocks = changeset_provider.get_changed_blocks(previous_code, current_code)

        changed_methods = changeset_provider.get_changed_methods(methods, blocks)
        self.assertGreater(len(changed_methods.items), 0)
