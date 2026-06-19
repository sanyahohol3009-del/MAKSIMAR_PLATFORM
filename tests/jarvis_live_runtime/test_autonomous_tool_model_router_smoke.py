from __future__ import annotations

from tools.jarvis_live_runtime.autonomous_tool_model_router import build_autonomous_tool_model_decision
from tools.jarvis_live_runtime.memory_context_builder import build_jarvis_live_brain_context
from tools.jarvis_live_runtime.owner_identity_claim import (
    OwnerIdentityClaim,
    build_owner_identity_claim_for_terminal,
    build_owner_identity_claim_for_voice_unverified,
)


def _verified_terminal_claim() -> OwnerIdentityClaim:
    claim = build_owner_identity_claim_for_terminal()
    if claim.verified:
        return claim
    return OwnerIdentityClaim(
        claim_id="test_verified_terminal_claim_v1",
        source="local_terminal_session",
        verified=True,
        verification_method="test_os_user_match",
        session_token_present=False,
        process_owner_matches_os_user=True,
        reason_codes=("os_user_verified",),
    )


def test_terminal_verified_owner_gets_direct_browser_action() -> None:
    decision = build_autonomous_tool_model_decision(
        "Джарвис, открой браузер",
        input_channel="text",
        owner_identity_claim=_verified_terminal_claim(),
    )

    assert decision["normalized_intent"] == "safe_pc_open_browser"
    assert decision["selected_model_role_id"] == "jarvis_chat_model"
    assert decision["selected_model_id"] == "jarvis:chat8b"
    assert decision["selected_tools"] == ("pc_open_browser",)
    assert decision["safe_direct_action_allowed"] is True
    assert decision["selected_model_role"]["pc_tool_direct_allowed"] is True


def test_voice_channel_never_gets_direct_action_even_for_safe_intent() -> None:
    decision = build_autonomous_tool_model_decision(
        "Джарвис, открой браузер",
        input_channel="voice",
        owner_identity_claim=build_owner_identity_claim_for_voice_unverified(),
    )

    assert decision["normalized_intent"] == "safe_pc_open_browser"
    assert decision["selected_tools"] == ("pc_open_browser",)
    assert decision["safe_direct_action_allowed"] is False
    assert decision["selected_model_role"]["pc_tool_direct_allowed"] is False
    assert decision["owner_identity_claim"]["source"] == "voice_unverified"


def test_router_selects_weather_tool_without_slash_command() -> None:
    decision = build_autonomous_tool_model_decision(
        "Какая погода сегодня?",
        input_channel="text",
        owner_identity_claim=_verified_terminal_claim(),
    )
    assert decision["normalized_intent"] == "weather_lookup"
    assert decision["selected_tools"] == ("weather_lookup",)
    assert decision["needs_ollama"] is False


def test_router_selects_daily_coder_for_pytest_failure() -> None:
    decision = build_autonomous_tool_model_decision(
        "Джарвис, pytest упал, проверь ошибку",
        input_channel="text",
        owner_identity_claim=_verified_terminal_claim(),
    )
    assert decision["normalized_intent"] == "code_debug"
    assert decision["selected_model_role_id"] == "daily_coder_model"
    assert decision["selected_model_id"] == "jarvis:coder7b"
    assert "repo_search" in decision["selected_tools"]


def test_router_selects_heavy_coder_for_complex_architecture_traceback() -> None:
    decision = build_autonomous_tool_model_decision(
        "сложный architecture traceback regression",
        input_channel="text",
        owner_identity_claim=_verified_terminal_claim(),
    )
    assert decision["selected_model_role_id"] == "heavy_coder_model"
    assert decision["selected_model_id"] == "jarvis:coder14b"
    assert decision["heavy_model_selected"] is True
    assert decision["parallel_heavy_model_allowed"] is False
    assert decision["conversation_model_kept_warm"] is True


def test_router_sends_risk_action_to_gate() -> None:
    decision = build_autonomous_tool_model_decision(
        "Джарвис, сделай git push",
        input_channel="text",
        owner_identity_claim=_verified_terminal_claim(),
    )
    assert decision["normalized_intent"] == "risk_action_request"
    assert decision["risk_gate_required"] is True
    assert decision["safe_direct_action_allowed"] is False
    assert "risk_gate" in decision["selected_tools"]


def test_brain_context_exposes_autonomous_orchestration_decision() -> None:
    context = build_jarvis_live_brain_context(
        "Джарвис, pytest упал, проверь ошибку",
        {"recent_turns": [], "rolling_summary": "", "active_topics": []},
        owner_identity_claim=_verified_terminal_claim(),
    )
    read_model = context.to_read_model()
    decision = read_model["orchestration_decision"]

    assert decision["model_selection_working"] is True
    assert decision["tool_selection_working"] is True
    assert decision["selected_model_role_id"] == "daily_coder_model"
    assert "repo_search" in decision["selected_tools"]
    assert read_model["selected_model_role"]["model_id"] == "jarvis:coder7b"
