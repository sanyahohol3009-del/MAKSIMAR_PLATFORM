from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class SecurityRiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SecurityActionKind(str, Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    UPDATE = "update"
    DELETE = "delete"
    DEPLOY = "deploy"
    HARDWARE = "hardware"
    NETWORK = "network"


class SecuritySubjectKind(str, Enum):
    OWNER = "owner"
    OPERATOR = "operator"
    SERVICE = "service"
    WORKER = "worker"
    DASHBOARD = "dashboard"
    UNKNOWN = "unknown"


class SecurityResourceKind(str, Enum):
    CORE = "core"
    CONTROL_PLANE = "control_plane"
    EXECUTION_RUNTIME = "execution_runtime"
    DATA_PLANE = "data_plane"
    MEMORY = "memory"
    UPDATE_RECOVERY = "update_recovery"
    NETWORK = "network"
    PRODUCT = "product"
    DASHBOARD = "dashboard"
    EXTERNAL_BACKEND = "external_backend"


@dataclass(frozen=True, slots=True)
class SecuritySubject:
    subject_id: str
    subject_kind: SecuritySubjectKind
    roles: tuple[str, ...]
    authenticated: bool
    voice_identity_verified: bool = False
    service_identity_verified: bool = False

    def __post_init__(self) -> None:
        if not self.subject_id:
            raise ValueError("subject_id must not be empty")
        if not isinstance(self.subject_kind, SecuritySubjectKind):
            raise TypeError("subject_kind must be SecuritySubjectKind")
        if not isinstance(self.roles, tuple):
            raise TypeError("roles must be a tuple")
        for role in self.roles:
            if not role:
                raise ValueError("roles must not contain empty values")
        if self.subject_kind is SecuritySubjectKind.DASHBOARD and self.roles:
            raise ValueError("dashboard subjects must not carry execution roles")


@dataclass(frozen=True, slots=True)
class SecurityResource:
    resource_id: str
    resource_kind: SecurityResourceKind
    path_hint: str = ""

    def __post_init__(self) -> None:
        if not self.resource_id:
            raise ValueError("resource_id must not be empty")
        if not isinstance(self.resource_kind, SecurityResourceKind):
            raise TypeError("resource_kind must be SecurityResourceKind")
        if self.path_hint.startswith("/"):
            raise ValueError("path_hint must be project-relative when present")
        if ".." in self.path_hint.split("/"):
            raise ValueError("path_hint must not contain '..'")


@dataclass(frozen=True, slots=True)
class SecurityRequestContext:
    request_id: str
    trace_id: str
    source_layer_id: str
    target_layer_id: str
    reason: str
    metadata: dict[str, Any]

    def __post_init__(self) -> None:
        for field_name, value in (
            ("request_id", self.request_id),
            ("trace_id", self.trace_id),
            ("source_layer_id", self.source_layer_id),
            ("target_layer_id", self.target_layer_id),
            ("reason", self.reason),
        ):
            if not value:
                raise ValueError(f"{field_name} must not be empty")
        if not isinstance(self.metadata, dict):
            raise TypeError("metadata must be a dict")


@dataclass(frozen=True, slots=True)
class SecurityRequest:
    subject: SecuritySubject
    resource: SecurityResource
    action: SecurityActionKind
    risk_level: SecurityRiskLevel
    context: SecurityRequestContext
    requires_approval: bool
    requires_voice_identity: bool
    requires_signature: bool
    dashboard_safe: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.subject, SecuritySubject):
            raise TypeError("subject must be SecuritySubject")
        if not isinstance(self.resource, SecurityResource):
            raise TypeError("resource must be SecurityResource")
        if not isinstance(self.action, SecurityActionKind):
            raise TypeError("action must be SecurityActionKind")
        if not isinstance(self.risk_level, SecurityRiskLevel):
            raise TypeError("risk_level must be SecurityRiskLevel")
        if not isinstance(self.context, SecurityRequestContext):
            raise TypeError("context must be SecurityRequestContext")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false at request model layer")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false at request model layer")
        if self.risk_level in (SecurityRiskLevel.HIGH, SecurityRiskLevel.CRITICAL):
            if not self.requires_approval:
                raise ValueError("high/critical risk requests must require approval")
            if not self.requires_voice_identity:
                raise ValueError("high/critical risk requests must require voice identity")
        if self.action in (
            SecurityActionKind.UPDATE,
            SecurityActionKind.DELETE,
            SecurityActionKind.DEPLOY,
        ):
            if not self.requires_signature:
                raise ValueError("update/delete/deploy requests must require signature")


def build_security_request(
    *,
    request_id: str,
    trace_id: str,
    subject_id: str,
    subject_kind: SecuritySubjectKind,
    roles: tuple[str, ...],
    authenticated: bool,
    resource_id: str,
    resource_kind: SecurityResourceKind,
    action: SecurityActionKind,
    risk_level: SecurityRiskLevel,
    source_layer_id: str,
    target_layer_id: str,
    reason: str,
    metadata: dict[str, Any] | None = None,
    voice_identity_verified: bool = False,
    service_identity_verified: bool = False,
    requires_approval: bool | None = None,
    requires_voice_identity: bool | None = None,
    requires_signature: bool | None = None,
) -> SecurityRequest:
    high_risk = risk_level in (SecurityRiskLevel.HIGH, SecurityRiskLevel.CRITICAL)
    signature_action = action in (
        SecurityActionKind.UPDATE,
        SecurityActionKind.DELETE,
        SecurityActionKind.DEPLOY,
    )

    return SecurityRequest(
        subject=SecuritySubject(
            subject_id=subject_id,
            subject_kind=subject_kind,
            roles=roles,
            authenticated=authenticated,
            voice_identity_verified=voice_identity_verified,
            service_identity_verified=service_identity_verified,
        ),
        resource=SecurityResource(
            resource_id=resource_id,
            resource_kind=resource_kind,
        ),
        action=action,
        risk_level=risk_level,
        context=SecurityRequestContext(
            request_id=request_id,
            trace_id=trace_id,
            source_layer_id=source_layer_id,
            target_layer_id=target_layer_id,
            reason=reason,
            metadata=metadata or {},
        ),
        requires_approval=high_risk if requires_approval is None else requires_approval,
        requires_voice_identity=(
            high_risk if requires_voice_identity is None else requires_voice_identity
        ),
        requires_signature=(
            signature_action if requires_signature is None else requires_signature
        ),
    )
