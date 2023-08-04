import json
from typing import List, Tuple
from azure_devops.api import AzureDevOpsClient
from core.code_review.base import (
    BasePullRequestDataProvider,
    BasePullRequestDecoratorService,
)
from core.code_review.models import (
    CodeFileChange,
    ReviewComment,
    ReviewCommentsCollection,
)


class AzureDevOpsPullRequestDataProvider(BasePullRequestDataProvider):
    """Provides access to Azure DevOps pull request data."""

    def __init__(self, org: str, project_name: str, repo_name: str = None) -> None:
        super().__init__()
        self._org = org
        self._project_name = project_name
        self._repo_name = repo_name if repo_name is not None else project_name

    def get_changed_files(self, pull_request_id: str) -> List[CodeFileChange]:
        api_client = AzureDevOpsClient()
        source, target = self._get_pr_branches(api_client, pull_request_id)
        changesets = list()
        for file_path, file_url, is_new in self._get_pr_diff(
            api_client, source, target
        ):
            file_contents = api_client.send_api_request(file_url, "GET", raw_data=True)
            if not is_new:
                target_file_url = f"https://dev.azure.com/{self._org}/{self._project_name}/_apis/git/repositories/{self._repo_name}/items?path={file_path}&versionDescriptor.version={target}&api-version=6.0"
                target_file_contents = api_client.send_api_request(
                    target_file_url, "GET", raw_data=True
                )
            changeset = CodeFileChange(
                path=file_path,
                contents=file_contents,
                original_contents=target_file_contents,
                is_new_file=is_new,
            )
            changesets.append(changeset)
        return changesets

    def _get_pr_branches(
        self, api_client: AzureDevOpsClient, pr_id: str
    ) -> Tuple[str, str]:
        pr_api_url = f"https://dev.azure.com/{self._org}/{self._project_name}/_apis/git/repositories/{self._repo_name}/pullrequests/{pr_id}?api-version=6.1-preview.1"
        pr_response = api_client.send_api_request(pr_api_url, "GET")
        sourceBranchName = pr_response["sourceRefName"].replace("refs/heads/", "")
        targetBranchName = pr_response["targetRefName"].replace("refs/heads/", "")
        return (sourceBranchName, targetBranchName)

    def _get_pr_diff(self, api_client: AzureDevOpsClient, source: str, target: str):
        diff_api_url = f"https://dev.azure.com/{self._org}/{self._project_name}/_apis/git/repositories/{self._repo_name}/diffs/commits?baseVersion={target}&targetVersion={source}&api-version=7.1-preview.1"
        diff_response = api_client.send_api_request(diff_api_url, "GET")
        for change in diff_response["changes"]:
            if change["item"]["gitObjectType"] == "blob" and change["changeType"] in (
                "add",
                "edit",
            ):
                file_path = change["item"]["path"]
                file_url = change["item"]["url"]
                is_new = True if change["changeType"] == "add" else False
                yield (file_path, file_url, is_new)


class AzureDevOpsPullRequestDecoratorService(BasePullRequestDecoratorService):
    """Provides the ability to annotate pull requests with comments."""

    def __init__(self, org: str, project_name: str, repo_name: str = None) -> None:
        super().__init__()
        self._org = org
        self._project_name = project_name
        self._repo_name = repo_name if repo_name is not None else project_name

    def post_comments(
        self,
        pull_request_id: str,
        file_path: str,
        line_num: int,
        comments: ReviewCommentsCollection,
    ) -> None:
        api_url = f"https://dev.azure.com/{self._org}/{self._project_name}/_apis/git/repositories/{self._repo_name}/pullRequests/{pull_request_id}/threads?api-version=6.1-preview.1"
        api = AzureDevOpsClient()
        for comment in comments.items:
            payload = self._get_comment_payload(file_path, line_num, comment)
            api.send_api_request(api_url, "POST", data=payload)

    def _get_comment_payload(
        self, file_path: str, line_num: int, comment: ReviewComment
    ):
        comment_text = f"{comment.feedback} \n ```\n{comment.example}\n```"
        payload = json.dumps(
            {
                "comments": [
                    {"parentCommentId": 0, "content": comment_text, "commentType": 1}
                ],
                "status": 1,
                "threadContext": {
                    "filePath": file_path,
                    "leftFileEnd": None,
                    "leftFileStart": None,
                    "rightFileEnd": {"line": line_num, "offset": 1},
                    "rightFileStart": {"line": line_num, "offset": 1},
                },
                "pullRequestThreadContext": {"changeTrackingId": 0},
            }
        )
        return payload
