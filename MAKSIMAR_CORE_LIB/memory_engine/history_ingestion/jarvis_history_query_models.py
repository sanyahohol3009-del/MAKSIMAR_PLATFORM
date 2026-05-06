from __future__ import annotations

from dataclasses import dataclass


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


@dataclass(frozen=True)
class JarvisHistoryQuery:
    query_text: str
    query_scope: str
    query_ready: bool

    def __post_init__(self) -> None:
        query_text = _ensure_non_empty_str(self.query_text, "query_text")
        query_scope = _ensure_non_empty_str(self.query_scope, "query_scope")
        if not self.query_ready:
            raise ValueError("query_ready must be True")

        object.__setattr__(self, "query_text", query_text)
        object.__setattr__(self, "query_scope", query_scope)
