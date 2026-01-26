from __future__ import annotations

import re
import subprocess
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class GitCommit:
    sha: str
    authored_datetime: datetime
    author_name: str
    author_email: str
    subject: str


_GIT_RECORD_SEP = "\x1e"
_GIT_FIELD_SEP = "\x1f"


def _is_probably_url(repo: str) -> bool:
    return bool(re.match(r"^https?://", repo, re.IGNORECASE))


def _run_git(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        check=False,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )


def _clone_repo(url: str) -> tempfile.TemporaryDirectory[str]:
    td = tempfile.TemporaryDirectory(prefix="ai_commit_audit_")
    dest = Path(td.name)

    cp = subprocess.run(
        ["git", "clone", "--no-tags", url, str(dest)],
        check=False,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )

    if cp.returncode != 0:
        td.cleanup()
        raise RuntimeError(cp.stderr.strip() or "git clone failed")

    return td


def iter_commits(
    repo: str,
    *,
    since: str | None = None,
    until: str | None = None,
    author: str | None = None,
) -> Iterable[GitCommit]:
    temp_dir: tempfile.TemporaryDirectory[str] | None = None

    try:
        if _is_probably_url(repo):
            temp_dir = _clone_repo(repo)
            repo_path = Path(temp_dir.name)
        else:
            repo_path = Path(repo)

        fmt = f"%H{_GIT_FIELD_SEP}%aI{_GIT_FIELD_SEP}%an{_GIT_FIELD_SEP}%ae{_GIT_FIELD_SEP}%s{_GIT_RECORD_SEP}"
        args = ["log", f"--pretty=format:{fmt}"]

        if since:
            args.append(f"--since={since}")
        if until:
            args.append(f"--until={until}")
        if author:
            args.append(f"--author={author}")

        cp = _run_git(args, cwd=repo_path)
        if cp.returncode != 0:
            err = (cp.stderr or "").strip()
            if "does not have any commits yet" in err:
                return
            raise RuntimeError(err or "git log failed")

        raw = cp.stdout
        if not raw.strip():
            return

        for rec in raw.split(_GIT_RECORD_SEP):
            if not rec:
                continue
            parts = rec.split(_GIT_FIELD_SEP)
            if len(parts) != 5:
                continue
            sha, authored_iso, author_name, author_email, subject = parts
            try:
                dt = datetime.fromisoformat(authored_iso.replace("Z", "+00:00"))
            except ValueError:
                continue
            yield GitCommit(
                sha=sha,
                authored_datetime=dt,
                author_name=author_name,
                author_email=author_email,
                subject=subject,
            )
    finally:
        if temp_dir is not None:
            temp_dir.cleanup()
