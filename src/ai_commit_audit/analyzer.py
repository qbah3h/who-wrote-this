from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from .models import AuditResult


@dataclass(frozen=True)
class AnalyzeOptions:
    since: date | None = None
    until: date | None = None
    author: str | None = None
    strict: bool = False


def analyze_repository(repo: str, options: AnalyzeOptions) -> AuditResult:
    raise NotImplementedError("Step 4 will implement Git parsing and aggregation.")
