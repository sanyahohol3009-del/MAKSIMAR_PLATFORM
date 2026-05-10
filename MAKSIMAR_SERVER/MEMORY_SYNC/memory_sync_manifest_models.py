from __future__ import annotations

import re
from dataclasses import dataclass

from MAKSIMAR_SERVER.MEMORY_SYNC.memory_sync_models import build_memory_sync_contract
from MAKSIMAR_SERVER.MEMORY_SYNC.node_memory_scope_models import build_node_memory_scope_contract

_MANIFEST_ID_PATTERN = re.compile(r"^memory_sync_manifest_[a-z][a-z0-9_]*_[0-9]{3}$")


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
class MemorySyncManifestEntry:
    manifest_id: str
    node_id: str
    memory_map_id: str
    memory_scope_namespace: str
    manifest_namespace: str
    sync_links: tuple[str, ...]
    registry_bound: bool
    policy_bound: bool
    observability_bound: bool
    preview_required: bool
    checksum_required: bool
    read_only: bool
    canonical_write_allowed: bool
    manifest_ready: bool
    description: str

    def __post_init__(self) -> None:
        manifest_id = _ensure_non_empty_str(self.manifest_id, "manifest_id")
        if not _MANIFEST_ID_PATTERN.fullmatch(manifest_id):
            raise ValueError(f"Invalid manifest_id: {manifest_id}")

        for field_name in (
            "node_id",
            "memory_map_id",
            "memory_scope_namespace",
            "manifest_namespace",
            "description",
        ):
            _ensure_non_empty_str(getattr(self, field_name), field_name)

        if not isinstance(self.sync_links, tuple) or not self.sync_links:
            raise ValueError("sync_links must be a non-empty tuple")
        if len(set(self.sync_links)) != len(self.sync_links):
            raise ValueError("sync_links must contain unique values")
        for sync_link in self.sync_links:
            _ensure_non_empty_str(sync_link, "sync_link")

        for field_name in (
            "registry_bound",
            "policy_bound",
            "observability_bound",
            "preview_required",
            "checksum_required",
            "read_only",
            "canonical_write_allowed",
            "manifest_ready",
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
        if not self.checksum_required:
            raise ValueError("checksum_required must be True")
        if not self.read_only:
            raise ValueError("read_only must be True")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must be False")
        if not self.manifest_ready:
            raise ValueError("manifest_ready must be True")


@dataclass(frozen=True, slots=True)
class MemorySyncManifestContract:
    total_manifests: int
    ready_manifests: int
    registry_bound_manifests: int
    policy_bound_manifests: int
    observability_bound_manifests: int
    preview_required_manifests: int
    checksum_required_manifests: int
    read_only_manifests: int
    canonical_write_allowed_manifests: int
    entries: tuple[MemorySyncManifestEntry, ...]

    def __post_init__(self) -> None:
        if self.total_manifests != len(self.entries):
            raise ValueError("total_manifests must match entries length")
        if self.total_manifests != 3:
            raise ValueError("DEV/HOME/MOBILE manifest contract must contain exactly 3 manifests")

        expected = {
            "ready_manifests": sum(1 for entry in self.entries if entry.manifest_ready),
            "registry_bound_manifests": sum(1 for entry in self.entries if entry.registry_bound),
            "policy_bound_manifests": sum(1 for entry in self.entries if entry.policy_bound),
            "observability_bound_manifests": sum(1 for entry in self.entries if entry.observability_bound),
            "preview_required_manifests": sum(1 for entry in self.entries if entry.preview_required),
            "checksum_required_manifests": sum(1 for entry in self.entries if entry.checksum_required),
            "read_only_manifests": sum(1 for entry in self.entries if entry.read_only),
            "canonical_write_allowed_manifests": sum(1 for entry in self.entries if entry.canonical_write_allowed),
        }

        for field_name, expected_value in expected.items():
            if getattr(self, field_name) != expected_value:
                raise ValueError(f"{field_name} must match computed count")

        if self.ready_manifests != self.total_manifests:
            raise ValueError("all memory sync manifests must be ready")
        if self.registry_bound_manifests != self.total_manifests:
            raise ValueError("all memory sync manifests must be registry-bound")
        if self.policy_bound_manifests != self.total_manifests:
            raise ValueError("all memory sync manifests must be policy-bound")
        if self.observability_bound_manifests != self.total_manifests:
            raise ValueError("all memory sync manifests must be observability-bound")
        if self.preview_required_manifests != self.total_manifests:
            raise ValueError("all memory sync manifests must require preview")
        if self.checksum_required_manifests != self.total_manifests:
            raise ValueError("all memory sync manifests must require checksum")
        if self.read_only_manifests != self.total_manifests:
            raise ValueError("all memory sync manifests must be read-only")
        if self.canonical_write_allowed_manifests != 0:
            raise ValueError("canonical write must remain blocked")


def build_memory_sync_manifest_contract() -> MemorySyncManifestContract:
    scopes = build_node_memory_scope_contract()
    sync = build_memory_sync_contract()

    sync_links_by_node: dict[str, list[str]] = {entry.node_id: [] for entry in scopes.entries}
    for link in sync.entries:
        sync_links_by_node[link.source_node_id].append(link.memory_sync_id)
        sync_links_by_node[link.target_node_id].append(link.memory_sync_id)

    entries = tuple(
        MemorySyncManifestEntry(
            manifest_id=f"memory_sync_manifest_{scope.node_id}_001",
            node_id=scope.node_id,
            memory_map_id=scope.memory_map_id,
            memory_scope_namespace=scope.memory_scope_namespace,
            manifest_namespace=f"memory_sync_manifest::{scope.node_id}",
            sync_links=tuple(sorted(sync_links_by_node[scope.node_id])),
            registry_bound=True,
            policy_bound=True,
            observability_bound=True,
            preview_required=True,
            checksum_required=True,
            read_only=True,
            canonical_write_allowed=False,
            manifest_ready=scope.scope_ready and bool(sync_links_by_node[scope.node_id]),
            description=f"Read-only memory sync manifest for {scope.node_id}.",
        )
        for scope in scopes.entries
    )

    return MemorySyncManifestContract(
        total_manifests=len(entries),
        ready_manifests=sum(1 for entry in entries if entry.manifest_ready),
        registry_bound_manifests=sum(1 for entry in entries if entry.registry_bound),
        policy_bound_manifests=sum(1 for entry in entries if entry.policy_bound),
        observability_bound_manifests=sum(1 for entry in entries if entry.observability_bound),
        preview_required_manifests=sum(1 for entry in entries if entry.preview_required),
        checksum_required_manifests=sum(1 for entry in entries if entry.checksum_required),
        read_only_manifests=sum(1 for entry in entries if entry.read_only),
        canonical_write_allowed_manifests=sum(1 for entry in entries if entry.canonical_write_allowed),
        entries=entries,
    )
