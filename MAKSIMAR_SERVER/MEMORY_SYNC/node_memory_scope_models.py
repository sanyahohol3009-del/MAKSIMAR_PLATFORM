from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

NodeRole = Literal["DEV_NODE", "HOME_NODE", "MOBILE_NODE"]

_NODE_ID_PATTERN = re.compile(r"^(dev_node|home_node|mobile_node)_[0-9]{3}$")
_MEMORY_MAP_ID_PATTERN = re.compile(r"^memory_map_[a-z][a-z0-9_]*_[0-9]{3}$")


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
class NodeMemoryScopeEntry:
    node_id: str
    node_role: NodeRole
    memory_map_id: str
    memory_scope_namespace: str
    can_read_memory_map: bool
    canonical_write_allowed: bool
    client_canonical_write_allowed: bool
    mobile_security_root: bool
    parallel_truth_allowed: bool
    sync_manifest_required: bool
    read_only_scope: bool
    scope_ready: bool
    description: str

    def __post_init__(self) -> None:
        node_id = _ensure_non_empty_str(self.node_id, "node_id")
        memory_map_id = _ensure_non_empty_str(self.memory_map_id, "memory_map_id")

        if not _NODE_ID_PATTERN.fullmatch(node_id):
            raise ValueError(f"Invalid node_id: {node_id}")
        if not _MEMORY_MAP_ID_PATTERN.fullmatch(memory_map_id):
            raise ValueError(f"Invalid memory_map_id: {memory_map_id}")

        for field_name in ("memory_scope_namespace", "description"):
            _ensure_non_empty_str(getattr(self, field_name), field_name)

        for field_name in (
            "can_read_memory_map",
            "canonical_write_allowed",
            "client_canonical_write_allowed",
            "mobile_security_root",
            "parallel_truth_allowed",
            "sync_manifest_required",
            "read_only_scope",
            "scope_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.can_read_memory_map:
            raise ValueError("can_read_memory_map must be True")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must be False")
        if self.client_canonical_write_allowed:
            raise ValueError("client_canonical_write_allowed must be False")
        if self.mobile_security_root:
            raise ValueError("mobile_security_root must be False")
        if self.parallel_truth_allowed:
            raise ValueError("parallel_truth_allowed must be False")
        if not self.sync_manifest_required:
            raise ValueError("sync_manifest_required must be True")
        if not self.read_only_scope:
            raise ValueError("read_only_scope must be True")
        if not self.scope_ready:
            raise ValueError("scope_ready must be True")


@dataclass(frozen=True, slots=True)
class NodeMemoryScopeContract:
    total_scopes: int
    ready_scopes: int
    read_enabled_scopes: int
    read_only_scopes: int
    canonical_write_allowed_scopes: int
    client_canonical_write_allowed_scopes: int
    mobile_security_root_scopes: int
    parallel_truth_allowed_scopes: int
    sync_manifest_required_scopes: int
    entries: tuple[NodeMemoryScopeEntry, ...]

    def __post_init__(self) -> None:
        if self.total_scopes != len(self.entries):
            raise ValueError("total_scopes must match entries length")
        if self.total_scopes != 3:
            raise ValueError("DEV/HOME/MOBILE scope contract must contain exactly 3 scopes")

        expected = {
            "ready_scopes": sum(1 for entry in self.entries if entry.scope_ready),
            "read_enabled_scopes": sum(1 for entry in self.entries if entry.can_read_memory_map),
            "read_only_scopes": sum(1 for entry in self.entries if entry.read_only_scope),
            "canonical_write_allowed_scopes": sum(1 for entry in self.entries if entry.canonical_write_allowed),
            "client_canonical_write_allowed_scopes": sum(1 for entry in self.entries if entry.client_canonical_write_allowed),
            "mobile_security_root_scopes": sum(1 for entry in self.entries if entry.mobile_security_root),
            "parallel_truth_allowed_scopes": sum(1 for entry in self.entries if entry.parallel_truth_allowed),
            "sync_manifest_required_scopes": sum(1 for entry in self.entries if entry.sync_manifest_required),
        }

        for field_name, expected_value in expected.items():
            if getattr(self, field_name) != expected_value:
                raise ValueError(f"{field_name} must match computed count")

        if self.ready_scopes != self.total_scopes:
            raise ValueError("all node memory scopes must be ready")
        if self.read_enabled_scopes != self.total_scopes:
            raise ValueError("all node memory scopes must read memory map")
        if self.read_only_scopes != self.total_scopes:
            raise ValueError("all node memory scopes must be read-only")
        if self.canonical_write_allowed_scopes != 0:
            raise ValueError("canonical write must remain blocked")
        if self.client_canonical_write_allowed_scopes != 0:
            raise ValueError("client canonical write must remain blocked")
        if self.mobile_security_root_scopes != 0:
            raise ValueError("mobile security root must remain blocked")
        if self.parallel_truth_allowed_scopes != 0:
            raise ValueError("parallel truth must remain blocked")
        if self.sync_manifest_required_scopes != self.total_scopes:
            raise ValueError("all node memory scopes must require sync manifest")

        memory_map_ids = {entry.memory_map_id for entry in self.entries}
        if len(memory_map_ids) != 1:
            raise ValueError("DEV/HOME/MOBILE must reference one consistent memory_map_id")


def build_node_memory_scope_contract() -> NodeMemoryScopeContract:
    entries = (
        NodeMemoryScopeEntry(
            node_id="dev_node_001",
            node_role="DEV_NODE",
            memory_map_id="memory_map_global_001",
            memory_scope_namespace="memory_sync::dev_node_001",
            can_read_memory_map=True,
            canonical_write_allowed=False,
            client_canonical_write_allowed=False,
            mobile_security_root=False,
            parallel_truth_allowed=False,
            sync_manifest_required=True,
            read_only_scope=True,
            scope_ready=True,
            description="Read-only DEV node memory map scope.",
        ),
        NodeMemoryScopeEntry(
            node_id="home_node_001",
            node_role="HOME_NODE",
            memory_map_id="memory_map_global_001",
            memory_scope_namespace="memory_sync::home_node_001",
            can_read_memory_map=True,
            canonical_write_allowed=False,
            client_canonical_write_allowed=False,
            mobile_security_root=False,
            parallel_truth_allowed=False,
            sync_manifest_required=True,
            read_only_scope=True,
            scope_ready=True,
            description="Read-only HOME node memory map scope.",
        ),
        NodeMemoryScopeEntry(
            node_id="mobile_node_001",
            node_role="MOBILE_NODE",
            memory_map_id="memory_map_global_001",
            memory_scope_namespace="memory_sync::mobile_node_001",
            can_read_memory_map=True,
            canonical_write_allowed=False,
            client_canonical_write_allowed=False,
            mobile_security_root=False,
            parallel_truth_allowed=False,
            sync_manifest_required=True,
            read_only_scope=True,
            scope_ready=True,
            description="Read-only MOBILE node memory map scope.",
        ),
    )

    return NodeMemoryScopeContract(
        total_scopes=len(entries),
        ready_scopes=sum(1 for entry in entries if entry.scope_ready),
        read_enabled_scopes=sum(1 for entry in entries if entry.can_read_memory_map),
        read_only_scopes=sum(1 for entry in entries if entry.read_only_scope),
        canonical_write_allowed_scopes=sum(1 for entry in entries if entry.canonical_write_allowed),
        client_canonical_write_allowed_scopes=sum(1 for entry in entries if entry.client_canonical_write_allowed),
        mobile_security_root_scopes=sum(1 for entry in entries if entry.mobile_security_root),
        parallel_truth_allowed_scopes=sum(1 for entry in entries if entry.parallel_truth_allowed),
        sync_manifest_required_scopes=sum(1 for entry in entries if entry.sync_manifest_required),
        entries=entries,
    )
