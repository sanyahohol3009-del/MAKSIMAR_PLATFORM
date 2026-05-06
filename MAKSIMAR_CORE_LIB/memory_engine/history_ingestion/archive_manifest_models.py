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
class ArchiveManifest:
    manifest_id: str
    import_session_id: str
    source_id: str
    source_type: str
    document_id: str
    segment_count: int
    content_count: int
    extraction_path: str
    deterministic_output: bool
    parallel_safe_by_design: bool

    def __post_init__(self) -> None:
        manifest_id = _ensure_non_empty_str(self.manifest_id, "manifest_id")
        import_session_id = _ensure_non_empty_str(
            self.import_session_id,
            "import_session_id",
        )
        source_id = _ensure_non_empty_str(self.source_id, "source_id")
        source_type = _ensure_non_empty_str(self.source_type, "source_type")
        document_id = _ensure_non_empty_str(self.document_id, "document_id")
        extraction_path = _ensure_non_empty_str(
            self.extraction_path,
            "extraction_path",
        )
        segment_count = _ensure_non_negative_int(segment_count := self.segment_count, "segment_count")
        content_count = _ensure_non_negative_int(content_count := self.content_count, "content_count")

        if not self.deterministic_output:
            raise ValueError("deterministic_output must be True")

        if not self.parallel_safe_by_design:
            raise ValueError("parallel_safe_by_design must be True")

        object.__setattr__(self, "manifest_id", manifest_id)
        object.__setattr__(self, "import_session_id", import_session_id)
        object.__setattr__(self, "source_id", source_id)
        object.__setattr__(self, "source_type", source_type)
        object.__setattr__(self, "document_id", document_id)
        object.__setattr__(self, "extraction_path", extraction_path)
        object.__setattr__(self, "segment_count", segment_count)
        object.__setattr__(self, "content_count", content_count)
