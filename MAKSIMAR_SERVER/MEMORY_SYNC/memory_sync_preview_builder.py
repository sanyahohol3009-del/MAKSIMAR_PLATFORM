from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.MEMORY_SYNC.memory_sync_conflict_guard import (
    build_memory_sync_conflict_guard_contract,
)
from MAKSIMAR_SERVER.MEMORY_SYNC.memory_sync_manifest_models import (
    build_memory_sync_manifest_contract,
)
from MAKSIMAR_SERVER.MEMORY_SYNC.memory_sync_models import (
    build_memory_sync_contract,
)
from MAKSIMAR_SERVER.MEMORY_SYNC.memory_sync_router import (
    build_memory_sync_route_contract,
)
from MAKSIMAR_SERVER.MEMORY_SYNC.memory_sync_summary_builder import (
    build_memory_sync_summary,
)
from MAKSIMAR_SERVER.MEMORY_SYNC.node_memory_scope_models import (
    build_node_memory_scope_contract,
)


_MEMORY_SYNC_PREVIEW_FLOW = (
    "node_memory_scope",
    "memory_sync",
    "memory_sync_manifest",
    "memory_sync_router",
    "memory_sync_conflict_guard",
    "memory_sync_summary",
    "memory_sync_preview",
)


def build_memory_sync_preview() -> Dict[str, object]:
    scopes = build_node_memory_scope_contract()
    sync = build_memory_sync_contract()
    manifests = build_memory_sync_manifest_contract()
    routes = build_memory_sync_route_contract()
    guards = build_memory_sync_conflict_guard_contract()
    summary = build_memory_sync_summary()

    return {
        "flow": _MEMORY_SYNC_PREVIEW_FLOW,
        "preview_ready": bool(summary["summary_ready"]),
        "summary_ready": summary["summary_ready"],
        "node_scopes": summary["node_scopes"],
        "sync_links": summary["sync_links"],
        "sync_manifests": summary["sync_manifests"],
        "sync_routes": summary["sync_routes"],
        "conflict_guards": summary["conflict_guards"],
        "canonical_write_allowed": summary["canonical_write_allowed"],
        "client_canonical_write_allowed": summary["client_canonical_write_allowed"],
        "parallel_truth_allowed": summary["parallel_truth_allowed"],
        "runtime_mutation_allowed": summary["runtime_mutation_allowed"],
        "auto_conflict_resolution_allowed": summary["auto_conflict_resolution_allowed"],
        "mobile_security_root_scopes": summary["mobile_security_root_scopes"],
        "node_ids": tuple(entry.node_id for entry in scopes.entries),
        "node_roles": tuple(entry.node_role for entry in scopes.entries),
        "memory_map_ids": tuple(sorted({entry.memory_map_id for entry in scopes.entries})),
        "memory_sync_ids": tuple(entry.memory_sync_id for entry in sync.entries),
        "manifest_ids": tuple(entry.manifest_id for entry in manifests.entries),
        "route_ids": tuple(entry.route_id for entry in routes.entries),
        "guard_ids": tuple(entry.guard_id for entry in guards.entries),
    }
