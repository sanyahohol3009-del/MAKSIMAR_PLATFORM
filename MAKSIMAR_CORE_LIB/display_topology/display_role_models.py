from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.display_topology.display_topology_contract import (
    build_display_topology_contract,
)

DisplayRoleFamily = Literal[
    "dashboard_role",
    "engineering_role",
    "mobile_proxy_role",
    "other_display_role",
]

_ROLE_BINDING_ID_PATTERN = re.compile(r"^display_role_binding_[a-z][a-z0-9_]*$")


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _ensure_bool(value: bool, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field_name} must be bool")
    return value


def _role_family(display_role: str) -> DisplayRoleFamily:
    if display_role == "primary_dashboard_display":
        return "dashboard_role"
    if display_role == "engineering_display":
        return "engineering_role"
    if display_role == "mobile_display_proxy":
        return "mobile_proxy_role"
    return "other_display_role"


@dataclass(frozen=True, slots=True)
class DisplayRoleBindingEntry:
    display_role_binding_id: str
    display_id: str
    display_role: str
    role_family: DisplayRoleFamily
    visibility_mode: str
    private_role: bool
    shared_role: bool
    operator_visible: bool
    read_only: bool
    role_ready: bool
    description: str

    def __post_init__(self) -> None:
        binding_id = _ensure_non_empty_str(
            self.display_role_binding_id,
            "display_role_binding_id",
        )
        if not _ROLE_BINDING_ID_PATTERN.fullmatch(binding_id):
            raise ValueError(f"Invalid display_role_binding_id: {binding_id}")

        _ensure_non_empty_str(self.display_id, "display_id")
        _ensure_non_empty_str(self.display_role, "display_role")
        _ensure_non_empty_str(self.visibility_mode, "visibility_mode")
        _ensure_non_empty_str(self.description, "description")

        for field_name in (
            "private_role",
            "shared_role",
            "operator_visible",
            "read_only",
            "role_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if self.private_role == self.shared_role:
            raise ValueError("exactly one of private_role/shared_role must be True")
        if not self.operator_visible:
            raise ValueError("operator_visible must be True")
        if not self.read_only:
            raise ValueError("read_only must be True")
        if not self.role_ready:
            raise ValueError("role_ready must be True")


@dataclass(frozen=True, slots=True)
class DisplayRoleBindingContract:
    total_roles: int
    ready_roles: int
    private_roles: int
    shared_roles: int
    operator_visible_roles: int
    read_only_roles: int
    entries: tuple[DisplayRoleBindingEntry, ...]

    def __post_init__(self) -> None:
        if self.total_roles != len(self.entries):
            raise ValueError("total_roles must match entries length")
        if self.total_roles <= 0:
            raise ValueError("total_roles must be >= 1")

        expected = {
            "ready_roles": sum(1 for entry in self.entries if entry.role_ready),
            "private_roles": sum(1 for entry in self.entries if entry.private_role),
            "shared_roles": sum(1 for entry in self.entries if entry.shared_role),
            "operator_visible_roles": sum(1 for entry in self.entries if entry.operator_visible),
            "read_only_roles": sum(1 for entry in self.entries if entry.read_only),
        }

        for field_name, expected_value in expected.items():
            if getattr(self, field_name) != expected_value:
                raise ValueError(f"{field_name} must match computed count")

        if self.ready_roles != self.total_roles:
            raise ValueError("all display roles must be ready")
        if self.operator_visible_roles != self.total_roles:
            raise ValueError("all display roles must be operator-visible")
        if self.read_only_roles != self.total_roles:
            raise ValueError("all display roles must be read-only")

        roles = tuple(entry.display_role for entry in self.entries)
        if len(set(roles)) != len(roles):
            raise ValueError("duplicate display_role values detected")


def build_display_role_binding_contract() -> DisplayRoleBindingContract:
    topology = build_display_topology_contract()

    entries = tuple(
        DisplayRoleBindingEntry(
            display_role_binding_id=f"display_role_binding_{entry.display_role}",
            display_id=entry.display_id,
            display_role=entry.display_role,
            role_family=_role_family(entry.display_role),
            visibility_mode=entry.visibility_mode,
            private_role=entry.visibility_mode == "private",
            shared_role=entry.visibility_mode == "shared",
            operator_visible=True,
            read_only=True,
            role_ready=True,
            description=f"Read-only display role binding for {entry.display_role}.",
        )
        for entry in topology.entries
    )

    return DisplayRoleBindingContract(
        total_roles=len(entries),
        ready_roles=sum(1 for entry in entries if entry.role_ready),
        private_roles=sum(1 for entry in entries if entry.private_role),
        shared_roles=sum(1 for entry in entries if entry.shared_role),
        operator_visible_roles=sum(1 for entry in entries if entry.operator_visible),
        read_only_roles=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )
