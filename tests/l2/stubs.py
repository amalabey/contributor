from typing import List
from core.code_review.base import (
    BasePullRequestDataProvider,
    BasePullRequestDecoratorService,
)
from core.code_review.models import CodeFileChange, ReviewCommentsCollection


class PullRequestDataProviderStub(BasePullRequestDataProvider):
    def get_changed_files(self, pull_request_id: str) -> List[CodeFileChange]:
        return super().get_changed_files(pull_request_id)


class PullRequestDecoratorServiceStub(BasePullRequestDecoratorService):
    def post_comments(
        self, pull_request_id: str, comments: List[ReviewCommentsCollection]
    ):
        super().post_comments(pull_request_id, comments)
