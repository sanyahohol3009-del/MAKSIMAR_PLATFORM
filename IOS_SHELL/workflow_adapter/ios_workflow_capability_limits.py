from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from MAKSIMAR_CORE_LIB.workflow_engine.mobile_workflow_permission_profile import (
    MobileWorkflowPermissionProfile,
)


IOS_WORKFLOW_PLATFORM = "ios"
ALLOWED_IOS_WORKFLOW_SCOPES: Tuple[str, ...] = (
    "local_app_workflow",
    "device_assisted_workflow",
)
DEFAULT_IOS_WORKFLOW_CAPABILITIES: Tuple[str, ...] = (
    "local_ai_workflow_proposal",
    "explicit_user_approval",
    "sandbox_preview_review",
    "workflow_audit_event",
    "offline_intent_queue",
)


def _require_non_empty_text(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    return normalized


def _normalize_text_tuple(values: Tuple[str, ...], field_name: str, *, require_non_empty: bool) -> Tuple[str, ...]:
    if not isinstance(values, tuple):
        raise TypeError(f"{field_name} must be a tuple of strings")
    normalized = tuple(_require_non_empty_text(value, field_name) for value in values)
    if require_non_empty and not normalized:
        raise ValueError(f"{field_name} must not be empty")
    if len(set(normalized)) != len(normalized):
        raise ValueError(f"{field_name} must not contain duplicates")
    return normalized


def _require_true(value: bool, field_name: str) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must be True in iOS workflow capability limits")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must be False in iOS workflow capability limits")


@dataclass(frozen=True)
class IOSWorkflowCapabilityLimits:
    limits_id: str
    allowed_capability_refs: Tuple[str, ...]
    platform_capability_refs: Tuple[str, ...]
    allowed_workflow_scopes: Tuple[str, ...] = ALLOWED_IOS_WORKFLOW_SCOPES
    revoked_capability_refs: Tuple[str, ...] = ()
    requires_explicit_user_permission: bool = True
    requires_device_owner_confirmation: bool = True
    requires_sandbox_preview: bool = True
    requires_audit: bool = True
    local_first: bool = True
    server_optional: bool = True
    offline_queue_allowed: bool = True
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
        object.__setattr__(self, "limits_id", _require_non_empty_text(self.limits_id, "limits_id"))
        object.__setattr__(
            self,
            "allowed_capability_refs",
            _normalize_text_tuple(self.allowed_capability_refs, "allowed_capability_refs", require_non_empty=True),
        )
        object.__setattr__(
            self,
            "platform_capability_refs",
            _normalize_text_tuple(self.platform_capability_refs, "platform_capability_refs", require_non_empty=True),
        )
        object.__setattr__(
            self,
            "allowed_workflow_scopes",
            _normalize_text_tuple(self.allowed_workflow_scopes, "allowed_workflow_scopes", require_non_empty=True),
        )
        object.__setattr__(
            self,
            "revoked_capability_refs",
            _normalize_text_tuple(self.revoked_capability_refs, "revoked_capability_refs", require_non_empty=False),
        )

        unknown_scopes = tuple(scope for scope in self.allowed_workflow_scopes if scope not in ALLOWED_IOS_WORKFLOW_SCOPES)
        if unknown_scopes:
            raise ValueError(f"allowed_workflow_scopes contains unsupported iOS scopes: {unknown_scopes}")

        _require_true(self.requires_explicit_user_permission, "requires_explicit_user_permission")
        _require_true(self.requires_device_owner_confirmation, "requires_device_owner_confirmation")
        _require_true(self.requires_sandbox_preview, "requires_sandbox_preview")
        _require_true(self.requires_audit, "requires_audit")
        _require_true(self.local_first, "local_first")
        _require_true(self.server_optional, "server_optional")
        _require_true(self.offline_queue_allowed, "offline_queue_allowed")
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

    def missing_capability_refs(self, requested_capability_refs: Tuple[str, ...]) -> Tuple[str, ...]:
        requested = set(_normalize_text_tuple(requested_capability_refs, "requested_capability_refs", require_non_empty=True))
        allowed = set(self.allowed_capability_refs)
        return tuple(sorted(requested.difference(allowed)))

    def revoked_requested_capability_refs(self, requested_capability_refs: Tuple[str, ...]) -> Tuple[str, ...]:
        requested = set(_normalize_text_tuple(requested_capability_refs, "requested_capability_refs", require_non_empty=True))
        revoked = set(self.revoked_capability_refs)
        return tuple(sorted(requested.intersection(revoked)))

    def to_permission_profile(
        self,
        *,
        profile_id: str,
        explicit_user_permission_granted: bool,
        device_owner_confirmed: bool,
    ) -> MobileWorkflowPermissionProfile:
        return MobileWorkflowPermissionProfile(
            profile_id=profile_id,
            platform=IOS_WORKFLOW_PLATFORM,
            permission_source="user_settings",
            allowed_workflow_scopes=self.allowed_workflow_scopes,
            granted_capability_refs=self.allowed_capability_refs,
            platform_capability_refs=self.platform_capability_refs,
            explicit_user_permission_granted=explicit_user_permission_granted,
            device_owner_confirmed=device_owner_confirmed,
            revoked_capability_refs=self.revoked_capability_refs,
        )

    def to_read_model(self) -> dict[str, object]:
        return {
            "limits_id": self.limits_id,
            "platform": IOS_WORKFLOW_PLATFORM,
            "allowed_capability_refs": self.allowed_capability_refs,
            "platform_capability_refs": self.platform_capability_refs,
            "allowed_workflow_scopes": self.allowed_workflow_scopes,
            "revoked_capability_refs": self.revoked_capability_refs,
            "requires_explicit_user_permission": self.requires_explicit_user_permission,
            "requires_device_owner_confirmation": self.requires_device_owner_confirmation,
            "requires_sandbox_preview": self.requires_sandbox_preview,
            "requires_audit": self.requires_audit,
            "local_first": self.local_first,
            "server_optional": self.server_optional,
            "offline_queue_allowed": self.offline_queue_allowed,
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


def build_ios_workflow_capability_limits(
    *,
    limits_id: str = "ios.workflow.capability.limits.v1",
    revoked_capability_refs: Tuple[str, ...] = (),
) -> IOSWorkflowCapabilityLimits:
    return IOSWorkflowCapabilityLimits(
        limits_id=limits_id,
        allowed_capability_refs=DEFAULT_IOS_WORKFLOW_CAPABILITIES,
        platform_capability_refs=DEFAULT_IOS_WORKFLOW_CAPABILITIES,
        revoked_capability_refs=revoked_capability_refs,
    )


__all__ = [
    "ALLOWED_IOS_WORKFLOW_SCOPES",
    "DEFAULT_IOS_WORKFLOW_CAPABILITIES",
    "IOSWorkflowCapabilityLimits",
    "IOS_WORKFLOW_PLATFORM",
    "build_ios_workflow_capability_limits",
]
