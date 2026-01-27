from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from .aggregator import aggregate
from .exceptions import AuditError
from .exit_codes import ExitCode
from .git_reader import iter_commits
from .models import AuditResult


@dataclass(frozen=True)
class AnalyzeOptions:
    since: date | None = None
    until: date | None = None
    author: str | None = None
    strict: bool = False


def analyze_repository(repo: str, options: AnalyzeOptions) -> AuditResult:
    try:
        commits = list(
            iter_commits(
                repo,
                since=options.since.isoformat() if options.since else None,
                until=options.until.isoformat() if options.until else None,
                author=options.author,
            )
        )
    except Exception as e:  # noqa: BLE001
        raise AuditError(str(e), ExitCode.REPO_INVALID) from e

    if len(commits) == 0:
        raise AuditError("No commits found", ExitCode.NO_COMMITS_FOUND)

    result = aggregate(commits, repository=repo, since=options.since, until=options.until)

    if result.summary.analyzed_commits == 0:
        raise AuditError("No tagged commits found", ExitCode.NO_TAGGED_COMMITS_FOUND)

    if options.strict and result.summary.unclassified_commits > 0:
        raise AuditError("Strict mode: unclassified commits exist", ExitCode.NO_TAGGED_COMMITS_FOUND)

    return result
