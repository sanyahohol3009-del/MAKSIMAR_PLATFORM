from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


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
class ArchiveSourceMetadata:
    source_id: str
    source_name: str
    source_path: str
    file_size_bytes: int
    content_hash_sha256: Optional[str]
    imported_from_user_export: bool = True

    def __post_init__(self) -> None:
        source_id = _ensure_non_empty_str(self.source_id, "source_id")
        source_name = _ensure_non_empty_str(self.source_name, "source_name")
        source_path = _ensure_non_empty_str(self.source_path, "source_path")
        file_size_bytes = _ensure_non_negative_int(
            self.file_size_bytes,
            "file_size_bytes",
        )

        content_hash_sha256 = self.content_hash_sha256
        if content_hash_sha256 is not None:
            content_hash_sha256 = _ensure_non_empty_str(
                content_hash_sha256,
                "content_hash_sha256",
            )

        object.__setattr__(self, "source_id", source_id)
        object.__setattr__(self, "source_name", source_name)
        object.__setattr__(self, "source_path", source_path)
        object.__setattr__(self, "file_size_bytes", file_size_bytes)
        object.__setattr__(self, "content_hash_sha256", content_hash_sha256)

    @property
    def hash_available(self) -> bool:
        return self.content_hash_sha256 is not None
