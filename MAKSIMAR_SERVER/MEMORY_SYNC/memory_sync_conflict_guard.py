from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_SERVER.MEMORY_SYNC.memory_sync_router import (
    build_memory_sync_route_contract,
)

ConflictPolicy = Literal["manual_review_required"]

_GUARD_ID_PATTERN = re.compile(r"^memory_sync_conflict_guard_[a-z][a-z0-9_]*_[0-9]{3}$")


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
class MemorySyncConflictGuardEntry:
    guard_id: str
    route_id: str
    memory_sync_id: str
    source_node_id: str
    target_node_id: str
    memory_map_id: str
    conflict_policy: ConflictPolicy
    conflict_detection_required: bool
    conflict_marker_required: bool
    proposal_required: bool
    human_approval_required: bool
    rollback_reference_required: bool
    auto_conflict_resolution_allowed: bool
    parallel_truth_allowed: bool
    canonical_write_allowed: bool
    client_canonical_write_allowed: bool
    runtime_mutation_allowed: bool
    guard_ready: bool
    description: str

    def __post_init__(self) -> None:
        guard_id = _ensure_non_empty_str(self.guard_id, "guard_id")
        if not _GUARD_ID_PATTERN.fullmatch(guard_id):
            raise ValueError(f"Invalid guard_id: {guard_id}")

        for field_name in (
            "route_id",
            "memory_sync_id",
            "source_node_id",
            "target_node_id",
            "memory_map_id",
            "description",
        ):
            _ensure_non_empty_str(getattr(self, field_name), field_name)

        for field_name in (
            "conflict_detection_required",
            "conflict_marker_required",
            "proposal_required",
            "human_approval_required",
            "rollback_reference_required",
            "auto_conflict_resolution_allowed",
            "parallel_truth_allowed",
            "canonical_write_allowed",
            "client_canonical_write_allowed",
            "runtime_mutation_allowed",
            "guard_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.conflict_detection_required:
            raise ValueError("conflict_detection_required must be True")
        if not self.conflict_marker_required:
            raise ValueError("conflict_marker_required must be True")
        if not self.proposal_required:
            raise ValueError("proposal_required must be True")
        if not self.human_approval_required:
            raise ValueError("human_approval_required must be True")
        if not self.rollback_reference_required:
            raise ValueError("rollback_reference_required must be True")
        if self.auto_conflict_resolution_allowed:
            raise ValueError("auto_conflict_resolution_allowed must be False")
        if self.parallel_truth_allowed:
            raise ValueError("parallel_truth_allowed must be False")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must be False")
        if self.client_canonical_write_allowed:
            raise ValueError("client_canonical_write_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if not self.guard_ready:
            raise ValueError("guard_ready must be True")


@dataclass(frozen=True, slots=True)
class MemorySyncConflictGuardContract:
    total_guards: int
    ready_guards: int
    conflict_detection_required_guards: int
    conflict_marker_required_guards: int
    proposal_required_guards: int
    human_approval_required_guards: int
    rollback_reference_required_guards: int
    auto_conflict_resolution_allowed_guards: int
    parallel_truth_allowed_guards: int
    canonical_write_allowed_guards: int
    client_canonical_write_allowed_guards: int
    runtime_mutation_allowed_guards: int
    entries: tuple[MemorySyncConflictGuardEntry, ...]

    def __post_init__(self) -> None:
        if self.total_guards != len(self.entries):
            raise ValueError("total_guards must match entries length")
        if self.total_guards != 3:
            raise ValueError("DEV/HOME/MOBILE conflict guard contract must contain exactly 3 guards")

        expected = {
            "ready_guards": sum(1 for entry in self.entries if entry.guard_ready),
            "conflict_detection_required_guards": sum(1 for entry in self.entries if entry.conflict_detection_required),
            "conflict_marker_required_guards": sum(1 for entry in self.entries if entry.conflict_marker_required),
            "proposal_required_guards": sum(1 for entry in self.entries if entry.proposal_required),
            "human_approval_required_guards": sum(1 for entry in self.entries if entry.human_approval_required),
            "rollback_reference_required_guards": sum(1 for entry in self.entries if entry.rollback_reference_required),
            "auto_conflict_resolution_allowed_guards": sum(1 for entry in self.entries if entry.auto_conflict_resolution_allowed),
            "parallel_truth_allowed_guards": sum(1 for entry in self.entries if entry.parallel_truth_allowed),
            "canonical_write_allowed_guards": sum(1 for entry in self.entries if entry.canonical_write_allowed),
            "client_canonical_write_allowed_guards": sum(1 for entry in self.entries if entry.client_canonical_write_allowed),
            "runtime_mutation_allowed_guards": sum(1 for entry in self.entries if entry.runtime_mutation_allowed),
        }

        for field_name, expected_value in expected.items():
            if getattr(self, field_name) != expected_value:
                raise ValueError(f"{field_name} must match computed count")

        if self.ready_guards != self.total_guards:
            raise ValueError("all memory sync conflict guards must be ready")
        if self.conflict_detection_required_guards != self.total_guards:
            raise ValueError("all guards must require conflict detection")
        if self.conflict_marker_required_guards != self.total_guards:
            raise ValueError("all guards must require conflict markers")
        if self.proposal_required_guards != self.total_guards:
            raise ValueError("all guards must require proposals")
        if self.human_approval_required_guards != self.total_guards:
            raise ValueError("all guards must require human approval")
        if self.rollback_reference_required_guards != self.total_guards:
            raise ValueError("all guards must require rollback references")
        if self.auto_conflict_resolution_allowed_guards != 0:
            raise ValueError("auto conflict resolution must remain blocked")
        if self.parallel_truth_allowed_guards != 0:
            raise ValueError("parallel truth must remain blocked")
        if self.canonical_write_allowed_guards != 0:
            raise ValueError("canonical write must remain blocked")
        if self.client_canonical_write_allowed_guards != 0:
            raise ValueError("client canonical write must remain blocked")
        if self.runtime_mutation_allowed_guards != 0:
            raise ValueError("runtime mutation must remain blocked")


def build_memory_sync_conflict_guard_contract() -> MemorySyncConflictGuardContract:
    routes = build_memory_sync_route_contract()

    entries = tuple(
        MemorySyncConflictGuardEntry(
            guard_id=route.route_id.replace(
                "memory_sync_route_",
                "memory_sync_conflict_guard_",
                1,
            ),
            route_id=route.route_id,
            memory_sync_id=route.memory_sync_id,
            source_node_id=route.source_node_id,
            target_node_id=route.target_node_id,
            memory_map_id=route.memory_map_id,
            conflict_policy="manual_review_required",
            conflict_detection_required=True,
            conflict_marker_required=True,
            proposal_required=True,
            human_approval_required=True,
            rollback_reference_required=True,
            auto_conflict_resolution_allowed=False,
            parallel_truth_allowed=False,
            canonical_write_allowed=False,
            client_canonical_write_allowed=False,
            runtime_mutation_allowed=False,
            guard_ready=route.route_ready,
            description=f"Manual review conflict guard for {route.memory_sync_id}.",
        )
        for route in routes.entries
    )

    return MemorySyncConflictGuardContract(
        total_guards=len(entries),
        ready_guards=sum(1 for entry in entries if entry.guard_ready),
        conflict_detection_required_guards=sum(1 for entry in entries if entry.conflict_detection_required),
        conflict_marker_required_guards=sum(1 for entry in entries if entry.conflict_marker_required),
        proposal_required_guards=sum(1 for entry in entries if entry.proposal_required),
        human_approval_required_guards=sum(1 for entry in entries if entry.human_approval_required),
        rollback_reference_required_guards=sum(1 for entry in entries if entry.rollback_reference_required),
        auto_conflict_resolution_allowed_guards=sum(1 for entry in entries if entry.auto_conflict_resolution_allowed),
        parallel_truth_allowed_guards=sum(1 for entry in entries if entry.parallel_truth_allowed),
        canonical_write_allowed_guards=sum(1 for entry in entries if entry.canonical_write_allowed),
        client_canonical_write_allowed_guards=sum(1 for entry in entries if entry.client_canonical_write_allowed),
        runtime_mutation_allowed_guards=sum(1 for entry in entries if entry.runtime_mutation_allowed),
        entries=entries,
    )
