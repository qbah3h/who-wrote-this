from __future__ import annotations

import os
import subprocess
from datetime import date
from pathlib import Path

import pytest

from ai_commit_audit.analyzer import AnalyzeOptions, analyze_repository
from ai_commit_audit.exit_codes import ExitCode
from ai_commit_audit.exceptions import AuditError


def _run(cmd: list[str], cwd: Path, env: dict[str, str] | None = None) -> None:
    cp = subprocess.run(cmd, cwd=str(cwd), check=False, text=True, capture_output=True, env=env)
    assert cp.returncode == 0, cp.stderr


def _init_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    _run(["git", "init"], repo)
    _run(["git", "config", "user.email", "test@example.com"], repo)
    _run(["git", "config", "user.name", "Test"], repo)
    return repo


def _commit(repo: Path, msg: str, ymd: str) -> None:
    p = repo / "f.txt"
    p.write_text(msg + "\n", encoding="utf-8")
    _run(["git", "add", "f.txt"], repo)
    env = {
        **dict(os.environ),
        "GIT_AUTHOR_DATE": ymd + "T12:00:00",
        "GIT_COMMITTER_DATE": ymd + "T12:00:00",
    }
    _run(["git", "commit", "-m", msg], repo, env=env)


def test_analyze_repository_counts_and_timeline(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path)
    _commit(repo, "A [human]", "2024-01-10")
    _commit(repo, "B [ai]", "2024-01-11")
    _commit(repo, "C [human + ai]", "2024-02-01")
    _commit(repo, "D no tag", "2024-02-02")

    res = analyze_repository(str(repo), AnalyzeOptions(since=date(2024, 1, 1), until=date(2024, 12, 31)))

    assert res.summary.total_commits == 4
    assert res.summary.analyzed_commits == 3
    assert res.summary.unclassified_commits == 1

    assert res.tags_human.count == 1
    assert res.tags_ai.count == 1
    assert res.tags_human_plus_ai.count == 1

    assert [m.month for m in res.timeline] == ["2024-01", "2024-02"]


def test_analyze_repository_no_commits(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path)
    with pytest.raises(AuditError) as e:
        analyze_repository(str(repo), AnalyzeOptions())
    assert e.value.exit_code == ExitCode.NO_COMMITS_FOUND


def test_analyze_repository_no_tagged_commits(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path)
    _commit(repo, "A no tag", "2024-01-10")

    with pytest.raises(AuditError) as e:
        analyze_repository(str(repo), AnalyzeOptions())
    assert e.value.exit_code == ExitCode.NO_TAGGED_COMMITS_FOUND
