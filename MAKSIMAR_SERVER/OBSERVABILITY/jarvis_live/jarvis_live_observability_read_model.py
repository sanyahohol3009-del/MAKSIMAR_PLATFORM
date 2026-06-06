from __future__ import annotations

from typing import Any

from MAKSIMAR_CORE_LIB.oob_dashboard.jarvis_live_status_panel_contract import (
    build_jarvis_live_status_panel_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.jarvis_model_status_panel_contract import (
    build_jarvis_model_status_panel_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.jarvis_queue_status_panel_contract import (
    build_jarvis_queue_status_panel_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.jarvis_resource_status_panel_contract import (
    build_jarvis_resource_status_panel_contract,
)
from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.jarvis_live_full_roadmap_status_builder import (
    build_jarvis_live_full_roadmap_status,
)


def build_jarvis_live_observability_read_model() -> dict[str, Any]:
    roadmap_status = build_jarvis_live_full_roadmap_status()
    live_panel = build_jarvis_live_status_panel_contract(roadmap_status).to_read_model()
    model_panel = build_jarvis_model_status_panel_contract().to_read_model()
    resource_panel = build_jarvis_resource_status_panel_contract().to_read_model()
    queue_panel = build_jarvis_queue_status_panel_contract().to_read_model()

    return {
        "summary_id": "jarvis_live_observability_read_model_v0_1",
        "read_only": True,
        "dashboard_safe": True,
        "dashboard_execution_allowed": False,
        "runtime_start_allowed": bool(roadmap_status["runtime_start_allowed_now"]),
        "model_download_allowed": bool(roadmap_status["model_download_allowed_now"]),
        "live_status_panel": live_panel,
        "model_status_panel": model_panel,
        "resource_status_panel": resource_panel,
        "queue_status_panel": queue_panel,
        "ready_batches": roadmap_status["ready_batches"],
        "next_batch": roadmap_status["next_batch"],
        "gates": {
            "model_download_allowed": bool(roadmap_status["model_download_allowed_now"]),
            "runtime_start_allowed": bool(roadmap_status["runtime_start_allowed_now"]),
            "voice_allowed": bool(roadmap_status["voice_allowed_now"]),
            "pc_control_allowed": bool(roadmap_status["pc_control_allowed_now"]),
        },
    }

