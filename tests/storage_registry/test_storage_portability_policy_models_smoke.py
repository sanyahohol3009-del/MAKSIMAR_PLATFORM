from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.storage_registry import (
    build_storage_portability_policy,
)


def test_storage_portability_policy_models_smoke() -> None:
    policy = build_storage_portability_policy()

    assert policy.storage_node_portable is True
    assert policy.root_relocation_allowed is True
    assert policy.nas_ready_required is True
    assert policy.atomic_snapshot_required is True
