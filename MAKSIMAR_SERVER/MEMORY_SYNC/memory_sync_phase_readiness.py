from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple

from MAKSIMAR_SERVER.MEMORY_SYNC.memory_sync_conflict_guard import (
    build_memory_sync_conflict_guard_contract,
)
from MAKSIMAR_SERVER.MEMORY_SYNC.memory_sync_manifest_models import (
    build_memory_sync_manifest_contract,
)
from MAKSIMAR_SERVER.MEMORY_SYNC.memory_sync_models import (
    build_memory_sync_contract,
)
from MAKSIMAR_SERVER.MEMORY_SYNC.memory_sync_preview_builder import (
    build_memory_sync_preview,
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


_FORBIDDEN_MEMORY_SYNC_RUNTIME_ROOTS = (
    "parallel_memory_truth",
    "client_canonical_writer",
    "mobile_security_root",
    "direct_memory_sync_runtime",
    "shell_runtime_executor",
    "dev_home_mobile_truth_merger",
    "memory_sync_auto_conflict_resolver",
)


@dataclass(frozen=True, slots=True)
class MemorySyncPhaseReadiness:
    node_scopes: int
    sync_links: int
    sync_manifests: int
    sync_routes: int
    conflict_guards: int
    memory_map_ids: Tuple[str, ...]
    flow: Tuple[str, ...]
    node_scope_ready: bool
    sync_links_ready: bool
    manifests_ready: bool
    routes_ready: bool
    guards_ready: bool
    registry_bound_ready: bool
    policy_bound_ready: bool
    observability_bound_ready: bool
    preview_required_ready: bool
    checksum_required_ready: bool
    conflict_guard_ready: bool
    read_only_ready: bool
    no_canonical_write: bool
    no_client_canonical_write: bool
    no_parallel_truth: bool
    no_mobile_security_root: bool
    no_auto_conflict_resolution: bool
    no_runtime_mutation: bool
    no_forbidden_memory_sync_runtime_roots: bool
    phase_ready: bool


def _no_forbidden_memory_sync_runtime_roots() -> bool:
    return not any(Path(root_name).exists() for root_name in _FORBIDDEN_MEMORY_SYNC_RUNTIME_ROOTS)


def build_memory_sync_phase_readiness() -> MemorySyncPhaseReadiness:
    scopes = build_node_memory_scope_contract()
    sync = build_memory_sync_contract()
    manifests = build_memory_sync_manifest_contract()
    routes = build_memory_sync_route_contract()
    guards = build_memory_sync_conflict_guard_contract()
    summary = build_memory_sync_summary()
    preview = build_memory_sync_preview()

    node_scope_ready = scopes.ready_scopes == scopes.total_scopes
    sync_links_ready = sync.ready_syncs == sync.total_syncs
    manifests_ready = manifests.ready_manifests == manifests.total_manifests
    routes_ready = routes.ready_routes == routes.total_routes
    guards_ready = guards.ready_guards == guards.total_guards

    registry_bound_ready = (
        manifests.registry_bound_manifests == manifests.total_manifests
        and routes.registry_bound_routes == routes.total_routes
    )
    policy_bound_ready = (
        manifests.policy_bound_manifests == manifests.total_manifests
        and routes.policy_bound_routes == routes.total_routes
    )
    observability_bound_ready = (
        manifests.observability_bound_manifests == manifests.total_manifests
        and routes.observability_bound_routes == routes.total_routes
    )
    preview_required_ready = (
        manifests.preview_required_manifests == manifests.total_manifests
        and routes.preview_required_routes == routes.total_routes
    )
    checksum_required_ready = (
        manifests.checksum_required_manifests == manifests.total_manifests
        and routes.checksum_required_routes == routes.total_routes
    )
    conflict_guard_ready = (
        guards.conflict_detection_required_guards == guards.total_guards
        and guards.conflict_marker_required_guards == guards.total_guards
        and guards.proposal_required_guards == guards.total_guards
        and guards.human_approval_required_guards == guards.total_guards
        and guards.rollback_reference_required_guards == guards.total_guards
    )
    read_only_ready = (
        scopes.read_only_scopes == scopes.total_scopes
        and manifests.read_only_manifests == manifests.total_manifests
        and routes.read_only_routes == routes.total_routes
    )

    no_canonical_write = int(summary["canonical_write_allowed"]) == 0
    no_client_canonical_write = int(summary["client_canonical_write_allowed"]) == 0
    no_parallel_truth = int(summary["parallel_truth_allowed"]) == 0
    no_mobile_security_root = int(summary["mobile_security_root_scopes"]) == 0
    no_auto_conflict_resolution = int(summary["auto_conflict_resolution_allowed"]) == 0
    no_runtime_mutation = int(summary["runtime_mutation_allowed"]) == 0
    no_forbidden_memory_sync_runtime_roots = _no_forbidden_memory_sync_runtime_roots()

    memory_map_ids = tuple(str(item) for item in preview["memory_map_ids"])

    phase_ready = (
        bool(summary["summary_ready"])
        and bool(preview["preview_ready"])
        and node_scope_ready
        and sync_links_ready
        and manifests_ready
        and routes_ready
        and guards_ready
        and registry_bound_ready
        and policy_bound_ready
        and observability_bound_ready
        and preview_required_ready
        and checksum_required_ready
        and conflict_guard_ready
        and read_only_ready
        and no_canonical_write
        and no_client_canonical_write
        and no_parallel_truth
        and no_mobile_security_root
        and no_auto_conflict_resolution
        and no_runtime_mutation
        and no_forbidden_memory_sync_runtime_roots
        and memory_map_ids == ("memory_map_global_001",)
    )

    return MemorySyncPhaseReadiness(
        node_scopes=scopes.total_scopes,
        sync_links=sync.total_syncs,
        sync_manifests=manifests.total_manifests,
        sync_routes=routes.total_routes,
        conflict_guards=guards.total_guards,
        memory_map_ids=memory_map_ids,
        flow=tuple(str(item) for item in preview["flow"]),
        node_scope_ready=node_scope_ready,
        sync_links_ready=sync_links_ready,
        manifests_ready=manifests_ready,
        routes_ready=routes_ready,
        guards_ready=guards_ready,
        registry_bound_ready=registry_bound_ready,
        policy_bound_ready=policy_bound_ready,
        observability_bound_ready=observability_bound_ready,
        preview_required_ready=preview_required_ready,
        checksum_required_ready=checksum_required_ready,
        conflict_guard_ready=conflict_guard_ready,
        read_only_ready=read_only_ready,
        no_canonical_write=no_canonical_write,
        no_client_canonical_write=no_client_canonical_write,
        no_parallel_truth=no_parallel_truth,
        no_mobile_security_root=no_mobile_security_root,
        no_auto_conflict_resolution=no_auto_conflict_resolution,
        no_runtime_mutation=no_runtime_mutation,
        no_forbidden_memory_sync_runtime_roots=no_forbidden_memory_sync_runtime_roots,
        phase_ready=phase_ready,
    )


def build_memory_sync_phase_preview() -> Dict[str, object]:
    readiness = build_memory_sync_phase_readiness()

    return {
        "flow": readiness.flow,
        "preview_ready": readiness.phase_ready,
        "phase_ready": readiness.phase_ready,
        "node_scopes": readiness.node_scopes,
        "sync_links": readiness.sync_links,
        "sync_manifests": readiness.sync_manifests,
        "sync_routes": readiness.sync_routes,
        "conflict_guards": readiness.conflict_guards,
        "memory_map_ids": readiness.memory_map_ids,
        "node_scope_ready": readiness.node_scope_ready,
        "sync_links_ready": readiness.sync_links_ready,
        "manifests_ready": readiness.manifests_ready,
        "routes_ready": readiness.routes_ready,
        "guards_ready": readiness.guards_ready,
        "registry_bound_ready": readiness.registry_bound_ready,
        "policy_bound_ready": readiness.policy_bound_ready,
        "observability_bound_ready": readiness.observability_bound_ready,
        "preview_required_ready": readiness.preview_required_ready,
        "checksum_required_ready": readiness.checksum_required_ready,
        "conflict_guard_ready": readiness.conflict_guard_ready,
        "read_only_ready": readiness.read_only_ready,
        "no_canonical_write": readiness.no_canonical_write,
        "no_client_canonical_write": readiness.no_client_canonical_write,
        "no_parallel_truth": readiness.no_parallel_truth,
        "no_mobile_security_root": readiness.no_mobile_security_root,
        "no_auto_conflict_resolution": readiness.no_auto_conflict_resolution,
        "no_runtime_mutation": readiness.no_runtime_mutation,
        "no_forbidden_memory_sync_runtime_roots": readiness.no_forbidden_memory_sync_runtime_roots,
    }
