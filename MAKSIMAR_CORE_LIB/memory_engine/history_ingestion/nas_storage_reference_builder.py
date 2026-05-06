from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.portable_storage_reference_models import (
    PortableStorageReference,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.storage_layout_validators import (
    validate_nas_reference_ready,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.storage_root_models import (
    StorageRoot,
)


def build_nas_storage_reference_preview(
    reference: PortableStorageReference,
    root: StorageRoot,
) -> Dict[str, object]:
    validate_nas_reference_ready(reference)
    return {
        "storage_node_id": reference.storage_node_id,
        "root_id": root.root_id,
        "root_type": root.root_type,
        "relative_path": reference.relative_path,
        "nas_ready": reference.nas_ready,
    }
