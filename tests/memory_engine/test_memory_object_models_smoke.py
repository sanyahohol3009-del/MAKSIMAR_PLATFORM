from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_object_models import (
    MemoryObject,
    MemorySource,
)


def test_memory_object_models_smoke() -> None:
    obj = MemoryObject(
        memory_id="INC-0001",
        memory_type="incident",
        title="Deep test polluted subprocess.run",
        one_line_summary="Global monkeypatch leak broke unrelated modules.",
        status="validated",
        truth_level="validated_project_fact",
        project_area=("testing", "runtime"),
        source=MemorySource(
            source_type="chat",
            source_ref="working_chat_runtime_track_02",
            timestamp_utc="2026-05-04T00:00:00Z",
        ),
        affects=("tests/runtime_core/test_core_guard.py",),
        next_step_id="TEST-HARDENING-01",
        next_step_summary="Require local restore for monkeypatch tests.",
        tags=("incident", "testing"),
    )

    assert obj.memory_type == "incident"
    assert obj.panel_ready is True
    assert obj.timeline_ready is True
    assert obj.filter_ready is True


def test_memory_object_models_reject_empty_affects() -> None:
    with pytest.raises(ValueError, match="affects must not be empty"):
        MemoryObject(
            memory_id="INC-0002",
            memory_type="incident",
            title="Bad object",
            one_line_summary="Bad",
            status="validated",
            truth_level="validated_project_fact",
            project_area=("testing",),
            source=MemorySource(
                source_type="chat",
                source_ref="track",
                timestamp_utc="2026-05-04T00:00:00Z",
            ),
            affects=(),
            next_step_id="STEP-1",
            next_step_summary="Fix",
            tags=("incident",),
        )
