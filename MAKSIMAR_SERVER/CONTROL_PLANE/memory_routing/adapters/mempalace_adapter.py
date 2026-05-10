from __future__ import annotations

import re
from dataclasses import dataclass

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters.mempalace_adapter_models import (
    build_mempalace_adapter_contract,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters.mempalace_guard_validators import (
    build_mempalace_guard_validation_report,
)

_SURFACE_ID_PATTERN = re.compile(r"^mempalace_adapter_surface_[a-z][a-z0-9_]*_[0-9]{3}$")


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
class MemPalaceAdapterSurface:
    adapter_surface_id: str
    adapter_id: str
    query_only_surface_ready: bool
    external_backend_connected: bool
    vendor_acquisition_required: bool
    download_performed: bool
    real_backend_enabled: bool
    canonical_write_allowed: bool
    runtime_mutation_allowed: bool
    adapter_surface_ready: bool
    description: str

    def __post_init__(self) -> None:
        surface_id = _ensure_non_empty_str(self.adapter_surface_id, "adapter_surface_id")
        if not _SURFACE_ID_PATTERN.fullmatch(surface_id):
            raise ValueError(f"Invalid adapter_surface_id: {surface_id}")

        for field_name in ("adapter_id", "description"):
            _ensure_non_empty_str(getattr(self, field_name), field_name)

        for field_name in (
            "query_only_surface_ready",
            "external_backend_connected",
            "vendor_acquisition_required",
            "download_performed",
            "real_backend_enabled",
            "canonical_write_allowed",
            "runtime_mutation_allowed",
            "adapter_surface_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.query_only_surface_ready:
            raise ValueError("query_only_surface_ready must be True")
        if self.external_backend_connected:
            raise ValueError("external_backend_connected must be False before Vendor Acquisition Sandbox")
        if not self.vendor_acquisition_required:
            raise ValueError("vendor_acquisition_required must be True")
        if self.download_performed:
            raise ValueError("download_performed must be False in Batch 2")
        if self.real_backend_enabled:
            raise ValueError("real_backend_enabled must be False in Batch 2")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if not self.adapter_surface_ready:
            raise ValueError("adapter_surface_ready must be True")


def build_mempalace_adapter_surface() -> MemPalaceAdapterSurface:
    adapter = build_mempalace_adapter_contract()
    guards = build_mempalace_guard_validation_report()
    entry = adapter.entries[0]

    return MemPalaceAdapterSurface(
        adapter_surface_id="mempalace_adapter_surface_memory_routing_001",
        adapter_id=entry.adapter_id,
        query_only_surface_ready=guards.query_ready and guards.guard_validation_ready,
        external_backend_connected=False,
        vendor_acquisition_required=True,
        download_performed=False,
        real_backend_enabled=False,
        canonical_write_allowed=False,
        runtime_mutation_allowed=False,
        adapter_surface_ready=entry.adapter_ready and guards.guard_validation_ready,
        description="Read-only MemPalace adapter surface before vendor acquisition.",
    )
