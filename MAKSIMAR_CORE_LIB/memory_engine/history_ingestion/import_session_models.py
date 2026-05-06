from __future__ import annotations

from dataclasses import dataclass


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _ensure_non_negative_int(value: int, field_name: str) -> int:
    if value < 0:
        raise ValueError(f"{field_name} must be >= 0")
    return value


@dataclass(frozen=True)
class ImportSession:
    import_session_id: str
    source_id: str
    source_type: str
    source_path: str
    status: str
    segment_count: int
    content_count: int
    deterministic_output: bool
    parallel_safe_by_design: bool

    def __post_init__(self) -> None:
        import_session_id = _ensure_non_empty_str(
            self.import_session_id,
            "import_session_id",
        )
        source_id = _ensure_non_empty_str(self.source_id, "source_id")
        source_type = _ensure_non_empty_str(self.source_type, "source_type")
        source_path = _ensure_non_empty_str(self.source_path, "source_path")
        status = _ensure_non_empty_str(self.status, "status")
        segment_count = _ensure_non_negative_int(self.segment_count, "segment_count")
        content_count = _ensure_non_negative_int(self.content_count, "content_count")

        if status not in ("prepared", "completed"):
            raise ValueError("status must be 'prepared' or 'completed'")

        if not self.deterministic_output:
            raise ValueError("deterministic_output must be True")

        if not self.parallel_safe_by_design:
            raise ValueError("parallel_safe_by_design must be True")

        object.__setattr__(self, "import_session_id", import_session_id)
        object.__setattr__(self, "source_id", source_id)
        object.__setattr__(self, "source_type", source_type)
        object.__setattr__(self, "source_path", source_path)
        object.__setattr__(self, "status", status)
        object.__setattr__(self, "segment_count", segment_count)
        object.__setattr__(self, "content_count", content_count)
