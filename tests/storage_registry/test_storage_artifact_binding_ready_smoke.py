from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.storage_registry import (
    build_storage_registry_preview,
)
from MAKSIMAR_SERVER.EXECUTION_CONTROL.artifact_routing import (
    build_storage_artifact_routing_binding_preview,
)


def test_storage_artifact_binding_ready_smoke() -> None:
    storage_preview = build_storage_registry_preview()
    binding_preview = build_storage_artifact_routing_binding_preview()

    assert storage_preview["storage_ready_for_m2_nas"] is True
    assert binding_preview["binding_ready"] is True
    assert binding_preview["storage_required_entries"] >= 1
    assert binding_preview["storage_ready_entries"] == binding_preview["storage_required_entries"]
