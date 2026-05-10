from __future__ import annotations

import re
from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.display_topology.display_topology_contract import (
    build_display_topology_contract,
)

_CAPABILITY_BINDING_ID_PATTERN = re.compile(r"^display_capability_binding_[a-z][a-z0-9_]*$")


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


@dataclass(frozen=True, slots=True)
class DisplayCapabilityBindingEntry:
    capability_binding_id: str
    display_id: str
    display_role: str
    capability: str
    render_capability: bool
    private_capability: bool
    overlay_capability: bool
    read_only: bool
    direct_execution_allowed: bool
    capability_ready: bool
    description: str

    def __post_init__(self) -> None:
        capability_binding_id = _ensure_non_empty_str(
            self.capability_binding_id,
            "capability_binding_id",
        )
        if not _CAPABILITY_BINDING_ID_PATTERN.fullmatch(capability_binding_id):
            raise ValueError(f"Invalid capability_binding_id: {capability_binding_id}")

        _ensure_non_empty_str(self.display_id, "display_id")
        _ensure_non_empty_str(self.display_role, "display_role")
        _ensure_non_empty_str(self.capability, "capability")
        _ensure_non_empty_str(self.description, "description")

        for field_name in (
            "render_capability",
            "private_capability",
            "overlay_capability",
            "read_only",
            "direct_execution_allowed",
            "capability_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.read_only:
            raise ValueError("read_only must be True")
        if self.direct_execution_allowed:
            raise ValueError("direct_execution_allowed must be False")
        if not self.capability_ready:
            raise ValueError("capability_ready must be True")


@dataclass(frozen=True, slots=True)
class DisplayCapabilityBindingContract:
    total_capabilities: int
    ready_capabilities: int
    render_capabilities: int
    private_capabilities: int
    overlay_capabilities: int
    read_only_capabilities: int
    direct_execution_allowed_capabilities: int
    entries: tuple[DisplayCapabilityBindingEntry, ...]

    def __post_init__(self) -> None:
        if self.total_capabilities != len(self.entries):
            raise ValueError("total_capabilities must match entries length")
        if self.total_capabilities <= 0:
            raise ValueError("total_capabilities must be >= 1")

        expected = {
            "ready_capabilities": sum(1 for entry in self.entries if entry.capability_ready),
            "render_capabilities": sum(1 for entry in self.entries if entry.render_capability),
            "private_capabilities": sum(1 for entry in self.entries if entry.private_capability),
            "overlay_capabilities": sum(1 for entry in self.entries if entry.overlay_capability),
            "read_only_capabilities": sum(1 for entry in self.entries if entry.read_only),
            "direct_execution_allowed_capabilities": sum(
                1 for entry in self.entries if entry.direct_execution_allowed
            ),
        }

        for field_name, expected_value in expected.items():
            if getattr(self, field_name) != expected_value:
                raise ValueError(f"{field_name} must match computed count")

        if self.ready_capabilities != self.total_capabilities:
            raise ValueError("all display capabilities must be ready")
        if self.read_only_capabilities != self.total_capabilities:
            raise ValueError("all display capabilities must be read-only")
        if self.direct_execution_allowed_capabilities != 0:
            raise ValueError("display capabilities must not execute directly")

        binding_ids = tuple(entry.capability_binding_id for entry in self.entries)
        if len(set(binding_ids)) != len(binding_ids):
            raise ValueError("duplicate capability_binding_id values detected")


def build_display_capability_binding_contract() -> DisplayCapabilityBindingContract:
    topology = build_display_topology_contract()

    entries: list[DisplayCapabilityBindingEntry] = []
    for display in topology.entries:
        for capability in display.capabilities:
            entries.append(
                DisplayCapabilityBindingEntry(
                    capability_binding_id=(
                        f"display_capability_binding_{display.display_id.removeprefix('display_')}_{capability}"
                    ),
                    display_id=display.display_id,
                    display_role=display.display_role,
                    capability=capability,
                    render_capability=capability in {"render_panels", "render_explanations", "multi_window"},
                    private_capability=capability in {"mobile_proxy", "private_display"},
                    overlay_capability=capability in {"spatial_overlay", "wall_projection", "gesture_input"},
                    read_only=True,
                    direct_execution_allowed=False,
                    capability_ready=True,
                    description=f"Read-only capability binding for {display.display_id}:{capability}.",
                )
            )

    contract_entries = tuple(entries)

    return DisplayCapabilityBindingContract(
        total_capabilities=len(contract_entries),
        ready_capabilities=sum(1 for entry in contract_entries if entry.capability_ready),
        render_capabilities=sum(1 for entry in contract_entries if entry.render_capability),
        private_capabilities=sum(1 for entry in contract_entries if entry.private_capability),
        overlay_capabilities=sum(1 for entry in contract_entries if entry.overlay_capability),
        read_only_capabilities=sum(1 for entry in contract_entries if entry.read_only),
        direct_execution_allowed_capabilities=sum(
            1 for entry in contract_entries if entry.direct_execution_allowed
        ),
        entries=contract_entries,
    )
