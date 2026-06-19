from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.ai_orchestration.model_profile_registry_contract import (
    build_jarvis_live_runtime_model_role_profiles,
)
from tools.jarvis_live_runtime.owner_identity_claim import OwnerIdentityClaim


_DIRECT_ACTION_IDENTITY_SOURCES = {"local_terminal_session"}


@dataclass(frozen=True, slots=True)
class AutonomousRouteDecision:
    decision_id: str
    input_channel: str
    normalized_intent: str
    task_complexity: str
    selected_model_role_id: str
    selected_model_id: str
    selected_model_reason: str
    selected_tools: tuple[str, ...]
    selected_tool_reason: str
    owner_identity_claim: OwnerIdentityClaim
    safe_direct_action_allowed: bool
    risk_gate_required: bool
    needs_ollama: bool
    conversation_model_kept_warm: bool
    task_model_load_policy: str
    heavy_model_selected: bool
    parallel_heavy_model_allowed: bool
    direct_shell_allowed: bool
    direct_canonical_write_allowed: bool
    direct_network_mutation_allowed: bool

    def to_read_model(self) -> dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "input_channel": self.input_channel,
            "normalized_intent": self.normalized_intent,
            "task_complexity": self.task_complexity,
            "selected_model_role_id": self.selected_model_role_id,
            "selected_model_id": self.selected_model_id,
            "selected_model_reason": self.selected_model_reason,
            "selected_tools": self.selected_tools,
            "selected_tool_reason": self.selected_tool_reason,
            "owner_identity_claim": self.owner_identity_claim.to_read_model(),
            "safe_direct_action_allowed": self.safe_direct_action_allowed,
            "risk_gate_required": self.risk_gate_required,
            "needs_ollama": self.needs_ollama,
            "conversation_model_kept_warm": self.conversation_model_kept_warm,
            "task_model_load_policy": self.task_model_load_policy,
            "heavy_model_selected": self.heavy_model_selected,
            "parallel_heavy_model_allowed": self.parallel_heavy_model_allowed,
            "direct_shell_allowed": self.direct_shell_allowed,
            "direct_canonical_write_allowed": self.direct_canonical_write_allowed,
            "direct_network_mutation_allowed": self.direct_network_mutation_allowed,
        }


def build_autonomous_tool_model_decision(
    user_text: str,
    *,
    input_channel: str,
    owner_identity_claim: OwnerIdentityClaim,
) -> dict[str, Any]:
    text = str(user_text or "")
    lowered = text.casefold()
    channel = _normalize_input_channel(input_channel)

    intent = _classify_intent(lowered)
    complexity = _classify_complexity(lowered, intent)
    tools, tool_reason = _select_tools(intent)
    role_id, model_reason = _select_model_role(intent, complexity)
    profile = _profile_by_role_id(role_id)

    risk_gate = _is_risk_action(lowered, intent, tools)
    safe_direct = bool(
        owner_identity_claim.verified
        and owner_identity_claim.source in _DIRECT_ACTION_IDENTITY_SOURCES
        and _is_safe_direct_action(intent, tools)
        and not risk_gate
    )

    heavy = bool(profile["role_id"] == "heavy_coder_model" or profile.get("exclusive_gpu") is True)

    decision = AutonomousRouteDecision(
        decision_id="jarvis_autonomous_tool_model_router_v1",
        input_channel=channel,
        normalized_intent=intent,
        task_complexity=complexity,
        selected_model_role_id=profile["role_id"],
        selected_model_id=profile["model_id"],
        selected_model_reason=model_reason,
        selected_tools=tools,
        selected_tool_reason=tool_reason,
        owner_identity_claim=owner_identity_claim,
        safe_direct_action_allowed=safe_direct,
        risk_gate_required=risk_gate,
        needs_ollama=_needs_ollama(intent),
        conversation_model_kept_warm=True,
        task_model_load_policy=str(profile["load_policy"]),
        heavy_model_selected=heavy,
        parallel_heavy_model_allowed=False if heavy else True,
        direct_shell_allowed=False,
        direct_canonical_write_allowed=False,
        direct_network_mutation_allowed=False,
    )

    selected_model_role = {
        **profile,
        "selected_model_role": profile["role_id"],
        "route_reason": model_reason,
        "direct_execution_allowed": decision.safe_direct_action_allowed,
        "safe_direct_action_allowed": decision.safe_direct_action_allowed,
        "risk_gate_required": decision.risk_gate_required,
        "selected_tools": decision.selected_tools,
        "tool_route_reason": decision.selected_tool_reason,
        "owner_identity_claim": owner_identity_claim.to_read_model(),
        "pc_control_allowed": False,
        "pc_tool_direct_allowed": decision.safe_direct_action_allowed
        and any(tool.startswith("pc_") for tool in tools),
        "model_download_allowed": False,
        "runtime_start_allowed": False,
        "enqueue_required": heavy,
        "admission_required": True,
        "resource_gate_required": True,
        "parallel_heavy_model_allowed": decision.parallel_heavy_model_allowed,
        "conversation_model_kept_warm": decision.conversation_model_kept_warm,
        "queue_surface": "MAKSIMAR_CORE_LIB/execution_control",
        "worker_registry_surface": "MAKSIMAR_CORE_LIB/workers_registry",
    }

    payload = decision.to_read_model()
    payload["selected_model_role"] = selected_model_role
    payload["model_selection_working"] = True
    payload["tool_selection_working"] = True
    payload["voice_uses_same_router"] = channel == "voice"
    return payload


def _normalize_input_channel(input_channel: str) -> str:
    if input_channel not in {"text", "voice", "screen"}:
        raise ValueError(f"unsupported input_channel: {input_channel!r}")
    return input_channel


def _profile_by_role_id(role_id: str) -> dict[str, Any]:
    profiles = {profile.role_id: profile.to_read_model() for profile in build_jarvis_live_runtime_model_role_profiles()}
    if role_id not in profiles:
        raise ValueError(f"unknown runtime model role: {role_id}")
    return profiles[role_id]


def _classify_intent(lowered: str) -> str:
    if _is_risk_phrase(lowered):
        return "risk_action_request"
    if any(marker in lowered for marker in ("открой браузер", "open browser", "открой chrome", "открой edge")):
        return "safe_pc_open_browser"
    if any(marker in lowered for marker in ("открой vscode", "открой vs code", "открой терминал", "open terminal")):
        return "safe_pc_open_app"
    if any(marker in lowered for marker in ("погода", "weather", "температура на улице")):
        return "weather_lookup"
    if any(marker in lowered for marker in ("календар", "calendar", "термин", "встреч")):
        return "calendar_lookup"
    if any(marker in lowered for marker in ("почт", "gmail", "email", "письм")):
        return "mail_lookup"
    if any(marker in lowered for marker in ("экран", "screen", "что на экране", "видишь экран")):
        return "screen_observer"
    if any(marker in lowered for marker in ("структура проекта", "дерево проекта", "git status", "статус git", "проект", "repo")):
        return "project_workspace"
    if any(marker in lowered for marker in ("traceback", "architecture", "архитектур", "регресс", "сложн")):
        return "complex_code_analysis"
    if any(marker in lowered for marker in ("pytest", "тест", "ошибка", "код", "python", "diff", "патч")):
        return "code_debug"
    if any(marker in lowered for marker in ("классифиц", "кратко", "summary", "сводк")):
        return "classification_summary"
    return "conversation"


def _classify_complexity(lowered: str, intent: str) -> str:
    if intent == "complex_code_analysis":
        return "heavy"
    if intent in {"code_debug", "project_workspace"}:
        return "medium"
    if any(marker in lowered for marker in ("сложн", "architecture", "traceback", "регресс")):
        return "heavy"
    return "light"


def _select_model_role(intent: str, complexity: str) -> tuple[str, str]:
    if intent == "classification_summary":
        return "helper_classifier_model", "classification_or_summary"
    if complexity == "heavy":
        return "heavy_coder_model", "complex_code_or_architecture"
    if intent in {"code_debug", "project_workspace"}:
        return "daily_coder_model", "project_or_code_tool_assisted"
    return "jarvis_chat_model", "conversation_or_safe_tool_call"


def _select_tools(intent: str) -> tuple[tuple[str, ...], str]:
    if intent == "safe_pc_open_browser":
        return ("pc_open_browser",), "safe owner browser command"
    if intent == "safe_pc_open_app":
        return ("pc_open_app",), "safe owner app command"
    if intent == "weather_lookup":
        return ("weather_lookup",), "weather request"
    if intent == "calendar_lookup":
        return ("calendar_lookup",), "calendar request"
    if intent == "mail_lookup":
        return ("mail_lookup",), "mail request"
    if intent == "screen_observer":
        return ("screen_observer_read",), "screen read request"
    if intent == "project_workspace":
        return ("repo_git_status", "repo_tree", "repo_files", "read_file_snippet"), "project workspace request"
    if intent == "complex_code_analysis":
        return ("repo_search", "read_file_snippet", "read_file_outline"), "complex code analysis needs project read tools"
    if intent == "code_debug":
        return ("repo_search", "read_file_snippet", "pytest_report_read"), "code/debug request"
    if intent == "classification_summary":
        return ("session_memory", "local_chat_memory"), "summary/classification request"
    if intent == "risk_action_request":
        return ("risk_gate", "operator_proposal"), "high risk action requires gate"
    return (), "ordinary conversation"


def _is_safe_direct_action(intent: str, tools: tuple[str, ...]) -> bool:
    return intent in {"safe_pc_open_browser", "safe_pc_open_app"} and any(tool.startswith("pc_") for tool in tools)


def _is_risk_phrase(lowered: str) -> bool:
    return any(
        marker in lowered
        for marker in (
            "удали",
            "delete",
            "git push",
            "сделай push",
            "сделай коммит",
            "commit",
            "sudo",
            "pip install",
            "docker run",
            "firewall",
            "vpn",
            "отправь письмо",
            "send email",
            "деньги",
            "банк",
            "оплати",
        )
    )


def _is_risk_action(lowered: str, intent: str, tools: tuple[str, ...]) -> bool:
    return intent == "risk_action_request" or _is_risk_phrase(lowered) or "risk_gate" in tools


def _needs_ollama(intent: str) -> bool:
    return intent not in {"safe_pc_open_browser", "safe_pc_open_app", "weather_lookup", "calendar_lookup", "mail_lookup"}
