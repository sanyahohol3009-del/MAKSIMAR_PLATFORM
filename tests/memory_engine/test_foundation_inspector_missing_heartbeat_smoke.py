from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.memory_engine.foundation_inspector.runtime_reader import (
    MemoryRuntimeStatePaths,
    read_memory_foundation_inspector_state,
)


def test_foundation_inspector_missing_heartbeat_smoke(tmp_path: Path) -> None:
    """Missing heartbeat must build a safe read model with critical alert."""

    runtime_state_dir = tmp_path / "state"
    runtime_state_dir.mkdir(parents=True, exist_ok=True)

    heartbeat_file = runtime_state_dir / "memory_heartbeat_state.json"

    model = read_memory_foundation_inspector_state(
        paths=MemoryRuntimeStatePaths(
            runtime_state_dir=runtime_state_dir,
            heartbeat_file=heartbeat_file,
        ),
        memory_engine_alive=False,
        memory_registry_alive=False,
        retrieval_path_ready=False,
    )

    assert model.heartbeat.status == "missing"
    assert model.alert is not None
    assert model.alert.severity == "critical"
    assert model.alert.code == "memory_heartbeat_missing"
