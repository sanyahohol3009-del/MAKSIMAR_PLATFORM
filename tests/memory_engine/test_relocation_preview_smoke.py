from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.storage_layout_builders import (
    build_portable_storage_reference,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.storage_relocation_builder import (
    build_relocation_preview,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.storage_root_models import (
    StorageRoot,
)


def test_relocation_preview_smoke() -> None:
    old_root = StorageRoot(
        root_id="ROOT-LOCAL-001",
        root_type="local_ssd",
        root_path="/mnt/data/history",
        portable=True,
        relocation_ready=True,
        nas_ready=False,
    )
    new_root = StorageRoot(
        root_id="ROOT-M2-001",
        root_type="m2_ssd",
        root_path="/mnt/m2/history",
        portable=True,
        relocation_ready=True,
        nas_ready=False,
    )
    ref = build_portable_storage_reference(
        storage_node_id="HSTORE-REG-001",
        root=old_root,
        relative_path="registry/import_manifest.json",
    )
    preview = build_relocation_preview(ref, new_root)

    assert preview["relocation_ready"] is True
    assert preview["new_root_id"] == "ROOT-M2-001"
