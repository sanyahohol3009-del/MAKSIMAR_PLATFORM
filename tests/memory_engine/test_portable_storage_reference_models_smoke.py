from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.portable_storage_reference_models import (
    PortableStorageReference,
)


def test_portable_storage_reference_models_smoke() -> None:
    ref = PortableStorageReference(
        storage_node_id="HSTORE-NORM-001",
        root_id="ROOT-LOCAL-001",
        relative_path="normalized_history/HCHAT-0001.json",
        portable=True,
        manifest_safe=True,
        nas_ready=False,
    )

    assert ref.relative_path == "normalized_history/HCHAT-0001.json"
