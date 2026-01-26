from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Iterable


@dataclass(frozen=True)
class AnalyzedRange:
    since: date | None
    until: date | None


@dataclass(frozen=True)
class TagStat:
    count: int
    percentage: float


@dataclass(frozen=True)
class Summary:
    total_commits: int
    analyzed_commits: int
    unclassified_commits: int


@dataclass(frozen=True)
class Integrity:
    multiple_tags: int
    unknown_tags: int
    ignored_commits: int


@dataclass(frozen=True)
class TimelineMonth:
    month: str
    human: int
    ai: int
    human_plus_ai: int


@dataclass(frozen=True)
class AuditResult:
    version: str
    repository: str
    analyzed_range: AnalyzedRange
    summary: Summary
    tags_human: TagStat
    tags_ai: TagStat
    tags_human_plus_ai: TagStat
    timeline: tuple[TimelineMonth, ...]
    integrity: Integrity

    @staticmethod
    def from_parts(
        *,
        repository: str,
        analyzed_range: AnalyzedRange,
        summary: Summary,
        tags_human: TagStat,
        tags_ai: TagStat,
        tags_human_plus_ai: TagStat,
        timeline: Iterable[TimelineMonth],
        integrity: Integrity,
        version: str = "1.0",
    ) -> "AuditResult":
        return AuditResult(
            version=version,
            repository=repository,
            analyzed_range=analyzed_range,
            summary=summary,
            tags_human=tags_human,
            tags_ai=tags_ai,
            tags_human_plus_ai=tags_human_plus_ai,
            timeline=tuple(timeline),
            integrity=integrity,
        )
