from __future__ import annotations

import argparse
import json
import re
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any

from tools.jarvis_live_runtime.autonomous_tool_model_router import build_autonomous_tool_model_decision
from tools.jarvis_live_runtime.helper_model_decision_parser import parse_helper_model_decision_payload
from tools.jarvis_live_runtime.jarvis_skill_visibility import select_skills_for_tools
from tools.jarvis_live_runtime.owner_identity_claim import (
    OwnerIdentityClaim,
    build_owner_identity_claim_for_terminal,
    build_owner_identity_claim_for_voice_unverified,
)


OLLAMA_CHAT_URL = "http://127.0.0.1:11434/api/chat"
HELPER_MODEL_ID = "jarvis:helper3b"
HELPER_CONFIDENCE_THRESHOLD = 0.70


@dataclass(frozen=True, slots=True)
class HelperModelProbeResponse:
    available: bool
    raw_content: str
    parsed_json: dict[str, Any] | None
    error: str


def _helper_system_prompt() -> str:
    return (
        "You are JARVIS helper orchestration classifier. "
        "Classify by request meaning, not exact command syntax. "
        "Never authorize shell execution, direct mutation, deployment, or direct PC actions. "
        "Return exactly one JSON object. No markdown. No explanation. No code fence. "
        "Return JSON only with keys: intent_family, task_complexity, selected_model_role_id, "
        "selected_tools, selected_agent_roles, risk_class, workflow_steps, confidence, reason. "
        "Allowed selected_model_role_id: helper_classifier_model, jarvis_chat_model, daily_coder_model, heavy_coder_model. "
        "Allowed selected_agent_roles: conversation_agent, project_coder_agent, architect_agent, tool_selector_agent, safety_guard_agent, action_worker_agent. "
        "Allowed risk_class: read_only, safe_direct, risk_gate. "
        "Allowed tools include: weather_lookup, calendar_lookup, mail_lookup, screen_observer_read, repo_git_status, "
        "repo_tree, repo_files, repo_search, read_file_snippet, read_file_outline, pytest_report_read, session_memory, "
        "local_chat_memory, pc_open_browser, pc_open_app, risk_gate, operator_proposal, external_adapter:openai_agents_sdk, "
        "external_adapter:mcp_python_sdk, external_adapter:autogen_agentchat, external_adapter:autogen, "
        "external_adapter:autogen_ext, external_adapter:langgraph. "
        "Use safe_direct only for verified owner browser/app open requests; otherwise use risk_gate or read_only."
    )


def _helper_user_prompt(text: str, input_channel: str, owner_identity_claim: OwnerIdentityClaim) -> str:
    return json.dumps(
        {
            "request_text": text,
            "input_channel": input_channel,
            "owner_verified": owner_identity_claim.verified,
            "owner_identity_source": owner_identity_claim.source,
            "policy": {
                "no_shell_execution": True,
                "no_direct_mutation": True,
                "classification_by_meaning": True,
            },
            "examples": [
                {
                    "request": "На улице холодно или дождь? Нужно понять погоду.",
                    "intent_family": "weather_lookup",
                    "selected_model_role_id": "jarvis_chat_model",
                    "selected_tools": ["weather_lookup"],
                    "selected_agent_roles": ["tool_selector_agent"],
                    "risk_class": "read_only",
                },
                {
                    "request": "Разберись почему тесты посыпались и где ошибка в проекте.",
                    "intent_family": "code_debug",
                    "selected_model_role_id": "daily_coder_model",
                    "selected_tools": ["repo_search", "read_file_snippet", "pytest_report_read"],
                    "selected_agent_roles": ["project_coder_agent"],
                    "risk_class": "read_only",
                },
                {
                    "request": "Открой интернет, мне нужен браузер.",
                    "intent_family": "safe_pc_open_browser",
                    "selected_model_role_id": "jarvis_chat_model",
                    "selected_tools": ["pc_open_browser"],
                    "selected_agent_roles": ["action_worker_agent"],
                    "risk_class": "safe_direct",
                },
            ],
        },
        ensure_ascii=False,
    )


def _call_helper_model_ollama(text: str, input_channel: str, owner_identity_claim: OwnerIdentityClaim) -> HelperModelProbeResponse:
    payload = {
        "model": HELPER_MODEL_ID,
        "stream": False,
        "format": "json",
        "keep_alive": "10m",
        "options": {"temperature": 0, "num_predict": 768},
        "messages": [
            {"role": "system", "content": _helper_system_prompt()},
            {"role": "user", "content": _helper_user_prompt(text, input_channel, owner_identity_claim)},
        ],
    }
    request = urllib.request.Request(
        OLLAMA_CHAT_URL,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            raw_payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return HelperModelProbeResponse(
            available=False,
            raw_content="",
            parsed_json=None,
            error=f"http_error:{exc.code}",
        )
    except urllib.error.URLError as exc:
        return HelperModelProbeResponse(
            available=False,
            raw_content="",
            parsed_json=None,
            error=f"transport_error:{exc.reason}",
        )
    except Exception as exc:
        return HelperModelProbeResponse(
            available=False,
            raw_content="",
            parsed_json=None,
            error=f"unexpected_error:{type(exc).__name__}",
        )

    content = str(raw_payload.get("message", {}).get("content", "")).strip()
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        parsed = _extract_json_object_from_helper_content(content)
        if parsed is None:
            return HelperModelProbeResponse(
                available=True,
                raw_content=content,
                parsed_json=None,
                error=f"invalid_json_content:{content[:300]}",
            )
    if not isinstance(parsed, dict):
        return HelperModelProbeResponse(
            available=True,
            raw_content=content,
            parsed_json=None,
            error="helper_content_not_object",
        )
    return HelperModelProbeResponse(
        available=True,
        raw_content=content,
        parsed_json=parsed,
        error="",
    )


def _extract_json_object_from_helper_content(content: str) -> dict[str, Any] | None:
    text = str(content or "").strip()
    if not text:
        return None
    if text.lstrip().startswith("["):
        return None

    fenced_candidates = re.findall(r"```json\s*(.*?)```", text, flags=re.IGNORECASE | re.DOTALL)
    for candidate in fenced_candidates:
        parsed = _parse_json_object_candidate(candidate.strip())
        if parsed is not None:
            return parsed

    return _parse_json_object_candidate(text)


def _parse_json_object_candidate(candidate: str) -> dict[str, Any] | None:
    if not candidate:
        return None
    if candidate.lstrip().startswith("["):
        return None
    decoder = json.JSONDecoder()
    for start_index, char in enumerate(candidate):
        if char != "{":
            continue
        try:
            parsed, end_index = decoder.raw_decode(candidate[start_index:])
        except json.JSONDecodeError:
            continue
        if not isinstance(parsed, dict):
            return None
        trailing = candidate[start_index + end_index :].strip()
        if trailing:
            # Allow prose around the embedded object, but not another invalid fragment
            # to be mistaken for JSON when raw_decode already succeeded.
            return parsed
        return parsed
    return None


def _normalize_helper_decision_payload_for_request(
    payload: dict[str, Any],
    text: str,
    input_channel: str,
    owner_identity_claim: OwnerIdentityClaim,
) -> dict[str, Any]:
    normalized = dict(payload)
    lowered = str(text or "").casefold()

    # Canonical hard-risk override: destructive/git/shell/send/money actions must route to safety guard.
    risk_markers = (
        "git push",
        "сделай push",
        "push",
        "удали",
        "удалить",
        "delete",
        "rm ",
        "sudo",
        "pip install",
        "docker run",
        "chmod",
        "chown",
        "отправь письмо",
        "send email",
        "банк",
        "деньги",
        "оплати",
    )
    if any(marker in lowered for marker in risk_markers):
        normalized["intent_family"] = "risk_action_request"
        normalized["task_complexity"] = "light"
        normalized["selected_model_role_id"] = "jarvis_chat_model"
        normalized["selected_agent_roles"] = ["safety_guard_agent"]
        normalized["selected_tools"] = ["risk_gate", "operator_proposal"]
        normalized["risk_class"] = "risk_gate"
        normalized["workflow_steps"] = [
            "classify_risk",
            "route_to_risk_gate",
            "prepare_operator_proposal",
        ]
        normalized["reason"] = "Canonical policy routed destructive or publish action to safety guard."
        return normalized


    complexity = str(normalized.get("task_complexity", "")).casefold()
    complexity_map = {
        "low": "light",
        "simple": "light",
        "normal": "medium",
        "high": "heavy",
        "complex": "heavy",
        "advanced": "heavy",
        "severe": "heavy",
        "complicated": "heavy",
    }
    if complexity in complexity_map:
        normalized["task_complexity"] = complexity_map[complexity]

    tools = tuple(str(tool) for tool in normalized.get("selected_tools", ()) if str(tool).strip())

    # A helper model may incorrectly call read-only repo/tool work "safe_direct".
    # In this architecture safe_direct is only for verified-owner pc_* actions.
    if normalized.get("risk_class") == "safe_direct" and not any(tool.startswith("pc_") for tool in tools):
        normalized["risk_class"] = "read_only"

    # Hard semantic upgrade: architecture/regression analysis must not stay on daily coder.
    architecture_markers = (
        "архитектур",
        "architecture",
        "регресс",
        "regression",
        "сложн",
        "complex",
        "план фикса",
        "fix plan",
    )
    if any(marker in lowered for marker in architecture_markers):
        normalized["intent_family"] = "complex_code_analysis"
        normalized["task_complexity"] = "heavy"
        normalized["selected_model_role_id"] = "heavy_coder_model"
        normalized["selected_agent_roles"] = ["architect_agent"]
        normalized["selected_tools"] = ["repo_search", "read_file_snippet", "read_file_outline"]
        normalized["risk_class"] = "read_only"
        normalized["workflow_steps"] = [
            "collect_architecture_context",
            "analyze_regression_cause",
            "propose_fix_plan",
        ]

    # Voice without verified identity can never direct-execute PC actions.
    if input_channel == "voice" and any(tool.startswith("pc_") for tool in normalized.get("selected_tools", ())):
        normalized["risk_class"] = "risk_gate"

    if any(str(tool).startswith("pc_") for tool in normalized.get("selected_tools", ())) and not owner_identity_claim.verified:
        normalized["risk_class"] = "risk_gate"

    return normalized


def build_helper_model_orchestration_probe(
    text: str,
    *,
    input_channel: str,
    owner_identity_claim: OwnerIdentityClaim,
    require_live_helper: bool = False,
    helper_transport: Any | None = None,
) -> dict[str, Any]:
    transport = helper_transport or _call_helper_model_ollama
    helper_response = transport(text, input_channel, owner_identity_claim)
    if not isinstance(helper_response, HelperModelProbeResponse):
        raise TypeError("helper transport must return HelperModelProbeResponse")

    helper_decision = None
    normalized_helper_payload = None
    if helper_response.parsed_json is not None:
        normalized_helper_payload = _normalize_helper_decision_payload_for_request(
            helper_response.parsed_json,
            text,
            input_channel,
            owner_identity_claim,
        )
        try:
            helper_decision = parse_helper_model_decision_payload(normalized_helper_payload)
        except ValueError:
            helper_decision = None

    if require_live_helper and (
        helper_response.available is not True
        or helper_decision is None
        or helper_decision.confidence < HELPER_CONFIDENCE_THRESHOLD
    ):
        raise RuntimeError(
            f"live helper orchestration required but unavailable: {helper_response.error or 'invalid_decision'}"
        )

    router_payload = build_autonomous_tool_model_decision(
        text,
        input_channel=input_channel,
        owner_identity_claim=owner_identity_claim,
        helper_decision_input=normalized_helper_payload if helper_decision is not None else None,
        helper_model_called=True,
    )
    selected_skills = select_skills_for_tools(
        tuple(router_payload["selected_tools"]),
        tuple(router_payload["selected_agent_roles"]),
    )
    return {
        "helper_model_status": "ready"
        if helper_decision is not None
        else ("unavailable" if helper_response.available is False else "invalid"),
        "helper_model_called": router_payload["helper_model_called"],
        "helper_model_used": router_payload["helper_model_used"],
        "helper_model_id": router_payload["helper_model_id"],
        "helper_decision_confidence": router_payload["helper_decision_confidence"],
        "fallback_used": router_payload["fallback_used"],
        "selection_source": router_payload["selection_source"],
        "selected_model_role_id": router_payload["selected_model_role_id"],
        "selected_model_id": router_payload["selected_model_id"],
        "selected_agents": router_payload["selected_agent_roles"],
        "selected_tools": router_payload["selected_tools"],
        "selected_skills": selected_skills,
        "workflow_steps": router_payload["workflow_steps"],
        "risk_class": router_payload["risk_class"],
        "risk_gate_required": router_payload["risk_gate_required"],
        "safe_direct_action_allowed": router_payload["safe_direct_action_allowed"],
        "pc_tool_direct_allowed": router_payload["selected_model_role"]["pc_tool_direct_allowed"],
        "heavy_model_selected": router_payload["heavy_model_selected"],
        "parallel_heavy_model_allowed": router_payload["parallel_heavy_model_allowed"],
        "helper_raw_content": helper_response.raw_content,
        "helper_error": helper_response.error,
    }


def _default_claim_for_channel(channel: str) -> OwnerIdentityClaim:
    if channel == "voice":
        return build_owner_identity_claim_for_voice_unverified()
    return build_owner_identity_claim_for_terminal()


def main() -> int:
    parser = argparse.ArgumentParser(description="Live helper-backed orchestration probe for JARVIS.")
    parser.add_argument("--text", required=True)
    parser.add_argument("--channel", default="text", choices=("text", "voice", "screen"))
    parser.add_argument("--require-live-helper", action="store_true")
    args = parser.parse_args()

    payload = build_helper_model_orchestration_probe(
        args.text,
        input_channel=args.channel,
        owner_identity_claim=_default_claim_for_channel(args.channel),
        require_live_helper=args.require_live_helper,
    )
    print(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
