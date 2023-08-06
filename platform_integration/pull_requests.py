from typing import List
from core.code_review.base import (
    BasePullRequestDataProvider,
    BasePullRequestDecoratorService,
)
from core.code_review.models import (
    CodeFileChange,
    MethodInfo,
    ReviewCommentsCollection,
)
from platform_integration.base import BaseDevOpsApiClient


class PullRequestDataProvider(BasePullRequestDataProvider):
    """Provides access to Azure DevOps pull request data."""

    def __init__(
        self,
        api_client: BaseDevOpsApiClient,
    ) -> None:
        super().__init__()
        self._api_client = api_client

    def get_changed_files(self, pull_request_id: str) -> List[CodeFileChange]:
        source, target = self._api_client.get_pull_request_branches(pull_request_id)
        changesets = list()
        for file_path, file_url, is_new in self._api_client.get_pull_request_diff(
            source, target
        ):
            file_contents = self._api_client.get_file_by_url(file_url)
            if not is_new:
                target_file_contents = self._api_client.get_file_contents(
                    file_path, target
                )
            changeset = CodeFileChange(
                path=file_path,
                contents=file_contents,
                original_contents=target_file_contents,
                is_new_file=is_new,
            )
            changesets.append(changeset)
        return changesets


class PullRequestDecoratorService(BasePullRequestDecoratorService):
    """Provides the ability to annotate pull requests with comments."""

    def __init__(self, api_client: BaseDevOpsApiClient) -> None:
        super().__init__()
        self._api_client = api_client

    def post_comments(
        self,
        pull_request_id: str,
        file_path: str,
        method: MethodInfo,
        comments: ReviewCommentsCollection,
    ) -> None:
        existing_comments = self._api_client.get_pull_request_comments(
            pull_request_id, file_path, method.start_line, method.end_line
        )
        for review_comment in comments.items:
            if any(c for c in existing_comments if review_comment.comment in c):
                print(f"Comment already exists: {review_comment.comment}")
                continue
            comment_text = f"{review_comment.comment} \n {review_comment.example}"
            self._api_client.post_pull_request_comment(
                pull_request_id,
                file_path,
                method.start_line + review_comment.line,
                comment_text,
            )
