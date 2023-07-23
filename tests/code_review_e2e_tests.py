import unittest
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
