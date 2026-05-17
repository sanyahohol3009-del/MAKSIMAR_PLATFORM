from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Iterable, Mapping


ROOT_ARTIFACT_SEMANTIC_DUPLICATE_LAYER_ID = "ROOT_ARTIFACT_HYGIENE"
ROOT_ARTIFACT_SEMANTIC_DUPLICATE_BATCH_ID = "PHASE_0_BATCH_0_2"

NO_EXISTING_MATCH_SENTINEL = "__no_existing_match__"


class SemanticFamily(str, Enum):
    ROOT_ARTIFACT_HYGIENE = "root_artifact_hygiene"
    SECURITY = "security"
    DATA = "data"
    UPDATE_RECOVERY = "update_recovery"
    NETWORK_CONTAINERIZATION = "network_containerization"
    AI_ORCHESTRATION = "ai_orchestration"
    REGISTRY_ENROLLMENT = "registry_enrollment"
    OBSERVABILITY_DASHBOARD = "observability_dashboard"
    GOVERNANCE = "governance"
    EXECUTION = "execution"
    MEMORY = "memory"
    PRODUCT = "product"
    TESTING_TOOLING = "testing_tooling"
    UNKNOWN = "unknown"


class SemanticDuplicateRelation(str, Enum):
    SAME_PATH = "same_path"
    EXACT_NAME_MATCH = "exact_name_match"
    SEMANTIC_FAMILY_MATCH = "semantic_family_match"
    LEGACY_IMPLEMENTATION = "legacy_implementation"
    RELATED_RUNTIME_LAYER = "related_runtime_layer"
    CONTAINER_BOUNDARY_DUPLICATE = "container_boundary_duplicate"
    NO_RELATION = "no_relation"


class SemanticDuplicateAction(str, Enum):
    CREATE_NEW = "create_new"
    REUSE_IN_PLACE = "reuse_in_place"
    WRAP_AS_ADAPTER = "wrap_as_adapter"
    KEEP_LEGACY = "keep_legacy"
    MIGRATION_CANDIDATE = "migration_candidate"
    TRUE_DUPLICATE_RISK = "true_duplicate_risk"
    CONTAINER_BOUNDARY_DUPLICATE_ALLOWED = "container_boundary_duplicate_allowed"


class SemanticDuplicateRisk(str, Enum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(frozen=True, slots=True)
class SemanticDuplicateScanCandidate:
    target_path: str
    existing_path: str
    target_family: SemanticFamily
    existing_family: SemanticFamily
    duplicate_relation: SemanticDuplicateRelation
    action: SemanticDuplicateAction
    risk_level: SemanticDuplicateRisk
    reason_codes: tuple[str, ...] = field(default_factory=tuple)
    dashboard_safe: bool = True
    scan_readonly: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False
    auto_delete_allowed: bool = False
    auto_move_allowed: bool = False
    requires_approval: bool = False

    def __post_init__(self) -> None:
        _validate_relative_or_sentinel_path(
            self.target_path,
            field_name="target_path",
            allow_sentinel=False,
        )
        _validate_relative_or_sentinel_path(
            self.existing_path,
            field_name="existing_path",
            allow_sentinel=True,
        )

        if not isinstance(self.target_family, SemanticFamily):
            raise TypeError("target_family must be SemanticFamily")

        if not isinstance(self.existing_family, SemanticFamily):
            raise TypeError("existing_family must be SemanticFamily")

        if not isinstance(self.duplicate_relation, SemanticDuplicateRelation):
            raise TypeError("duplicate_relation must be SemanticDuplicateRelation")

        if not isinstance(self.action, SemanticDuplicateAction):
            raise TypeError("action must be SemanticDuplicateAction")

        if not isinstance(self.risk_level, SemanticDuplicateRisk):
            raise TypeError("risk_level must be SemanticDuplicateRisk")

        if not isinstance(self.reason_codes, tuple):
            raise TypeError("reason_codes must be a tuple")

        for reason_code in self.reason_codes:
            if not reason_code:
                raise ValueError("reason_codes must not contain empty values")

        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")

        if not self.scan_readonly:
            raise ValueError("scan_readonly must remain true")

        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")

        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")

        if self.auto_delete_allowed:
            raise ValueError("auto_delete_allowed must remain false")

        if self.auto_move_allowed:
            raise ValueError("auto_move_allowed must remain false")

        if self.action is SemanticDuplicateAction.TRUE_DUPLICATE_RISK:
            if self.risk_level is not SemanticDuplicateRisk.HIGH:
                raise ValueError("true_duplicate_risk action requires HIGH risk")

        if self.action is SemanticDuplicateAction.MIGRATION_CANDIDATE:
            if not self.requires_approval:
                raise ValueError("migration_candidate requires approval")

        if self.action is SemanticDuplicateAction.CONTAINER_BOUNDARY_DUPLICATE_ALLOWED:
            if self.duplicate_relation is not SemanticDuplicateRelation.CONTAINER_BOUNDARY_DUPLICATE:
                raise ValueError(
                    "container_boundary_duplicate_allowed requires "
                    "CONTAINER_BOUNDARY_DUPLICATE relation"
                )

        if self.action is SemanticDuplicateAction.CREATE_NEW:
            if self.existing_path != NO_EXISTING_MATCH_SENTINEL:
                raise ValueError("create_new action requires no-existing-match sentinel")
            if self.duplicate_relation is not SemanticDuplicateRelation.NO_RELATION:
                raise ValueError("create_new action requires NO_RELATION")

    def to_dict(self) -> dict[str, Any]:
        return {
            "target_path": self.target_path,
            "existing_path": self.existing_path,
            "target_family": self.target_family.value,
            "existing_family": self.existing_family.value,
            "duplicate_relation": self.duplicate_relation.value,
            "action": self.action.value,
            "risk_level": self.risk_level.value,
            "reason_codes": list(self.reason_codes),
            "dashboard_safe": self.dashboard_safe,
            "scan_readonly": self.scan_readonly,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "auto_delete_allowed": self.auto_delete_allowed,
            "auto_move_allowed": self.auto_move_allowed,
            "requires_approval": self.requires_approval,
        }


@dataclass(frozen=True, slots=True)
class SemanticDuplicateScanReadModel:
    scan_scope: str
    target_paths: tuple[str, ...]
    candidates: tuple[SemanticDuplicateScanCandidate, ...]
    layer_id: str = ROOT_ARTIFACT_SEMANTIC_DUPLICATE_LAYER_ID
    batch_id: str = ROOT_ARTIFACT_SEMANTIC_DUPLICATE_BATCH_ID
    status: str = "ready"
    readiness: float = 1.0
    scan_readonly: bool = True
    delete_allowed: bool = False
    move_allowed: bool = False
    dashboard_safe: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False
    warnings: tuple[str, ...] = field(default_factory=tuple)
    next_action: str = "proceed_to_root_report_builder"

    def __post_init__(self) -> None:
        if not self.scan_scope:
            raise ValueError("scan_scope must not be empty")

        if not isinstance(self.target_paths, tuple):
            raise TypeError("target_paths must be a tuple")

        if not self.target_paths:
            raise ValueError("target_paths must not be empty")

        for target_path in self.target_paths:
            _validate_relative_or_sentinel_path(
                target_path,
                field_name="target_paths",
                allow_sentinel=False,
            )

        if not isinstance(self.candidates, tuple):
            raise TypeError("candidates must be a tuple")

        for candidate in self.candidates:
            if not isinstance(candidate, SemanticDuplicateScanCandidate):
                raise TypeError(
                    "candidates must contain SemanticDuplicateScanCandidate instances"
                )

        if self.layer_id != ROOT_ARTIFACT_SEMANTIC_DUPLICATE_LAYER_ID:
            raise ValueError(
                f"layer_id must be {ROOT_ARTIFACT_SEMANTIC_DUPLICATE_LAYER_ID}"
            )

        if self.batch_id != ROOT_ARTIFACT_SEMANTIC_DUPLICATE_BATCH_ID:
            raise ValueError(
                f"batch_id must be {ROOT_ARTIFACT_SEMANTIC_DUPLICATE_BATCH_ID}"
            )

        if not 0.0 <= self.readiness <= 1.0:
            raise ValueError("readiness must be between 0.0 and 1.0")

        if not self.scan_readonly:
            raise ValueError("scan_readonly must remain true")

        if self.delete_allowed:
            raise ValueError("delete_allowed must remain false")

        if self.move_allowed:
            raise ValueError("move_allowed must remain false")

        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")

        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")

        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")

    @property
    def total_candidates(self) -> int:
        return len(self.candidates)

    @property
    def true_duplicate_risk_count(self) -> int:
        return self.count_by_action(SemanticDuplicateAction.TRUE_DUPLICATE_RISK)

    @property
    def container_boundary_duplicate_allowed_count(self) -> int:
        return self.count_by_action(
            SemanticDuplicateAction.CONTAINER_BOUNDARY_DUPLICATE_ALLOWED
        )

    @property
    def wrap_as_adapter_count(self) -> int:
        return self.count_by_action(SemanticDuplicateAction.WRAP_AS_ADAPTER)

    @property
    def keep_legacy_count(self) -> int:
        return self.count_by_action(SemanticDuplicateAction.KEEP_LEGACY)

    @property
    def migration_candidate_count(self) -> int:
        return self.count_by_action(SemanticDuplicateAction.MIGRATION_CANDIDATE)

    @property
    def create_new_count(self) -> int:
        return self.count_by_action(SemanticDuplicateAction.CREATE_NEW)

    @property
    def approval_required_count(self) -> int:
        return sum(1 for candidate in self.candidates if candidate.requires_approval)

    def count_by_action(self, action: SemanticDuplicateAction) -> int:
        return sum(1 for candidate in self.candidates if candidate.action is action)

    def to_dict(self) -> dict[str, Any]:
        return {
            "layer_id": self.layer_id,
            "batch_id": self.batch_id,
            "status": self.status,
            "readiness": self.readiness,
            "scan_scope": self.scan_scope,
            "target_paths": list(self.target_paths),
            "total_candidates": self.total_candidates,
            "true_duplicate_risk_count": self.true_duplicate_risk_count,
            "container_boundary_duplicate_allowed_count": (
                self.container_boundary_duplicate_allowed_count
            ),
            "wrap_as_adapter_count": self.wrap_as_adapter_count,
            "keep_legacy_count": self.keep_legacy_count,
            "migration_candidate_count": self.migration_candidate_count,
            "create_new_count": self.create_new_count,
            "approval_required_count": self.approval_required_count,
            "scan_readonly": self.scan_readonly,
            "delete_allowed": self.delete_allowed,
            "move_allowed": self.move_allowed,
            "dashboard_safe": self.dashboard_safe,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "warnings": list(self.warnings),
            "next_action": self.next_action,
            "candidates": [candidate.to_dict() for candidate in self.candidates],
        }

    @classmethod
    def from_candidates(
        cls,
        *,
        scan_scope: str,
        target_paths: Iterable[str],
        candidates: Iterable[SemanticDuplicateScanCandidate],
    ) -> SemanticDuplicateScanReadModel:
        target_tuple = tuple(target_paths)
        candidate_tuple = tuple(candidates)

        warnings: list[str] = []

        if any(
            candidate.action is SemanticDuplicateAction.TRUE_DUPLICATE_RISK
            for candidate in candidate_tuple
        ):
            warnings.append("true_duplicate_risk_present")

        if any(
            candidate.action is SemanticDuplicateAction.MIGRATION_CANDIDATE
            for candidate in candidate_tuple
        ):
            warnings.append("migration_candidates_present")

        if any(
            candidate.action is SemanticDuplicateAction.CONTAINER_BOUNDARY_DUPLICATE_ALLOWED
            for candidate in candidate_tuple
        ):
            warnings.append("container_boundary_duplicates_present")

        next_action = (
            "resolve_true_duplicate_or_migration_candidates"
            if any(warning in warnings for warning in (
                "true_duplicate_risk_present",
                "migration_candidates_present",
            ))
            else "proceed_to_root_report_builder"
        )

        return cls(
            scan_scope=scan_scope,
            target_paths=target_tuple,
            candidates=candidate_tuple,
            warnings=tuple(warnings),
            next_action=next_action,
        )


def semantic_duplicate_candidate_from_mapping(
    payload: Mapping[str, Any],
) -> SemanticDuplicateScanCandidate:
    return SemanticDuplicateScanCandidate(
        target_path=str(payload["target_path"]),
        existing_path=str(payload["existing_path"]),
        target_family=SemanticFamily(str(payload["target_family"])),
        existing_family=SemanticFamily(str(payload["existing_family"])),
        duplicate_relation=SemanticDuplicateRelation(str(payload["duplicate_relation"])),
        action=SemanticDuplicateAction(str(payload["action"])),
        risk_level=SemanticDuplicateRisk(str(payload["risk_level"])),
        reason_codes=tuple(str(item) for item in payload.get("reason_codes", [])),
        dashboard_safe=bool(payload.get("dashboard_safe", True)),
        scan_readonly=bool(payload.get("scan_readonly", True)),
        runtime_mutation_allowed=bool(payload.get("runtime_mutation_allowed", False)),
        canonical_write_allowed=bool(payload.get("canonical_write_allowed", False)),
        auto_delete_allowed=bool(payload.get("auto_delete_allowed", False)),
        auto_move_allowed=bool(payload.get("auto_move_allowed", False)),
        requires_approval=bool(payload.get("requires_approval", False)),
    )


def semantic_duplicate_read_model_from_mapping(
    payload: Mapping[str, Any],
) -> SemanticDuplicateScanReadModel:
    candidates_payload = payload.get("candidates", [])

    if not isinstance(candidates_payload, list):
        raise TypeError("payload['candidates'] must be a list")

    return SemanticDuplicateScanReadModel(
        scan_scope=str(payload["scan_scope"]),
        target_paths=tuple(str(item) for item in payload["target_paths"]),
        candidates=tuple(
            semantic_duplicate_candidate_from_mapping(item)
            for item in candidates_payload
            if isinstance(item, Mapping)
        ),
        status=str(payload.get("status", "ready")),
        readiness=float(payload.get("readiness", 1.0)),
        scan_readonly=bool(payload.get("scan_readonly", True)),
        delete_allowed=bool(payload.get("delete_allowed", False)),
        move_allowed=bool(payload.get("move_allowed", False)),
        dashboard_safe=bool(payload.get("dashboard_safe", True)),
        runtime_mutation_allowed=bool(payload.get("runtime_mutation_allowed", False)),
        canonical_write_allowed=bool(payload.get("canonical_write_allowed", False)),
        warnings=tuple(str(item) for item in payload.get("warnings", [])),
        next_action=str(payload.get("next_action", "proceed_to_root_report_builder")),
    )


def _validate_relative_or_sentinel_path(
    value: str,
    *,
    field_name: str,
    allow_sentinel: bool,
) -> None:
    if not value:
        raise ValueError(f"{field_name} must not be empty")

    if allow_sentinel and value == NO_EXISTING_MATCH_SENTINEL:
        return

    if value.startswith("/"):
        raise ValueError(f"{field_name} must be project-relative, not absolute")

    if "\\" in value:
        raise ValueError(f"{field_name} must use POSIX-style '/' separators")

    if ".." in Path(value).parts:
        raise ValueError(f"{field_name} must not contain '..'")
