from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


FingerprintKind = Literal[
    "file_fingerprint",
    "content_fingerprint",
    "unit_fingerprint",
]


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _ensure_sha256_hex(value: str, field_name: str) -> str:
    normalized = _ensure_non_empty_str(value, field_name).lower()
    if len(normalized) != 64:
        raise ValueError(f"{field_name} must be a 64-character sha256 hex digest")
    for char in normalized:
        if char not in "0123456789abcdef":
            raise ValueError(f"{field_name} must contain only lowercase hex characters")
    return normalized


@dataclass(frozen=True)
class FileFingerprint:
    fingerprint_id: str
    fingerprint_kind: FingerprintKind
    source_id: str
    sha256_hex: str
    deterministic: bool
    parallel_safe_by_design: bool

    def __post_init__(self) -> None:
        fingerprint_id = _ensure_non_empty_str(self.fingerprint_id, "fingerprint_id")
        source_id = _ensure_non_empty_str(self.source_id, "source_id")
        sha256_hex = _ensure_sha256_hex(self.sha256_hex, "sha256_hex")

        if self.fingerprint_kind != "file_fingerprint":
            raise ValueError("fingerprint_kind must be 'file_fingerprint'")

        if not self.deterministic:
            raise ValueError("deterministic must be True")

        if not self.parallel_safe_by_design:
            raise ValueError("parallel_safe_by_design must be True")

        object.__setattr__(self, "fingerprint_id", fingerprint_id)
        object.__setattr__(self, "source_id", source_id)
        object.__setattr__(self, "sha256_hex", sha256_hex)


@dataclass(frozen=True)
class ContentFingerprint:
    fingerprint_id: str
    fingerprint_kind: FingerprintKind
    document_id: str
    sha256_hex: str
    deterministic: bool
    parallel_safe_by_design: bool

    def __post_init__(self) -> None:
        fingerprint_id = _ensure_non_empty_str(self.fingerprint_id, "fingerprint_id")
        document_id = _ensure_non_empty_str(self.document_id, "document_id")
        sha256_hex = _ensure_sha256_hex(self.sha256_hex, "sha256_hex")

        if self.fingerprint_kind != "content_fingerprint":
            raise ValueError("fingerprint_kind must be 'content_fingerprint'")

        if not self.deterministic:
            raise ValueError("deterministic must be True")

        if not self.parallel_safe_by_design:
            raise ValueError("parallel_safe_by_design must be True")

        object.__setattr__(self, "fingerprint_id", fingerprint_id)
        object.__setattr__(self, "document_id", document_id)
        object.__setattr__(self, "sha256_hex", sha256_hex)


@dataclass(frozen=True)
class UnitFingerprint:
    fingerprint_id: str
    fingerprint_kind: FingerprintKind
    unit_id: str
    sha256_hex: str
    deterministic: bool
    parallel_safe_by_design: bool

    def __post_init__(self) -> None:
        fingerprint_id = _ensure_non_empty_str(self.fingerprint_id, "fingerprint_id")
        unit_id = _ensure_non_empty_str(self.unit_id, "unit_id")
        sha256_hex = _ensure_sha256_hex(self.sha256_hex, "sha256_hex")

        if self.fingerprint_kind != "unit_fingerprint":
            raise ValueError("fingerprint_kind must be 'unit_fingerprint'")

        if not self.deterministic:
            raise ValueError("deterministic must be True")

        if not self.parallel_safe_by_design:
            raise ValueError("parallel_safe_by_design must be True")

        object.__setattr__(self, "fingerprint_id", fingerprint_id)
        object.__setattr__(self, "unit_id", unit_id)
        object.__setattr__(self, "sha256_hex", sha256_hex)
