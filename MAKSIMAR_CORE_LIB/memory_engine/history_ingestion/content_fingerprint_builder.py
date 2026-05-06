from __future__ import annotations

import hashlib

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.extracted_document_models import (
    ExtractedDocument,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.fingerprint_models import (
    ContentFingerprint,
)


def _fingerprint_id(prefix: str, payload: str) -> str:
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return f"{prefix}-{digest[:12].upper()}"


def build_content_fingerprint(document: ExtractedDocument) -> ContentFingerprint:
    normalized_parts = []
    for content in document.contents:
        normalized_parts.append(
            f"{content.content_kind}|{content.source_type}|{content.byte_length_hint}|{content.text or ''}"
        )

    payload = "||".join(normalized_parts)
    sha256_hex = hashlib.sha256(payload.encode("utf-8")).hexdigest()

    return ContentFingerprint(
        fingerprint_id=_fingerprint_id("HCONTENTFP", payload),
        fingerprint_kind="content_fingerprint",
        document_id=document.document_id,
        sha256_hex=sha256_hex,
        deterministic=True,
        parallel_safe_by_design=True,
    )
