from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.storage_layout_builders import (
    build_portable_storage_reference,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.storage_root_models import (
    StorageRoot,
)


def test_manifest_portability_ready_smoke() -> None:
    root = StorageRoot(
        root_id="ROOT-M2-001",
        root_type="m2_ssd",
        root_path="/mnt/m2/history",
        portable=True,
        relocation_ready=True,
        nas_ready=False,
    )
    ref = build_portable_storage_reference(
        storage_node_id="HSTORE-REG-001",
        root=root,
        relative_path="registry/import_manifest.json",
    )

    assert ref.manifest_safe is True
