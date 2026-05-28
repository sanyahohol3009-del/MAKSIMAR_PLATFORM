from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.mobile_screen_observer.remote_assistance_intent_contract import (
    RemoteAssistanceIntentContract,
)


@dataclass(frozen=True)
class IOSRemoteAssistanceIntentBridge:
    device_id: str
    session_id: str
    owner_identity_id: str
    owner_approval_required: bool
    consent_required: bool
    audit_required: bool
    disabled_by_default: bool
    dashboard_direct_execute_allowed: bool
    device_control_execution_allowed: bool
    ios_platform_api_call_allowed: bool
    replaykit_allowed: bool
    accessibility_api_allowed: bool
    touch_execution_allowed: bool
    keyboard_execution_allowed: bool
    child_control_enabled: bool
    external_network_access_allowed: bool
    runtime_mutation_allowed: bool
    core_write_allowed: bool

    def __post_init__(self) -> None:
        for field_name in ("device_id", "session_id", "owner_identity_id"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")

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
        if self.ios_platform_api_call_allowed:
            raise ValueError("ios_platform_api_call_allowed must be False")
        if self.replaykit_allowed:
            raise ValueError("replaykit_allowed must be False")
        if self.accessibility_api_allowed:
            raise ValueError("accessibility_api_allowed must be False")
        if self.touch_execution_allowed:
            raise ValueError("touch_execution_allowed must be False")
        if self.keyboard_execution_allowed:
            raise ValueError("keyboard_execution_allowed must be False")
        if self.child_control_enabled:
            raise ValueError("normal iOS remote assistance cannot enable child control")
        if self.external_network_access_allowed:
            raise ValueError("external_network_access_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.core_write_allowed:
            raise ValueError("core_write_allowed must be False")

    @classmethod
    def default(
        cls,
        *,
        device_id: str,
        session_id: str,
        owner_identity_id: str,
    ) -> "IOSRemoteAssistanceIntentBridge":
        return cls(
            device_id=device_id,
            session_id=session_id,
            owner_identity_id=owner_identity_id,
            owner_approval_required=True,
            consent_required=True,
            audit_required=True,
            disabled_by_default=True,
            dashboard_direct_execute_allowed=False,
            device_control_execution_allowed=False,
            ios_platform_api_call_allowed=False,
            replaykit_allowed=False,
            accessibility_api_allowed=False,
            touch_execution_allowed=False,
            keyboard_execution_allowed=False,
            child_control_enabled=False,
            external_network_access_allowed=False,
            runtime_mutation_allowed=False,
            core_write_allowed=False,
        )

    def build_intent_contract(
        self,
        *,
        intent_id: str,
        intent_state: str = "approval_required",
    ) -> RemoteAssistanceIntentContract:
        if not isinstance(intent_id, str) or not intent_id.strip():
            raise ValueError("intent_id must be a non-empty string")

        return RemoteAssistanceIntentContract(
            intent_id=intent_id,
            session_id=self.session_id,
            intent_state=intent_state,
            owner_approval_required=self.owner_approval_required,
            consent_required=self.consent_required,
            audit_required=self.audit_required,
            disabled_by_default=self.disabled_by_default,
            dashboard_direct_execute_allowed=self.dashboard_direct_execute_allowed,
            device_control_execution_allowed=self.device_control_execution_allowed,
            runtime_mutation_allowed=self.runtime_mutation_allowed,
            core_write_allowed=self.core_write_allowed,
        )

    def to_read_model(self) -> dict[str, object]:
        return {
            "shell": "IOS_SHELL",
            "bridge": "remote_assistance_intent",
            "device_id": self.device_id,
            "session_id": self.session_id,
            "owner_identity_id": self.owner_identity_id,
            "owner_approval_required": self.owner_approval_required,
            "consent_required": self.consent_required,
            "audit_required": self.audit_required,
            "disabled_by_default": self.disabled_by_default,
            "dashboard_direct_execute_allowed": self.dashboard_direct_execute_allowed,
            "device_control_execution_allowed": self.device_control_execution_allowed,
            "ios_platform_api_call_allowed": self.ios_platform_api_call_allowed,
            "replaykit_allowed": self.replaykit_allowed,
            "accessibility_api_allowed": self.accessibility_api_allowed,
            "touch_execution_allowed": self.touch_execution_allowed,
            "keyboard_execution_allowed": self.keyboard_execution_allowed,
            "child_control_enabled": self.child_control_enabled,
            "external_network_access_allowed": self.external_network_access_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "core_write_allowed": self.core_write_allowed,
        }
