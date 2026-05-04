from __future__ import annotations

import json
import time
from pathlib import Path

from MAKSIMAR_CORE_LIB.memory_engine.foundation_inspector.models import (
    MemoryObjectPreview,
)
from MAKSIMAR_CORE_LIB.memory_engine.foundation_inspector.runtime_reader import (
    MemoryRuntimeStatePaths,
    read_memory_foundation_inspector_state,
)
from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.foundation_inspector_read_model import (
    MemoryFoundationInspectorObservabilityView,
)
from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.foundation_inspector_summary_builder import (
    build_memory_foundation_inspector_summary,
)


def test_foundation_inspector_smoke(tmp_path: Path) -> None:
    """Smoke test for the canonical memory foundation inspector read path."""

    runtime_state_dir = tmp_path / "state"
    runtime_state_dir.mkdir(parents=True, exist_ok=True)

    heartbeat_file = runtime_state_dir / "memory_heartbeat_state.json"
    heartbeat_file.write_text(
        json.dumps(
            {
                "timestamp_wall": "2026-05-04T20:00:00Z",
                "timestamp_monotonic": time.monotonic(),
                "pid": 12345,
                "status": "alive",
                "source": "memory_engine",
            }
        ),
        encoding="utf-8",
    )

    preview = MemoryObjectPreview(
        memory_id="ARCH-0001",
        memory_type="architecture_decision",
        title="Runtime truth path fixed",
        one_line_summary="Runtime truth path stabilized.",
        truth_level="validated_project_fact",
        status="validated",
    )

    model = read_memory_foundation_inspector_state(
        paths=MemoryRuntimeStatePaths(
            runtime_state_dir=runtime_state_dir,
            heartbeat_file=heartbeat_file,
        ),
        memory_engine_alive=True,
        memory_registry_alive=True,
        retrieval_path_ready=True,
        preview=preview,
    )

    assert model.heartbeat.source_name == "memory_engine"
    assert model.heartbeat.status in {"fresh", "stale"}
    assert model.memory_engine_alive is True
    assert model.memory_registry_alive is True
    assert model.retrieval_path_ready is True
    assert model.preview is not None
    assert model.preview.memory_id == "ARCH-0001"

    view = MemoryFoundationInspectorObservabilityView(read_model=model)
    summary = build_memory_foundation_inspector_summary(view)

    assert "heartbeat=" in summary
    assert "memory_engine_alive=True" in summary
    assert "preview=ARCH-0001" in summary
