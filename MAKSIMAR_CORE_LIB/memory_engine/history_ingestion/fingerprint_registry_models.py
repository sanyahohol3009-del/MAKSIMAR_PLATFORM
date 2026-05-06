from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.fingerprint_models import (
    ContentFingerprint,
    FileFingerprint,
    UnitFingerprint,
)


@dataclass(frozen=True)
class FingerprintRegistry:
    file_fingerprints: Tuple[FileFingerprint, ...]
    content_fingerprints: Tuple[ContentFingerprint, ...]
    unit_fingerprints: Tuple[UnitFingerprint, ...]

    def __post_init__(self) -> None:
        file_hashes = [fp.sha256_hex for fp in self.file_fingerprints]
        content_hashes = [fp.sha256_hex for fp in self.content_fingerprints]
        unit_hashes = [fp.sha256_hex for fp in self.unit_fingerprints]

        if len(file_hashes) != len(set(file_hashes)):
            raise ValueError("file_fingerprints must not contain duplicate sha256 values")

        if len(content_hashes) != len(set(content_hashes)):
            raise ValueError("content_fingerprints must not contain duplicate sha256 values")

        if len(unit_hashes) != len(set(unit_hashes)):
            raise ValueError("unit_fingerprints must not contain duplicate sha256 values")

    @property
    def file_duplicate_detection_ready(self) -> bool:
        return True

    @property
    def content_duplicate_detection_ready(self) -> bool:
        return True

    @property
    def unit_duplicate_detection_ready(self) -> bool:
        return True
