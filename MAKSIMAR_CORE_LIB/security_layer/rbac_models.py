from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.security_layer.security_request_models import (
    SecurityActionKind,
    SecurityResourceKind,
)


@dataclass(frozen=True, slots=True)
class RbacPermission:
    permission_id: str
    action: SecurityActionKind
    resource_kind: SecurityResourceKind

    def __post_init__(self) -> None:
        if not self.permission_id:
            raise ValueError("permission_id must not be empty")
        if not isinstance(self.action, SecurityActionKind):
            raise TypeError("action must be SecurityActionKind")
        if not isinstance(self.resource_kind, SecurityResourceKind):
            raise TypeError("resource_kind must be SecurityResourceKind")


@dataclass(frozen=True, slots=True)
class RbacRole:
    role_id: str
    permissions: tuple[RbacPermission, ...]

    def __post_init__(self) -> None:
        if not self.role_id:
            raise ValueError("role_id must not be empty")
        if not isinstance(self.permissions, tuple):
            raise TypeError("permissions must be a tuple")
        for permission in self.permissions:
            if not isinstance(permission, RbacPermission):
                raise TypeError("permissions must contain RbacPermission")


@dataclass(frozen=True, slots=True)
class RbacPolicy:
    policy_id: str
    roles: tuple[RbacRole, ...]
    default_allow: bool = False

    def __post_init__(self) -> None:
        if not self.policy_id:
            raise ValueError("policy_id must not be empty")
        if not isinstance(self.roles, tuple):
            raise TypeError("roles must be a tuple")
        seen: set[str] = set()
        for role in self.roles:
            if not isinstance(role, RbacRole):
                raise TypeError("roles must contain RbacRole")
            if role.role_id in seen:
                raise ValueError("duplicate role_id in roles")
            seen.add(role.role_id)
        if self.default_allow:
            raise ValueError("default_allow must remain false")


@dataclass(frozen=True, slots=True)
class RbacEvaluationResult:
    allowed: bool
    matched_role_ids: tuple[str, ...]
    matched_permission_ids: tuple[str, ...]
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.matched_role_ids, tuple):
            raise TypeError("matched_role_ids must be a tuple")
        if not isinstance(self.matched_permission_ids, tuple):
            raise TypeError("matched_permission_ids must be a tuple")
        if not isinstance(self.reason_codes, tuple):
            raise TypeError("reason_codes must be a tuple")
        if not self.reason_codes:
            raise ValueError("reason_codes must not be empty")
        if self.allowed and not self.matched_permission_ids:
            raise ValueError("allowed RBAC result requires matched permissions")
