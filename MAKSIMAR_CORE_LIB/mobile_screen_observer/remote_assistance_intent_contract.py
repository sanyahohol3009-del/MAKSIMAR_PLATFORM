from __future__ import annotations

from dataclasses import dataclass


_ALLOWED_INTENT_STATES = ("requested", "denied_by_default", "approval_required", "blocked")


@dataclass(frozen=True)
class RemoteAssistanceIntentContract:
    """Normal observer remote assistance intent.

    This does not execute device control. It only records a safe intent state.
    """

    intent_id: str
    session_id: str
    intent_state: str
    owner_approval_required: bool
    consent_required: bool
    audit_required: bool
    disabled_by_default: bool
    dashboard_direct_execute_allowed: bool
    device_control_execution_allowed: bool
    runtime_mutation_allowed: bool
    core_write_allowed: bool

    def __post_init__(self) -> None:
        if not self.intent_id.strip():
            raise ValueError("intent_id must be non-empty")
        if not self.session_id.strip():
            raise ValueError("session_id must be non-empty")
        if self.intent_state not in _ALLOWED_INTENT_STATES:
            raise ValueError(f"intent_state must be one of {_ALLOWED_INTENT_STATES}")
        if not self.owner_approval_required:
            raise ValueError("owner_approval_required must be True")
        if not self.consent_required:
            raise ValueError("consent_required must be True")
        if not self.audit_required:
            raise ValueError("audit_required must be True")
        if not self.disabled_by_default:
            raise ValueError("disabled_by_default must be True")
        if self.dashboard_direct_execute_allowed:
            raise ValueError("dashboard_direct_execute_allowed must be False")
        if self.device_control_execution_allowed:
            raise ValueError("device_control_execution_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.core_write_allowed:
            raise ValueError("core_write_allowed must be False")

    def requires_manual_approval(self) -> bool:
        return self.intent_state in {"requested", "approval_required"}
