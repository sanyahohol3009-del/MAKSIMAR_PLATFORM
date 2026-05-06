from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_models import (
    ArchiveSource,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.content_fingerprint_builder import (
    build_content_fingerprint,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.file_fingerprint_builder import (
    build_file_fingerprint,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.fingerprint_registry_models import (
    FingerprintRegistry,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.unified_extraction_reader import (
    read_unified_extraction,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.unit_fingerprint_builder import (
    build_unit_fingerprint,
)


def build_fingerprint_registry_for_source(
    source: ArchiveSource,
) -> FingerprintRegistry:
    document = read_unified_extraction(source)

    file_fingerprint = build_file_fingerprint(source)
    content_fingerprint = build_content_fingerprint(document)
    unit_fingerprints = tuple(build_unit_fingerprint(content) for content in document.contents)

    return FingerprintRegistry(
        file_fingerprints=(file_fingerprint,),
        content_fingerprints=(content_fingerprint,),
        unit_fingerprints=unit_fingerprints,
    )


def build_fingerprint_preview(
    source: ArchiveSource,
) -> Dict[str, object]:
    registry = build_fingerprint_registry_for_source(source)
    return {
        "file_fingerprint_count": len(registry.file_fingerprints),
        "content_fingerprint_count": len(registry.content_fingerprints),
        "unit_fingerprint_count": len(registry.unit_fingerprints),
        "file_duplicate_detection_ready": registry.file_duplicate_detection_ready,
        "content_duplicate_detection_ready": registry.content_duplicate_detection_ready,
        "unit_duplicate_detection_ready": registry.unit_duplicate_detection_ready,
    }


def build_fingerprint_comparison_preview(
    left: ArchiveSource,
    right: ArchiveSource,
) -> Dict[str, object]:
    left_registry = build_fingerprint_registry_for_source(left)
    right_registry = build_fingerprint_registry_for_source(right)

    left_file = left_registry.file_fingerprints[0]
    right_file = right_registry.file_fingerprints[0]
    left_content = left_registry.content_fingerprints[0]
    right_content = right_registry.content_fingerprints[0]
    left_unit = left_registry.unit_fingerprints[0]
    right_unit = right_registry.unit_fingerprints[0]

    return {
        "same_file_fingerprint": left_file.sha256_hex == right_file.sha256_hex,
        "same_content_fingerprint": left_content.sha256_hex == right_content.sha256_hex,
        "same_unit_fingerprint": left_unit.sha256_hex == right_unit.sha256_hex,
    }
