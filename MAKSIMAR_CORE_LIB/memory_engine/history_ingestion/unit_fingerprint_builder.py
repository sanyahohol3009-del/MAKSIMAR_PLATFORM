from __future__ import annotations

import hashlib

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.extracted_content_models import (
    ExtractedContent,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.fingerprint_models import (
    UnitFingerprint,
)


def _fingerprint_id(prefix: str, payload: str) -> str:
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return f"{prefix}-{digest[:12].upper()}"


def build_unit_fingerprint(content: ExtractedContent) -> UnitFingerprint:
    payload = (
        f"{content.content_kind}|{content.source_type}|"
        f"{content.byte_length_hint}|{content.text or ''}"
    )
    sha256_hex = hashlib.sha256(payload.encode("utf-8")).hexdigest()

    return UnitFingerprint(
        fingerprint_id=_fingerprint_id("HUNITFP", payload),
        fingerprint_kind="unit_fingerprint",
        unit_id=content.content_id,
        sha256_hex=sha256_hex,
        deterministic=True,
        parallel_safe_by_design=True,
    )
