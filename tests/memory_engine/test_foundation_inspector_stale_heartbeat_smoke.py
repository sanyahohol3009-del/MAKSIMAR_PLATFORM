from __future__ import annotations

import json
import time
from pathlib import Path

from MAKSIMAR_CORE_LIB.memory_engine.foundation_inspector.runtime_reader import (
    MemoryRuntimeStatePaths,
    read_memory_foundation_inspector_state,
)


def test_foundation_inspector_stale_heartbeat_smoke(tmp_path: Path) -> None:
    """Old heartbeat must become stale and produce warning alert."""

    runtime_state_dir = tmp_path / "state"
    runtime_state_dir.mkdir(parents=True, exist_ok=True)

    heartbeat_file = runtime_state_dir / "memory_heartbeat_state.json"
    heartbeat_file.write_text(
        json.dumps(
            {
                "timestamp_wall": "2026-05-04T20:00:00Z",
                "timestamp_monotonic": time.monotonic() - 10.0,
                "pid": 12345,
                "status": "alive",
                "source": "memory_engine",
            }
        ),
        encoding="utf-8",
    )

    model = read_memory_foundation_inspector_state(
        paths=MemoryRuntimeStatePaths(
            runtime_state_dir=runtime_state_dir,
            heartbeat_file=heartbeat_file,
        ),
        memory_engine_alive=True,
        memory_registry_alive=True,
        retrieval_path_ready=True,
    )

    assert model.heartbeat.status == "stale"
    assert model.alert is not None
    assert model.alert.severity == "warning"
    assert model.alert.code == "memory_heartbeat_stale"
