from abc import ABC, abstractmethod
from typing import Iterator, Tuple, List


class BaseDevOpsApiClient(ABC):
    @abstractmethod
    def get_pull_request_branches(self, pr_id: str) -> Tuple[str, str]:
        pass

    @abstractmethod
    def get_pull_request_diff(
        self, source: str, target: str
    ) -> Iterator[Tuple[str, str, bool]]:
        pass

    @abstractmethod
    def get_file_contents(self, file_path: str, target_version: str) -> str:
        pass

    @abstractmethod
    def get_file_by_url(self, file_url: str) -> str:
        pass

    @abstractmethod
    def post_pull_request_comment(
        self, pull_request_id: str, file_path: str, line_num: int, comment_text: str
    ) -> None:
        pass

    @abstractmethod
    def get_pull_request_comments(
        self, pr_id: str, target_file: str, start_line: int, end_line: int
    ) -> List[str]:
        pass


class BaseWebhookSubscriber(ABC):
    @abstractmethod
    def subscribe(self, base_url: str, api_key: str = None) -> None:
        pass
