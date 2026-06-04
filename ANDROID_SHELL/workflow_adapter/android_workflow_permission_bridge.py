from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ANDROID_SHELL.workflow_adapter.android_workflow_capability_limits import (
    ANDROID_WORKFLOW_PLATFORM,
    AndroidWorkflowCapabilityLimits,
    build_android_workflow_capability_limits,
)
from MAKSIMAR_CORE_LIB.workflow_engine.local_ai_workflow_proposal_contract import (
    LocalAIWorkflowProposalContract,
)
from MAKSIMAR_CORE_LIB.workflow_engine.mobile_workflow_permission_profile import (
    MobileWorkflowPermissionDecision,
    MobileWorkflowPermissionProfile,
)


def _require_non_empty_text(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    return normalized


def _require_true(value: bool, field_name: str) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must be True in Android workflow permission bridge")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must be False in Android workflow permission bridge")


@dataclass(frozen=True)
class AndroidWorkflowPermissionBridgeResult:
    bridge_id: str
    platform: str
    permission_decision: MobileWorkflowPermissionDecision
    permission_profile: MobileWorkflowPermissionProfile

    def __post_init__(self) -> None:
        object.__setattr__(self, "bridge_id", _require_non_empty_text(self.bridge_id, "bridge_id"))
        if self.platform != ANDROID_WORKFLOW_PLATFORM:
            raise ValueError("platform must be android")
        if not isinstance(self.permission_decision, MobileWorkflowPermissionDecision):
            raise TypeError("permission_decision must be a MobileWorkflowPermissionDecision")
        if not isinstance(self.permission_profile, MobileWorkflowPermissionProfile):
            raise TypeError("permission_profile must be a MobileWorkflowPermissionProfile")

    def to_read_model(self) -> dict[str, object]:
        return {
            "bridge_id": self.bridge_id,
            "platform": self.platform,
            "permission_decision": self.permission_decision.to_read_model(),
            "permission_profile": self.permission_profile.to_read_model(),
        }


@dataclass(frozen=True)
class AndroidWorkflowPermissionBridge:
    bridge_id: str
    capability_limits: AndroidWorkflowCapabilityLimits
    explicit_user_permission_granted: bool
    device_owner_confirmed: bool
    contract_only: bool = True
    direct_phone_control_allowed: bool = False
    hidden_remote_control_allowed: bool = False
    direct_core_write_allowed: bool = False
    direct_server_canonical_write_allowed: bool = False
    network_allowed_by_default: bool = False
    socket_allowed_by_default: bool = False
    tunnel_allowed_by_default: bool = False
    runtime_mutation_allowed: bool = False
    platform_api_call_allowed: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "bridge_id", _require_non_empty_text(self.bridge_id, "bridge_id"))
        if not isinstance(self.capability_limits, AndroidWorkflowCapabilityLimits):
            raise TypeError("capability_limits must be an AndroidWorkflowCapabilityLimits")
        if not isinstance(self.explicit_user_permission_granted, bool):
            raise TypeError("explicit_user_permission_granted must be a boolean")
        if not isinstance(self.device_owner_confirmed, bool):
            raise TypeError("device_owner_confirmed must be a boolean")

        _require_true(self.contract_only, "contract_only")
        _require_false(self.direct_phone_control_allowed, "direct_phone_control_allowed")
        _require_false(self.hidden_remote_control_allowed, "hidden_remote_control_allowed")
        _require_false(self.direct_core_write_allowed, "direct_core_write_allowed")
        _require_false(self.direct_server_canonical_write_allowed, "direct_server_canonical_write_allowed")
        _require_false(self.network_allowed_by_default, "network_allowed_by_default")
        _require_false(self.socket_allowed_by_default, "socket_allowed_by_default")
        _require_false(self.tunnel_allowed_by_default, "tunnel_allowed_by_default")
        _require_false(self.runtime_mutation_allowed, "runtime_mutation_allowed")
        _require_false(self.platform_api_call_allowed, "platform_api_call_allowed")

    def build_permission_profile(self) -> MobileWorkflowPermissionProfile:
        return self.capability_limits.to_permission_profile(
            profile_id=f"{self.bridge_id}.permission.profile",
            explicit_user_permission_granted=self.explicit_user_permission_granted,
            device_owner_confirmed=self.device_owner_confirmed,
        )

    def evaluate_proposal(self, proposal: LocalAIWorkflowProposalContract) -> AndroidWorkflowPermissionBridgeResult:
        if not isinstance(proposal, LocalAIWorkflowProposalContract):
            raise TypeError("proposal must be a LocalAIWorkflowProposalContract")
        profile = self.build_permission_profile()
        decision = profile.evaluate_proposal(proposal)
        return AndroidWorkflowPermissionBridgeResult(
            bridge_id=self.bridge_id,
            platform=ANDROID_WORKFLOW_PLATFORM,
            permission_decision=decision,
            permission_profile=profile,
        )

    def to_read_model(self) -> dict[str, object]:
        return {
            "bridge_id": self.bridge_id,
            "platform": ANDROID_WORKFLOW_PLATFORM,
            "capability_limits": self.capability_limits.to_read_model(),
            "explicit_user_permission_granted": self.explicit_user_permission_granted,
            "device_owner_confirmed": self.device_owner_confirmed,
            "contract_only": self.contract_only,
            "direct_phone_control_allowed": self.direct_phone_control_allowed,
            "hidden_remote_control_allowed": self.hidden_remote_control_allowed,
            "direct_core_write_allowed": self.direct_core_write_allowed,
            "direct_server_canonical_write_allowed": self.direct_server_canonical_write_allowed,
            "network_allowed_by_default": self.network_allowed_by_default,
            "socket_allowed_by_default": self.socket_allowed_by_default,
            "tunnel_allowed_by_default": self.tunnel_allowed_by_default,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "platform_api_call_allowed": self.platform_api_call_allowed,
        }


def build_android_workflow_permission_bridge(
    *,
    bridge_id: str = "android.workflow.permission.bridge.v1",
    capability_limits: Optional[AndroidWorkflowCapabilityLimits] = None,
    explicit_user_permission_granted: bool,
    device_owner_confirmed: bool,
) -> AndroidWorkflowPermissionBridge:
    return AndroidWorkflowPermissionBridge(
        bridge_id=bridge_id,
        capability_limits=capability_limits or build_android_workflow_capability_limits(),
        explicit_user_permission_granted=explicit_user_permission_granted,
        device_owner_confirmed=device_owner_confirmed,
    )


__all__ = [
    "AndroidWorkflowPermissionBridge",
    "AndroidWorkflowPermissionBridgeResult",
    "build_android_workflow_permission_bridge",
]
