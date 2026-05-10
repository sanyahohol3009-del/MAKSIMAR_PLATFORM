from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.display_topology.display_topology_contract import (
    build_display_topology_contract,
)
from MAKSIMAR_CORE_LIB.display_topology.display_topology_summary_builder import (
    build_display_topology_summary,
)
from MAKSIMAR_SERVER.DISPLAY_ORCHESTRATION import (
    build_display_orchestration_contract,
)


_DISPLAY_TOPOLOGY_PREVIEW_FLOW = (
    "display_topology_contract",
    "dashboard_read_only_binding",
    "skill_domain_binding",
    "display_orchestration_binding",
    "display_topology_summary",
    "display_topology_preview",
)


def build_display_topology_preview() -> Dict[str, object]:
    topology = build_display_topology_contract()
    orchestration = build_display_orchestration_contract()
    summary = build_display_topology_summary()

    return {
        "flow": _DISPLAY_TOPOLOGY_PREVIEW_FLOW,
        "preview_ready": bool(summary["summary_ready"]),
        "summary_ready": summary["summary_ready"],
        "display_topology_displays": summary["display_topology_displays"],
        "display_topology_private_displays": summary["display_topology_private_displays"],
        "display_topology_shared_displays": summary["display_topology_shared_displays"],
        "display_topology_multilingual_ready_displays": summary[
            "display_topology_multilingual_ready_displays"
        ],
        "display_topology_explainable_displays": summary[
            "display_topology_explainable_displays"
        ],
        "display_topology_registry_routed_displays": summary[
            "display_topology_registry_routed_displays"
        ],
        "display_orchestration_entries": summary["display_orchestration_entries"],
        "dashboard_root_entries": summary["dashboard_root_entries"],
        "dashboard_read_only_phase_ready": summary["dashboard_read_only_phase_ready"],
        "skill_domain_summary_ready": summary["skill_domain_summary_ready"],
        "skill_domain_preview_ready": summary["skill_domain_preview_ready"],
        "action_execution_allowed": summary["action_execution_allowed"],
        "backend_execution_allowed": summary["backend_execution_allowed"],
        "display_ids": tuple(entry.display_id for entry in topology.entries),
        "display_roles": tuple(entry.display_role for entry in topology.entries),
        "display_visibility_modes": tuple(
            entry.visibility_mode for entry in topology.entries
        ),
        "orchestration_route_ids": tuple(
            entry.route_request_id for entry in orchestration.entries
        ),
        "orchestration_intents": tuple(
            entry.command_intent for entry in orchestration.entries
        ),
        "orchestration_selected_display_ids": tuple(
            entry.selected_display_id for entry in orchestration.entries
        ),
    }
