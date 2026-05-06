from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.storage_layout_builders import (
    build_portable_storage_reference,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.storage_relocation_builder import (
    build_relocated_absolute_path,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.storage_root_models import (
    StorageRoot,
)


def test_storage_relocation_ready_smoke() -> None:
    old_root = StorageRoot(
        root_id="ROOT-LOCAL-001",
        root_type="local_ssd",
        root_path="/mnt/data/history",
        portable=True,
        relocation_ready=True,
        nas_ready=False,
    )
    nas_root = StorageRoot(
        root_id="ROOT-NAS-001",
        root_type="nas_share",
        root_path="/mnt/nas/history",
        portable=True,
        relocation_ready=True,
        nas_ready=True,
    )

    ref = build_portable_storage_reference(
        storage_node_id="HSTORE-RAW-001",
        root=old_root,
        relative_path="raw/input/export1.html",
    )

    relocated = build_relocated_absolute_path(ref, nas_root)
    assert relocated == "/mnt/nas/history/raw/input/export1.html"
