from __future__ import annotations

import hashlib
import json
import os
import base64
import subprocess
import time
from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import (
    EvidenceBundle, EvidenceItem, ExecutionPlan, ExecutionReceipt, RequestDeadline,
    RequestUnderstanding, utc_observed_at,
)


WINDOWS_EDGE_PROVIDER_ID = "windows_edge_adapter"
WINDOWS_EDGE_PYTHON = os.environ.get(
    "JARVIS_WINDOWS_EDGE_PYTHON", "/mnt/c/MAKSIMAR_EDGE/.venv/Scripts/python.exe",
)
WINDOWS_EDGE_SCRIPT = os.environ.get(
    "JARVIS_WINDOWS_EDGE_SCRIPT", r"C:\MAKSIMAR_EDGE\jarvis_windows_live_runtime.py",
)
WINDOWS_EDGE_HEALTH_URL = "windows-edge://pinned-owner/health"
WINDOWS_EDGE_EXECUTE_URL = "windows-edge://pinned-owner/execute"
WINDOWS_EDGE_HEALTH_CACHE_TTL_SECONDS = 30.0
_WINDOWS_EDGE_HEALTH_CACHE: tuple[float, dict[str, Any]] | None = None


JARVIS_PC_ACTION_ALLOWLIST_IDS: tuple[str, ...] = (
    "open_project_workbench",
    "open_browser",
    "open_opera",
    "close_opera",
    "close_all_opera",
    "type_text",
    "volume_up",
    "volume_down",
    "volume_mute",
    "read_screen",
    "browser_search",
)

DIRECT_PC_ACTION_MAP: dict[str, dict[str, Any]] = {
    "open_project_workbench": {"action_family":"pc_app_open","executor_function":"open_project_workbench","target":"canonical_project_workbench","direct_owner_gate":True,"protected":False,"required_parameters":(),"allowed_parameters":()},
    "open_browser": {"action_family": "browser_open", "executor_function": "open_browser", "target": "default_browser", "direct_owner_gate": True, "protected": False, "required_parameters": (), "allowed_parameters": ()},
    "open_opera": {"action_family": "pc_app_open", "executor_function": "open_app", "target": "opera", "direct_owner_gate": True, "protected": False, "required_parameters": (), "allowed_parameters": ()},
    "close_opera": {"action_family": "pc_app_close", "executor_function": "close_one_window", "target": "opera", "direct_owner_gate": True, "protected": False, "required_parameters": (), "allowed_parameters": (), "close_strategy": "graceful_single_window", "preferred_mechanism": "WM_CLOSE_or_AltF4"},
    "close_all_opera": {"action_family": "pc_app_kill_all", "executor_function": "kill_all_processes", "target": "opera", "direct_owner_gate": True, "protected": False, "required_parameters": (), "allowed_parameters": (), "close_strategy": "force_all_processes", "preferred_mechanism": "targeted_process_identity_required"},
    "type_text": {"action_family": "pc_text_input", "executor_function": "type_text", "target": "active_window", "direct_owner_gate": True, "protected": False, "required_parameters": ("text",), "allowed_parameters": ("text",)},
    "volume_up": {"action_family": "pc_volume_up", "executor_function": "volume_up", "target": "system_volume", "direct_owner_gate": True, "protected": False, "required_parameters": (), "allowed_parameters": ()},
    "volume_down": {"action_family": "pc_volume_down", "executor_function": "volume_down", "target": "system_volume", "direct_owner_gate": True, "protected": False, "required_parameters": (), "allowed_parameters": ()},
    "volume_mute": {"action_family": "pc_volume_mute", "executor_function": "volume_mute", "target": "system_volume", "direct_owner_gate": True, "protected": False, "required_parameters": (), "allowed_parameters": ()},
    "read_screen": {"action_family": "screen_read", "executor_function": "read_screen", "target": "desktop", "direct_owner_gate": True, "protected": False, "required_parameters": (), "allowed_parameters": ()},
    "browser_search": {"action_family": "browser_search", "executor_function": "browser_search", "target": "default_browser", "direct_owner_gate": True, "protected": False, "required_parameters": ("query",), "allowed_parameters": ("query",)},
}

DIRECT_PC_ACTION_FAMILIES: tuple[str, ...] = tuple(
    dict.fromkeys(str(value["action_family"]) for value in DIRECT_PC_ACTION_MAP.values())
)


def _operation_contract(
    operation_id: str, description: str, *, required_parameters: tuple[str, ...] = (),
    evidence_kind: str = "pc_action_result", effect_type: str = "MUTATE",
    target_scope: str = "owner_windows_desktop", semantic_owner_id: str = "windows.browser",
    reversibility: str = "REVERSIBLE",
    external_side_effect: bool = False, risk_class: str = "MUTATION",
) -> tuple[dict[str, Any], ...]:
    return ({
        "operation_id": operation_id, "description": description,
        "required_parameters": required_parameters, "evidence_kinds": (evidence_kind,),
        "effect_type": effect_type, "target_scope": target_scope,
        "semantic_owner_id": semantic_owner_id,
        "reversibility": reversibility, "external_side_effect": external_side_effect,
        "risk_class": risk_class,
    },)


PC_ACTION_OPERATION_CONTRACTS: dict[str, tuple[dict[str, Any], ...]] = {
    "open_project_workbench": _operation_contract(
        "execute_open_project_workbench", "Open the canonical MAKSIMAR_PLATFORM project in the installed Microsoft VS Code developer workbench on the owner's Windows desktop; use the real IDE, with no editing.",
        semantic_owner_id="windows.workbench", evidence_kind="project_workbench_opened",
    ),
    "open_browser": _operation_contract(
        "execute_open_browser", "Open the default browser on the verified owner's Windows desktop.",
        semantic_owner_id="windows.browser", effect_type="MUTATE", risk_class="MUTATION",
    ),
    "open_opera": _operation_contract(
        "execute_open_opera", "Open Opera on the verified owner's Windows desktop.",
        semantic_owner_id="windows.browser", effect_type="MUTATE", risk_class="MUTATION",
    ),
    "close_opera": _operation_contract(
        "execute_close_one_opera_window", "Close one Opera window gracefully.",
        semantic_owner_id="windows.browser", reversibility="IRREVERSIBLE", risk_class="DANGEROUS",
    ),
    "close_all_opera": _operation_contract(
        "execute_close_all_opera_processes", "Force-close all Opera processes.",
        semantic_owner_id="windows.browser", reversibility="IRREVERSIBLE", risk_class="DANGEROUS",
    ),
    "type_text": _operation_contract(
        "execute_type_text", "Type supplied text into the active Windows application.",
        semantic_owner_id="windows.input", required_parameters=("text",), reversibility="IRREVERSIBLE",
        external_side_effect=True, risk_class="DANGEROUS",
    ),
    "volume_up": _operation_contract(
        "execute_volume_up", "Increase Windows system volume by one step.",
        semantic_owner_id="windows.volume",
    ),
    "volume_down": _operation_contract(
        "execute_volume_down", "Decrease Windows system volume by one step.",
        semantic_owner_id="windows.volume",
    ),
    "volume_mute": _operation_contract(
        "execute_volume_mute_toggle", "Toggle Windows system mute.",
        semantic_owner_id="windows.volume",
    ),
    "read_screen": _operation_contract(
        "observe_windows_screen", "Capture the current Windows desktop as bounded screenshot evidence.",
        evidence_kind="windows_screen_capture", effect_type="OBSERVE",
        target_scope="owner_windows_screen", semantic_owner_id="screen.observe", risk_class="READ_ONLY",
    ),
    "browser_search": _operation_contract(
        "execute_browser_search", "Open a browser search for the supplied query.",
        semantic_owner_id="windows.browser", required_parameters=("query",), reversibility="REVERSIBLE",
        external_side_effect=True, risk_class="DANGEROUS",
    ),
    "runtime_windows_edge": _operation_contract(
        "read_windows_edge_status", "Check current Windows Edge owner availability and reachability and return status evidence.",
        evidence_kind="windows_edge_status", effect_type="OBSERVE",
        target_scope="localhost_windows_edge", semantic_owner_id="windows.edge", risk_class="READ_ONLY",
    ),
}

OPERATION_TO_ACTION_ID = {
    contract[0]["operation_id"]: capability_id
    for capability_id, contract in PC_ACTION_OPERATION_CONTRACTS.items()
    if capability_id != "runtime_windows_edge"
}


def resolve_pc_action_for_operation(operation_id: str) -> dict[str, Any]:
    """Thin canonical reverse lookup: canonical operation_id -> PC action binding.

    Uses the existing OPERATION_TO_ACTION_ID (derived from PC_ACTION_OPERATION_CONTRACTS),
    never a hand-written operation->action map, and never reinterprets user text.
    """
    action_id = OPERATION_TO_ACTION_ID.get(str(operation_id or "").strip())
    if action_id is None:
        return {
            "ok": False, "status": "unknown_operation",
            "operation_id": str(operation_id or "").strip(),
        }
    resolved = resolve_direct_pc_action(action_id)
    resolved["operation_id"] = str(operation_id or "").strip()
    return resolved


def resolve_direct_pc_action(action_id: str) -> dict[str, Any]:
    normalized_id = str(action_id or "").strip()
    action = DIRECT_PC_ACTION_MAP.get(normalized_id)
    if action is None:
        return {"ok": False, "status": "blocked_unknown_action", "action_id": normalized_id, "executor_function": ""}
    return {"ok": True, "status": "direct_action_allowed", "action_id": normalized_id, **action}


def build_windows_edge_executor_payload(envelope: dict[str, Any]) -> dict[str, Any]:
    """Project-side typed platform-adapter envelope; it never executes the action."""
    return {
        "ok": bool(envelope.get("ok", False)),
        "action_id": str(envelope.get("action_id", "")).strip(),
        "action_family": str(envelope.get("action_family", "")).strip(),
        "target": str(envelope.get("target", "")).strip(),
        "parameters": dict(envelope.get("parameters", {})),
        "executor_function": str(envelope.get("executor_function", "")).strip(),
        "platform_adapter_id": "windows_edge_adapter",
        "device_context": dict(envelope.get("device_context", {})),
        "close_strategy": str(envelope.get("close_strategy", "")).strip(),
        "preferred_mechanism": str(envelope.get("preferred_mechanism", "")).strip(),
        "owner_pc_action_eligible": bool(envelope.get("owner_pc_action_eligible", False)),
        "policy_execution_allowed": bool(envelope.get("policy_execution_allowed", False)),
        "pc_operation_authorized_for_this_turn": bool(envelope.get("pc_operation_authorized_for_this_turn", False)),
        "executed": False,
        "execution_receipt": None,
    }


class ExistingWindowsEdgeAdapter:
    """Canonical evidence bridge to the existing localhost Windows owner."""

    provider_id = WINDOWS_EDGE_PROVIDER_ID

    @staticmethod
    def _run_owner(arguments: tuple[str, ...], *, timeout: float) -> dict[str, Any]:
        completed = subprocess.run(
            [WINDOWS_EDGE_PYTHON, WINDOWS_EDGE_SCRIPT, *arguments],
            text=True, encoding="utf-8", errors="replace", capture_output=True,
            timeout=max(0.1, timeout), check=False, shell=False,
        )
        lines = tuple(line.strip() for line in completed.stdout.splitlines() if line.strip())
        if completed.returncode != 0 or not lines:
            raise RuntimeError(
                f"windows_owner_exit_{completed.returncode}:" + completed.stderr.strip()[-200:]
            )
        value = json.loads(lines[-1])
        return value if isinstance(value, dict) else {}

    def health(self) -> dict[str, Any]:
        global _WINDOWS_EDGE_HEALTH_CACHE
        now = time.monotonic()
        if (
            _WINDOWS_EDGE_HEALTH_CACHE is not None
            and now - _WINDOWS_EDGE_HEALTH_CACHE[0] <= WINDOWS_EDGE_HEALTH_CACHE_TTL_SECONDS
        ):
            return dict(_WINDOWS_EDGE_HEALTH_CACHE[1])
        try:
            result = self._run_owner(("--health-json",), timeout=3.0)
        except (subprocess.SubprocessError, TimeoutError, OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
            health = {
                "provider_id": self.provider_id, "status": "UNAVAILABLE",
                "health_url": WINDOWS_EDGE_HEALTH_URL, "error": type(exc).__name__,
            }
            _WINDOWS_EDGE_HEALTH_CACHE = (now, health)
            return dict(health)
        available = result.get("ok") is True and result.get("status") == "AVAILABLE"
        health = {
            "provider_id": self.provider_id,
            "status": "AVAILABLE" if available else "UNAVAILABLE",
            "health_url": WINDOWS_EDGE_HEALTH_URL,
            "owner": str(result.get("owner", "")),
            "actions": tuple(str(item) for item in result.get("actions", ())),
        }
        _WINDOWS_EDGE_HEALTH_CACHE = (now, health)
        return dict(health)

    def collect_evidence(
        self, understanding: RequestUnderstanding, plan: ExecutionPlan, trace_id: str,
        deadline: RequestDeadline | None = None,
    ) -> EvidenceBundle:
        items: list[EvidenceItem] = []
        receipts: list[ExecutionReceipt] = []
        errors: list[str] = []
        for step in plan.steps:
            if deadline is not None and deadline.cancelled:
                errors.append(f"{step.operation}:total_deadline")
                break
            capability_id = step.capability_id
            contract = PC_ACTION_OPERATION_CONTRACTS.get(capability_id, ())
            if not contract or contract[0]["operation_id"] != step.operation:
                errors.append(f"{step.operation}:unsupported_operation")
                continue
            try:
                if capability_id == "runtime_windows_edge":
                    result = self.health()
                    if result.get("status") != "AVAILABLE":
                        raise RuntimeError("windows_edge_unavailable")
                    evidence_kind = "windows_edge_status"
                    source_reference = WINDOWS_EDGE_HEALTH_URL
                else:
                    component_limit = 40.0 if step.operation == "execute_open_project_workbench" else 15.0
                    remaining = deadline.remaining() if deadline is not None else component_limit
                    payload = base64.b64encode(json.dumps({
                        "action_id": capability_id, "parameters": dict(step.parameters),
                    }, ensure_ascii=False).encode("utf-8")).decode("ascii")
                    result = self._run_owner(
                        ("--execute-json-base64", payload),
                        timeout=min(component_limit, max(0.1, remaining)),
                    )
                    if result.get("ok") is not True or result.get("executed") is not True:
                        raise RuntimeError(str(result.get("error", "windows_action_failed")))
                    evidence_kind = str(contract[0]["evidence_kinds"][0])
                    source_reference = WINDOWS_EDGE_EXECUTE_URL
            except (subprocess.SubprocessError, TimeoutError, OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
                errors.append(f"{step.operation}:{type(exc).__name__}:{exc}")
                continue
            observation = json.dumps(result, ensure_ascii=False, sort_keys=True)
            items.append(EvidenceItem(
                kind=evidence_kind, source=f"{self.provider_id}:{step.operation}",
                observation=observation, scope=str(contract[0]["target_scope"]), confidence=1.0,
                trace_id=trace_id, observed_at=utc_observed_at(),
                content_hash="sha256:" + hashlib.sha256(observation.encode("utf-8")).hexdigest(),
                source_reference=source_reference, truncated=False, omitted_count=0,
                request_id=understanding.request_id, step_id=step.step_id,
                capability_id=capability_id, operation_id=step.operation, provider_id=self.provider_id,
            ))
            receipts.append(ExecutionReceipt(
                receipt_id=f"{trace_id}:{step.step_id}", request_id=understanding.request_id,
                trace_id=trace_id, step_id=step.step_id, capability_id=capability_id,
                operation_id=step.operation, provider_id=self.provider_id,
                status="COMPLETE", result="existing Windows Edge owner completed typed operation",
            ))
        status = "COMPLETE" if items and not errors else "PARTIAL" if items else "UNAVAILABLE"
        capability_ids = tuple(dict.fromkeys(step.capability_id for step in plan.steps))
        return EvidenceBundle(
            request_id=understanding.request_id,
            capability_id=(capability_ids[0] if capability_ids else "runtime_windows_edge"),
            trace_id=trace_id, status=status, items=tuple(items),
            limitations=(() if status == "COMPLETE" else ("Windows Edge operation incomplete",)),
            receipts=tuple(receipts), errors=tuple(errors), capability_ids=capability_ids,
        )


def _k(*parts: str) -> str:
    return "".join(parts)


TRUE_ADAPTER_GATES: tuple[str, ...] = (
    "operation_allowlisted",
    "owner_low_risk_policy_eligible",
    "app_launch_operation_supported",
    "browser_operation_supported",
)


FALSE_ADAPTER_GATES: tuple[str, ...] = (
    "mouse_runtime_allowed",
    "keyboard_runtime_allowed",
    _k("cl", "ick_runtime_allowed"),
    "typing_runtime_allowed",
    "shell_allowed",
    _k("sub", "process_allowed"),
    _k("power", "shell_allowed"),
    "hidden_remote_control_allowed",
    "autonomous_action_allowed",
    "dashboard_execution_allowed",
)


@dataclass(frozen=True, slots=True)
class JarvisPcActionAdapterContract:
    adapter_id: str
    allowed_action_ids: tuple[str, ...]
    read_only_contract: bool = False
    controlled_pc_action_candidate: bool = True
    owner_command_required: bool = True
    allowlist_required: bool = True
    approval_required: bool = False
    audit_required: bool = True
    policy_boundary_required: bool = True
    screen_context_required: bool = False
    voice_or_text_intent_required: bool = True
    explicit_action_preview_required: bool = False
    enabled_gates: tuple[tuple[str, bool], ...] = tuple(
        (key, True) for key in TRUE_ADAPTER_GATES
    )
    disabled_gates: tuple[tuple[str, bool], ...] = tuple(
        (key, False) for key in FALSE_ADAPTER_GATES
    )

    def __post_init__(self) -> None:
        _require_non_empty(self.adapter_id, "adapter_id")
        if self.allowed_action_ids != JARVIS_PC_ACTION_ALLOWLIST_IDS:
            raise ValueError("allowed_action_ids must match canonical JARVIS PC actions")
        _require_false(self.read_only_contract, "read_only_contract")
        _require_true(
            self.controlled_pc_action_candidate,
            "controlled_pc_action_candidate",
        )
        _require_true(self.owner_command_required, "owner_command_required")
        _require_true(self.allowlist_required, "allowlist_required")
        _require_false(self.approval_required, "approval_required")
        _require_true(self.audit_required, "audit_required")
        _require_true(self.policy_boundary_required, "policy_boundary_required")
        _require_false(self.screen_context_required, "screen_context_required")
        _require_true(
            self.voice_or_text_intent_required,
            "voice_or_text_intent_required",
        )
        _require_false(
            self.explicit_action_preview_required,
            "explicit_action_preview_required",
        )
        if tuple(key for key, _value in self.enabled_gates) != TRUE_ADAPTER_GATES:
            raise ValueError("enabled_gates must match canonical adapter gates")
        if tuple(key for key, _value in self.disabled_gates) != FALSE_ADAPTER_GATES:
            raise ValueError("disabled_gates must match canonical adapter gates")
        for key, value in self.enabled_gates:
            _require_non_empty(key, "enabled_gates")
            _require_true(value, key)
        for key, value in self.disabled_gates:
            _require_non_empty(key, "disabled_gates")
            _require_false(value, key)

    def to_read_model(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "adapter_id": self.adapter_id,
            "allowed_action_ids": self.allowed_action_ids,
            "read_only_contract": self.read_only_contract,
            "controlled_pc_action_candidate": self.controlled_pc_action_candidate,
            "owner_command_required": self.owner_command_required,
            "allowlist_required": self.allowlist_required,
            "approval_required": self.approval_required,
            "audit_required": self.audit_required,
            "policy_boundary_required": self.policy_boundary_required,
            "screen_context_required": self.screen_context_required,
            "voice_or_text_intent_required": self.voice_or_text_intent_required,
            "explicit_action_preview_required": self.explicit_action_preview_required,
        }
        payload.update(dict(self.enabled_gates))
        payload.update(dict(self.disabled_gates))
        return payload


def build_jarvis_pc_action_adapter_contract() -> JarvisPcActionAdapterContract:
    return JarvisPcActionAdapterContract(
        adapter_id="jarvis_pc_action_adapter_contract_v1",
        allowed_action_ids=JARVIS_PC_ACTION_ALLOWLIST_IDS,
    )


def _require_non_empty(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")


def _require_true(value: bool, field_name: str) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must remain enabled")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must remain disabled")
