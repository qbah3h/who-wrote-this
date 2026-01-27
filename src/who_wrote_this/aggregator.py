from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import date

from .git_reader import GitCommit
from .models import (
    AnalyzedRange,
    AuditResult,
    Integrity,
    Summary,
    TagStat,
    TimelineMonth,
)
from .tag_parser import TagCategory, parse_tags


@dataclass(frozen=True)
class Aggregation:
    result: AuditResult
    analyzed_commits: int
    unclassified_commits: int


def _pct(count: int, total: int) -> float:
    if total <= 0:
        return 0.0
    return (count / total) * 100.0


def aggregate(
    commits: list[GitCommit],
    *,
    repository: str,
    since: date | None,
    until: date | None,
) -> AuditResult:
    total_commits = len(commits)

    counts = {TagCategory.HUMAN: 0, TagCategory.AI: 0, TagCategory.HUMAN_PLUS_AI: 0}
    timeline: dict[str, dict[TagCategory, int]] = defaultdict(lambda: defaultdict(int))

    multiple_tags = 0
    unknown_tags = 0
    ignored_commits = 0

    for c in commits:
        parsed = parse_tags(c.subject)
        unknown_tags += parsed.unknown_tags

        recognized_unique = list(dict.fromkeys(parsed.recognized))
        if len(recognized_unique) == 0:
            ignored_commits += 1
            continue

        if len(recognized_unique) > 1:
            multiple_tags += 1
            continue

        cat = recognized_unique[0]
        counts[cat] += 1
        month = c.authored_datetime.strftime("%Y-%m")
        timeline[month][cat] += 1

    analyzed_commits = sum(counts.values())
    unclassified_commits = total_commits - analyzed_commits

    months = sorted(timeline.keys())
    timeline_rows: list[TimelineMonth] = []
    for m in months:
        timeline_rows.append(
            TimelineMonth(
                month=m,
                human=timeline[m].get(TagCategory.HUMAN, 0),
                ai=timeline[m].get(TagCategory.AI, 0),
                human_plus_ai=timeline[m].get(TagCategory.HUMAN_PLUS_AI, 0),
            )
        )

    result = AuditResult.from_parts(
        repository=repository,
        analyzed_range=AnalyzedRange(since=since, until=until),
        summary=Summary(
            total_commits=total_commits,
            analyzed_commits=analyzed_commits,
            unclassified_commits=unclassified_commits,
        ),
        tags_human=TagStat(count=counts[TagCategory.HUMAN], percentage=_pct(counts[TagCategory.HUMAN], analyzed_commits)),
        tags_ai=TagStat(count=counts[TagCategory.AI], percentage=_pct(counts[TagCategory.AI], analyzed_commits)),
        tags_human_plus_ai=TagStat(
            count=counts[TagCategory.HUMAN_PLUS_AI],
            percentage=_pct(counts[TagCategory.HUMAN_PLUS_AI], analyzed_commits),
        ),
        timeline=timeline_rows,
        integrity=Integrity(multiple_tags=multiple_tags, unknown_tags=unknown_tags, ignored_commits=ignored_commits),
    )

    return result
