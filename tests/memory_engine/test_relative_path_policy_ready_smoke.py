from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.storage_layout_builders import (
    build_portable_storage_reference,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.storage_root_models import (
    StorageRoot,
)


def test_relative_path_policy_ready_smoke() -> None:
    root = StorageRoot(
        root_id="ROOT-LOCAL-001",
        root_type="local_ssd",
        root_path="/mnt/data/history",
        portable=True,
        relocation_ready=True,
        nas_ready=False,
    )
    ref = build_portable_storage_reference(
        storage_node_id="HSTORE-NORM-001",
        root=root,
        relative_path="normalized_history/HCHAT-0001.json",
    )

    assert not ref.relative_path.startswith("/")
