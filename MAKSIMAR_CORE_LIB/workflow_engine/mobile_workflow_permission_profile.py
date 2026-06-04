from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from MAKSIMAR_CORE_LIB.workflow_engine.local_ai_workflow_proposal_contract import (
    LocalAIWorkflowProposalContract,
)


ALLOWED_MOBILE_WORKFLOW_PLATFORMS: Tuple[str, ...] = ("android", "ios", "mobile_shared")
ALLOWED_PERMISSION_SOURCES: Tuple[str, ...] = (
    "user_settings",
    "system_permission",
    "guardian_policy",
    "owner_policy",
)
ALLOWED_PERMISSION_DECISION_CODES: Tuple[str, ...] = (
    "allowed",
    "explicit_permission_missing",
    "device_owner_not_confirmed",
    "workflow_scope_not_allowed",
    "capability_missing",
    "capability_revoked",
    "platform_capability_missing",
)


def _require_non_empty_text(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    return normalized


def _require_allowed(value: str, field_name: str, allowed_values: Tuple[str, ...]) -> str:
    normalized = _require_non_empty_text(value, field_name)
    if normalized not in allowed_values:
        raise ValueError(f"{field_name} must be one of {allowed_values}")
    return normalized


def _normalize_text_tuple(values: Tuple[str, ...], field_name: str) -> Tuple[str, ...]:
    if not isinstance(values, tuple):
        raise TypeError(f"{field_name} must be a tuple of strings")
    normalized = tuple(_require_non_empty_text(value, field_name) for value in values)
    if len(set(normalized)) != len(normalized):
        raise ValueError(f"{field_name} must not contain duplicates")
    return normalized


def _require_true(value: bool, field_name: str) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must be True in mobile workflow permission profiles")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must be False in mobile workflow permission profiles")


@dataclass(frozen=True)
class MobileWorkflowPermissionDecision:
    allowed: bool
    reason_code: str
    missing_capability_refs: Tuple[str, ...] = ()
    revoked_capability_refs: Tuple[str, ...] = ()
    platform_missing_capability_refs: Tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.allowed, bool):
            raise TypeError("allowed must be a boolean")
        object.__setattr__(
            self,
            "reason_code",
            _require_allowed(self.reason_code, "reason_code", ALLOWED_PERMISSION_DECISION_CODES),
        )
        object.__setattr__(
            self,
            "missing_capability_refs",
            _normalize_text_tuple(self.missing_capability_refs, "missing_capability_refs"),
        )
        object.__setattr__(
            self,
            "revoked_capability_refs",
            _normalize_text_tuple(self.revoked_capability_refs, "revoked_capability_refs"),
        )
        object.__setattr__(
            self,
            "platform_missing_capability_refs",
            _normalize_text_tuple(
                self.platform_missing_capability_refs,
                "platform_missing_capability_refs",
            ),
        )

    def to_read_model(self) -> dict[str, object]:
        return {
            "allowed": self.allowed,
            "reason_code": self.reason_code,
            "missing_capability_refs": self.missing_capability_refs,
            "revoked_capability_refs": self.revoked_capability_refs,
            "platform_missing_capability_refs": self.platform_missing_capability_refs,
        }


@dataclass(frozen=True)
class MobileWorkflowPermissionProfile:
    profile_id: str
    platform: str
    permission_source: str
    allowed_workflow_scopes: Tuple[str, ...]
    granted_capability_refs: Tuple[str, ...]
    platform_capability_refs: Tuple[str, ...]
    explicit_user_permission_granted: bool
    device_owner_confirmed: bool
    revoked_capability_refs: Tuple[str, ...] = ()
    user_approval_required: bool = True
    audit_required: bool = True
    sandbox_preview_required: bool = True
    contract_only: bool = True
    direct_phone_control_allowed: bool = False
    hidden_remote_control_allowed: bool = False
    direct_core_write_allowed: bool = False
    direct_server_canonical_write_allowed: bool = False
    network_allowed: bool = False
    socket_allowed: bool = False
    tunnel_allowed: bool = False
    network_socket_tunnel_allowed: bool = False
    runtime_mutation_allowed: bool = False
    platform_api_call_allowed: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "profile_id", _require_non_empty_text(self.profile_id, "profile_id"))
        object.__setattr__(
            self,
            "platform",
            _require_allowed(self.platform, "platform", ALLOWED_MOBILE_WORKFLOW_PLATFORMS),
        )
        object.__setattr__(
            self,
            "permission_source",
            _require_allowed(self.permission_source, "permission_source", ALLOWED_PERMISSION_SOURCES),
        )
        object.__setattr__(
            self,
            "allowed_workflow_scopes",
            _normalize_text_tuple(self.allowed_workflow_scopes, "allowed_workflow_scopes"),
        )
        object.__setattr__(
            self,
            "granted_capability_refs",
            _normalize_text_tuple(self.granted_capability_refs, "granted_capability_refs"),
        )
        object.__setattr__(
            self,
            "platform_capability_refs",
            _normalize_text_tuple(self.platform_capability_refs, "platform_capability_refs"),
        )
        object.__setattr__(
            self,
            "revoked_capability_refs",
            _normalize_text_tuple(self.revoked_capability_refs, "revoked_capability_refs"),
        )

        _require_true(self.user_approval_required, "user_approval_required")
        _require_true(self.audit_required, "audit_required")
        _require_true(self.sandbox_preview_required, "sandbox_preview_required")
        _require_true(self.contract_only, "contract_only")

        _require_false(self.direct_phone_control_allowed, "direct_phone_control_allowed")
        _require_false(self.hidden_remote_control_allowed, "hidden_remote_control_allowed")
        _require_false(self.direct_core_write_allowed, "direct_core_write_allowed")
        _require_false(self.direct_server_canonical_write_allowed, "direct_server_canonical_write_allowed")
        _require_false(self.network_allowed, "network_allowed")
        _require_false(self.socket_allowed, "socket_allowed")
        _require_false(self.tunnel_allowed, "tunnel_allowed")
        _require_false(self.network_socket_tunnel_allowed, "network_socket_tunnel_allowed")
        _require_false(self.runtime_mutation_allowed, "runtime_mutation_allowed")
        _require_false(self.platform_api_call_allowed, "platform_api_call_allowed")

    def evaluate_proposal(self, proposal: LocalAIWorkflowProposalContract) -> MobileWorkflowPermissionDecision:
        if not isinstance(proposal, LocalAIWorkflowProposalContract):
            raise TypeError("proposal must be a LocalAIWorkflowProposalContract")

        if self.explicit_user_permission_granted is not True:
            return MobileWorkflowPermissionDecision(False, "explicit_permission_missing")

        if self.device_owner_confirmed is not True:
            return MobileWorkflowPermissionDecision(False, "device_owner_not_confirmed")

        workflow_scope = proposal.graph.local_scope.workflow_scope
        if workflow_scope not in self.allowed_workflow_scopes:
            return MobileWorkflowPermissionDecision(False, "workflow_scope_not_allowed")

        granted = set(self.granted_capability_refs)
        requested = set(proposal.requested_capability_refs)
        revoked = requested.intersection(set(self.revoked_capability_refs))
        if revoked:
            return MobileWorkflowPermissionDecision(
                False,
                "capability_revoked",
                revoked_capability_refs=tuple(sorted(revoked)),
            )

        missing = requested.difference(granted)
        if missing:
            return MobileWorkflowPermissionDecision(
                False,
                "capability_missing",
                missing_capability_refs=tuple(sorted(missing)),
            )

        platform_capabilities = set(self.platform_capability_refs)
        platform_missing = requested.difference(platform_capabilities)
        if platform_missing:
            return MobileWorkflowPermissionDecision(
                False,
                "platform_capability_missing",
                platform_missing_capability_refs=tuple(sorted(platform_missing)),
            )

        return MobileWorkflowPermissionDecision(True, "allowed")

    def to_read_model(self) -> dict[str, object]:
        return {
            "profile_id": self.profile_id,
            "platform": self.platform,
            "permission_source": self.permission_source,
            "allowed_workflow_scopes": self.allowed_workflow_scopes,
            "granted_capability_refs": self.granted_capability_refs,
            "platform_capability_refs": self.platform_capability_refs,
            "explicit_user_permission_granted": self.explicit_user_permission_granted,
            "device_owner_confirmed": self.device_owner_confirmed,
            "revoked_capability_refs": self.revoked_capability_refs,
            "user_approval_required": self.user_approval_required,
            "audit_required": self.audit_required,
            "sandbox_preview_required": self.sandbox_preview_required,
            "contract_only": self.contract_only,
            "direct_phone_control_allowed": self.direct_phone_control_allowed,
            "hidden_remote_control_allowed": self.hidden_remote_control_allowed,
            "direct_core_write_allowed": self.direct_core_write_allowed,
            "direct_server_canonical_write_allowed": self.direct_server_canonical_write_allowed,
            "network_allowed": self.network_allowed,
            "socket_allowed": self.socket_allowed,
            "tunnel_allowed": self.tunnel_allowed,
            "network_socket_tunnel_allowed": self.network_socket_tunnel_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "platform_api_call_allowed": self.platform_api_call_allowed,
        }


def build_mobile_workflow_permission_profile(
    *,
    profile_id: str,
    platform: str,
    granted_capability_refs: Tuple[str, ...],
    platform_capability_refs: Tuple[str, ...],
    explicit_user_permission_granted: bool,
    device_owner_confirmed: bool,
) -> MobileWorkflowPermissionProfile:
    return MobileWorkflowPermissionProfile(
        profile_id=profile_id,
        platform=platform,
        permission_source="user_settings",
        allowed_workflow_scopes=("local_app_workflow", "device_assisted_workflow"),
        granted_capability_refs=granted_capability_refs,
        platform_capability_refs=platform_capability_refs,
        explicit_user_permission_granted=explicit_user_permission_granted,
        device_owner_confirmed=device_owner_confirmed,
    )


__all__ = [
    "ALLOWED_MOBILE_WORKFLOW_PLATFORMS",
    "ALLOWED_PERMISSION_DECISION_CODES",
    "ALLOWED_PERMISSION_SOURCES",
    "MobileWorkflowPermissionDecision",
    "MobileWorkflowPermissionProfile",
    "build_mobile_workflow_permission_profile",
]
