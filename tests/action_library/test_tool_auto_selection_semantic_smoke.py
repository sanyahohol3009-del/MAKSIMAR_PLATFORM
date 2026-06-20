from __future__ import annotations

from MAKSIMAR_CORE_LIB.action_library_adapters.computer_use_worker_contract import (
    build_action_request_from_intent,
)
from tools.jarvis_live_runtime.autonomous_tool_model_router import build_autonomous_tool_model_decision
from tools.jarvis_live_runtime.owner_identity_claim import (
    OwnerIdentityClaim,
    build_owner_identity_claim_for_voice_unverified,
)


def _verified_terminal_claim() -> OwnerIdentityClaim:
    return OwnerIdentityClaim(
        claim_id="tool_semantic_verified_terminal_v1",
        source="local_terminal_session",
        verified=True,
        verification_method="test_override",
        session_token_present=False,
        process_owner_matches_os_user=True,
        reason_codes=("os_user_verified",),
    )


def test_tool_auto_selection_semantic_smoke() -> None:
    browser_request = build_action_request_from_intent(
        "Открой интернет, мне нужен браузер.",
        input_channel="text",
        owner_identity_claim=_verified_terminal_claim(),
    )
    risk_request = build_action_request_from_intent(
        "Сделай git push и удали мусор.",
        input_channel="text",
        owner_identity_claim=_verified_terminal_claim(),
    )
    voice_browser = build_autonomous_tool_model_decision(
        "Открой интернет, мне нужен браузер.",
        input_channel="voice",
        owner_identity_claim=build_owner_identity_claim_for_voice_unverified(),
    )
    screen_tool = build_autonomous_tool_model_decision(
        "найди подходящий инструмент для чтения экрана",
        input_channel="text",
        owner_identity_claim=_verified_terminal_claim(),
    )

    assert browser_request is not None
    assert browser_request.capability_id == "browser_worker"
    assert browser_request.action_name == "open_browser"
    assert risk_request is not None
    assert risk_request.capability_id == "cli_worker"
    assert voice_browser["safe_direct_action_allowed"] is False
    assert voice_browser["risk_gate_required"] is True
    assert screen_tool["selected_tools"] == ("screen_observer_read",)
    assert screen_tool["selected_agent_roles"] == ("tool_selector_agent",)
