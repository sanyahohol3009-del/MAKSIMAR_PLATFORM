from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.storage_layout_builders import (
    build_portable_storage_reference,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.storage_root_models import (
    StorageRoot,
)


def test_nas_readiness_smoke() -> None:
    root = StorageRoot(
        root_id="ROOT-NAS-001",
        root_type="nas_share",
        root_path="/mnt/nas/history",
        portable=True,
        relocation_ready=True,
        nas_ready=True,
    )
    ref = build_portable_storage_reference(
        storage_node_id="HSTORE-NORM-001",
        root=root,
        relative_path="normalized_history/HCHAT-0001.json",
    )

    assert ref.nas_ready is True
