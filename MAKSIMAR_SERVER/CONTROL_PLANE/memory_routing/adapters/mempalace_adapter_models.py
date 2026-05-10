from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

MemPalaceAdapterStatus = Literal["configured_read_only"]
MemPalaceBackendKind = Literal["subordinate_backend_adapter"]

_ADAPTER_ID_PATTERN = re.compile(r"^mempalace_adapter_[a-z][a-z0-9_]*_[0-9]{3}$")


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
class MemPalaceAdapterEntry:
    adapter_id: str
    backend_kind: MemPalaceBackendKind
    adapter_status: MemPalaceAdapterStatus
    routing_namespace: str
    registry_bound: bool
    policy_bound: bool
    observability_bound: bool
    preview_required: bool
    mempalace_is_source_of_truth: bool
    canonical_write_allowed: bool
    runtime_mutation_allowed: bool
    adapter_ready: bool
    description: str

    def __post_init__(self) -> None:
        adapter_id = _ensure_non_empty_str(self.adapter_id, "adapter_id")
        if not _ADAPTER_ID_PATTERN.fullmatch(adapter_id):
            raise ValueError(f"Invalid adapter_id: {adapter_id}")

        for field_name in ("routing_namespace", "description"):
            _ensure_non_empty_str(getattr(self, field_name), field_name)

        for field_name in (
            "registry_bound",
            "policy_bound",
            "observability_bound",
            "preview_required",
            "mempalace_is_source_of_truth",
            "canonical_write_allowed",
            "runtime_mutation_allowed",
            "adapter_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.registry_bound:
            raise ValueError("registry_bound must be True")
        if not self.policy_bound:
            raise ValueError("policy_bound must be True")
        if not self.observability_bound:
            raise ValueError("observability_bound must be True")
        if not self.preview_required:
            raise ValueError("preview_required must be True")
        if self.mempalace_is_source_of_truth:
            raise ValueError("MemPalace must not be source of truth")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if not self.adapter_ready:
            raise ValueError("adapter_ready must be True")


@dataclass(frozen=True, slots=True)
class MemPalaceAdapterContract:
    total_adapters: int
    ready_adapters: int
    registry_bound_adapters: int
    policy_bound_adapters: int
    observability_bound_adapters: int
    preview_required_adapters: int
    source_of_truth_adapters: int
    canonical_write_allowed_adapters: int
    runtime_mutation_allowed_adapters: int
    entries: tuple[MemPalaceAdapterEntry, ...]

    def __post_init__(self) -> None:
        if self.total_adapters != len(self.entries):
            raise ValueError("total_adapters must match entries length")
        if self.total_adapters != 1:
            raise ValueError("MemPalace adapter contract must contain exactly one adapter")

        expected = {
            "ready_adapters": sum(1 for entry in self.entries if entry.adapter_ready),
            "registry_bound_adapters": sum(1 for entry in self.entries if entry.registry_bound),
            "policy_bound_adapters": sum(1 for entry in self.entries if entry.policy_bound),
            "observability_bound_adapters": sum(1 for entry in self.entries if entry.observability_bound),
            "preview_required_adapters": sum(1 for entry in self.entries if entry.preview_required),
            "source_of_truth_adapters": sum(1 for entry in self.entries if entry.mempalace_is_source_of_truth),
            "canonical_write_allowed_adapters": sum(1 for entry in self.entries if entry.canonical_write_allowed),
            "runtime_mutation_allowed_adapters": sum(1 for entry in self.entries if entry.runtime_mutation_allowed),
        }

        for field_name, expected_value in expected.items():
            if getattr(self, field_name) != expected_value:
                raise ValueError(f"{field_name} must match computed count")

        if self.ready_adapters != self.total_adapters:
            raise ValueError("all MemPalace adapters must be ready")
        if self.registry_bound_adapters != self.total_adapters:
            raise ValueError("all MemPalace adapters must be registry-bound")
        if self.policy_bound_adapters != self.total_adapters:
            raise ValueError("all MemPalace adapters must be policy-bound")
        if self.observability_bound_adapters != self.total_adapters:
            raise ValueError("all MemPalace adapters must be observability-bound")
        if self.preview_required_adapters != self.total_adapters:
            raise ValueError("all MemPalace adapters must require preview")
        if self.source_of_truth_adapters != 0:
            raise ValueError("MemPalace source-of-truth adapters must be zero")
        if self.canonical_write_allowed_adapters != 0:
            raise ValueError("MemPalace canonical write must remain blocked")
        if self.runtime_mutation_allowed_adapters != 0:
            raise ValueError("MemPalace runtime mutation must remain blocked")


def build_mempalace_adapter_contract() -> MemPalaceAdapterContract:
    entries = (
        MemPalaceAdapterEntry(
            adapter_id="mempalace_adapter_memory_routing_001",
            backend_kind="subordinate_backend_adapter",
            adapter_status="configured_read_only",
            routing_namespace="memory_routing::adapters::mempalace",
            registry_bound=True,
            policy_bound=True,
            observability_bound=True,
            preview_required=True,
            mempalace_is_source_of_truth=False,
            canonical_write_allowed=False,
            runtime_mutation_allowed=False,
            adapter_ready=True,
            description="Read-only subordinate MemPalace backend adapter contract.",
        ),
    )

    return MemPalaceAdapterContract(
        total_adapters=len(entries),
        ready_adapters=sum(1 for entry in entries if entry.adapter_ready),
        registry_bound_adapters=sum(1 for entry in entries if entry.registry_bound),
        policy_bound_adapters=sum(1 for entry in entries if entry.policy_bound),
        observability_bound_adapters=sum(1 for entry in entries if entry.observability_bound),
        preview_required_adapters=sum(1 for entry in entries if entry.preview_required),
        source_of_truth_adapters=sum(1 for entry in entries if entry.mempalace_is_source_of_truth),
        canonical_write_allowed_adapters=sum(1 for entry in entries if entry.canonical_write_allowed),
        runtime_mutation_allowed_adapters=sum(1 for entry in entries if entry.runtime_mutation_allowed),
        entries=entries,
    )
