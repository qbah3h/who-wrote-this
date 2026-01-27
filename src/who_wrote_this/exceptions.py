from __future__ import annotations

from dataclasses import dataclass

from .exit_codes import ExitCode


@dataclass(frozen=True)
class AuditError(Exception):
    message: str
    exit_code: ExitCode

    def __str__(self) -> str:  # pragma: no cover
        return self.message
