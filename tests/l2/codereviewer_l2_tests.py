import unittest
from unittest.mock import MagicMock
from core.code_review.changeset import ChangesetProvider
from core.code_review.comments import ReviewCommentProvider
from core.code_review.lang import LanguageDetector
from core.code_review.reviewer import CodeReviwer
from core.code_review.syntax import SyntaxProvider
from tests.builders.model_builder import ModelBuilder
from tests.builders.pull_request_builder import PullRequestBuilder
from tests.l2.stubs import PullRequestDataProviderStub, PullRequestDecoratorServiceStub


class CodeReviewerL2Tests(unittest.TestCase):
    def test_review_pull_request_when_single_changed_file_posts_valid_comments(self):
        llm_model = (
            ModelBuilder().with_azure_chat_open_ai(env_config_file=".env").build()
        )
        syntax_provider = SyntaxProvider(llm_model, verbose=True)
        changeset_provider = ChangesetProvider()
        review_provider = ReviewCommentProvider(llm_model, verbose=True)
        lang_detector = LanguageDetector()
        code_file_changes = (
            PullRequestBuilder()
            .with_code_file(
                "tests/data/BasketService.cs", "tests/data/BasketService-previous.cs"
            )
            .build()
        )
        pr_data_provider_mock = PullRequestDataProviderStub()
        pr_data_provider_mock.get_changed_files = MagicMock(
            return_value=code_file_changes
        )
        pr_decorator_mock = PullRequestDecoratorServiceStub()
        pr_decorator_mock.post_comments = MagicMock()

        code_reviewer = CodeReviwer(
            pr_data_provider_mock,
            pr_decorator_mock,
            changeset_provider,
            syntax_provider,
            lang_detector,
            review_provider,
        )
        code_reviewer.review_pull_request("123")

        self.assertEqual(pr_decorator_mock.post_comments.call_count, 2)
