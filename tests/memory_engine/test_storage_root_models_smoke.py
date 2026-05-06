from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.storage_root_models import (
    StorageRoot,
)


def test_storage_root_models_smoke() -> None:
    root = StorageRoot(
        root_id="ROOT-LOCAL-001",
        root_type="local_ssd",
        root_path="/mnt/data/history",
        portable=True,
        relocation_ready=True,
        nas_ready=False,
    )

    assert root.root_type == "local_ssd"
    assert root.relocation_ready is True
