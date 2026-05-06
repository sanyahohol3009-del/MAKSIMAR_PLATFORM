from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.fingerprint_models import (
    ContentFingerprint,
    FileFingerprint,
    UnitFingerprint,
)


VALID_SHA = "a" * 64


def test_fingerprint_models_smoke() -> None:
    file_fp = FileFingerprint(
        fingerprint_id="HFILEFP-0001",
        fingerprint_kind="file_fingerprint",
        source_id="HSOURCE-0001",
        sha256_hex=VALID_SHA,
        deterministic=True,
        parallel_safe_by_design=True,
    )
    content_fp = ContentFingerprint(
        fingerprint_id="HCONTENTFP-0001",
        fingerprint_kind="content_fingerprint",
        document_id="HDOC-0001",
        sha256_hex=VALID_SHA,
        deterministic=True,
        parallel_safe_by_design=True,
    )
    unit_fp = UnitFingerprint(
        fingerprint_id="HUNITFP-0001",
        fingerprint_kind="unit_fingerprint",
        unit_id="HCONTENT-0001",
        sha256_hex=VALID_SHA,
        deterministic=True,
        parallel_safe_by_design=True,
    )

    assert file_fp.fingerprint_kind == "file_fingerprint"
    assert content_fp.fingerprint_kind == "content_fingerprint"
    assert unit_fp.fingerprint_kind == "unit_fingerprint"


def test_fingerprint_models_reject_bad_sha_length() -> None:
    with pytest.raises(ValueError, match="sha256_hex must be a 64-character sha256 hex digest"):
        FileFingerprint(
            fingerprint_id="HFILEFP-0002",
            fingerprint_kind="file_fingerprint",
            source_id="HSOURCE-0002",
            sha256_hex="short",
            deterministic=True,
            parallel_safe_by_design=True,
        )
