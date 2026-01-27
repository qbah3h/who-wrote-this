from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum


class TagCategory(str, Enum):
    HUMAN = "human"
    AI = "ai"
    HUMAN_PLUS_AI = "human_plus_ai"


_KNOWN = {
    "human": TagCategory.HUMAN,
    "ai": TagCategory.AI,
    "human+ai": TagCategory.HUMAN_PLUS_AI,
    "human + ai": TagCategory.HUMAN_PLUS_AI,
}


_TAG_TOKEN_RE = re.compile(r"\[([^\]]+)\]")


def _normalize_token(token: str) -> str:
    t = token.strip().lower()
    t = re.sub(r"\s+", " ", t)
    t = re.sub(r"\s*\+\s*", " + ", t)
    t = t.replace(" + ", " + ")
    if t == "human + ai":
        return "human + ai"
    if t == "human+ai":
        return "human+ai"
    return t


@dataclass(frozen=True)
class ParsedTags:
    recognized: tuple[TagCategory, ...]
    unknown_tags: int


def parse_tags(subject: str) -> ParsedTags:
    tokens = _TAG_TOKEN_RE.findall(subject)
    recognized: list[TagCategory] = []
    unknown = 0

    for tok in tokens:
        norm = _normalize_token(tok)
        if norm in _KNOWN:
            recognized.append(_KNOWN[norm])
            continue

        # Only count as "unknown" if it looks like an attempt to tag human/ai.
        if "human" in norm or norm == "ai" or " ai" in norm or "ai " in norm:
            unknown += 1

    return ParsedTags(recognized=tuple(recognized), unknown_tags=unknown)
