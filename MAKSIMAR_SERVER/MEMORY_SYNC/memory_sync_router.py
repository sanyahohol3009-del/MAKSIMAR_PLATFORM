from __future__ import annotations

import re
from dataclasses import dataclass

from MAKSIMAR_SERVER.MEMORY_SYNC.memory_sync_manifest_models import (
    build_memory_sync_manifest_contract,
)
from MAKSIMAR_SERVER.MEMORY_SYNC.memory_sync_models import (
    build_memory_sync_contract,
)

_ROUTE_ID_PATTERN = re.compile(r"^memory_sync_route_[a-z][a-z0-9_]*_[0-9]{3}$")


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
class MemorySyncRouteEntry:
    route_id: str
    memory_sync_id: str
    source_node_id: str
    target_node_id: str
    memory_map_id: str
    route_namespace: str
    source_manifest_id: str
    target_manifest_id: str
    source_manifest_bound: bool
    target_manifest_bound: bool
    registry_bound: bool
    policy_bound: bool
    observability_bound: bool
    preview_required: bool
    checksum_required: bool
    read_only: bool
    canonical_write_allowed: bool
    client_canonical_write_allowed: bool
    runtime_mutation_allowed: bool
    route_ready: bool
    description: str

    def __post_init__(self) -> None:
        route_id = _ensure_non_empty_str(self.route_id, "route_id")
        if not _ROUTE_ID_PATTERN.fullmatch(route_id):
            raise ValueError(f"Invalid route_id: {route_id}")

        for field_name in (
            "memory_sync_id",
            "source_node_id",
            "target_node_id",
            "memory_map_id",
            "route_namespace",
            "source_manifest_id",
            "target_manifest_id",
            "description",
        ):
            _ensure_non_empty_str(getattr(self, field_name), field_name)

        if self.source_node_id == self.target_node_id:
            raise ValueError("source_node_id and target_node_id must differ")

        for field_name in (
            "source_manifest_bound",
            "target_manifest_bound",
            "registry_bound",
            "policy_bound",
            "observability_bound",
            "preview_required",
            "checksum_required",
            "read_only",
            "canonical_write_allowed",
            "client_canonical_write_allowed",
            "runtime_mutation_allowed",
            "route_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.source_manifest_bound:
            raise ValueError("source_manifest_bound must be True")
        if not self.target_manifest_bound:
            raise ValueError("target_manifest_bound must be True")
        if not self.registry_bound:
            raise ValueError("registry_bound must be True")
        if not self.policy_bound:
            raise ValueError("policy_bound must be True")
        if not self.observability_bound:
            raise ValueError("observability_bound must be True")
        if not self.preview_required:
            raise ValueError("preview_required must be True")
        if not self.checksum_required:
            raise ValueError("checksum_required must be True")
        if not self.read_only:
            raise ValueError("read_only must be True")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must be False")
        if self.client_canonical_write_allowed:
            raise ValueError("client_canonical_write_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if not self.route_ready:
            raise ValueError("route_ready must be True")


@dataclass(frozen=True, slots=True)
class MemorySyncRouteContract:
    total_routes: int
    ready_routes: int
    source_manifest_bound_routes: int
    target_manifest_bound_routes: int
    registry_bound_routes: int
    policy_bound_routes: int
    observability_bound_routes: int
    preview_required_routes: int
    checksum_required_routes: int
    read_only_routes: int
    canonical_write_allowed_routes: int
    client_canonical_write_allowed_routes: int
    runtime_mutation_allowed_routes: int
    entries: tuple[MemorySyncRouteEntry, ...]

    def __post_init__(self) -> None:
        if self.total_routes != len(self.entries):
            raise ValueError("total_routes must match entries length")
        if self.total_routes != 3:
            raise ValueError("DEV/HOME/MOBILE route contract must contain exactly 3 routes")

        expected = {
            "ready_routes": sum(1 for entry in self.entries if entry.route_ready),
            "source_manifest_bound_routes": sum(1 for entry in self.entries if entry.source_manifest_bound),
            "target_manifest_bound_routes": sum(1 for entry in self.entries if entry.target_manifest_bound),
            "registry_bound_routes": sum(1 for entry in self.entries if entry.registry_bound),
            "policy_bound_routes": sum(1 for entry in self.entries if entry.policy_bound),
            "observability_bound_routes": sum(1 for entry in self.entries if entry.observability_bound),
            "preview_required_routes": sum(1 for entry in self.entries if entry.preview_required),
            "checksum_required_routes": sum(1 for entry in self.entries if entry.checksum_required),
            "read_only_routes": sum(1 for entry in self.entries if entry.read_only),
            "canonical_write_allowed_routes": sum(1 for entry in self.entries if entry.canonical_write_allowed),
            "client_canonical_write_allowed_routes": sum(1 for entry in self.entries if entry.client_canonical_write_allowed),
            "runtime_mutation_allowed_routes": sum(1 for entry in self.entries if entry.runtime_mutation_allowed),
        }

        for field_name, expected_value in expected.items():
            if getattr(self, field_name) != expected_value:
                raise ValueError(f"{field_name} must match computed count")

        if self.ready_routes != self.total_routes:
            raise ValueError("all memory sync routes must be ready")
        if self.source_manifest_bound_routes != self.total_routes:
            raise ValueError("all routes must be source-manifest-bound")
        if self.target_manifest_bound_routes != self.total_routes:
            raise ValueError("all routes must be target-manifest-bound")
        if self.registry_bound_routes != self.total_routes:
            raise ValueError("all routes must be registry-bound")
        if self.policy_bound_routes != self.total_routes:
            raise ValueError("all routes must be policy-bound")
        if self.observability_bound_routes != self.total_routes:
            raise ValueError("all routes must be observability-bound")
        if self.preview_required_routes != self.total_routes:
            raise ValueError("all routes must require preview")
        if self.checksum_required_routes != self.total_routes:
            raise ValueError("all routes must require checksum")
        if self.read_only_routes != self.total_routes:
            raise ValueError("all routes must be read-only")
        if self.canonical_write_allowed_routes != 0:
            raise ValueError("canonical write must remain blocked")
        if self.client_canonical_write_allowed_routes != 0:
            raise ValueError("client canonical write must remain blocked")
        if self.runtime_mutation_allowed_routes != 0:
            raise ValueError("runtime mutation must remain blocked")


def build_memory_sync_route_contract() -> MemorySyncRouteContract:
    sync = build_memory_sync_contract()
    manifests = build_memory_sync_manifest_contract()
    manifest_by_node = {entry.node_id: entry for entry in manifests.entries}

    entries = tuple(
        MemorySyncRouteEntry(
            route_id=sync_entry.memory_sync_id.replace(
                "memory_sync_",
                "memory_sync_route_",
                1,
            ),
            memory_sync_id=sync_entry.memory_sync_id,
            source_node_id=sync_entry.source_node_id,
            target_node_id=sync_entry.target_node_id,
            memory_map_id=sync_entry.memory_map_id,
            route_namespace=f"memory_sync_route::{sync_entry.source_node_id}::{sync_entry.target_node_id}",
            source_manifest_id=manifest_by_node[sync_entry.source_node_id].manifest_id,
            target_manifest_id=manifest_by_node[sync_entry.target_node_id].manifest_id,
            source_manifest_bound=True,
            target_manifest_bound=True,
            registry_bound=True,
            policy_bound=True,
            observability_bound=True,
            preview_required=True,
            checksum_required=True,
            read_only=True,
            canonical_write_allowed=False,
            client_canonical_write_allowed=False,
            runtime_mutation_allowed=False,
            route_ready=(
                sync_entry.sync_ready
                and manifest_by_node[sync_entry.source_node_id].manifest_ready
                and manifest_by_node[sync_entry.target_node_id].manifest_ready
            ),
            description=f"Read-only memory sync route for {sync_entry.memory_sync_id}.",
        )
        for sync_entry in sync.entries
    )

    return MemorySyncRouteContract(
        total_routes=len(entries),
        ready_routes=sum(1 for entry in entries if entry.route_ready),
        source_manifest_bound_routes=sum(1 for entry in entries if entry.source_manifest_bound),
        target_manifest_bound_routes=sum(1 for entry in entries if entry.target_manifest_bound),
        registry_bound_routes=sum(1 for entry in entries if entry.registry_bound),
        policy_bound_routes=sum(1 for entry in entries if entry.policy_bound),
        observability_bound_routes=sum(1 for entry in entries if entry.observability_bound),
        preview_required_routes=sum(1 for entry in entries if entry.preview_required),
        checksum_required_routes=sum(1 for entry in entries if entry.checksum_required),
        read_only_routes=sum(1 for entry in entries if entry.read_only),
        canonical_write_allowed_routes=sum(1 for entry in entries if entry.canonical_write_allowed),
        client_canonical_write_allowed_routes=sum(1 for entry in entries if entry.client_canonical_write_allowed),
        runtime_mutation_allowed_routes=sum(1 for entry in entries if entry.runtime_mutation_allowed),
        entries=entries,
    )
