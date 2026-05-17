from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Iterable, Mapping

from MAKSIMAR_CORE_LIB.root_artifact_hygiene.root_surface_inventory_models import (
    RootArtifactCandidateKind,
    RootSurfaceInventoryEntry,
    RootSurfacePathType,
)


ROOT_ARTIFACT_CLASSIFICATION_LAYER_ID = "ROOT_ARTIFACT_HYGIENE"
ROOT_ARTIFACT_CLASSIFICATION_BATCH_ID = "PHASE_0_BATCH_0_2"


class ArtifactLocationStatus(str, Enum):
    CORRECT_LOCATION = "correct_location"
    WRONG_LOCATION = "wrong_location"
    LEGACY_LOCATION = "legacy_location"
    TEMPORARY_GENERATED = "temporary_generated"
    BACKUP = "backup"
    AUDIT_REPORT = "audit_report"
    EXTERNAL_VENDOR = "external_vendor"
    CANDIDATE_FOR_CORRECTION_PASS = "candidate_for_correction_pass"


class ArtifactAllowedAction(str, Enum):
    USE_IN_PLACE = "use_in_place"
    REVIEW_ONLY = "review_only"
    ARCHIVE_LATER_WITH_APPROVAL = "archive_later_with_approval"
    MIGRATION_PASS_REQUIRED = "migration_pass_required"
    IGNORE_GENERATED = "ignore_generated"
    KEEP_VENDOR_SANDBOXED = "keep_vendor_sandboxed"


class ArtifactRiskLevel(str, Enum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(frozen=True, slots=True)
class ArtifactClassificationEntry:
    artifact_path: str
    artifact_class: RootArtifactCandidateKind
    current_location: str
    expected_location: str
    location_status: ArtifactLocationStatus
    risk_level: ArtifactRiskLevel
    allowed_action: ArtifactAllowedAction
    correction_required: bool
    archive_candidate: bool
    reason_codes: tuple[str, ...] = field(default_factory=tuple)
    auto_delete_allowed: bool = False
    auto_move_allowed: bool = False
    requires_approval: bool = False
    dashboard_safe: bool = True

    def __post_init__(self) -> None:
        if not self.artifact_path:
            raise ValueError("artifact_path must not be empty")

        if self.artifact_path.startswith("/"):
            raise ValueError("artifact_path must be project-relative, not absolute")

        if "\\" in self.artifact_path:
            raise ValueError("artifact_path must use POSIX-style '/' separators")

        if ".." in Path(self.artifact_path).parts:
            raise ValueError("artifact_path must not contain '..'")

        if not self.current_location:
            raise ValueError("current_location must not be empty")

        if not self.expected_location:
            raise ValueError("expected_location must not be empty")

        if not isinstance(self.artifact_class, RootArtifactCandidateKind):
            raise TypeError("artifact_class must be RootArtifactCandidateKind")

        if not isinstance(self.location_status, ArtifactLocationStatus):
            raise TypeError("location_status must be ArtifactLocationStatus")

        if not isinstance(self.risk_level, ArtifactRiskLevel):
            raise TypeError("risk_level must be ArtifactRiskLevel")

        if not isinstance(self.allowed_action, ArtifactAllowedAction):
            raise TypeError("allowed_action must be ArtifactAllowedAction")

        if not isinstance(self.reason_codes, tuple):
            raise TypeError("reason_codes must be a tuple")

        for reason_code in self.reason_codes:
            if not reason_code:
                raise ValueError("reason_codes must not contain empty values")

        if self.auto_delete_allowed:
            raise ValueError("auto_delete_allowed must always remain false")

        if self.auto_move_allowed:
            raise ValueError("auto_move_allowed must always remain false")

        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must always remain true")

        if self.allowed_action is ArtifactAllowedAction.MIGRATION_PASS_REQUIRED and not self.correction_required:
            raise ValueError("migration pass action requires correction_required=True")

        if self.location_status is ArtifactLocationStatus.CANDIDATE_FOR_CORRECTION_PASS and not self.correction_required:
            raise ValueError("candidate_for_correction_pass requires correction_required=True")

        if self.allowed_action is ArtifactAllowedAction.ARCHIVE_LATER_WITH_APPROVAL and not self.requires_approval:
            raise ValueError("archive action requires explicit approval")

    def to_dict(self) -> dict[str, Any]:
        return {
            "artifact_path": self.artifact_path,
            "artifact_class": self.artifact_class.value,
            "current_location": self.current_location,
            "expected_location": self.expected_location,
            "location_status": self.location_status.value,
            "risk_level": self.risk_level.value,
            "allowed_action": self.allowed_action.value,
            "correction_required": self.correction_required,
            "archive_candidate": self.archive_candidate,
            "reason_codes": list(self.reason_codes),
            "auto_delete_allowed": self.auto_delete_allowed,
            "auto_move_allowed": self.auto_move_allowed,
            "requires_approval": self.requires_approval,
            "dashboard_safe": self.dashboard_safe,
        }


@dataclass(frozen=True, slots=True)
class ArtifactClassificationReadModel:
    scanned_root: str
    classifications: tuple[ArtifactClassificationEntry, ...]
    layer_id: str = ROOT_ARTIFACT_CLASSIFICATION_LAYER_ID
    batch_id: str = ROOT_ARTIFACT_CLASSIFICATION_BATCH_ID
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
        if not self.scanned_root:
            raise ValueError("scanned_root must not be empty")

        if not isinstance(self.classifications, tuple):
            raise TypeError("classifications must be a tuple")

        for classification in self.classifications:
            if not isinstance(classification, ArtifactClassificationEntry):
                raise TypeError("classifications must contain ArtifactClassificationEntry instances")

        if self.layer_id != ROOT_ARTIFACT_CLASSIFICATION_LAYER_ID:
            raise ValueError(f"layer_id must be {ROOT_ARTIFACT_CLASSIFICATION_LAYER_ID}")

        if self.batch_id != ROOT_ARTIFACT_CLASSIFICATION_BATCH_ID:
            raise ValueError(f"batch_id must be {ROOT_ARTIFACT_CLASSIFICATION_BATCH_ID}")

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
    def total_classifications(self) -> int:
        return len(self.classifications)

    @property
    def correct_location_count(self) -> int:
        return self.count_by_status(ArtifactLocationStatus.CORRECT_LOCATION)

    @property
    def wrong_location_count(self) -> int:
        return self.count_by_status(ArtifactLocationStatus.WRONG_LOCATION)

    @property
    def legacy_location_count(self) -> int:
        return self.count_by_status(ArtifactLocationStatus.LEGACY_LOCATION)

    @property
    def generated_count(self) -> int:
        return self.count_by_status(ArtifactLocationStatus.TEMPORARY_GENERATED)

    @property
    def backup_count(self) -> int:
        return self.count_by_status(ArtifactLocationStatus.BACKUP)

    @property
    def audit_report_count(self) -> int:
        return self.count_by_status(ArtifactLocationStatus.AUDIT_REPORT)

    @property
    def external_vendor_count(self) -> int:
        return self.count_by_status(ArtifactLocationStatus.EXTERNAL_VENDOR)

    @property
    def correction_required_count(self) -> int:
        return sum(1 for item in self.classifications if item.correction_required)

    @property
    def archive_candidate_count(self) -> int:
        return sum(1 for item in self.classifications if item.archive_candidate)

    @property
    def approval_required_count(self) -> int:
        return sum(1 for item in self.classifications if item.requires_approval)

    def count_by_status(self, status: ArtifactLocationStatus) -> int:
        return sum(1 for item in self.classifications if item.location_status is status)

    def to_dict(self) -> dict[str, Any]:
        return {
            "layer_id": self.layer_id,
            "batch_id": self.batch_id,
            "status": self.status,
            "readiness": self.readiness,
            "scanned_root": self.scanned_root,
            "total_classifications": self.total_classifications,
            "correct_location_count": self.correct_location_count,
            "wrong_location_count": self.wrong_location_count,
            "legacy_location_count": self.legacy_location_count,
            "generated_count": self.generated_count,
            "backup_count": self.backup_count,
            "audit_report_count": self.audit_report_count,
            "external_vendor_count": self.external_vendor_count,
            "correction_required_count": self.correction_required_count,
            "archive_candidate_count": self.archive_candidate_count,
            "approval_required_count": self.approval_required_count,
            "scan_readonly": self.scan_readonly,
            "delete_allowed": self.delete_allowed,
            "move_allowed": self.move_allowed,
            "dashboard_safe": self.dashboard_safe,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "warnings": list(self.warnings),
            "next_action": self.next_action,
            "classifications": [item.to_dict() for item in self.classifications],
        }

    @classmethod
    def from_entries(
        cls,
        *,
        scanned_root: str,
        classifications: Iterable[ArtifactClassificationEntry],
    ) -> ArtifactClassificationReadModel:
        classification_tuple = tuple(classifications)

        warnings: list[str] = []

        if any(item.correction_required for item in classification_tuple):
            warnings.append("correction_required_candidates_present")

        if any(item.archive_candidate for item in classification_tuple):
            warnings.append("archive_candidates_present")

        if any(item.location_status is ArtifactLocationStatus.WRONG_LOCATION for item in classification_tuple):
            warnings.append("wrong_location_candidates_present")

        if any(item.location_status is ArtifactLocationStatus.EXTERNAL_VENDOR for item in classification_tuple):
            warnings.append("external_vendor_candidates_present")

        next_action = (
            "prepare_correction_or_archive_review"
            if warnings
            else "proceed_to_root_report_builder"
        )

        return cls(
            scanned_root=scanned_root,
            classifications=classification_tuple,
            warnings=tuple(warnings),
            next_action=next_action,
        )


def artifact_classification_entry_from_mapping(
    payload: Mapping[str, Any],
) -> ArtifactClassificationEntry:
    return ArtifactClassificationEntry(
        artifact_path=str(payload["artifact_path"]),
        artifact_class=RootArtifactCandidateKind(str(payload["artifact_class"])),
        current_location=str(payload["current_location"]),
        expected_location=str(payload["expected_location"]),
        location_status=ArtifactLocationStatus(str(payload["location_status"])),
        risk_level=ArtifactRiskLevel(str(payload["risk_level"])),
        allowed_action=ArtifactAllowedAction(str(payload["allowed_action"])),
        correction_required=bool(payload["correction_required"]),
        archive_candidate=bool(payload["archive_candidate"]),
        reason_codes=tuple(str(item) for item in payload.get("reason_codes", [])),
        auto_delete_allowed=bool(payload.get("auto_delete_allowed", False)),
        auto_move_allowed=bool(payload.get("auto_move_allowed", False)),
        requires_approval=bool(payload.get("requires_approval", False)),
        dashboard_safe=bool(payload.get("dashboard_safe", True)),
    )


def artifact_classification_read_model_from_mapping(
    payload: Mapping[str, Any],
) -> ArtifactClassificationReadModel:
    classifications_payload = payload.get("classifications", [])

    if not isinstance(classifications_payload, list):
        raise TypeError("payload['classifications'] must be a list")

    return ArtifactClassificationReadModel(
        scanned_root=str(payload["scanned_root"]),
        classifications=tuple(
            artifact_classification_entry_from_mapping(item)
            for item in classifications_payload
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


def entry_from_inventory_candidate(
    entry: RootSurfaceInventoryEntry,
    *,
    expected_location: str,
    location_status: ArtifactLocationStatus,
    risk_level: ArtifactRiskLevel,
    allowed_action: ArtifactAllowedAction,
    correction_required: bool = False,
    archive_candidate: bool = False,
    requires_approval: bool = False,
    extra_reason_codes: Iterable[str] = (),
) -> ArtifactClassificationEntry:
    reason_codes = tuple(entry.reason_codes) + tuple(extra_reason_codes)

    return ArtifactClassificationEntry(
        artifact_path=entry.relative_path,
        artifact_class=entry.candidate_kind,
        current_location=_top_level_location(entry.relative_path),
        expected_location=expected_location,
        location_status=location_status,
        risk_level=risk_level,
        allowed_action=allowed_action,
        correction_required=correction_required,
        archive_candidate=archive_candidate,
        reason_codes=reason_codes,
        auto_delete_allowed=False,
        auto_move_allowed=False,
        requires_approval=requires_approval,
        dashboard_safe=True,
    )


def _top_level_location(relative_path: str) -> str:
    parts = Path(relative_path).parts
    if not parts:
        return "."
    return parts[0]
