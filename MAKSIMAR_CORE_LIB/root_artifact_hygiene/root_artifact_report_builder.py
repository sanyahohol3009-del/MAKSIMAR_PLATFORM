from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping

from MAKSIMAR_CORE_LIB.root_artifact_hygiene.artifact_classification_models import (
    ArtifactAllowedAction,
    ArtifactClassificationEntry,
    ArtifactClassificationReadModel,
    ArtifactLocationStatus,
)
from MAKSIMAR_CORE_LIB.root_artifact_hygiene.artifact_location_policy import (
    build_artifact_classification_read_model,
)
from MAKSIMAR_CORE_LIB.root_artifact_hygiene.root_surface_inventory_models import (
    RootArtifactCandidateKind,
    RootSurfaceInventoryReadModel,
    build_root_surface_inventory,
)


ROOT_ARTIFACT_REPORT_LAYER_ID = "ROOT_ARTIFACT_HYGIENE"
ROOT_ARTIFACT_REPORT_BATCH_ID = "PHASE_0_BATCH_0_3"


@dataclass(frozen=True, slots=True)
class RootArtifactReportItem:
    artifact_path: str
    artifact_class: str
    current_location: str
    expected_location: str
    location_status: str
    allowed_action: str
    correction_required: bool
    archive_candidate: bool
    requires_approval: bool
    risk_level: str
    reason_codes: tuple[str, ...] = field(default_factory=tuple)
    dashboard_safe: bool = True
    auto_delete_allowed: bool = False
    auto_move_allowed: bool = False

    def __post_init__(self) -> None:
        _validate_project_relative_path(self.artifact_path, "artifact_path")

        if not self.artifact_class:
            raise ValueError("artifact_class must not be empty")

        if not self.current_location:
            raise ValueError("current_location must not be empty")

        if not self.expected_location:
            raise ValueError("expected_location must not be empty")

        if not self.location_status:
            raise ValueError("location_status must not be empty")

        if not self.allowed_action:
            raise ValueError("allowed_action must not be empty")

        if not self.risk_level:
            raise ValueError("risk_level must not be empty")

        if not isinstance(self.reason_codes, tuple):
            raise TypeError("reason_codes must be a tuple")

        for reason_code in self.reason_codes:
            if not reason_code:
                raise ValueError("reason_codes must not contain empty values")

        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")

        if self.auto_delete_allowed:
            raise ValueError("auto_delete_allowed must remain false")

        if self.auto_move_allowed:
            raise ValueError("auto_move_allowed must remain false")

    def to_dict(self) -> dict[str, Any]:
        return {
            "artifact_path": self.artifact_path,
            "artifact_class": self.artifact_class,
            "current_location": self.current_location,
            "expected_location": self.expected_location,
            "location_status": self.location_status,
            "allowed_action": self.allowed_action,
            "correction_required": self.correction_required,
            "archive_candidate": self.archive_candidate,
            "requires_approval": self.requires_approval,
            "risk_level": self.risk_level,
            "reason_codes": list(self.reason_codes),
            "dashboard_safe": self.dashboard_safe,
            "auto_delete_allowed": self.auto_delete_allowed,
            "auto_move_allowed": self.auto_move_allowed,
        }


@dataclass(frozen=True, slots=True)
class RootArtifactReportReadModel:
    scanned_root: str
    items: tuple[RootArtifactReportItem, ...]
    layer_id: str = ROOT_ARTIFACT_REPORT_LAYER_ID
    batch_id: str = ROOT_ARTIFACT_REPORT_BATCH_ID
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
        if not self.scanned_root:
            raise ValueError("scanned_root must not be empty")

        if not isinstance(self.items, tuple):
            raise TypeError("items must be a tuple")

        for item in self.items:
            if not isinstance(item, RootArtifactReportItem):
                raise TypeError("items must contain RootArtifactReportItem instances")

        if self.layer_id != ROOT_ARTIFACT_REPORT_LAYER_ID:
            raise ValueError(f"layer_id must be {ROOT_ARTIFACT_REPORT_LAYER_ID}")

        if self.batch_id != ROOT_ARTIFACT_REPORT_BATCH_ID:
            raise ValueError(f"batch_id must be {ROOT_ARTIFACT_REPORT_BATCH_ID}")

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
    def source_count(self) -> int:
        return self.count_by_artifact_class(RootArtifactCandidateKind.SOURCE_CANDIDATE.value)

    @property
    def generated_count(self) -> int:
        return self.count_by_artifact_class(RootArtifactCandidateKind.GENERATED_CANDIDATE.value)

    @property
    def backup_count(self) -> int:
        return self.count_by_artifact_class(RootArtifactCandidateKind.BACKUP_CANDIDATE.value)

    @property
    def audit_report_count(self) -> int:
        return self.count_by_artifact_class(RootArtifactCandidateKind.AUDIT_CANDIDATE.value)

    @property
    def vendor_count(self) -> int:
        return self.count_by_artifact_class(RootArtifactCandidateKind.VENDOR_CANDIDATE.value)

    @property
    def unknown_count(self) -> int:
        return self.count_by_artifact_class(RootArtifactCandidateKind.UNKNOWN_CANDIDATE.value)

    @property
    def correction_required_count(self) -> int:
        return sum(1 for item in self.items if item.correction_required)

    @property
    def archive_candidate_count(self) -> int:
        return sum(1 for item in self.items if item.archive_candidate)

    @property
    def approval_required_count(self) -> int:
        return sum(1 for item in self.items if item.requires_approval)

    @property
    def correct_location_count(self) -> int:
        return self.count_by_location_status(ArtifactLocationStatus.CORRECT_LOCATION.value)

    @property
    def wrong_or_review_location_count(self) -> int:
        return sum(
            1
            for item in self.items
            if item.location_status
            in {
                ArtifactLocationStatus.WRONG_LOCATION.value,
                ArtifactLocationStatus.CANDIDATE_FOR_CORRECTION_PASS.value,
                ArtifactLocationStatus.LEGACY_LOCATION.value,
            }
        )

    def count_by_artifact_class(self, artifact_class: str) -> int:
        return sum(1 for item in self.items if item.artifact_class == artifact_class)

    def count_by_location_status(self, location_status: str) -> int:
        return sum(1 for item in self.items if item.location_status == location_status)

    def to_dict(self) -> dict[str, Any]:
        return {
            "layer_id": self.layer_id,
            "batch_id": self.batch_id,
            "status": self.status,
            "readiness": self.readiness,
            "scanned_root": self.scanned_root,
            "total_items": self.total_items,
            "source_count": self.source_count,
            "generated_count": self.generated_count,
            "backup_count": self.backup_count,
            "audit_report_count": self.audit_report_count,
            "vendor_count": self.vendor_count,
            "unknown_count": self.unknown_count,
            "correction_required_count": self.correction_required_count,
            "archive_candidate_count": self.archive_candidate_count,
            "approval_required_count": self.approval_required_count,
            "correct_location_count": self.correct_location_count,
            "wrong_or_review_location_count": self.wrong_or_review_location_count,
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
        scanned_root: str,
        items: Iterable[RootArtifactReportItem],
    ) -> RootArtifactReportReadModel:
        item_tuple = tuple(items)
        warnings: list[str] = []

        if any(item.correction_required for item in item_tuple):
            warnings.append("correction_required_items_present")

        if any(item.archive_candidate for item in item_tuple):
            warnings.append("archive_candidate_items_present")

        if any(item.requires_approval for item in item_tuple):
            warnings.append("approval_required_items_present")

        next_action = (
            "review_correction_and_archive_candidates"
            if warnings
            else "proceed_to_preview_and_documentation"
        )

        return cls(
            scanned_root=scanned_root,
            items=item_tuple,
            warnings=tuple(warnings),
            next_action=next_action,
        )


def build_root_artifact_report(
    classification_read_model: ArtifactClassificationReadModel,
) -> RootArtifactReportReadModel:
    return RootArtifactReportReadModel.from_items(
        scanned_root=classification_read_model.scanned_root,
        items=(
            root_artifact_report_item_from_classification(classification)
            for classification in classification_read_model.classifications
        ),
    )


def build_root_artifact_report_from_inventory(
    inventory_read_model: RootSurfaceInventoryReadModel,
) -> RootArtifactReportReadModel:
    classification_read_model = build_artifact_classification_read_model(inventory_read_model)
    return build_root_artifact_report(classification_read_model)


def build_root_artifact_report_from_project_root(
    project_root: str | Path,
    *,
    max_depth: int = 2,
) -> RootArtifactReportReadModel:
    inventory = build_root_surface_inventory(project_root, max_depth=max_depth)
    return build_root_artifact_report_from_inventory(inventory)


def root_artifact_report_item_from_classification(
    classification: ArtifactClassificationEntry,
) -> RootArtifactReportItem:
    return RootArtifactReportItem(
        artifact_path=classification.artifact_path,
        artifact_class=classification.artifact_class.value,
        current_location=classification.current_location,
        expected_location=classification.expected_location,
        location_status=classification.location_status.value,
        allowed_action=classification.allowed_action.value,
        correction_required=classification.correction_required,
        archive_candidate=classification.archive_candidate,
        requires_approval=classification.requires_approval,
        risk_level=classification.risk_level.value,
        reason_codes=classification.reason_codes,
        dashboard_safe=classification.dashboard_safe,
        auto_delete_allowed=classification.auto_delete_allowed,
        auto_move_allowed=classification.auto_move_allowed,
    )


def root_artifact_report_read_model_from_mapping(
    payload: Mapping[str, Any],
) -> RootArtifactReportReadModel:
    items_payload = payload.get("items", [])

    if not isinstance(items_payload, list):
        raise TypeError("payload['items'] must be a list")

    return RootArtifactReportReadModel(
        scanned_root=str(payload["scanned_root"]),
        items=tuple(
            root_artifact_report_item_from_mapping(item)
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


def root_artifact_report_item_from_mapping(
    payload: Mapping[str, Any],
) -> RootArtifactReportItem:
    return RootArtifactReportItem(
        artifact_path=str(payload["artifact_path"]),
        artifact_class=str(payload["artifact_class"]),
        current_location=str(payload["current_location"]),
        expected_location=str(payload["expected_location"]),
        location_status=str(payload["location_status"]),
        allowed_action=str(payload["allowed_action"]),
        correction_required=bool(payload["correction_required"]),
        archive_candidate=bool(payload["archive_candidate"]),
        requires_approval=bool(payload["requires_approval"]),
        risk_level=str(payload["risk_level"]),
        reason_codes=tuple(str(item) for item in payload.get("reason_codes", [])),
        dashboard_safe=bool(payload.get("dashboard_safe", True)),
        auto_delete_allowed=bool(payload.get("auto_delete_allowed", False)),
        auto_move_allowed=bool(payload.get("auto_move_allowed", False)),
    )


def _validate_project_relative_path(value: str, field_name: str) -> None:
    if not value:
        raise ValueError(f"{field_name} must not be empty")

    if value.startswith("/"):
        raise ValueError(f"{field_name} must be project-relative, not absolute")

    if "\\" in value:
        raise ValueError(f"{field_name} must use POSIX-style '/' separators")

    if ".." in Path(value).parts:
        raise ValueError(f"{field_name} must not contain '..'")
