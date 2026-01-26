import json
from datetime import date

from ai_commit_audit.formatters import format_csv_summary, format_csv_timeline, format_json, format_table
from ai_commit_audit.models import (
    AnalyzedRange,
    AuditResult,
    Integrity,
    Summary,
    TagStat,
    TimelineMonth,
)


def _fixture_result() -> AuditResult:
    return AuditResult.from_parts(
        repository="https://github.com/user/repo",
        analyzed_range=AnalyzedRange(since=date(2024, 1, 1), until=date(2024, 12, 31)),
        summary=Summary(total_commits=342, analyzed_commits=324, unclassified_commits=18),
        tags_human=TagStat(count=143, percentage=44.1),
        tags_ai=TagStat(count=97, percentage=29.9),
        tags_human_plus_ai=TagStat(count=84, percentage=25.9),
        timeline=(
            TimelineMonth(month="2024-01", human=12, ai=4, human_plus_ai=3),
            TimelineMonth(month="2024-02", human=9, ai=6, human_plus_ai=5),
        ),
        integrity=Integrity(multiple_tags=5, unknown_tags=3, ignored_commits=18),
    )


def test_format_table_contains_expected_sections() -> None:
    out = format_table(_fixture_result())
    assert "AI Commit Audit — v1" in out
    assert "Repository: https://github.com/user/repo" in out
    assert "Analyzed range: 2024-01-01 → 2024-12-31" in out
    assert "Tag            Commits    Percentage" in out
    assert "Timeline (by month)" in out
    assert "Integrity notes:" in out


def test_format_json_schema_keys() -> None:
    data = json.loads(format_json(_fixture_result()))
    assert data["version"] == "1.0"
    assert data["repository"] == "https://github.com/user/repo"
    assert data["summary"]["total_commits"] == 342
    assert set(data["tags"].keys()) == {"human", "ai", "human_plus_ai"}
    assert isinstance(data["timeline"], list)


def test_format_csv_outputs_headers() -> None:
    summary_csv = format_csv_summary(_fixture_result())
    timeline_csv = format_csv_timeline(_fixture_result())
    assert summary_csv.splitlines()[0] == "tag,count,percentage"
    assert timeline_csv.splitlines()[0] == "month,human,ai,human_plus_ai"
