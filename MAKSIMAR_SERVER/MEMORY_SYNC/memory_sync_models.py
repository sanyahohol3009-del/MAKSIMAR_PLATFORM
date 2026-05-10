from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_SERVER.MEMORY_SYNC.node_memory_scope_models import (
    build_node_memory_scope_contract,
)

SyncPairKind = Literal["dev_home", "home_mobile", "dev_mobile"]

_SYNC_ID_PATTERN = re.compile(r"^memory_sync_[a-z][a-z0-9_]*_[0-9]{3}$")


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
class MemorySyncEntry:
    memory_sync_id: str
    sync_pair_kind: SyncPairKind
    source_node_id: str
    target_node_id: str
    memory_map_id: str
    sync_namespace: str
    read_model_sync: bool
    manifest_required: bool
    canonical_write_allowed: bool
    client_canonical_write_allowed: bool
    parallel_truth_allowed: bool
    auto_conflict_resolution_allowed: bool
    runtime_mutation_allowed: bool
    sync_ready: bool
    description: str

    def __post_init__(self) -> None:
        sync_id = _ensure_non_empty_str(self.memory_sync_id, "memory_sync_id")
        if not _SYNC_ID_PATTERN.fullmatch(sync_id):
            raise ValueError(f"Invalid memory_sync_id: {sync_id}")

        for field_name in (
            "source_node_id",
            "target_node_id",
            "memory_map_id",
            "sync_namespace",
            "description",
        ):
            _ensure_non_empty_str(getattr(self, field_name), field_name)

        if self.source_node_id == self.target_node_id:
            raise ValueError("source_node_id and target_node_id must differ")

        for field_name in (
            "read_model_sync",
            "manifest_required",
            "canonical_write_allowed",
            "client_canonical_write_allowed",
            "parallel_truth_allowed",
            "auto_conflict_resolution_allowed",
            "runtime_mutation_allowed",
            "sync_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.read_model_sync:
            raise ValueError("read_model_sync must be True")
        if not self.manifest_required:
            raise ValueError("manifest_required must be True")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must be False")
        if self.client_canonical_write_allowed:
            raise ValueError("client_canonical_write_allowed must be False")
        if self.parallel_truth_allowed:
            raise ValueError("parallel_truth_allowed must be False")
        if self.auto_conflict_resolution_allowed:
            raise ValueError("auto_conflict_resolution_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if not self.sync_ready:
            raise ValueError("sync_ready must be True")


@dataclass(frozen=True, slots=True)
class MemorySyncContract:
    total_syncs: int
    ready_syncs: int
    read_model_syncs: int
    manifest_required_syncs: int
    canonical_write_allowed_syncs: int
    client_canonical_write_allowed_syncs: int
    parallel_truth_allowed_syncs: int
    auto_conflict_resolution_allowed_syncs: int
    runtime_mutation_allowed_syncs: int
    entries: tuple[MemorySyncEntry, ...]

    def __post_init__(self) -> None:
        if self.total_syncs != len(self.entries):
            raise ValueError("total_syncs must match entries length")
        if self.total_syncs != 3:
            raise ValueError("DEV/HOME/MOBILE sync contract must contain exactly 3 sync links")

        expected = {
            "ready_syncs": sum(1 for entry in self.entries if entry.sync_ready),
            "read_model_syncs": sum(1 for entry in self.entries if entry.read_model_sync),
            "manifest_required_syncs": sum(1 for entry in self.entries if entry.manifest_required),
            "canonical_write_allowed_syncs": sum(1 for entry in self.entries if entry.canonical_write_allowed),
            "client_canonical_write_allowed_syncs": sum(1 for entry in self.entries if entry.client_canonical_write_allowed),
            "parallel_truth_allowed_syncs": sum(1 for entry in self.entries if entry.parallel_truth_allowed),
            "auto_conflict_resolution_allowed_syncs": sum(1 for entry in self.entries if entry.auto_conflict_resolution_allowed),
            "runtime_mutation_allowed_syncs": sum(1 for entry in self.entries if entry.runtime_mutation_allowed),
        }

        for field_name, expected_value in expected.items():
            if getattr(self, field_name) != expected_value:
                raise ValueError(f"{field_name} must match computed count")

        if self.ready_syncs != self.total_syncs:
            raise ValueError("all memory sync links must be ready")
        if self.read_model_syncs != self.total_syncs:
            raise ValueError("all memory sync links must be read-model syncs")
        if self.manifest_required_syncs != self.total_syncs:
            raise ValueError("all memory sync links must require manifests")
        if self.canonical_write_allowed_syncs != 0:
            raise ValueError("canonical write must remain blocked")
        if self.client_canonical_write_allowed_syncs != 0:
            raise ValueError("client canonical write must remain blocked")
        if self.parallel_truth_allowed_syncs != 0:
            raise ValueError("parallel truth must remain blocked")
        if self.auto_conflict_resolution_allowed_syncs != 0:
            raise ValueError("auto conflict resolution must remain blocked")
        if self.runtime_mutation_allowed_syncs != 0:
            raise ValueError("runtime mutation must remain blocked")


def build_memory_sync_contract() -> MemorySyncContract:
    scopes = build_node_memory_scope_contract()
    scope_by_node = {entry.node_id: entry for entry in scopes.entries}

    pairs = (
        ("memory_sync_dev_home_001", "dev_home", "dev_node_001", "home_node_001"),
        ("memory_sync_home_mobile_001", "home_mobile", "home_node_001", "mobile_node_001"),
        ("memory_sync_dev_mobile_001", "dev_mobile", "dev_node_001", "mobile_node_001"),
    )

    entries = tuple(
        MemorySyncEntry(
            memory_sync_id=sync_id,
            sync_pair_kind=pair_kind,
            source_node_id=source_node_id,
            target_node_id=target_node_id,
            memory_map_id=scope_by_node[source_node_id].memory_map_id,
            sync_namespace=f"memory_sync::{source_node_id}::{target_node_id}",
            read_model_sync=True,
            manifest_required=True,
            canonical_write_allowed=False,
            client_canonical_write_allowed=False,
            parallel_truth_allowed=False,
            auto_conflict_resolution_allowed=False,
            runtime_mutation_allowed=False,
            sync_ready=scope_by_node[source_node_id].memory_map_id == scope_by_node[target_node_id].memory_map_id,
            description=f"Read-only memory map sync link {source_node_id} to {target_node_id}.",
        )
        for sync_id, pair_kind, source_node_id, target_node_id in pairs
    )

    return MemorySyncContract(
        total_syncs=len(entries),
        ready_syncs=sum(1 for entry in entries if entry.sync_ready),
        read_model_syncs=sum(1 for entry in entries if entry.read_model_sync),
        manifest_required_syncs=sum(1 for entry in entries if entry.manifest_required),
        canonical_write_allowed_syncs=sum(1 for entry in entries if entry.canonical_write_allowed),
        client_canonical_write_allowed_syncs=sum(1 for entry in entries if entry.client_canonical_write_allowed),
        parallel_truth_allowed_syncs=sum(1 for entry in entries if entry.parallel_truth_allowed),
        auto_conflict_resolution_allowed_syncs=sum(1 for entry in entries if entry.auto_conflict_resolution_allowed),
        runtime_mutation_allowed_syncs=sum(1 for entry in entries if entry.runtime_mutation_allowed),
        entries=entries,
    )
