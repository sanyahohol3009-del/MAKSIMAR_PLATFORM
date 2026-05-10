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
from MAKSIMAR_SERVER.MEMORY_SYNC.node_memory_scope_models import (
    build_node_memory_scope_contract,
)


def build_memory_sync_summary() -> Dict[str, object]:
    scopes = build_node_memory_scope_contract()
    sync = build_memory_sync_contract()
    manifests = build_memory_sync_manifest_contract()
    routes = build_memory_sync_route_contract()
    guards = build_memory_sync_conflict_guard_contract()

    canonical_write_allowed = (
        scopes.canonical_write_allowed_scopes
        + sync.canonical_write_allowed_syncs
        + manifests.canonical_write_allowed_manifests
        + routes.canonical_write_allowed_routes
        + guards.canonical_write_allowed_guards
    )
    client_canonical_write_allowed = (
        scopes.client_canonical_write_allowed_scopes
        + sync.client_canonical_write_allowed_syncs
        + routes.client_canonical_write_allowed_routes
        + guards.client_canonical_write_allowed_guards
    )
    parallel_truth_allowed = (
        scopes.parallel_truth_allowed_scopes
        + sync.parallel_truth_allowed_syncs
        + guards.parallel_truth_allowed_guards
    )
    runtime_mutation_allowed = (
        sync.runtime_mutation_allowed_syncs
        + routes.runtime_mutation_allowed_routes
        + guards.runtime_mutation_allowed_guards
    )
    auto_conflict_resolution_allowed = (
        sync.auto_conflict_resolution_allowed_syncs
        + guards.auto_conflict_resolution_allowed_guards
    )

    summary_ready = (
        scopes.ready_scopes == scopes.total_scopes
        and sync.ready_syncs == sync.total_syncs
        and manifests.ready_manifests == manifests.total_manifests
        and routes.ready_routes == routes.total_routes
        and guards.ready_guards == guards.total_guards
        and manifests.registry_bound_manifests == manifests.total_manifests
        and manifests.policy_bound_manifests == manifests.total_manifests
        and manifests.observability_bound_manifests == manifests.total_manifests
        and routes.registry_bound_routes == routes.total_routes
        and routes.policy_bound_routes == routes.total_routes
        and routes.observability_bound_routes == routes.total_routes
        and guards.human_approval_required_guards == guards.total_guards
        and guards.rollback_reference_required_guards == guards.total_guards
        and canonical_write_allowed == 0
        and client_canonical_write_allowed == 0
        and parallel_truth_allowed == 0
        and runtime_mutation_allowed == 0
        and auto_conflict_resolution_allowed == 0
        and scopes.mobile_security_root_scopes == 0
    )

    return {
        "node_scopes": scopes.total_scopes,
        "ready_node_scopes": scopes.ready_scopes,
        "sync_links": sync.total_syncs,
        "ready_sync_links": sync.ready_syncs,
        "sync_manifests": manifests.total_manifests,
        "ready_sync_manifests": manifests.ready_manifests,
        "sync_routes": routes.total_routes,
        "ready_sync_routes": routes.ready_routes,
        "conflict_guards": guards.total_guards,
        "ready_conflict_guards": guards.ready_guards,
        "registry_bound_manifests": manifests.registry_bound_manifests,
        "policy_bound_manifests": manifests.policy_bound_manifests,
        "observability_bound_manifests": manifests.observability_bound_manifests,
        "registry_bound_routes": routes.registry_bound_routes,
        "policy_bound_routes": routes.policy_bound_routes,
        "observability_bound_routes": routes.observability_bound_routes,
        "human_approval_required_guards": guards.human_approval_required_guards,
        "rollback_reference_required_guards": guards.rollback_reference_required_guards,
        "canonical_write_allowed": canonical_write_allowed,
        "client_canonical_write_allowed": client_canonical_write_allowed,
        "parallel_truth_allowed": parallel_truth_allowed,
        "runtime_mutation_allowed": runtime_mutation_allowed,
        "auto_conflict_resolution_allowed": auto_conflict_resolution_allowed,
        "mobile_security_root_scopes": scopes.mobile_security_root_scopes,
        "summary_ready": summary_ready,
    }
