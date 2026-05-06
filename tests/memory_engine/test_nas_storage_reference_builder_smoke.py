from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.nas_storage_reference_builder import (
    build_nas_storage_reference_preview,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.storage_layout_builders import (
    build_portable_storage_reference,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.storage_root_models import (
    StorageRoot,
)


def test_nas_storage_reference_builder_smoke() -> None:
    root = StorageRoot(
        root_id="ROOT-NAS-001",
        root_type="nas_share",
        root_path="/mnt/nas/history",
        portable=True,
        relocation_ready=True,
        nas_ready=True,
    )
    ref = build_portable_storage_reference(
        storage_node_id="HSTORE-REG-001",
        root=root,
        relative_path="registry/import_manifest.json",
    )

    preview = build_nas_storage_reference_preview(ref, root)
    assert preview["nas_ready"] is True
