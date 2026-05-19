from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from MAKSIMAR_CORE_LIB.security_layer.rbac_models import (
    RbacPermission,
    RbacPolicy,
    RbacRole,
)
from MAKSIMAR_CORE_LIB.security_layer.security_read_model import (
    SecurityAdapterReadModel,
    SecurityReadModelStatus,
)
from MAKSIMAR_CORE_LIB.security_layer.security_request_models import (
    SecurityActionKind,
    SecurityResourceKind,
)


@dataclass(frozen=True, slots=True)
class ExistingPolicySource:
    path: str
    relation: str
    action: str

    def __post_init__(self) -> None:
        for field_name, value in (
            ("path", self.path),
            ("relation", self.relation),
            ("action", self.action),
        ):
            if not value:
                raise ValueError(f"{field_name} must not be empty")
        if self.path.startswith("/") or ".." in self.path.split("/"):
            raise ValueError("path must be project-relative and must not contain '..'")


@dataclass(frozen=True, slots=True)
class ExistingPolicyPermissionBinding:
    role_id: str
    permission_id: str
    action: SecurityActionKind
    resource_kind: SecurityResourceKind
    source_path: str

    def __post_init__(self) -> None:
        if not self.role_id:
            raise ValueError("role_id must not be empty")
        if not self.permission_id:
            raise ValueError("permission_id must not be empty")
        if not isinstance(self.action, SecurityActionKind):
            raise TypeError("action must be SecurityActionKind")
        if not isinstance(self.resource_kind, SecurityResourceKind):
            raise TypeError("resource_kind must be SecurityResourceKind")
        if not self.source_path:
            raise ValueError("source_path must not be empty")
        if self.source_path.startswith("/") or ".." in self.source_path.split("/"):
            raise ValueError("source_path must be project-relative and must not contain '..'")


@dataclass(frozen=True, slots=True)
class ExistingPolicyAdapterSnapshot:
    adapter_id: str
    sources: tuple[ExistingPolicySource, ...]
    permission_bindings: tuple[ExistingPolicyPermissionBinding, ...]
    read_only: bool = True
    dashboard_safe: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False
    direct_execution_allowed: bool = False

    def __post_init__(self) -> None:
        if not self.adapter_id:
            raise ValueError("adapter_id must not be empty")
        if not isinstance(self.sources, tuple):
            raise TypeError("sources must be a tuple")
        if not isinstance(self.permission_bindings, tuple):
            raise TypeError("permission_bindings must be a tuple")
        for source in self.sources:
            if not isinstance(source, ExistingPolicySource):
                raise TypeError("sources must contain ExistingPolicySource")
        for binding in self.permission_bindings:
            if not isinstance(binding, ExistingPolicyPermissionBinding):
                raise TypeError("permission_bindings must contain ExistingPolicyPermissionBinding")
        if not self.read_only:
            raise ValueError("read_only must remain true")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")
        if self.direct_execution_allowed:
            raise ValueError("direct_execution_allowed must remain false")

    def to_read_model(self) -> SecurityAdapterReadModel:
        status = SecurityReadModelStatus.HEALTHY if self.sources else SecurityReadModelStatus.DEGRADED
        reason = "existing_policy_sources_bound" if self.sources else "existing_policy_sources_empty"
        return SecurityAdapterReadModel(
            adapter_id=self.adapter_id,
            adapter_kind="existing_policy_adapter",
            source_count=len(self.sources),
            status=status,
            reason_codes=(reason,),
        )


def load_existing_policy_sources_from_binding_file(path: Path) -> tuple[ExistingPolicySource, ...]:
    if not path.exists():
        raise FileNotFoundError(f"existing policy binding file not found: {path}")

    sources: list[ExistingPolicySource] = []
    current_path = ""

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("- path:"):
            current_path = line.split(":", 1)[1].strip()
        elif line.startswith("relation:") and current_path:
            relation = line.split(":", 1)[1].strip()
            sources.append(
                ExistingPolicySource(
                    path=current_path,
                    relation=relation,
                    action="reference_only",
                )
            )
            current_path = ""

    return tuple(sources)


def build_existing_policy_adapter_snapshot(
    *,
    sources: tuple[ExistingPolicySource, ...],
    permission_bindings: tuple[ExistingPolicyPermissionBinding, ...],
    adapter_id: str = "security_existing_policy_adapter",
) -> ExistingPolicyAdapterSnapshot:
    return ExistingPolicyAdapterSnapshot(
        adapter_id=adapter_id,
        sources=sources,
        permission_bindings=permission_bindings,
    )


def build_rbac_policy_from_existing_policy_adapter(
    snapshot: ExistingPolicyAdapterSnapshot,
    *,
    policy_id: str,
) -> RbacPolicy:
    role_to_permissions: dict[str, list[RbacPermission]] = {}

    for binding in snapshot.permission_bindings:
        role_to_permissions.setdefault(binding.role_id, []).append(
            RbacPermission(
                permission_id=binding.permission_id,
                action=binding.action,
                resource_kind=binding.resource_kind,
            )
        )

    roles = tuple(
        RbacRole(role_id=role_id, permissions=tuple(permissions))
        for role_id, permissions in sorted(role_to_permissions.items())
    )

    return RbacPolicy(policy_id=policy_id, roles=roles)
