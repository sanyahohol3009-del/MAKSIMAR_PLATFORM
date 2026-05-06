from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.portable_storage_reference_models import (
    PortableStorageReference,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.storage_root_models import (
    StorageRoot,
)


def build_relocated_absolute_path(
    reference: PortableStorageReference,
    new_root: StorageRoot,
) -> str:
    base = new_root.root_path.rstrip("/")
    rel = reference.relative_path.lstrip("/")
    return f"{base}/{rel}"


def build_relocation_preview(
    reference: PortableStorageReference,
    new_root: StorageRoot,
) -> Dict[str, object]:
    return {
        "storage_node_id": reference.storage_node_id,
        "old_root_id": reference.root_id,
        "new_root_id": new_root.root_id,
        "relative_path": reference.relative_path,
        "relocated_absolute_path": build_relocated_absolute_path(reference, new_root),
        "relocation_ready": True,
    }
