from __future__ import annotations

import argparse
import sys
from datetime import date

from .analyzer import AnalyzeOptions, analyze_repository
from .exceptions import AuditError
from .exit_codes import ExitCode
from .formatters import format_csv_summary, format_csv_timeline, format_json, format_table


def _parse_date(s: str | None) -> date | None:
    if not s:
        return None
    return date.fromisoformat(s)


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="ai-commit-audit")
    sub = p.add_subparsers(dest="command", required=True)

    a = sub.add_parser("analyze")
    a.add_argument("repo")
    a.add_argument("--since")
    a.add_argument("--until")
    a.add_argument("--author")
    a.add_argument("--format", default="table", choices=["table", "json", "csv"])
    a.add_argument("--out")
    a.add_argument("--strict", action="store_true")

    return p


def main(argv: list[str] | None = None) -> None:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command != "analyze":
        raise SystemExit(int(ExitCode.SUCCESS))

    options = AnalyzeOptions(
        since=_parse_date(args.since),
        until=_parse_date(args.until),
        author=args.author,
        strict=bool(args.strict),
    )

    try:
        result = analyze_repository(args.repo, options)
    except AuditError as e:
        sys.stderr.write(str(e) + "\n")
        raise SystemExit(int(e.exit_code))

    if args.format == "table":
        output = format_table(result)
        if args.out:
            with open(args.out, "w", encoding="utf-8", newline="\n") as f:
                f.write(output)
        else:
            sys.stdout.write(output)
        raise SystemExit(int(ExitCode.SUCCESS))

    if args.format == "json":
        output = format_json(result)
        if args.out:
            with open(args.out, "w", encoding="utf-8", newline="\n") as f:
                f.write(output)
        else:
            sys.stdout.write(output)
        raise SystemExit(int(ExitCode.SUCCESS))

    if args.format == "csv":
        summary_csv = format_csv_summary(result)
        timeline_csv = format_csv_timeline(result)

        if args.out:
            base = args.out
            if base.lower().endswith(".csv"):
                base = base[: -len(".csv")]

            with open(base + "_summary.csv", "w", encoding="utf-8", newline="") as f:
                f.write(summary_csv)
            with open(base + "_timeline.csv", "w", encoding="utf-8", newline="") as f:
                f.write(timeline_csv)
        else:
            sys.stdout.write(summary_csv)
            sys.stdout.write("\n")
            sys.stdout.write(timeline_csv)

        raise SystemExit(int(ExitCode.SUCCESS))

    raise SystemExit(int(ExitCode.SUCCESS))
