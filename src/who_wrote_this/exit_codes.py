from enum import IntEnum


class ExitCode(IntEnum):
    SUCCESS = 0
    REPO_INVALID = 1
    NO_COMMITS_FOUND = 2
    NO_TAGGED_COMMITS_FOUND = 3
