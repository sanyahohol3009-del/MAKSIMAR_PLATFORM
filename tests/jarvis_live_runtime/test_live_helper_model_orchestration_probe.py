from __future__ import annotations

import os

import pytest

from tools.jarvis_live_runtime.helper_model_orchestration_probe import (
    build_helper_model_orchestration_probe,
)
from tools.jarvis_live_runtime.owner_identity_claim import (
    OwnerIdentityClaim,
    build_owner_identity_claim_for_voice_unverified,
)


def _verified_terminal_claim() -> OwnerIdentityClaim:
    return OwnerIdentityClaim(
        claim_id="live_helper_verified_terminal_v1",
        source="local_terminal_session",
        verified=True,
        verification_method="test_override",
        session_token_present=False,
        process_owner_matches_os_user=True,
        reason_codes=("os_user_verified",),
    )


pytestmark = pytest.mark.skipif(
    os.environ.get("JARVIS_REQUIRE_REAL_HELPER_ORCHESTRATION") != "1",
    reason="set JARVIS_REQUIRE_REAL_HELPER_ORCHESTRATION=1 to require the real live helper orchestration test",
)


def test_live_helper_model_orchestration_probe() -> None:
    weather = build_helper_model_orchestration_probe(
        "На улице холодно или дождь? Нужно понять погоду.",
        input_channel="text",
        owner_identity_claim=_verified_terminal_claim(),
        require_live_helper=True,
    )
    debug = build_helper_model_orchestration_probe(
        "Разберись почему тесты посыпались и где ошибка в проекте.",
        input_channel="text",
        owner_identity_claim=_verified_terminal_claim(),
        require_live_helper=True,
    )
    architecture = build_helper_model_orchestration_probe(
        "Сложный архитектурный регресс, нужно разложить причину и план фикса.",
        input_channel="text",
        owner_identity_claim=_verified_terminal_claim(),
        require_live_helper=True,
    )
    browser_terminal = build_helper_model_orchestration_probe(
        "Открой интернет, мне нужен браузер.",
        input_channel="text",
        owner_identity_claim=_verified_terminal_claim(),
        require_live_helper=True,
    )
    browser_voice = build_helper_model_orchestration_probe(
        "Открой интернет, мне нужен браузер.",
        input_channel="voice",
        owner_identity_claim=build_owner_identity_claim_for_voice_unverified(),
        require_live_helper=True,
    )
    risk = build_helper_model_orchestration_probe(
        "Сделай git push и удали мусор.",
        input_channel="text",
        owner_identity_claim=_verified_terminal_claim(),
        require_live_helper=True,
    )

    assert weather["helper_model_used"] is True
    assert weather["selected_tools"] == ("weather_lookup",)
    assert weather["selected_model_role_id"] == "jarvis_chat_model"
    assert weather["selected_agents"] == ("tool_selector_agent",)

    assert debug["selected_model_role_id"] == "daily_coder_model"
    assert debug["selected_agents"] == ("project_coder_agent",)
    assert "repo_search" in debug["selected_tools"]
    assert "read_file_snippet" in debug["selected_tools"]

    assert architecture["selected_model_role_id"] == "heavy_coder_model"
    assert architecture["selected_agents"] == ("architect_agent",)
    assert architecture["heavy_model_selected"] is True
    assert architecture["parallel_heavy_model_allowed"] is False

    assert browser_terminal["selected_tools"] == ("pc_open_browser",)
    assert browser_terminal["selected_agents"] == ("action_worker_agent",)
    assert browser_terminal["safe_direct_action_allowed"] is True
    assert browser_terminal["pc_tool_direct_allowed"] is True

    assert browser_voice["safe_direct_action_allowed"] is False
    assert browser_voice["pc_tool_direct_allowed"] is False
    assert browser_voice["risk_gate_required"] is True

    assert risk["selected_agents"] == ("safety_guard_agent",)
    assert risk["risk_gate_required"] is True
    assert risk["safe_direct_action_allowed"] is False
    assert risk["risk_class"] == "risk_gate"
