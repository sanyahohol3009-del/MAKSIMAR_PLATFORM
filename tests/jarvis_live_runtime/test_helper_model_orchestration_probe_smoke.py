from __future__ import annotations

import json

from tools.jarvis_live_runtime.helper_model_orchestration_probe import (
    HelperModelProbeResponse,
    _extract_json_object_from_helper_content,
    build_helper_model_orchestration_probe,
)
from tools.jarvis_live_runtime.owner_identity_claim import OwnerIdentityClaim


def _verified_terminal_claim() -> OwnerIdentityClaim:
    return OwnerIdentityClaim(
        claim_id="helper_probe_verified_terminal_v1",
        source="local_terminal_session",
        verified=True,
        verification_method="test_override",
        session_token_present=False,
        process_owner_matches_os_user=True,
        reason_codes=("os_user_verified",),
    )


def test_helper_model_orchestration_probe_uses_helper_when_decision_is_valid() -> None:
    def fake_transport(text: str, input_channel: str, owner_identity_claim: OwnerIdentityClaim) -> HelperModelProbeResponse:
        assert text
        assert input_channel == "text"
        assert owner_identity_claim.verified is True
        payload = {
            "intent_family": "code_debug",
            "task_complexity": "medium",
            "selected_model_role_id": "daily_coder_model",
            "selected_tools": ["repo_search", "read_file_snippet", "pytest_report_read"],
            "selected_agent_roles": ["project_coder_agent"],
            "risk_class": "read_only",
            "workflow_steps": ["inspect_failure_context", "locate_relevant_code", "propose_fix"],
            "confidence": 0.95,
            "reason": "helper selected semantic debug route",
        }
        return HelperModelProbeResponse(
            available=True,
            raw_content=json.dumps(payload, ensure_ascii=False),
            parsed_json=payload,
            error="",
        )

    payload = build_helper_model_orchestration_probe(
        "посмотри почему всё сломалось после последнего изменения",
        input_channel="text",
        owner_identity_claim=_verified_terminal_claim(),
        helper_transport=fake_transport,
    )

    assert payload["helper_model_called"] is True
    assert payload["helper_model_used"] is True
    assert payload["fallback_used"] is False
    assert payload["selection_source"] == "helper_model"
    assert payload["selected_model_role_id"] == "daily_coder_model"
    assert payload["selected_agents"] == ("project_coder_agent",)
    assert "repo_search" in payload["selected_tools"]
    assert "project_workspace_analysis" in payload["selected_skills"]
    assert len(payload["workflow_steps"]) == 3


def test_helper_model_orchestration_probe_falls_back_when_helper_output_is_invalid() -> None:
    def fake_transport(_: str, __: str, ___: OwnerIdentityClaim) -> HelperModelProbeResponse:
        payload = {
            "intent_family": "weather_lookup",
            "task_complexity": "light",
            "selected_model_role_id": "jarvis_chat_model",
            "selected_tools": "weather_lookup",
            "selected_agent_roles": ["tool_selector_agent"],
            "risk_class": "read_only",
            "workflow_steps": ["select_weather_tool"],
            "confidence": 0.9,
            "reason": "invalid selected_tools list",
        }
        return HelperModelProbeResponse(
            available=True,
            raw_content=json.dumps(payload, ensure_ascii=False),
            parsed_json=payload,
            error="",
        )

    payload = build_helper_model_orchestration_probe(
        "мне надо понять погоду без ручных команд",
        input_channel="text",
        owner_identity_claim=_verified_terminal_claim(),
        helper_transport=fake_transport,
    )

    assert payload["helper_model_status"] == "invalid"
    assert payload["helper_model_called"] is True
    assert payload["helper_model_used"] is False
    assert payload["fallback_used"] is True
    assert payload["selection_source"] == "deterministic_fallback"
    assert payload["selected_model_role_id"] == "jarvis_chat_model"
    assert payload["selected_tools"] == ("weather_lookup",)


def test_extract_json_object_from_helper_content_parses_pure_json() -> None:
    content = json.dumps({"intent_family": "weather_lookup"}, ensure_ascii=False)

    parsed = _extract_json_object_from_helper_content(content)

    assert parsed == {"intent_family": "weather_lookup"}


def test_extract_json_object_from_helper_content_parses_json_fenced_block() -> None:
    content = "before\n```json\n{\"intent_family\": \"code_debug\"}\n```\nafter"

    parsed = _extract_json_object_from_helper_content(content)

    assert parsed == {"intent_family": "code_debug"}


def test_extract_json_object_from_helper_content_parses_embedded_prose_json() -> None:
    content = "Helper decision follows: {\"intent_family\": \"safe_pc_open_browser\", \"confidence\": 0.9} done."

    parsed = _extract_json_object_from_helper_content(content)

    assert parsed == {"intent_family": "safe_pc_open_browser", "confidence": 0.9}


def test_extract_json_object_from_helper_content_rejects_invalid_prose() -> None:
    assert _extract_json_object_from_helper_content("no json here") is None


def test_extract_json_object_from_helper_content_rejects_array() -> None:
    assert _extract_json_object_from_helper_content("[{\"intent_family\": \"weather_lookup\"}]") is None
