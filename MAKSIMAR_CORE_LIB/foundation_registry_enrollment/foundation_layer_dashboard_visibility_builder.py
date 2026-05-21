from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_layer_readiness_summary_builder import (
    FoundationLayerReadinessEntry,
    FoundationLayerReadinessSummaryReadModel,
    build_foundation_layer_readiness_summary_read_model,
)


@dataclass(frozen=True, slots=True)
class FoundationLayerDashboardVisibilityEntry:
    layer_id: str
    dashboard_visible: bool
    dashboard_read_only: bool
    dashboard_control_allowed: bool
    execution_allowed: bool
    registry_write_allowed: bool
    runtime_mutation_allowed: bool

    def __post_init__(self) -> None:
        _validate_non_empty("layer_id", self.layer_id)
        _validate_true("dashboard_visible", self.dashboard_visible)
        _validate_true("dashboard_read_only", self.dashboard_read_only)
        _validate_false("dashboard_control_allowed", self.dashboard_control_allowed)
        _validate_false("execution_allowed", self.execution_allowed)
        _validate_false("registry_write_allowed", self.registry_write_allowed)
        _validate_false("runtime_mutation_allowed", self.runtime_mutation_allowed)

    def to_dict(self) -> dict[str, Any]:
        return {
            "layer_id": self.layer_id,
            "dashboard_visible": self.dashboard_visible,
            "dashboard_read_only": self.dashboard_read_only,
            "dashboard_control_allowed": self.dashboard_control_allowed,
            "execution_allowed": self.execution_allowed,
            "registry_write_allowed": self.registry_write_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
        }


@dataclass(frozen=True, slots=True)
class FoundationLayerDashboardVisibilityReadModel:
    read_model_id: str
    visibility_entries: tuple[FoundationLayerDashboardVisibilityEntry, ...]
    source_readiness_summary: FoundationLayerReadinessSummaryReadModel
    total_layers: int
    dashboard_visible_layers: int
    dashboard_visibility_mandatory: bool
    all_foundation_layers_dashboard_visible: bool
    dashboard_read_only: bool
    dashboard_control_allowed: bool
    execution_allowed: bool
    registry_write_allowed: bool
    runtime_mutation_allowed: bool
    preview_tools_read_only: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        _validate_non_empty("read_model_id", self.read_model_id)
        if not isinstance(self.visibility_entries, tuple):
            raise TypeError("visibility_entries must be a tuple")
        if not self.visibility_entries:
            raise ValueError("visibility_entries must not be empty")
        for entry in self.visibility_entries:
            if not isinstance(entry, FoundationLayerDashboardVisibilityEntry):
                raise TypeError("visibility_entries must contain FoundationLayerDashboardVisibilityEntry values")
        if not isinstance(self.source_readiness_summary, FoundationLayerReadinessSummaryReadModel):
            raise TypeError("source_readiness_summary must be FoundationLayerReadinessSummaryReadModel")

        _validate_count("total_layers", self.total_layers, len(self.visibility_entries))
        _validate_count(
            "dashboard_visible_layers",
            self.dashboard_visible_layers,
            sum(1 for entry in self.visibility_entries if entry.dashboard_visible),
        )
        _validate_true("dashboard_visibility_mandatory", self.dashboard_visibility_mandatory)
        _validate_true("all_foundation_layers_dashboard_visible", self.all_foundation_layers_dashboard_visible)
        _validate_true("dashboard_read_only", self.dashboard_read_only)
        _validate_false("dashboard_control_allowed", self.dashboard_control_allowed)
        _validate_false("execution_allowed", self.execution_allowed)
        _validate_false("registry_write_allowed", self.registry_write_allowed)
        _validate_false("runtime_mutation_allowed", self.runtime_mutation_allowed)
        _validate_true("preview_tools_read_only", self.preview_tools_read_only)
        _validate_non_empty_tuple("reason_codes", self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "read_model_id": self.read_model_id,
            "visibility_entries": tuple(entry.to_dict() for entry in self.visibility_entries),
            "source_readiness_summary": self.source_readiness_summary.to_dict(),
            "total_layers": self.total_layers,
            "dashboard_visible_layers": self.dashboard_visible_layers,
            "dashboard_visibility_mandatory": self.dashboard_visibility_mandatory,
            "all_foundation_layers_dashboard_visible": self.all_foundation_layers_dashboard_visible,
            "dashboard_read_only": self.dashboard_read_only,
            "dashboard_control_allowed": self.dashboard_control_allowed,
            "execution_allowed": self.execution_allowed,
            "registry_write_allowed": self.registry_write_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "preview_tools_read_only": self.preview_tools_read_only,
            "reason_codes": self.reason_codes,
        }


def build_foundation_layer_dashboard_visibility_read_model() -> FoundationLayerDashboardVisibilityReadModel:
    readiness_summary = build_foundation_layer_readiness_summary_read_model()
    visibility_entries = tuple(
        _visibility_entry_from_readiness_entry(entry)
        for entry in readiness_summary.readiness_entries
    )

    return FoundationLayerDashboardVisibilityReadModel(
        read_model_id="foundation_layer_dashboard_visibility_read_model_v1",
        visibility_entries=visibility_entries,
        source_readiness_summary=readiness_summary,
        total_layers=len(visibility_entries),
        dashboard_visible_layers=sum(1 for entry in visibility_entries if entry.dashboard_visible),
        dashboard_visibility_mandatory=True,
        all_foundation_layers_dashboard_visible=True,
        dashboard_read_only=True,
        dashboard_control_allowed=False,
        execution_allowed=False,
        registry_write_allowed=False,
        runtime_mutation_allowed=False,
        preview_tools_read_only=True,
        reason_codes=(
            "dashboard_visibility_mandatory",
            "all_foundation_layers_dashboard_visible",
            "dashboard_read_only",
            "dashboard_execution_blocked",
        ),
    )


def _visibility_entry_from_readiness_entry(
    entry: FoundationLayerReadinessEntry,
) -> FoundationLayerDashboardVisibilityEntry:
    return FoundationLayerDashboardVisibilityEntry(
        layer_id=entry.layer_id,
        dashboard_visible=entry.dashboard_visible,
        dashboard_read_only=entry.read_only,
        dashboard_control_allowed=False,
        execution_allowed=entry.execution_allowed,
        registry_write_allowed=entry.registry_write_allowed,
        runtime_mutation_allowed=entry.runtime_mutation_allowed,
    )


def _validate_non_empty(field_name: str, value: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    if not value:
        raise ValueError(f"{field_name} must not be empty")


def _validate_true(field_name: str, value: bool) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must remain true")


def _validate_false(field_name: str, value: bool) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must remain false")


def _validate_count(field_name: str, value: int, expected: int) -> None:
    if not isinstance(value, int):
        raise TypeError(f"{field_name} must be an integer")
    if value != expected:
        raise ValueError(f"{field_name} must equal {expected}")


def _validate_non_empty_tuple(field_name: str, value: tuple[str, ...]) -> None:
    if not isinstance(value, tuple):
        raise TypeError(f"{field_name} must be a tuple")
    if not value:
        raise ValueError(f"{field_name} must not be empty")
    for item in value:
        _validate_non_empty(field_name, item)
