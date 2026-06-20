from __future__ import annotations

import json

from tools.jarvis_live_runtime.helper_model_orchestration_probe import (
    HelperModelProbeResponse,
    build_helper_model_orchestration_probe,
)
from tools.jarvis_live_runtime.autonomous_tool_model_router import build_autonomous_tool_model_decision
from tools.jarvis_live_runtime.owner_identity_claim import OwnerIdentityClaim


def _verified_terminal_claim() -> OwnerIdentityClaim:
    return OwnerIdentityClaim(
        claim_id="external_tooling_helper_verified_terminal_v1",
        source="local_terminal_session",
        verified=True,
        verification_method="test_override",
        session_token_present=False,
        process_owner_matches_os_user=True,
        reason_codes=("os_user_verified",),
    )


def _fake_helper_transport(text: str, input_channel: str, owner_identity_claim: OwnerIdentityClaim) -> HelperModelProbeResponse:
    assert input_channel == "text"
    assert owner_identity_claim.verified is True
    lowered = text.casefold()
    if "mcp" in lowered:
        payload = {
            "intent_family": "external_agent_tooling",
            "task_complexity": "medium",
            "selected_model_role_id": "helper_classifier_model",
            "selected_tools": ["external_adapter:mcp_python_sdk"],
            "selected_agent_roles": ["tool_selector_agent"],
            "risk_class": "risk_gate",
            "workflow_steps": ["load_external_adapter_registry", "select_external_adapter", "prepare_risk_gated_adapter_plan"],
            "confidence": 0.96,
            "reason": "helper selected MCP adapter tooling",
        }
    elif "сравни" in lowered or "compare" in lowered:
        payload = {
            "intent_family": "agent_engine_comparison",
            "task_complexity": "medium",
            "selected_model_role_id": "helper_classifier_model",
            "selected_tools": [
                "external_adapter:openai_agents_sdk",
                "external_adapter:autogen_agentchat",
                "external_adapter:autogen",
                "external_adapter:autogen_ext",
                "external_adapter:langgraph",
            ],
            "selected_agent_roles": ["tool_selector_agent"],
            "risk_class": "risk_gate",
            "workflow_steps": ["load_external_adapter_registry", "compare_agent_providers", "recommend_adapter"],
            "confidence": 0.95,
            "reason": "helper selected comparison route",
        }
    else:
        payload = {
            "intent_family": "external_agent_tooling",
            "task_complexity": "medium",
            "selected_model_role_id": "helper_classifier_model",
            "selected_tools": ["external_adapter:autogen_agentchat", "external_adapter:langgraph"],
            "selected_agent_roles": ["tool_selector_agent"],
            "risk_class": "risk_gate",
            "workflow_steps": ["load_external_adapter_registry", "select_external_adapter", "prepare_risk_gated_adapter_plan"],
            "confidence": 0.93,
            "reason": "helper selected agent workflow tooling",
        }
    return HelperModelProbeResponse(
        available=True,
        raw_content=json.dumps(payload, ensure_ascii=False),
        parsed_json=payload,
        error="",
    )


def test_helper_selects_external_agent_tooling_smoke() -> None:
    fallback = build_autonomous_tool_model_decision(
        "построй агентный workflow",
        input_channel="text",
        owner_identity_claim=_verified_terminal_claim(),
    )
    workflow = build_helper_model_orchestration_probe(
        "построй агентный workflow",
        input_channel="text",
        owner_identity_claim=_verified_terminal_claim(),
        helper_transport=_fake_helper_transport,
    )
    mcp = build_helper_model_orchestration_probe(
        "нужен MCP tool",
        input_channel="text",
        owner_identity_claim=_verified_terminal_claim(),
        helper_transport=_fake_helper_transport,
    )
    comparison = build_helper_model_orchestration_probe(
        "сравни LangGraph и AutoGen для задачи",
        input_channel="text",
        owner_identity_claim=_verified_terminal_claim(),
        helper_transport=_fake_helper_transport,
    )

    assert fallback["normalized_intent"] == "external_agent_tooling"
    assert "external_adapter:autogen_agentchat" in fallback["selected_tools"]
    assert fallback["selected_agent_roles"] == ("tool_selector_agent",)

    assert workflow["helper_model_used"] is True
    assert workflow["selection_source"] == "helper_model"
    assert "external_adapter:langgraph" in workflow["selected_tools"]
    assert "external_agent_tooling" in workflow["selected_skills"]
    assert workflow["risk_class"] == "risk_gate"

    assert mcp["helper_model_used"] is True
    assert mcp["selected_tools"] == ("external_adapter:mcp_python_sdk",)
    assert "external_agent_tooling" in mcp["selected_skills"]

    assert comparison["helper_model_used"] is True
    assert "external_adapter:autogen_agentchat" in comparison["selected_tools"]
    assert "external_adapter:autogen_ext" in comparison["selected_tools"]
    assert "external_agent_tooling" in comparison["selected_skills"]
