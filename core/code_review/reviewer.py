from core.code_review.base import (
    BasePullRequestDataProvider,
    BasePullRequestDecoratorService,
)
from core.code_review.changeset import BaseChangesetProvider
from core.code_review.comments import BaseReviewCommentProvider
from core.code_review.lang import BaseLanguageDetector
from core.shared.syntax import BaseSyntaxProvider


""" Orchestrates the code review process """


class CodeReviwer(object):
    def __init__(
        self,
        pr_data_provider: BasePullRequestDataProvider,
        pr_decorator_svc: BasePullRequestDecoratorService,
        changeset_provider: BaseChangesetProvider,
        syntax_provider: BaseSyntaxProvider,
        language_detector: BaseLanguageDetector,
        review_comment_provider: BaseReviewCommentProvider,
    ) -> None:
        self.pr_data_provider = pr_data_provider
        self.pr_decorator_svc = pr_decorator_svc
        self.changeset_provider = changeset_provider
        self.syntax_provider = syntax_provider
        self.review_comment_provider = review_comment_provider
        self.language_detector = language_detector

    def review_pull_request(self, pull_request_id: str) -> None:
        changed_files = self.pr_data_provider.get_changed_files(pull_request_id)
        for changed_file in changed_files:
            language = self.language_detector.detect_language(changed_file)
            method_blocks = self.syntax_provider.get_method_blocks(
                changed_file.contents, language
            )
            changed_blocks = self.changeset_provider.get_changed_blocks(
                changed_file.contents, changed_file.original_contents
            )
            changed_methods = self.changeset_provider.get_changed_methods(
                method_blocks, changed_blocks
            )
            method_feedback = self.review_comment_provider.get_review_comments(
                changed_file.contents, changed_methods, language
            )
            for method, review_comments in method_feedback:
                self.pr_decorator_svc.post_comments(
                    pull_request_id,
                    changed_file.path,
                    method,
                    review_comments,
                )
