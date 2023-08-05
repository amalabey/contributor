import base64
import json
import os
from typing import Iterator, List, Tuple
import requests
from platform_integration.base import BaseDevOpsApiClient


class AzureDevOpsApi(object):
    def __init__(self, personal_access_token=None):
        if personal_access_token is not None:
            self.personal_access_token = personal_access_token
        else:
            from_env_var = os.getenv("AZURE_DEVOPS_PAT")
            self.personal_access_token = from_env_var

    def send_api_request(
        self, url, method="GET", data=None, raiseOnErr=True, raw_data=False
    ):
        header_value = f":{self.personal_access_token}"
        header_bytes = header_value.encode("utf-8")
        basic_auth_header_bytes = base64.b64encode(header_bytes)
        basic_auth_header = basic_auth_header_bytes.decode("utf-8")
        headers = {
            "Authorization": f"Basic {basic_auth_header}",
            "Content-Type": "application/json",
        }

        response = requests.request(method, url, headers=headers, data=data)
        if raiseOnErr:
            response.raise_for_status()

        if raw_data:
            return response.text
        else:
            return response.json()


class AzureDevOpsApiClient(BaseDevOpsApiClient):
    def __init__(self, org: str, project_name: str, repo_name: str = None) -> None:
        super().__init__()
        self._org = org
        self._project_name = project_name
        self._repo_name = repo_name if repo_name is not None else project_name
        self._api = AzureDevOpsApi()

    def get_pull_request_branches(self, pr_id: str) -> Tuple[str, str]:
        pr_api_url = f"https://dev.azure.com/{self._org}/{self._project_name}/_apis/git/repositories/{self._repo_name}/pullrequests/{pr_id}?api-version=6.1-preview.1"
        pr_response = self._api.send_api_request(pr_api_url, "GET")
        sourceBranchName = pr_response["sourceRefName"].replace("refs/heads/", "")
        targetBranchName = pr_response["targetRefName"].replace("refs/heads/", "")
        return (sourceBranchName, targetBranchName)

    def get_pull_request_diff(
        self, source: str, target: str
    ) -> Iterator[Tuple[str, str, bool]]:
        diff_api_url = f"https://dev.azure.com/{self._org}/{self._project_name}/_apis/git/repositories/{self._repo_name}/diffs/commits?baseVersion={target}&targetVersion={source}&api-version=7.1-preview.1"
        diff_response = self._api.send_api_request(diff_api_url, "GET")
        for change in diff_response["changes"]:
            if change["item"]["gitObjectType"] == "blob" and change["changeType"] in (
                "add",
                "edit",
            ):
                file_path = change["item"]["path"]
                file_url = change["item"]["url"]
                is_new = True if change["changeType"] == "add" else False
                yield (file_path, file_url, is_new)

    def get_file_contents(self, file_path: str, target_version: str) -> str:
        target_file_url = f"https://dev.azure.com/{self._org}/{self._project_name}/_apis/git/repositories/{self._repo_name}/items?path={file_path}&versionDescriptor.version={target_version}&api-version=6.0"
        return self._api.send_api_request(target_file_url, "GET", raw_data=True)

    def get_file_by_url(self, file_url: str) -> str:
        return self._api.send_api_request(file_url, "GET", raw_data=True)

    def post_pull_request_comment(
        self, pull_request_id: str, file_path: str, line_num: int, comment_text: str
    ) -> None:
        api_url = f"https://dev.azure.com/{self._org}/{self._project_name}/_apis/git/repositories/{self._repo_name}/pullRequests/{pull_request_id}/threads?api-version=6.1-preview.1"
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
        self._api.send_api_request(api_url, "POST", data=payload)

    def get_pull_request_comments(
        self, pr_id: str, target_file: str, line_num: int
    ) -> List[str]:
        existing_comments = list()
        api_url = f"https://dev.azure.com/{self._org}/{self._project_name}/_apis/git/repositories/{self._repo_name}/pullRequests/{pr_id}/threads?api-version=7.0"
        response = self._api.send_api_request(api_url, "GET")
        for thread in response["value"]:
            if "threadContext" not in thread or thread["threadContext"] is None:
                continue
            file_path = (
                thread["threadContext"]["filePath"]
                if "filePath" in thread["threadContext"]
                else None
            )
            line = (
                thread["threadContext"]["rightFileStart"]["line"]
                if "rightFileStart" in thread["threadContext"]
                else 0
            )

            if file_path == target_file and line == line_num:
                for comment in thread["comments"]:
                    content = comment["content"] if "content" in comment else None
                    if content is not None:
                        existing_comments.append(content)
        return existing_comments
