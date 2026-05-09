from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal


ShellAdapterRole = Literal[
    "mobile_shell",
    "desktop_shell",
    "server_shell",
    "engineering_shell",
]

_SHELL_BINDING_ID_PATTERN = re.compile(r"^shell_adapter_binding_[a-z][a-z0-9_]*$")


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _ensure_non_negative_int(value: int, field_name: str) -> int:
    if not isinstance(value, int):
        raise ValueError(f"{field_name} must be an int")
    if value < 0:
        raise ValueError(f"{field_name} must be >= 0")
    return value


def _ensure_bool(value: bool, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field_name} must be bool")
    return value


def safe_id_suffix(value: str) -> str:
    suffix = re.sub(r"[^a-zA-Z0-9_]+", "_", value.strip().lower()).strip("_")
    if not suffix:
        raise ValueError("id suffix must be non-empty")
    if not suffix[0].isalpha():
        suffix = f"item_{suffix}"
    return suffix


@dataclass(frozen=True, slots=True)
class ShellAdapterBindingEntry:
    shell_adapter_binding_id: str
    shell_role: ShellAdapterRole
    shell_ref: str
    linked_skill_bindings: int
    linked_cube_bindings: int
    registry_backed: bool
    dashboard_visible: bool
    read_only: bool
    action_execution_allowed: bool
    binding_ready: bool
    description: str

    def __post_init__(self) -> None:
        shell_adapter_binding_id = _ensure_non_empty_str(
            self.shell_adapter_binding_id,
            "shell_adapter_binding_id",
        )
        shell_ref = _ensure_non_empty_str(self.shell_ref, "shell_ref")
        description = _ensure_non_empty_str(self.description, "description")

        if not _SHELL_BINDING_ID_PATTERN.fullmatch(shell_adapter_binding_id):
            raise ValueError(
                f"Invalid shell_adapter_binding_id: {shell_adapter_binding_id}"
            )

        _ensure_non_negative_int(self.linked_skill_bindings, "linked_skill_bindings")
        _ensure_non_negative_int(self.linked_cube_bindings, "linked_cube_bindings")

        for field_name in (
            "registry_backed",
            "dashboard_visible",
            "read_only",
            "action_execution_allowed",
            "binding_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.registry_backed:
            raise ValueError("registry_backed must be True")
        if not self.dashboard_visible:
            raise ValueError("dashboard_visible must be True")
        if not self.read_only:
            raise ValueError("read_only must be True")
        if self.action_execution_allowed:
            raise ValueError("action_execution_allowed must be False")
        if not self.binding_ready:
            raise ValueError("binding_ready must be True")

        object.__setattr__(self, "shell_adapter_binding_id", shell_adapter_binding_id)
        object.__setattr__(self, "shell_ref", shell_ref)
        object.__setattr__(self, "description", description)


@dataclass(frozen=True, slots=True)
class ShellAdapterBindingContract:
    total_bindings: int
    ready_bindings: int
    registry_backed_bindings: int
    dashboard_visible_bindings: int
    read_only_bindings: int
    action_execution_allowed_bindings: int
    entries: tuple[ShellAdapterBindingEntry, ...]

    def __post_init__(self) -> None:
        total_bindings = _ensure_non_negative_int(
            self.total_bindings,
            "total_bindings",
        )
        if total_bindings != len(self.entries):
            raise ValueError("total_bindings must match entries length")
        if total_bindings <= 0:
            raise ValueError("total_bindings must be >= 1")

        computed_ready = sum(1 for entry in self.entries if entry.binding_ready)
        computed_registry = sum(1 for entry in self.entries if entry.registry_backed)
        computed_dashboard = sum(1 for entry in self.entries if entry.dashboard_visible)
        computed_read_only = sum(1 for entry in self.entries if entry.read_only)
        computed_action = sum(
            1 for entry in self.entries if entry.action_execution_allowed
        )

        expected = {
            "ready_bindings": computed_ready,
            "registry_backed_bindings": computed_registry,
            "dashboard_visible_bindings": computed_dashboard,
            "read_only_bindings": computed_read_only,
            "action_execution_allowed_bindings": computed_action,
        }

        for field_name, expected_value in expected.items():
            if getattr(self, field_name) != expected_value:
                raise ValueError(f"{field_name} must match computed count")

        if self.ready_bindings != total_bindings:
            raise ValueError("all shell adapter bindings must be ready")
        if self.registry_backed_bindings != total_bindings:
            raise ValueError("all shell adapter bindings must be registry-backed")
        if self.dashboard_visible_bindings != total_bindings:
            raise ValueError("all shell adapter bindings must be dashboard-visible")
        if self.read_only_bindings != total_bindings:
            raise ValueError("all shell adapter bindings must be read-only")
        if self.action_execution_allowed_bindings != 0:
            raise ValueError("shell adapter bindings must not execute actions")

        binding_ids = tuple(entry.shell_adapter_binding_id for entry in self.entries)
        if len(set(binding_ids)) != len(binding_ids):
            raise ValueError("duplicate shell_adapter_binding_id values detected")


def build_shell_adapter_binding_contract() -> ShellAdapterBindingContract:
    from MAKSIMAR_CORE_LIB.skill_domain_binding.cube_binding_models import (
        build_cube_binding_contract,
    )
    from MAKSIMAR_CORE_LIB.skill_domain_binding.skill_binding_models import (
        build_skill_binding_contract,
    )

    skills = build_skill_binding_contract()
    cubes = build_cube_binding_contract()

    shell_roles: tuple[tuple[ShellAdapterRole, str], ...] = (
        ("mobile_shell", "logical://shell/mobile"),
        ("desktop_shell", "logical://shell/desktop"),
        ("server_shell", "logical://shell/server"),
        ("engineering_shell", "logical://shell/engineering"),
    )

    entries = tuple(
        ShellAdapterBindingEntry(
            shell_adapter_binding_id=f"shell_adapter_binding_{safe_id_suffix(role)}",
            shell_role=role,
            shell_ref=shell_ref,
            linked_skill_bindings=skills.ready_bindings,
            linked_cube_bindings=cubes.ready_cubes,
            registry_backed=True,
            dashboard_visible=True,
            read_only=True,
            action_execution_allowed=False,
            binding_ready=(
                skills.ready_bindings == skills.total_bindings
                and cubes.ready_cubes == cubes.total_cubes
            ),
            description=f"Read-only shell adapter binding for {role}.",
        )
        for role, shell_ref in shell_roles
    )

    return ShellAdapterBindingContract(
        total_bindings=len(entries),
        ready_bindings=sum(1 for entry in entries if entry.binding_ready),
        registry_backed_bindings=sum(1 for entry in entries if entry.registry_backed),
        dashboard_visible_bindings=sum(
            1 for entry in entries if entry.dashboard_visible
        ),
        read_only_bindings=sum(1 for entry in entries if entry.read_only),
        action_execution_allowed_bindings=sum(
            1 for entry in entries if entry.action_execution_allowed
        ),
        entries=entries,
    )
