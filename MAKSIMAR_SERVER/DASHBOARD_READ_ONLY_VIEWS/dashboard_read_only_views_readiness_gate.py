from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.dashboard_read_only_views_contract import (
    build_dashboard_read_only_views_contract,
)
from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.memory_registry_views import (
    build_memory_registry_view_contract,
    build_memory_registry_view_preview,
)


_EXPECTED_PHASE_1_8_FLOW = (
    "dashboard_root_contract",
    "memory_registry_views",
    "root_binding",
    "read_only_gate",
    "no_action_gate",
    "no_display_orchestration_gate",
    "phase_readiness",
)


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


@dataclass(frozen=True, slots=True)
class DashboardReadOnlyViewsPhaseReadiness:
    root_total_entries: int
    legacy_root_entries: int
    memory_registry_root_entries: int
    memory_registry_view_entries: int
    active_entries: int
    multilingual_ready_entries: int
    explanation_available_entries: int
    read_only_entries: int
    memory_registry_preview_ready_views: int
    memory_registry_dashboard_visible_views: int
    flow: tuple[str, ...]
    root_contract_ready: bool
    memory_registry_views_bound: bool
    read_only_enforced: bool
    no_action_exposure: bool
    no_display_orchestration: bool
    no_mutation_surface: bool
    phase_ready: bool

    def __post_init__(self) -> None:
        root_total_entries = _ensure_non_negative_int(
            self.root_total_entries,
            "root_total_entries",
        )
        legacy_root_entries = _ensure_non_negative_int(
            self.legacy_root_entries,
            "legacy_root_entries",
        )
        memory_registry_root_entries = _ensure_non_negative_int(
            self.memory_registry_root_entries,
            "memory_registry_root_entries",
        )
        memory_registry_view_entries = _ensure_non_negative_int(
            self.memory_registry_view_entries,
            "memory_registry_view_entries",
        )
        active_entries = _ensure_non_negative_int(self.active_entries, "active_entries")
        multilingual_ready_entries = _ensure_non_negative_int(
            self.multilingual_ready_entries,
            "multilingual_ready_entries",
        )
        explanation_available_entries = _ensure_non_negative_int(
            self.explanation_available_entries,
            "explanation_available_entries",
        )
        read_only_entries = _ensure_non_negative_int(
            self.read_only_entries,
            "read_only_entries",
        )
        memory_registry_preview_ready_views = _ensure_non_negative_int(
            self.memory_registry_preview_ready_views,
            "memory_registry_preview_ready_views",
        )
        memory_registry_dashboard_visible_views = _ensure_non_negative_int(
            self.memory_registry_dashboard_visible_views,
            "memory_registry_dashboard_visible_views",
        )

        if tuple(self.flow) != _EXPECTED_PHASE_1_8_FLOW:
            raise ValueError("flow must match expected PHASE 1.8 flow")

        for field_name in (
            "root_contract_ready",
            "memory_registry_views_bound",
            "read_only_enforced",
            "no_action_exposure",
            "no_display_orchestration",
            "no_mutation_surface",
            "phase_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if root_total_entries <= 0:
            raise ValueError("root_total_entries must be >= 1")
        if legacy_root_entries <= 0:
            raise ValueError("legacy_root_entries must be >= 1")
        if memory_registry_root_entries <= 0:
            raise ValueError("memory_registry_root_entries must be >= 1")
        if memory_registry_view_entries <= 0:
            raise ValueError("memory_registry_view_entries must be >= 1")
        if memory_registry_root_entries != memory_registry_view_entries:
            raise ValueError("memory_registry_root_entries must match memory_registry_view_entries")
        if root_total_entries != legacy_root_entries + memory_registry_root_entries:
            raise ValueError("root_total_entries must equal legacy + memory registry root entries")
        if active_entries != root_total_entries:
            raise ValueError("all root dashboard views must be active")
        if multilingual_ready_entries != root_total_entries:
            raise ValueError("all root dashboard views must be multilingual-ready")
        if explanation_available_entries != root_total_entries:
            raise ValueError("all root dashboard views must expose explanation")
        if read_only_entries != root_total_entries:
            raise ValueError("all root dashboard views must be read-only")
        if memory_registry_preview_ready_views != memory_registry_view_entries:
            raise ValueError("all memory registry views must be preview-ready")
        if memory_registry_dashboard_visible_views != memory_registry_view_entries:
            raise ValueError("all memory registry views must be dashboard-visible")

        if not self.root_contract_ready:
            raise ValueError("root_contract_ready must be True")
        if not self.memory_registry_views_bound:
            raise ValueError("memory_registry_views_bound must be True")
        if not self.read_only_enforced:
            raise ValueError("read_only_enforced must be True")
        if not self.no_action_exposure:
            raise ValueError("no_action_exposure must be True")
        if not self.no_display_orchestration:
            raise ValueError("no_display_orchestration must be True")
        if not self.no_mutation_surface:
            raise ValueError("no_mutation_surface must be True")
        if not self.phase_ready:
            raise ValueError("phase_ready must be True")

        object.__setattr__(self, "root_total_entries", root_total_entries)
        object.__setattr__(self, "legacy_root_entries", legacy_root_entries)
        object.__setattr__(self, "memory_registry_root_entries", memory_registry_root_entries)
        object.__setattr__(self, "memory_registry_view_entries", memory_registry_view_entries)
        object.__setattr__(self, "active_entries", active_entries)
        object.__setattr__(self, "multilingual_ready_entries", multilingual_ready_entries)
        object.__setattr__(self, "explanation_available_entries", explanation_available_entries)
        object.__setattr__(self, "read_only_entries", read_only_entries)
        object.__setattr__(
            self,
            "memory_registry_preview_ready_views",
            memory_registry_preview_ready_views,
        )
        object.__setattr__(
            self,
            "memory_registry_dashboard_visible_views",
            memory_registry_dashboard_visible_views,
        )


def build_dashboard_read_only_views_phase_readiness() -> DashboardReadOnlyViewsPhaseReadiness:
    root_contract = build_dashboard_read_only_views_contract()
    memory_registry_contract = build_memory_registry_view_contract()
    memory_registry_preview = build_memory_registry_view_preview()

    legacy_root_entries = sum(
        1
        for entry in root_contract.entries
        if entry.view_kind != "memory_registry_read_only_view"
    )
    memory_registry_root_entries = sum(
        1
        for entry in root_contract.entries
        if entry.view_kind == "memory_registry_read_only_view"
    )
    read_only_entries = sum(
        1
        for entry in root_contract.entries
        if entry.read_only_mode == "read_only"
    )

    root_memory_registry_view_ids = {
        entry.view_id
        for entry in root_contract.entries
        if entry.view_kind == "memory_registry_read_only_view"
    }
    memory_registry_view_ids = {
        entry.view_id
        for entry in memory_registry_contract.entries
    }

    memory_registry_views_bound = (
        root_memory_registry_view_ids == memory_registry_view_ids
        and memory_registry_root_entries == memory_registry_contract.total_views
    )

    read_only_enforced = read_only_entries == root_contract.total_entries
    no_action_exposure = (
        bool(memory_registry_preview["action_exposure_allowed"]) is False
        and int(memory_registry_preview["action_exposure_allowed_panels"]) == 0
    )
    no_display_orchestration = (
        bool(memory_registry_preview["display_orchestration_allowed"]) is False
        and int(memory_registry_preview["display_orchestration_allowed_panels"]) == 0
    )
    no_mutation_surface = read_only_enforced and no_action_exposure and no_display_orchestration

    root_contract_ready = (
        root_contract.total_entries >= 1
        and root_contract.active_entries == root_contract.total_entries
        and root_contract.multilingual_ready_entries == root_contract.total_entries
        and root_contract.explanation_available_entries == root_contract.total_entries
    )

    phase_ready = (
        root_contract_ready
        and memory_registry_views_bound
        and read_only_enforced
        and no_action_exposure
        and no_display_orchestration
        and no_mutation_surface
        and bool(memory_registry_preview["preview_ready"])
    )

    return DashboardReadOnlyViewsPhaseReadiness(
        root_total_entries=root_contract.total_entries,
        legacy_root_entries=legacy_root_entries,
        memory_registry_root_entries=memory_registry_root_entries,
        memory_registry_view_entries=memory_registry_contract.total_views,
        active_entries=root_contract.active_entries,
        multilingual_ready_entries=root_contract.multilingual_ready_entries,
        explanation_available_entries=root_contract.explanation_available_entries,
        read_only_entries=read_only_entries,
        memory_registry_preview_ready_views=int(memory_registry_preview["preview_ready_views"]),
        memory_registry_dashboard_visible_views=int(memory_registry_preview["dashboard_visible_views"]),
        flow=_EXPECTED_PHASE_1_8_FLOW,
        root_contract_ready=root_contract_ready,
        memory_registry_views_bound=memory_registry_views_bound,
        read_only_enforced=read_only_enforced,
        no_action_exposure=no_action_exposure,
        no_display_orchestration=no_display_orchestration,
        no_mutation_surface=no_mutation_surface,
        phase_ready=phase_ready,
    )


def build_dashboard_read_only_views_phase_preview() -> Dict[str, object]:
    readiness = build_dashboard_read_only_views_phase_readiness()

    return {
        "flow": readiness.flow,
        "root_total_entries": readiness.root_total_entries,
        "legacy_root_entries": readiness.legacy_root_entries,
        "memory_registry_root_entries": readiness.memory_registry_root_entries,
        "memory_registry_view_entries": readiness.memory_registry_view_entries,
        "active_entries": readiness.active_entries,
        "multilingual_ready_entries": readiness.multilingual_ready_entries,
        "explanation_available_entries": readiness.explanation_available_entries,
        "read_only_entries": readiness.read_only_entries,
        "root_contract_ready": readiness.root_contract_ready,
        "memory_registry_views_bound": readiness.memory_registry_views_bound,
        "read_only_enforced": readiness.read_only_enforced,
        "no_action_exposure": readiness.no_action_exposure,
        "no_display_orchestration": readiness.no_display_orchestration,
        "no_mutation_surface": readiness.no_mutation_surface,
        "phase_ready": readiness.phase_ready,
        "preview_ready": True,
    }
