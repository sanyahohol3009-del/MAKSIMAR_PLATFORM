from __future__ import annotations

from MAKSIMAR_SERVER.SWARM_COORDINATION_RUNTIME.swarm_task_router import route_swarm_task
from tools.jarvis_live_runtime.owner_identity_claim import (
    OwnerIdentityClaim,
    build_owner_identity_claim_for_terminal,
)


def _verified_terminal_claim() -> OwnerIdentityClaim:
    claim = build_owner_identity_claim_for_terminal()
    if claim.verified:
        return claim
    return OwnerIdentityClaim(
        claim_id="swarm_router_verified_terminal_v1",
        source="local_terminal_session",
        verified=True,
        verification_method="test_override",
        session_token_present=False,
        process_owner_matches_os_user=True,
        reason_codes=("os_user_verified",),
    )


def test_swarm_task_router_maps_intents_to_agent_roles_and_models() -> None:
    weather = route_swarm_task(
        "weather in Berlin",
        input_channel="text",
        owner_identity_claim=_verified_terminal_claim(),
    )
    pytest_failure = route_swarm_task(
        "pytest failure in runtime",
        input_channel="text",
        owner_identity_claim=_verified_terminal_claim(),
    )
    architecture = route_swarm_task(
        "architecture traceback regression",
        input_channel="text",
        owner_identity_claim=_verified_terminal_claim(),
    )
    browser = route_swarm_task(
        "open browser",
        input_channel="text",
        owner_identity_claim=_verified_terminal_claim(),
    )
    risk = route_swarm_task(
        "git push origin main",
        input_channel="text",
        owner_identity_claim=_verified_terminal_claim(),
    )

    assert weather.selected_agent_role == "tool_selector_agent"
    assert weather.selected_tools == ("weather_lookup",)
    assert pytest_failure.selected_agent_role == "project_coder_agent"
    assert pytest_failure.selected_model_id == "jarvis:coder7b"
    assert architecture.selected_agent_role == "architect_agent"
    assert architecture.selected_model_id == "jarvis:coder14b"
    assert architecture.heavy_model_requested is True
    assert browser.selected_agent_role == "action_worker_agent"
    assert browser.delegated_execution_surface == "action_library"
    assert risk.selected_agent_role == "safety_guard_agent"
    assert risk.delegated_execution_surface == "risk_gate"
