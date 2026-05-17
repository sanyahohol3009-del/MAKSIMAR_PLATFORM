from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping

from MAKSIMAR_CORE_LIB.root_artifact_hygiene.semantic_duplicate_scan_models import (
    SemanticDuplicateAction,
    SemanticDuplicateRisk,
    SemanticDuplicateScanCandidate,
    SemanticDuplicateScanReadModel,
)
from MAKSIMAR_CORE_LIB.root_artifact_hygiene.semantic_duplicate_scan_policy import (
    build_semantic_duplicate_scan_read_model,
)


ROOT_ARTIFACT_SEMANTIC_DUPLICATE_REPORT_LAYER_ID = "ROOT_ARTIFACT_HYGIENE"
ROOT_ARTIFACT_SEMANTIC_DUPLICATE_REPORT_BATCH_ID = "PHASE_0_BATCH_0_3"


@dataclass(frozen=True, slots=True)
class SemanticDuplicateReportItem:
    target_path: str
    existing_path: str
    target_family: str
    existing_family: str
    duplicate_relation: str
    action: str
    risk_level: str
    requires_approval: bool
    reason_codes: tuple[str, ...] = field(default_factory=tuple)
    dashboard_safe: bool = True
    scan_readonly: bool = True
    auto_delete_allowed: bool = False
    auto_move_allowed: bool = False
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False

    def __post_init__(self) -> None:
        _validate_path_like(self.target_path, "target_path", allow_sentinel=False)
        _validate_path_like(self.existing_path, "existing_path", allow_sentinel=True)

        for field_name, value in (
            ("target_family", self.target_family),
            ("existing_family", self.existing_family),
            ("duplicate_relation", self.duplicate_relation),
            ("action", self.action),
            ("risk_level", self.risk_level),
        ):
            if not value:
                raise ValueError(f"{field_name} must not be empty")

        if not isinstance(self.reason_codes, tuple):
            raise TypeError("reason_codes must be a tuple")

        for reason_code in self.reason_codes:
            if not reason_code:
                raise ValueError("reason_codes must not contain empty values")

        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")

        if not self.scan_readonly:
            raise ValueError("scan_readonly must remain true")

        if self.auto_delete_allowed:
            raise ValueError("auto_delete_allowed must remain false")

        if self.auto_move_allowed:
            raise ValueError("auto_move_allowed must remain false")

        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")

        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")

    def to_dict(self) -> dict[str, Any]:
        return {
            "target_path": self.target_path,
            "existing_path": self.existing_path,
            "target_family": self.target_family,
            "existing_family": self.existing_family,
            "duplicate_relation": self.duplicate_relation,
            "action": self.action,
            "risk_level": self.risk_level,
            "requires_approval": self.requires_approval,
            "reason_codes": list(self.reason_codes),
            "dashboard_safe": self.dashboard_safe,
            "scan_readonly": self.scan_readonly,
            "auto_delete_allowed": self.auto_delete_allowed,
            "auto_move_allowed": self.auto_move_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
        }


@dataclass(frozen=True, slots=True)
class SemanticDuplicateReportReadModel:
    scan_scope: str
    target_paths: tuple[str, ...]
    items: tuple[SemanticDuplicateReportItem, ...]
    layer_id: str = ROOT_ARTIFACT_SEMANTIC_DUPLICATE_REPORT_LAYER_ID
    batch_id: str = ROOT_ARTIFACT_SEMANTIC_DUPLICATE_REPORT_BATCH_ID
    status: str = "ready"
    readiness: float = 1.0
    scan_readonly: bool = True
    delete_allowed: bool = False
    move_allowed: bool = False
    dashboard_safe: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False
    warnings: tuple[str, ...] = field(default_factory=tuple)
    next_action: str = "proceed_to_preview_and_documentation"

    def __post_init__(self) -> None:
        if not self.scan_scope:
            raise ValueError("scan_scope must not be empty")

        if not isinstance(self.target_paths, tuple):
            raise TypeError("target_paths must be a tuple")

        if not self.target_paths:
            raise ValueError("target_paths must not be empty")

        for target_path in self.target_paths:
            _validate_path_like(target_path, "target_paths", allow_sentinel=False)

        if not isinstance(self.items, tuple):
            raise TypeError("items must be a tuple")

        for item in self.items:
            if not isinstance(item, SemanticDuplicateReportItem):
                raise TypeError("items must contain SemanticDuplicateReportItem instances")

        if self.layer_id != ROOT_ARTIFACT_SEMANTIC_DUPLICATE_REPORT_LAYER_ID:
            raise ValueError(
                f"layer_id must be {ROOT_ARTIFACT_SEMANTIC_DUPLICATE_REPORT_LAYER_ID}"
            )

        if self.batch_id != ROOT_ARTIFACT_SEMANTIC_DUPLICATE_REPORT_BATCH_ID:
            raise ValueError(
                f"batch_id must be {ROOT_ARTIFACT_SEMANTIC_DUPLICATE_REPORT_BATCH_ID}"
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
    def total_items(self) -> int:
        return len(self.items)

    @property
    def true_duplicate_risk_count(self) -> int:
        return self.count_by_action(SemanticDuplicateAction.TRUE_DUPLICATE_RISK.value)

    @property
    def container_boundary_duplicate_allowed_count(self) -> int:
        return self.count_by_action(
            SemanticDuplicateAction.CONTAINER_BOUNDARY_DUPLICATE_ALLOWED.value
        )

    @property
    def wrap_as_adapter_count(self) -> int:
        return self.count_by_action(SemanticDuplicateAction.WRAP_AS_ADAPTER.value)

    @property
    def keep_legacy_count(self) -> int:
        return self.count_by_action(SemanticDuplicateAction.KEEP_LEGACY.value)

    @property
    def migration_candidate_count(self) -> int:
        return self.count_by_action(SemanticDuplicateAction.MIGRATION_CANDIDATE.value)

    @property
    def create_new_count(self) -> int:
        return self.count_by_action(SemanticDuplicateAction.CREATE_NEW.value)

    @property
    def approval_required_count(self) -> int:
        return sum(1 for item in self.items if item.requires_approval)

    @property
    def high_risk_count(self) -> int:
        return sum(1 for item in self.items if item.risk_level == SemanticDuplicateRisk.HIGH.value)

    def count_by_action(self, action: str) -> int:
        return sum(1 for item in self.items if item.action == action)

    def to_dict(self) -> dict[str, Any]:
        return {
            "layer_id": self.layer_id,
            "batch_id": self.batch_id,
            "status": self.status,
            "readiness": self.readiness,
            "scan_scope": self.scan_scope,
            "target_paths": list(self.target_paths),
            "total_items": self.total_items,
            "true_duplicate_risk_count": self.true_duplicate_risk_count,
            "container_boundary_duplicate_allowed_count": (
                self.container_boundary_duplicate_allowed_count
            ),
            "wrap_as_adapter_count": self.wrap_as_adapter_count,
            "keep_legacy_count": self.keep_legacy_count,
            "migration_candidate_count": self.migration_candidate_count,
            "create_new_count": self.create_new_count,
            "approval_required_count": self.approval_required_count,
            "high_risk_count": self.high_risk_count,
            "scan_readonly": self.scan_readonly,
            "delete_allowed": self.delete_allowed,
            "move_allowed": self.move_allowed,
            "dashboard_safe": self.dashboard_safe,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "warnings": list(self.warnings),
            "next_action": self.next_action,
            "items": [item.to_dict() for item in self.items],
        }

    @classmethod
    def from_items(
        cls,
        *,
        scan_scope: str,
        target_paths: Iterable[str],
        items: Iterable[SemanticDuplicateReportItem],
    ) -> SemanticDuplicateReportReadModel:
        target_tuple = tuple(target_paths)
        item_tuple = tuple(items)
        warnings: list[str] = []

        if any(item.action == SemanticDuplicateAction.TRUE_DUPLICATE_RISK.value for item in item_tuple):
            warnings.append("true_duplicate_risk_present")

        if any(item.action == SemanticDuplicateAction.MIGRATION_CANDIDATE.value for item in item_tuple):
            warnings.append("migration_candidates_present")

        if any(
            item.action == SemanticDuplicateAction.CONTAINER_BOUNDARY_DUPLICATE_ALLOWED.value
            for item in item_tuple
        ):
            warnings.append("container_boundary_duplicates_present")

        next_action = (
            "resolve_true_duplicate_or_migration_candidates"
            if any(
                warning in warnings
                for warning in (
                    "true_duplicate_risk_present",
                    "migration_candidates_present",
                )
            )
            else "proceed_to_preview_and_documentation"
        )

        return cls(
            scan_scope=scan_scope,
            target_paths=target_tuple,
            items=item_tuple,
            warnings=tuple(warnings),
            next_action=next_action,
        )


def build_semantic_duplicate_report(
    scan_read_model: SemanticDuplicateScanReadModel,
) -> SemanticDuplicateReportReadModel:
    return SemanticDuplicateReportReadModel.from_items(
        scan_scope=scan_read_model.scan_scope,
        target_paths=scan_read_model.target_paths,
        items=(
            semantic_duplicate_report_item_from_candidate(candidate)
            for candidate in scan_read_model.candidates
        ),
    )


def build_semantic_duplicate_report_from_paths(
    *,
    target_paths: Iterable[str | Path],
    existing_paths: Iterable[str | Path],
    scan_scope: str = "project",
) -> SemanticDuplicateReportReadModel:
    scan_read_model = build_semantic_duplicate_scan_read_model(
        target_paths=target_paths,
        existing_paths=existing_paths,
        scan_scope=scan_scope,
    )
    return build_semantic_duplicate_report(scan_read_model)


def semantic_duplicate_report_item_from_candidate(
    candidate: SemanticDuplicateScanCandidate,
) -> SemanticDuplicateReportItem:
    return SemanticDuplicateReportItem(
        target_path=candidate.target_path,
        existing_path=candidate.existing_path,
        target_family=candidate.target_family.value,
        existing_family=candidate.existing_family.value,
        duplicate_relation=candidate.duplicate_relation.value,
        action=candidate.action.value,
        risk_level=candidate.risk_level.value,
        requires_approval=candidate.requires_approval,
        reason_codes=candidate.reason_codes,
        dashboard_safe=candidate.dashboard_safe,
        scan_readonly=candidate.scan_readonly,
        auto_delete_allowed=candidate.auto_delete_allowed,
        auto_move_allowed=candidate.auto_move_allowed,
        runtime_mutation_allowed=candidate.runtime_mutation_allowed,
        canonical_write_allowed=candidate.canonical_write_allowed,
    )


def semantic_duplicate_report_read_model_from_mapping(
    payload: Mapping[str, Any],
) -> SemanticDuplicateReportReadModel:
    items_payload = payload.get("items", [])

    if not isinstance(items_payload, list):
        raise TypeError("payload['items'] must be a list")

    return SemanticDuplicateReportReadModel(
        scan_scope=str(payload["scan_scope"]),
        target_paths=tuple(str(item) for item in payload["target_paths"]),
        items=tuple(
            semantic_duplicate_report_item_from_mapping(item)
            for item in items_payload
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
        next_action=str(payload.get("next_action", "proceed_to_preview_and_documentation")),
    )


def semantic_duplicate_report_item_from_mapping(
    payload: Mapping[str, Any],
) -> SemanticDuplicateReportItem:
    return SemanticDuplicateReportItem(
        target_path=str(payload["target_path"]),
        existing_path=str(payload["existing_path"]),
        target_family=str(payload["target_family"]),
        existing_family=str(payload["existing_family"]),
        duplicate_relation=str(payload["duplicate_relation"]),
        action=str(payload["action"]),
        risk_level=str(payload["risk_level"]),
        requires_approval=bool(payload["requires_approval"]),
        reason_codes=tuple(str(item) for item in payload.get("reason_codes", [])),
        dashboard_safe=bool(payload.get("dashboard_safe", True)),
        scan_readonly=bool(payload.get("scan_readonly", True)),
        auto_delete_allowed=bool(payload.get("auto_delete_allowed", False)),
        auto_move_allowed=bool(payload.get("auto_move_allowed", False)),
        runtime_mutation_allowed=bool(payload.get("runtime_mutation_allowed", False)),
        canonical_write_allowed=bool(payload.get("canonical_write_allowed", False)),
    )


def _validate_path_like(
    value: str,
    field_name: str,
    *,
    allow_sentinel: bool,
) -> None:
    if not value:
        raise ValueError(f"{field_name} must not be empty")

    if allow_sentinel and value == "__no_existing_match__":
        return

    if value.startswith("/"):
        raise ValueError(f"{field_name} must be project-relative, not absolute")

    if "\\" in value:
        raise ValueError(f"{field_name} must use POSIX-style '/' separators")

    if ".." in Path(value).parts:
        raise ValueError(f"{field_name} must not contain '..'")
