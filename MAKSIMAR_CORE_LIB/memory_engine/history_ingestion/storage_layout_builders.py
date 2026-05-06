from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.portable_storage_reference_models import (
    PortableStorageReference,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.storage_layout_validators import (
    validate_portable_reference_ready,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.storage_root_models import (
    StorageRoot,
)


def build_portable_storage_reference(
    *,
    storage_node_id: str,
    root: StorageRoot,
    relative_path: str,
) -> PortableStorageReference:
    reference = PortableStorageReference(
        storage_node_id=storage_node_id,
        root_id=root.root_id,
        relative_path=relative_path,
        portable=True,
        manifest_safe=True,
        nas_ready=root.nas_ready,
    )
    validate_portable_reference_ready(reference)
    return reference


def build_portable_storage_preview(
    reference: PortableStorageReference,
) -> Dict[str, object]:
    return {
        "storage_node_id": reference.storage_node_id,
        "root_id": reference.root_id,
        "relative_path": reference.relative_path,
        "portable": reference.portable,
        "manifest_safe": reference.manifest_safe,
        "nas_ready": reference.nas_ready,
    }
