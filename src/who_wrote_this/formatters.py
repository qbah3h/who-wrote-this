from __future__ import annotations

import csv
import io
import json
from datetime import date

from .models import AuditResult


def _fmt_date(d: date | None) -> str:
    return d.isoformat() if d else "(none)"


def format_table(result: AuditResult) -> str:
    since = _fmt_date(result.analyzed_range.since)
    until = _fmt_date(result.analyzed_range.until)

    lines: list[str] = []
    lines.append("Who Wrote This — v1")
    lines.append(f"Repository: {result.repository}")
    lines.append(f"Analyzed range: {since} → {until}")
    lines.append(f"Total commits found: {result.summary.total_commits}")
    lines.append(f"Commits analyzed: {result.summary.analyzed_commits}")
    lines.append(f"Unclassified commits: {result.summary.unclassified_commits}")
    lines.append("")

    lines.append("Tag            Commits    Percentage")
    lines.append("------------------------------------")
    lines.append(f"[human]           {result.tags_human.count:<5}     {result.tags_human.percentage:.1f}%")
    lines.append(f"[ai]              {result.tags_ai.count:<5}     {result.tags_ai.percentage:.1f}%")
    lines.append(
        f"[human + ai]       {result.tags_human_plus_ai.count:<5}     {result.tags_human_plus_ai.percentage:.1f}%"
    )
    lines.append("")

    lines.append("Timeline (by month)")
    lines.append("")
    lines.append("Month     [human]   [ai]   [human + ai]")
    lines.append("--------------------------------------")
    for m in result.timeline:
        lines.append(f"{m.month:<8} {m.human:>6} {m.ai:>6} {m.human_plus_ai:>12}")
    lines.append("")

    lines.append("Integrity notes:")
    lines.append(f"- {result.integrity.multiple_tags} commits contained multiple tags")
    lines.append(f"- {result.integrity.unknown_tags} commits used unknown tags")
    lines.append(f"- {result.integrity.ignored_commits} commits were ignored (no valid tag)")

    return "\n".join(lines) + "\n"


def format_json(result: AuditResult) -> str:
    payload = {
        "version": result.version,
        "repository": result.repository,
        "analyzed_range": {
            "since": result.analyzed_range.since.isoformat() if result.analyzed_range.since else None,
            "until": result.analyzed_range.until.isoformat() if result.analyzed_range.until else None,
        },
        "summary": {
            "total_commits": result.summary.total_commits,
            "analyzed_commits": result.summary.analyzed_commits,
            "unclassified_commits": result.summary.unclassified_commits,
        },
        "tags": {
            "human": {"count": result.tags_human.count, "percentage": round(result.tags_human.percentage, 1)},
            "ai": {"count": result.tags_ai.count, "percentage": round(result.tags_ai.percentage, 1)},
            "human_plus_ai": {
                "count": result.tags_human_plus_ai.count,
                "percentage": round(result.tags_human_plus_ai.percentage, 1),
            },
        },
        "timeline": [
            {
                "month": m.month,
                "human": m.human,
                "ai": m.ai,
                "human_plus_ai": m.human_plus_ai,
            }
            for m in result.timeline
        ],
        "integrity": {
            "multiple_tags": result.integrity.multiple_tags,
            "unknown_tags": result.integrity.unknown_tags,
            "ignored_commits": result.integrity.ignored_commits,
        },
    }
    return json.dumps(payload, indent=2, sort_keys=False) + "\n"


def format_csv_summary(result: AuditResult) -> str:
    buf = io.StringIO(newline="")
    w = csv.writer(buf)
    w.writerow(["tag", "count", "percentage"])
    w.writerow(["human", result.tags_human.count, f"{result.tags_human.percentage:.1f}"])
    w.writerow(["ai", result.tags_ai.count, f"{result.tags_ai.percentage:.1f}"])
    w.writerow(["human_plus_ai", result.tags_human_plus_ai.count, f"{result.tags_human_plus_ai.percentage:.1f}"])
    return buf.getvalue()


def format_csv_timeline(result: AuditResult) -> str:
    buf = io.StringIO(newline="")
    w = csv.writer(buf)
    w.writerow(["month", "human", "ai", "human_plus_ai"])
    for m in result.timeline:
        w.writerow([m.month, m.human, m.ai, m.human_plus_ai])
    return buf.getvalue()
