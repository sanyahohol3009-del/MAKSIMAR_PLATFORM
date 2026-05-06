from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.portable_storage_reference_models import (
    PortableStorageReference,
)


def validate_portable_reference_ready(
    reference: PortableStorageReference,
) -> None:
    if not reference.portable:
        raise ValueError("Portable storage reference must be portable")
    if not reference.manifest_safe:
        raise ValueError("Portable storage reference must be manifest_safe")


def validate_nas_reference_ready(
    reference: PortableStorageReference,
) -> None:
    validate_portable_reference_ready(reference)
    if not reference.nas_ready:
        raise ValueError("Portable storage reference must be nas_ready")
