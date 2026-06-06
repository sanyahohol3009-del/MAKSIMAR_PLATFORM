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

    assert "JARVIS_LIVE_CI_STATUS" in output
    assert "JARVIS_DRIFT_GUARD_OK=true" in output
    assert "READY_BATCHES=JL-0,JL-1" in output
    assert "NEXT_BATCH=JL-2" in output
    assert "MODEL_DOWNLOAD_ALLOWED=false" in output
    assert "VOICE_ALLOWED=false" in output
    assert "PC_CONTROL_ALLOWED=false" in output
    assert "XRAY_COMMAND=" in output
    assert "DRIFT_COMMAND=" in output
    assert "FULL_AUTO_COMMAND=" in output

