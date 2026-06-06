from __future__ import annotations

from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.jarvis_live_full_roadmap_status_builder import (
    build_jarvis_live_full_roadmap_status,
)
from tools.project_readiness_control.jarvis_live_ci_status import (
    render_jarvis_live_ci_status,
)


def test_jarvis_live_ci_status_render_is_operator_readable() -> None:
    status = build_jarvis_live_full_roadmap_status()
    output = render_jarvis_live_ci_status(status)

    ready_batches = ",".join(status["ready_batches"])
    next_batch = status["next_batch"]
    assert next_batch is not None

    assert "JARVIS_LIVE_CI_STATUS" in output
    assert "JARVIS_DRIFT_GUARD_OK=true" in output
    assert f"READY_BATCHES={ready_batches}" in output
    assert f"NEXT_BATCH={next_batch['batch_id']}" in output
    assert "MODEL_DOWNLOAD_ALLOWED=false" in output
    assert "RUNTIME_START_ALLOWED=false" in output
    assert "VOICE_ALLOWED=false" in output
    assert "PC_CONTROL_ALLOWED=false" in output
    assert "XRAY_COMMAND=" in output
    assert "DRIFT_COMMAND=" in output
    assert "FULL_AUTO_COMMAND=" in output
    assert "FORBIDDEN_PARALLEL_WORLD_ROOTS_PRESENT=NONE" in output


def test_jarvis_live_ci_status_reports_current_next_batch_dynamically() -> None:
    status = build_jarvis_live_full_roadmap_status()
    output = render_jarvis_live_ci_status(status)

    next_batch = status["next_batch"]
    assert next_batch is not None

    assert f"READY_BATCHES={','.join(status['ready_batches'])}" in output
    assert f"NEXT_BATCH={next_batch['batch_id']}" in output

    if "JL-4" in status["ready_batches"]:
        assert "NEXT_BATCH=JL-5" in output
    elif "JL-3" in status["ready_batches"]:
        assert "NEXT_BATCH=JL-4" in output
