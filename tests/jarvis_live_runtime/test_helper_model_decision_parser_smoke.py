from __future__ import annotations

import pytest

from tools.jarvis_live_runtime.helper_model_decision_parser import parse_helper_model_decision_payload


def test_helper_model_decision_parser_smoke() -> None:
    decision = parse_helper_model_decision_payload(
        {
            "intent_family": "code_debug",
            "task_complexity": "medium",
            "selected_model_role_id": "daily_coder_model",
            "selected_tools": ["repo_search", "read_file_snippet", "pytest_report_read"],
            "selected_agent_roles": ["project_coder_agent"],
            "risk_class": "read_only",
            "workflow_steps": ["inspect_failure_context", "locate_relevant_code", "propose_fix"],
            "confidence": 1.2,
            "reason": "semantic code-debug classification",
        }
    ).to_read_model()

    assert decision["selected_model_role_id"] == "daily_coder_model"
    assert decision["selected_model_id"] == "jarvis:coder7b"
    assert decision["selected_agent_roles"] == ("project_coder_agent",)
    assert decision["confidence"] == 1.0


def test_helper_model_decision_parser_rejects_missing_and_invalid_fields() -> None:
    with pytest.raises(ValueError, match="missing helper decision fields"):
        parse_helper_model_decision_payload({"intent_family": "weather_lookup"})

    with pytest.raises(ValueError, match="unknown selected_model_role_id"):
        parse_helper_model_decision_payload(
            {
                "intent_family": "weather_lookup",
                "task_complexity": "light",
                "selected_model_role_id": "unknown_model",
                "selected_tools": ["weather_lookup"],
                "selected_agent_roles": ["tool_selector_agent"],
                "risk_class": "read_only",
                "workflow_steps": ["select_weather_tool"],
                "confidence": 0.9,
                "reason": "bad model",
            }
        )

    with pytest.raises(ValueError, match="unknown selected_agent_roles"):
        parse_helper_model_decision_payload(
            {
                "intent_family": "weather_lookup",
                "task_complexity": "light",
                "selected_model_role_id": "jarvis_chat_model",
                "selected_tools": ["weather_lookup"],
                "selected_agent_roles": ["bad_agent"],
                "risk_class": "read_only",
                "workflow_steps": ["select_weather_tool"],
                "confidence": 0.9,
                "reason": "bad agent",
            }
        )

    with pytest.raises(ValueError, match="unknown risk_class"):
        parse_helper_model_decision_payload(
            {
                "intent_family": "weather_lookup",
                "task_complexity": "light",
                "selected_model_role_id": "jarvis_chat_model",
                "selected_tools": ["weather_lookup"],
                "selected_agent_roles": ["tool_selector_agent"],
                "risk_class": "unsafe",
                "workflow_steps": ["select_weather_tool"],
                "confidence": 0.9,
                "reason": "bad risk",
            }
        )

    with pytest.raises(ValueError, match="selected_tools must be a list"):
        parse_helper_model_decision_payload(
            {
                "intent_family": "weather_lookup",
                "task_complexity": "light",
                "selected_model_role_id": "jarvis_chat_model",
                "selected_tools": "weather_lookup",
                "selected_agent_roles": ["tool_selector_agent"],
                "risk_class": "read_only",
                "workflow_steps": ["select_weather_tool"],
                "confidence": 0.9,
                "reason": "bad list",
            }
        )
