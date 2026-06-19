from __future__ import annotations

from MAKSIMAR_SERVER.SWARM_COORDINATION_RUNTIME.swarm_conflict_detector import detect_swarm_conflicts
from MAKSIMAR_SERVER.SWARM_COORDINATION_RUNTIME.swarm_observability_runtime import (
    build_swarm_observability_read_model,
)
from MAKSIMAR_SERVER.SWARM_COORDINATION_RUNTIME.swarm_task_router import route_swarm_task
from tools.jarvis_live_runtime.owner_identity_claim import OwnerIdentityClaim


def test_swarm_observability_runtime_exposes_required_read_model_fields() -> None:
    route = route_swarm_task(
        "open browser",
        input_channel="text",
        owner_identity_claim=OwnerIdentityClaim(
            claim_id="swarm_observability_owner_v1",
            source="local_terminal_session",
            verified=True,
            verification_method="test_override",
            session_token_present=False,
            process_owner_matches_os_user=True,
            reason_codes=("os_user_verified",),
        ),
    )
    payload = build_swarm_observability_read_model(route, detect_swarm_conflicts((route,)))

    assert payload["active_agents"] == ("action_worker_agent",)
    assert payload["selected_model_role"] == "jarvis_chat_model"
    assert payload["selected_tools"] == ("pc_open_browser",)
    assert payload["heavy_gpu_lock_status"] == "unlocked"
    assert payload["direct_execution_disabled_for_swarm"] is True
    assert payload["safe_action_delegated_to_action_library"] is True
    assert payload["delegated_execution_surface"] == "action_library"
