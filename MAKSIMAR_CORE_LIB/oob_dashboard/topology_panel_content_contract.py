from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_truth_consistency_view import (
    build_foundation_truth_consistency_view,
)

TopologyPanelState = Literal[
    "normal",
    "empty",
    "degraded",
    "incident",
    "stale",
    "loading",
]

ALL_TOPOLOGY_PANEL_STATES: tuple[TopologyPanelState, ...] = (
    "normal",
    "empty",
    "degraded",
    "incident",
    "stale",
    "loading",
)

EXPECTED_TOPOLOGY_SCOPES: tuple[str, ...] = (
    "runtime",
    "guard",
    "core_guard",
    "kernel_guard",
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class TopologyPanelContentEntry:
    """Canonical content entry for the topology panel."""

    panel_id: str
    panel_state: TopologyPanelState
    total_topology_entries: int
    runtime_nodes: int
    guard_nodes: int
    core_guard_nodes: int
    kernel_guard_nodes: int
    topology_relationships: int
    alive_nodes: int
    degraded_nodes: int
    broken_nodes: int
    dead_nodes: int
    truth_consistent_nodes: int
    truth_partial_nodes: int
    truth_mismatch_nodes: int
    historical_only_nodes: int
    current_live_visible_nodes: int
    startup_order_valid: bool
    visible_in_main_dashboard: bool
    visible_in_oob_dashboard: bool
    read_only: bool
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.panel_id, "panel_id")
        _require_non_empty(self.description, "description")

        if self.panel_state not in ALL_TOPOLOGY_PANEL_STATES:
            raise ValueError(
                "panel_state must be one of "
                f"{ALL_TOPOLOGY_PANEL_STATES}, got {self.panel_state!r}."
            )

        integer_fields = {
            "total_topology_entries": self.total_topology_entries,
            "runtime_nodes": self.runtime_nodes,
            "guard_nodes": self.guard_nodes,
            "core_guard_nodes": self.core_guard_nodes,
            "kernel_guard_nodes": self.kernel_guard_nodes,
            "topology_relationships": self.topology_relationships,
            "alive_nodes": self.alive_nodes,
            "degraded_nodes": self.degraded_nodes,
            "broken_nodes": self.broken_nodes,
            "dead_nodes": self.dead_nodes,
            "truth_consistent_nodes": self.truth_consistent_nodes,
            "truth_partial_nodes": self.truth_partial_nodes,
            "truth_mismatch_nodes": self.truth_mismatch_nodes,
            "historical_only_nodes": self.historical_only_nodes,
            "current_live_visible_nodes": self.current_live_visible_nodes,
        }
        for field_name, field_value in integer_fields.items():
            if field_value < 0:
                raise ValueError(f"{field_name} must be >= 0.")

        if self.total_topology_entries > 0:
            required_nodes = (
                self.runtime_nodes,
                self.guard_nodes,
                self.core_guard_nodes,
                self.kernel_guard_nodes,
            )
            if not all(count == 1 for count in required_nodes):
                raise ValueError(
                    "canonical topology content requires exactly one node for "
                    "runtime, guard, core_guard, and kernel_guard."
                )

        if not self.visible_in_main_dashboard:
            raise ValueError(
                "visible_in_main_dashboard must remain true for canonical topology content."
            )

        if not self.visible_in_oob_dashboard:
            raise ValueError(
                "visible_in_oob_dashboard must remain true for canonical topology content."
            )

        if not self.read_only:
            raise ValueError(
                "read_only must remain true for canonical topology content."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical topology content."
            )


@dataclass(frozen=True, slots=True)
class TopologyPanelContentContract:
    """Canonical content contract for the topology panel."""

    contract_id: str
    total_entries: int
    read_only_entries: int
    main_dashboard_visible_entries: int
    oob_visible_entries: int
    operator_visible_entries: int
    entries: tuple[TopologyPanelContentEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")

        if self.read_only_entries != sum(1 for entry in self.entries if entry.read_only):
            raise ValueError("read_only_entries must match read_only count.")

        if self.main_dashboard_visible_entries != sum(
            1 for entry in self.entries if entry.visible_in_main_dashboard
        ):
            raise ValueError(
                "main_dashboard_visible_entries must match visible_in_main_dashboard count."
            )

        if self.oob_visible_entries != sum(
            1 for entry in self.entries if entry.visible_in_oob_dashboard
        ):
            raise ValueError(
                "oob_visible_entries must match visible_in_oob_dashboard count."
            )

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )


def _derive_topology_panel_state(
    total_entries: int, broken_nodes: int, dead_nodes: int, degraded_nodes: int,
    truth_mismatch_nodes: int, historical_only_nodes: int, warming_up_nodes: int,
    *, unknown_nodes: int = 0, partial_nodes: int = 0,
    alive_nodes: int = 0, consistent_nodes: int = 0,
) -> TopologyPanelState:
    if broken_nodes > 0 or dead_nodes > 0:
        return "incident"
    if total_entries == 0:
        return "empty"
    if truth_mismatch_nodes > 0:
        return "stale"
    if (total_entries != 4 or unknown_nodes > 0 or partial_nodes > 0
            or degraded_nodes > 0 or historical_only_nodes > 0):
        return "degraded"
    if warming_up_nodes > 0:
        return "loading"
    return "normal" if alive_nodes == total_entries == consistent_nodes else "degraded"


def build_topology_panel_content_contract(observation: dict | None = None) -> TopologyPanelContentContract:
    """Build canonical content contract for the topology panel."""
    truth_consistency_view = build_foundation_truth_consistency_view(observation=observation)
    statuses = [item.derived_status for item in truth_consistency_view.entries]
    historical = (4 if isinstance(observation, dict) and observation.get("historical_only") is True else 0)
    current_visible = sum(value != "UNKNOWN" for value in statuses) if not historical else 0

    scopes = tuple(item.truth_scope for item in truth_consistency_view.entries)
    runtime_nodes = sum(1 for scope in scopes if scope == "runtime")
    guard_nodes = sum(1 for scope in scopes if scope == "guard")
    core_guard_nodes = sum(1 for scope in scopes if scope == "core_guard")
    kernel_guard_nodes = sum(1 for scope in scopes if scope == "kernel_guard")

    total_topology_entries = len(scopes)
    topology_relationships = max(total_topology_entries - 1, 0)

    entry = TopologyPanelContentEntry(
        panel_id="topology",
        panel_state=_derive_topology_panel_state(
            total_entries=total_topology_entries,
            broken_nodes=statuses.count("BROKEN"),
            dead_nodes=statuses.count("DEAD"),
            degraded_nodes=statuses.count("DEGRADED"),
            truth_mismatch_nodes=truth_consistency_view.mismatch_entries,
            historical_only_nodes=historical,
            warming_up_nodes=statuses.count("WARMING_UP"),
            unknown_nodes=statuses.count("UNKNOWN"),
            partial_nodes=truth_consistency_view.partial_entries,
            alive_nodes=statuses.count("ALIVE"),
            consistent_nodes=truth_consistency_view.consistent_entries,
        ),
        total_topology_entries=total_topology_entries,
        runtime_nodes=runtime_nodes,
        guard_nodes=guard_nodes,
        core_guard_nodes=core_guard_nodes,
        kernel_guard_nodes=kernel_guard_nodes,
        topology_relationships=topology_relationships,
        alive_nodes=statuses.count("ALIVE"),
        degraded_nodes=statuses.count("DEGRADED"),
        broken_nodes=statuses.count("BROKEN"),
        dead_nodes=statuses.count("DEAD"),
        truth_consistent_nodes=truth_consistency_view.consistent_entries,
        truth_partial_nodes=truth_consistency_view.partial_entries,
        truth_mismatch_nodes=truth_consistency_view.mismatch_entries,
        historical_only_nodes=historical,
        current_live_visible_nodes=current_visible,
        startup_order_valid=scopes == EXPECTED_TOPOLOGY_SCOPES,
        visible_in_main_dashboard=True,
        visible_in_oob_dashboard=True,
        read_only=True,
        operator_visible=True,
        description=(
            "Canonical topology panel content contract derived from "
            "one canonical observation and "
            "and foundation truth consistency view."
        ),
    )

    entries = (entry,)

    return TopologyPanelContentContract(
        contract_id="topology_panel_content_contract_001",
        total_entries=len(entries),
        read_only_entries=sum(1 for item in entries if item.read_only),
        main_dashboard_visible_entries=sum(
            1 for item in entries if item.visible_in_main_dashboard
        ),
        oob_visible_entries=sum(
            1 for item in entries if item.visible_in_oob_dashboard
        ),
        operator_visible_entries=sum(
            1 for item in entries if item.operator_visible
        ),
        entries=entries,
    )
