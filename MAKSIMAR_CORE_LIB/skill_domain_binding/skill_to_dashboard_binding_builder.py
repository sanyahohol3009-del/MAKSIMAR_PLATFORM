from __future__ import annotations

import re
from dataclasses import dataclass


_BINDING_ID_PATTERN = re.compile(r"^skill_to_dashboard_binding_[a-z][a-z0-9_]*$")


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
class SkillToDashboardBindingEntry:
    binding_id: str
    skill_id: str
    module_slug: str
    panel_ids: tuple[str, ...]
    matched_dashboard_views: int
    dashboard_reference_bound: bool
    dashboard_root_ready: bool
    read_only: bool
    action_execution_allowed: bool
    binding_ready: bool

    def __post_init__(self) -> None:
        binding_id = _ensure_non_empty_str(self.binding_id, "binding_id")
        skill_id = _ensure_non_empty_str(self.skill_id, "skill_id")
        module_slug = _ensure_non_empty_str(self.module_slug, "module_slug")

        if not _BINDING_ID_PATTERN.fullmatch(binding_id):
            raise ValueError(f"Invalid binding_id: {binding_id}")

        if not isinstance(self.panel_ids, tuple) or not self.panel_ids:
            raise ValueError("panel_ids must be a non-empty tuple")
        if len(set(self.panel_ids)) != len(self.panel_ids):
            raise ValueError("panel_ids must be unique")

        _ensure_non_negative_int(self.matched_dashboard_views, "matched_dashboard_views")

        for field_name in (
            "dashboard_reference_bound",
            "dashboard_root_ready",
            "read_only",
            "action_execution_allowed",
            "binding_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.dashboard_reference_bound:
            raise ValueError("dashboard_reference_bound must be True")
        if not self.dashboard_root_ready:
            raise ValueError("dashboard_root_ready must be True")
        if not self.read_only:
            raise ValueError("read_only must be True")
        if self.action_execution_allowed:
            raise ValueError("action_execution_allowed must be False")
        if not self.binding_ready:
            raise ValueError("binding_ready must be True")

        object.__setattr__(self, "binding_id", binding_id)
        object.__setattr__(self, "skill_id", skill_id)
        object.__setattr__(self, "module_slug", module_slug)


@dataclass(frozen=True, slots=True)
class SkillToDashboardBindingContract:
    total_bindings: int
    ready_bindings: int
    dashboard_reference_bound_bindings: int
    dashboard_root_ready_bindings: int
    read_only_bindings: int
    action_execution_allowed_bindings: int
    entries: tuple[SkillToDashboardBindingEntry, ...]

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
        computed_dashboard = sum(
            1 for entry in self.entries if entry.dashboard_reference_bound
        )
        computed_root = sum(1 for entry in self.entries if entry.dashboard_root_ready)
        computed_read_only = sum(1 for entry in self.entries if entry.read_only)
        computed_action = sum(
            1 for entry in self.entries if entry.action_execution_allowed
        )

        expected = {
            "ready_bindings": computed_ready,
            "dashboard_reference_bound_bindings": computed_dashboard,
            "dashboard_root_ready_bindings": computed_root,
            "read_only_bindings": computed_read_only,
            "action_execution_allowed_bindings": computed_action,
        }

        for field_name, expected_value in expected.items():
            if getattr(self, field_name) != expected_value:
                raise ValueError(f"{field_name} must match computed count")

        if self.ready_bindings != total_bindings:
            raise ValueError("all skill-to-dashboard bindings must be ready")
        if self.dashboard_reference_bound_bindings != total_bindings:
            raise ValueError("all skills must be dashboard-bound")
        if self.dashboard_root_ready_bindings != total_bindings:
            raise ValueError("dashboard root must be ready for all bindings")
        if self.read_only_bindings != total_bindings:
            raise ValueError("all dashboard bindings must be read-only")
        if self.action_execution_allowed_bindings != 0:
            raise ValueError("dashboard bindings must not execute actions")


def build_skill_to_dashboard_binding_contract() -> SkillToDashboardBindingContract:
    from MAKSIMAR_CORE_LIB.skill_domain_binding.skill_binding_models import (
        build_skill_binding_contract,
    )
    from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS import (
        build_dashboard_read_only_views_contract,
        build_dashboard_read_only_views_phase_readiness,
    )

    skills = build_skill_binding_contract()
    dashboard = build_dashboard_read_only_views_contract()
    dashboard_ready = build_dashboard_read_only_views_phase_readiness()

    dashboard_skill_ids = {
        entry.linked_skill_id
        for entry in dashboard.entries
        if entry.linked_skill_id
    }
    dashboard_panel_ids = {entry.panel_id for entry in dashboard.entries}

    entries = tuple(
        SkillToDashboardBindingEntry(
            binding_id=f"skill_to_dashboard_binding_{safe_id_suffix(skill.skill_id)}",
            skill_id=skill.skill_id,
            module_slug=skill.module_slug,
            panel_ids=skill.panel_ids,
            matched_dashboard_views=sum(
                1
                for panel_id in skill.panel_ids
                if panel_id in dashboard_panel_ids
            ),
            dashboard_reference_bound=(
                skill.dashboard_reference_bound
                and (
                    skill.skill_id in dashboard_skill_ids
                    or any(panel_id in dashboard_panel_ids for panel_id in skill.panel_ids)
                )
            ),
            dashboard_root_ready=dashboard_ready.phase_ready,
            read_only=True,
            action_execution_allowed=False,
            binding_ready=(
                skill.dashboard_reference_bound
                and dashboard_ready.phase_ready
                and (
                    skill.skill_id in dashboard_skill_ids
                    or any(panel_id in dashboard_panel_ids for panel_id in skill.panel_ids)
                )
            ),
        )
        for skill in skills.entries
    )

    return SkillToDashboardBindingContract(
        total_bindings=len(entries),
        ready_bindings=sum(1 for entry in entries if entry.binding_ready),
        dashboard_reference_bound_bindings=sum(
            1 for entry in entries if entry.dashboard_reference_bound
        ),
        dashboard_root_ready_bindings=sum(
            1 for entry in entries if entry.dashboard_root_ready
        ),
        read_only_bindings=sum(1 for entry in entries if entry.read_only),
        action_execution_allowed_bindings=sum(
            1 for entry in entries if entry.action_execution_allowed
        ),
        entries=entries,
    )
