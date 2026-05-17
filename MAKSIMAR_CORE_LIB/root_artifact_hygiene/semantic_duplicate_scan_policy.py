from __future__ import annotations

from pathlib import Path
from typing import Iterable

from MAKSIMAR_CORE_LIB.root_artifact_hygiene.semantic_duplicate_scan_models import (
    NO_EXISTING_MATCH_SENTINEL,
    SemanticDuplicateAction,
    SemanticDuplicateRelation,
    SemanticDuplicateRisk,
    SemanticDuplicateScanCandidate,
    SemanticDuplicateScanReadModel,
    SemanticFamily,
)


FAMILY_TOKEN_MAP: tuple[tuple[SemanticFamily, tuple[str, ...]], ...] = (
    (
        SemanticFamily.ROOT_ARTIFACT_HYGIENE,
        (
            "root_artifact_hygiene",
            "artifact_classification",
            "artifact_location",
            "semantic_duplicate",
            "root_surface_inventory",
            "root_artifact_report",
        ),
    ),
    (
        SemanticFamily.SECURITY,
        (
            "security",
            "rbac",
            "policy_enforcer",
            "policy_engine",
            "policy_loader",
            "approval",
            "signature_verifier",
            "vault",
            "quarantine",
            "usb_guard",
            "voice_identity",
        ),
    ),
    (
        SemanticFamily.DATA,
        (
            "data_plane",
            "append_only",
            "immutable_ledger",
            "ledger",
            "storage",
            "object_storage",
            "vector_store",
            "postgres",
            "event_journal",
            "artifact_routing",
            "memory_index",
        ),
    ),
    (
        SemanticFamily.UPDATE_RECOVERY,
        (
            "update_recovery",
            "update_channel",
            "secure_sync_update",
            "recovery",
            "rollback",
            "snapshot",
            "signed_update",
            "offline_import",
            "update_signature",
        ),
    ),
    (
        SemanticFamily.NETWORK_CONTAINERIZATION,
        (
            "network_containerization",
            "network_segmentation",
            "network_trust",
            "container_contract",
            "container_adapter_boundary",
            "docker",
            "compose",
            "vpn",
            "healthcheck",
            "restart_policy",
            "forbidden_edges",
        ),
    ),
    (
        SemanticFamily.AI_ORCHESTRATION,
        (
            "ai_orchestration",
            "ai_services",
            "model_router",
            "model_request",
            "model_response",
            "agent_plan",
            "tool_call",
            "proposal_staging",
            "model_provenance",
            "finops",
            "feedback_engine",
            "workers",
        ),
    ),
    (
        SemanticFamily.REGISTRY_ENROLLMENT,
        (
            "registry_enrollment",
            "auto_enrollment",
            "domain_enrollment",
            "memory_registry",
            "dashboard_visibility",
            "foundation_registry",
            "layer_manifest",
        ),
    ),
    (
        SemanticFamily.OBSERVABILITY_DASHBOARD,
        (
            "observability",
            "dashboard",
            "read_model",
            "telemetry",
            "preview",
            "metrics",
            "incident",
            "panel",
        ),
    ),
    (
        SemanticFamily.GOVERNANCE,
        (
            "governance",
            "risk",
            "consent",
            "regulatory",
            "legal",
            "retention",
            "anti_scam",
        ),
    ),
    (
        SemanticFamily.EXECUTION,
        (
            "execution",
            "runtime",
            "supervisor",
            "admission",
            "backpressure",
            "degraded_mode",
            "worker",
        ),
    ),
    (
        SemanticFamily.MEMORY,
        (
            "memory_engine",
            "memory_routing",
            "retrieval",
            "evidence",
            "mempalace",
            "knowledge",
        ),
    ),
    (
        SemanticFamily.PRODUCT,
        (
            "product",
            "cube",
            "module",
            "module_manifest",
            "productization",
            "skill",
        ),
    ),
    (
        SemanticFamily.TESTING_TOOLING,
        (
            "pytest",
            "test_",
            "tools/",
            "ci_check",
            "schema",
            "roadmap",
            "provenance",
        ),
    ),
)

LEGACY_OR_EXISTING_ROOTS: tuple[str, ...] = (
    "AI_SERVICES/",
    "CONTROL_PLANE/",
    "CORE_ROOT/",
    "EVENT_BUS/",
    "MAKSIMAR_CORE/",
    "MAKSIMAR_CORE_LIB/",
    "MAKSIMAR_SERVER/",
    "RUNTIME/",
    "SUPERVISOR/",
    "VPN_LAYER/",
)

CONTAINER_BOUNDARY_MARKERS: tuple[str, ...] = (
    "adapter",
    "adapters",
    "boundary",
    "boundaries",
    "container",
    "facade",
    "proxy",
)

EXTERNAL_VENDOR_MARKERS: tuple[str, ...] = (
    "EXTERNAL_BACKENDS/",
    "vendor_",
)


def infer_semantic_family(path: str | Path) -> SemanticFamily:
    normalized = _normalize_path(path)
    lowered = normalized.lower()

    for family, tokens in FAMILY_TOKEN_MAP:
        for token in tokens:
            if token in lowered:
                return family

    return SemanticFamily.UNKNOWN


def classify_semantic_duplicate_relation(
    *,
    target_path: str | Path,
    existing_path: str | Path,
) -> SemanticDuplicateRelation:
    target = _normalize_path(target_path)
    existing = _normalize_path(existing_path)

    if target == existing:
        return SemanticDuplicateRelation.SAME_PATH

    target_name = Path(target).name
    existing_name = Path(existing).name

    if target_name == existing_name:
        return SemanticDuplicateRelation.EXACT_NAME_MATCH

    target_family = infer_semantic_family(target)
    existing_family = infer_semantic_family(existing)

    if _has_container_boundary_marker(target) and _has_container_boundary_marker(existing):
        if target_family == existing_family and target_family is not SemanticFamily.UNKNOWN:
            return SemanticDuplicateRelation.CONTAINER_BOUNDARY_DUPLICATE

    if target_family == existing_family and target_family is not SemanticFamily.UNKNOWN:
        if _looks_like_legacy_or_existing(existing):
            return SemanticDuplicateRelation.LEGACY_IMPLEMENTATION

        return SemanticDuplicateRelation.SEMANTIC_FAMILY_MATCH

    if (
        target_family == existing_family
        and target_family is not SemanticFamily.UNKNOWN
        and _shares_top_runtime_area(target, existing)
    ):
        return SemanticDuplicateRelation.RELATED_RUNTIME_LAYER

    return SemanticDuplicateRelation.NO_RELATION


def build_semantic_duplicate_candidate(
    *,
    target_path: str | Path,
    existing_path: str | Path,
) -> SemanticDuplicateScanCandidate:
    target = _normalize_path(target_path)
    existing = _normalize_path(existing_path)

    target_family = infer_semantic_family(target)
    existing_family = infer_semantic_family(existing)

    if existing == NO_EXISTING_MATCH_SENTINEL:
        return SemanticDuplicateScanCandidate(
            target_path=target,
            existing_path=NO_EXISTING_MATCH_SENTINEL,
            target_family=target_family,
            existing_family=SemanticFamily.UNKNOWN,
            duplicate_relation=SemanticDuplicateRelation.NO_RELATION,
            action=SemanticDuplicateAction.CREATE_NEW,
            risk_level=SemanticDuplicateRisk.NONE,
            reason_codes=("no_existing_semantic_match_found",),
            requires_approval=False,
        )

    relation = classify_semantic_duplicate_relation(
        target_path=target,
        existing_path=existing,
    )
    action = _action_for_relation(
        relation=relation,
        existing_path=existing,
    )
    risk_level = _risk_for_action(action)
    requires_approval = action in {
        SemanticDuplicateAction.MIGRATION_CANDIDATE,
        SemanticDuplicateAction.TRUE_DUPLICATE_RISK,
    }

    return SemanticDuplicateScanCandidate(
        target_path=target,
        existing_path=existing,
        target_family=target_family,
        existing_family=existing_family,
        duplicate_relation=relation,
        action=action,
        risk_level=risk_level,
        reason_codes=_reason_codes_for_relation(
            relation=relation,
            action=action,
            existing_path=existing,
        ),
        requires_approval=requires_approval,
    )


def build_semantic_duplicate_scan_read_model(
    *,
    target_paths: Iterable[str | Path],
    existing_paths: Iterable[str | Path],
    scan_scope: str = "project",
) -> SemanticDuplicateScanReadModel:
    target_tuple = tuple(_normalize_path(path) for path in target_paths)
    existing_tuple = tuple(_normalize_path(path) for path in existing_paths)

    candidates: list[SemanticDuplicateScanCandidate] = []

    for target in target_tuple:
        target_candidates: list[SemanticDuplicateScanCandidate] = []

        for existing in existing_tuple:
            candidate = build_semantic_duplicate_candidate(
                target_path=target,
                existing_path=existing,
            )

            if candidate.duplicate_relation is SemanticDuplicateRelation.NO_RELATION:
                continue

            target_candidates.append(candidate)

        if target_candidates:
            candidates.extend(target_candidates)
        else:
            candidates.append(
                build_semantic_duplicate_candidate(
                    target_path=target,
                    existing_path=NO_EXISTING_MATCH_SENTINEL,
                )
            )

    return SemanticDuplicateScanReadModel.from_candidates(
        scan_scope=scan_scope,
        target_paths=target_tuple,
        candidates=tuple(candidates),
    )


def _action_for_relation(
    *,
    relation: SemanticDuplicateRelation,
    existing_path: str,
) -> SemanticDuplicateAction:
    if relation is SemanticDuplicateRelation.SAME_PATH:
        return SemanticDuplicateAction.REUSE_IN_PLACE

    if relation is SemanticDuplicateRelation.EXACT_NAME_MATCH:
        return SemanticDuplicateAction.TRUE_DUPLICATE_RISK

    if relation is SemanticDuplicateRelation.CONTAINER_BOUNDARY_DUPLICATE:
        return SemanticDuplicateAction.CONTAINER_BOUNDARY_DUPLICATE_ALLOWED

    if relation is SemanticDuplicateRelation.LEGACY_IMPLEMENTATION:
        if _looks_like_external_vendor(existing_path):
            return SemanticDuplicateAction.KEEP_LEGACY
        return SemanticDuplicateAction.WRAP_AS_ADAPTER

    if relation is SemanticDuplicateRelation.RELATED_RUNTIME_LAYER:
        return SemanticDuplicateAction.WRAP_AS_ADAPTER

    if relation is SemanticDuplicateRelation.SEMANTIC_FAMILY_MATCH:
        return SemanticDuplicateAction.MIGRATION_CANDIDATE

    return SemanticDuplicateAction.KEEP_LEGACY


def _risk_for_action(action: SemanticDuplicateAction) -> SemanticDuplicateRisk:
    if action is SemanticDuplicateAction.TRUE_DUPLICATE_RISK:
        return SemanticDuplicateRisk.HIGH

    if action in {
        SemanticDuplicateAction.WRAP_AS_ADAPTER,
        SemanticDuplicateAction.MIGRATION_CANDIDATE,
        SemanticDuplicateAction.KEEP_LEGACY,
    }:
        return SemanticDuplicateRisk.MEDIUM

    if action is SemanticDuplicateAction.CONTAINER_BOUNDARY_DUPLICATE_ALLOWED:
        return SemanticDuplicateRisk.LOW

    return SemanticDuplicateRisk.NONE


def _reason_codes_for_relation(
    *,
    relation: SemanticDuplicateRelation,
    action: SemanticDuplicateAction,
    existing_path: str,
) -> tuple[str, ...]:
    reason_codes: list[str] = [
        f"relation:{relation.value}",
        f"action:{action.value}",
    ]

    if _looks_like_external_vendor(existing_path):
        reason_codes.append("existing_path_is_external_vendor")

    if _has_container_boundary_marker(existing_path):
        reason_codes.append("container_or_adapter_boundary_marker_present")

    if _looks_like_legacy_or_existing(existing_path):
        reason_codes.append("existing_or_legacy_runtime_path_present")

    return tuple(reason_codes)


def _normalize_path(path: str | Path) -> str:
    if isinstance(path, Path):
        raw = path.as_posix()
    else:
        raw = str(path)

    normalized = raw.strip()

    if not normalized:
        raise ValueError("path must not be empty")

    if normalized == NO_EXISTING_MATCH_SENTINEL:
        return normalized

    if normalized.startswith("/"):
        raise ValueError("path must be project-relative, not absolute")

    if "\\" in normalized:
        raise ValueError("path must use POSIX-style '/' separators")

    if ".." in Path(normalized).parts:
        raise ValueError("path must not contain '..'")

    return normalized


def _has_container_boundary_marker(path: str) -> bool:
    lowered = path.lower()
    return any(marker in lowered for marker in CONTAINER_BOUNDARY_MARKERS)


def _looks_like_external_vendor(path: str) -> bool:
    return any(marker.lower() in path.lower() for marker in EXTERNAL_VENDOR_MARKERS)


def _looks_like_legacy_or_existing(path: str) -> bool:
    return any(path.startswith(root) for root in LEGACY_OR_EXISTING_ROOTS)


def _shares_top_runtime_area(target: str, existing: str) -> bool:
    target_parts = Path(target).parts
    existing_parts = Path(existing).parts

    if not target_parts or not existing_parts:
        return False

    return target_parts[0] == existing_parts[0]
