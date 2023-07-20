from abc import ABC, abstractmethod
from typing import List
import os
from gitignore_parser import parse_gitignore


class CodebaseIndexer(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def index(self):
        pass

    def get_repo_files(self, directory: str,
                       exclusions: List[str] = None,
                       included_extensions: List[str] = None,
                       matches=None) -> List[str]:
        # check if there is a .gitignore file
        gitignore_path = os.path.join(directory, ".gitignore")
        if os.path.isfile(gitignore_path):
            matches = parse_gitignore(gitignore_path, directory)

        repo_files = list()
        for entry in os.listdir(directory):
            if (exclusions is not None and entry in exclusions):
                continue

            entry_path = os.path.join(directory, entry)
            if os.path.isdir(entry_path):
                sub_dir_files = self.get_repo_files(entry_path,
                                                    exclusions,
                                                    included_extensions,
                                                    matches)
                repo_files.extend(sub_dir_files)
            else:
                _, ext = os.path.splitext(entry_path)
                if (included_extensions is not None and ext not in included_extensions):
                    continue
                if (not matches(entry_path)):
                    repo_files.append(entry_path)
        return repo_files
