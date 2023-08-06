from abc import ABC, abstractmethod
from typing import List

from core.code_review.models import CodeFileChange, MethodInfo, ReviewCommentsCollection


class BasePullRequestDataProvider(ABC):
    @abstractmethod
    def get_changed_files(self, pull_request_id: str) -> List[CodeFileChange]:
        pass


class BasePullRequestDecoratorService(ABC):
    @abstractmethod
    def post_comments(
        self,
        pull_request_id: str,
        file_path: str,
        method: MethodInfo,
        comments: ReviewCommentsCollection,
    ):
        pass
