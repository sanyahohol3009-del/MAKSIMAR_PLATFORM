from __future__ import annotations

from pathlib import Path
from typing import Iterable

from MAKSIMAR_CORE_LIB.root_artifact_hygiene.artifact_classification_models import (
    ArtifactAllowedAction,
    ArtifactClassificationEntry,
    ArtifactClassificationReadModel,
    ArtifactLocationStatus,
    ArtifactRiskLevel,
    entry_from_inventory_candidate,
)
from MAKSIMAR_CORE_LIB.root_artifact_hygiene.root_surface_inventory_models import (
    RootArtifactCandidateKind,
    RootSurfaceInventoryEntry,
    RootSurfaceInventoryReadModel,
)


CANONICAL_SOURCE_ROOTS: frozenset[str] = frozenset(
    {
        "ACTION_LIBRARY",
        "AI_SERVICES",
        "BOOT",
        "CAD_3D_CAM_LAYER",
        "CONTROL_PLANE",
        "CORE_ROOT",
        "DATA_PLANE",
        "EVENT_BUS",
        "MAKSIMAR_CORE",
        "MAKSIMAR_CORE_LIB",
        "MAKSIMAR_SERVER",
        "OBSERVABILITY_LAYER",
        "PRODUCTS",
        "RUNTIME",
        "SAFETY_FOUNDATION",
        "SANDBOX",
        "SUPERVISOR",
        "TESTS",
        "UI_LAYER",
        "VPN_LAYER",
        "docs",
        "frontend",
        "requirements",
        "runtime_history_store",
        "runtime_imports",
        "scripts",
        "tests",
        "tools",
    }
)

GENERATED_RUNTIME_ROOTS: frozenset[str] = frozenset(
    {
        ".pytest_cache",
        "_dashboard_audit_pack",
        "_display_restore_audit",
        "_frontend_graveyard",
        "build",
        "dist",
        "htmlcov",
        "node_modules",
        "project_audit",
    }
)

AUDIT_ARCHIVE_ROOT = "docs/archive/audits"
REPORT_ARCHIVE_ROOT = "docs/archive/reports"
BACKUP_ARCHIVE_ROOT = "docs/archive/backups"
HISTORY_TRACK_ARCHIVE_ROOT = "docs/archive/history_track"
VENDOR_EXPECTED_ROOT = "EXTERNAL_BACKENDS"


def classify_inventory_entry_location(
    entry: RootSurfaceInventoryEntry,
) -> ArtifactClassificationEntry:
    top_level = _top_level(entry.relative_path)

    if entry.candidate_kind is RootArtifactCandidateKind.SOURCE_CANDIDATE:
        if top_level in CANONICAL_SOURCE_ROOTS or entry.relative_path in {"README.md", "pytest.ini", "Makefile"}:
            return entry_from_inventory_candidate(
                entry,
                expected_location=top_level,
                location_status=ArtifactLocationStatus.CORRECT_LOCATION,
                risk_level=ArtifactRiskLevel.NONE,
                allowed_action=ArtifactAllowedAction.USE_IN_PLACE,
                extra_reason_codes=("source_candidate_in_canonical_or_known_root",),
            )

        return entry_from_inventory_candidate(
            entry,
            expected_location="canonical_source_layer",
            location_status=ArtifactLocationStatus.CANDIDATE_FOR_CORRECTION_PASS,
            risk_level=ArtifactRiskLevel.MEDIUM,
            allowed_action=ArtifactAllowedAction.MIGRATION_PASS_REQUIRED,
            correction_required=True,
            requires_approval=True,
            extra_reason_codes=("source_candidate_outside_canonical_root",),
        )

    if entry.candidate_kind is RootArtifactCandidateKind.GENERATED_CANDIDATE:
        return entry_from_inventory_candidate(
            entry,
            expected_location=top_level if top_level in GENERATED_RUNTIME_ROOTS else "generated_runtime_or_audit_area",
            location_status=ArtifactLocationStatus.TEMPORARY_GENERATED,
            risk_level=ArtifactRiskLevel.LOW,
            allowed_action=ArtifactAllowedAction.IGNORE_GENERATED,
            extra_reason_codes=("generated_artifact_no_commit_no_delete_in_batch",),
        )

    if entry.candidate_kind is RootArtifactCandidateKind.BACKUP_CANDIDATE:
        return entry_from_inventory_candidate(
            entry,
            expected_location=BACKUP_ARCHIVE_ROOT,
            location_status=ArtifactLocationStatus.BACKUP,
            risk_level=ArtifactRiskLevel.LOW,
            allowed_action=ArtifactAllowedAction.ARCHIVE_LATER_WITH_APPROVAL,
            archive_candidate=True,
            requires_approval=True,
            extra_reason_codes=("backup_requires_archive_pass",),
        )

    if entry.candidate_kind is RootArtifactCandidateKind.AUDIT_CANDIDATE:
        return entry_from_inventory_candidate(
            entry,
            expected_location=_expected_audit_or_report_archive(entry.relative_path),
            location_status=ArtifactLocationStatus.AUDIT_REPORT,
            risk_level=ArtifactRiskLevel.LOW,
            allowed_action=ArtifactAllowedAction.ARCHIVE_LATER_WITH_APPROVAL,
            archive_candidate=True,
            requires_approval=True,
            extra_reason_codes=("audit_or_report_requires_archive_pass",),
        )

    if entry.candidate_kind is RootArtifactCandidateKind.VENDOR_CANDIDATE:
        return entry_from_inventory_candidate(
            entry,
            expected_location=VENDOR_EXPECTED_ROOT,
            location_status=ArtifactLocationStatus.EXTERNAL_VENDOR,
            risk_level=ArtifactRiskLevel.MEDIUM,
            allowed_action=ArtifactAllowedAction.KEEP_VENDOR_SANDBOXED,
            extra_reason_codes=("vendor_artifact_must_remain_sandboxed",),
        )

    return entry_from_inventory_candidate(
        entry,
        expected_location="manual_review_required",
        location_status=ArtifactLocationStatus.CANDIDATE_FOR_CORRECTION_PASS,
        risk_level=ArtifactRiskLevel.MEDIUM,
        allowed_action=ArtifactAllowedAction.MIGRATION_PASS_REQUIRED,
        correction_required=True,
        requires_approval=True,
        extra_reason_codes=("unknown_candidate_requires_manual_location_review",),
    )


def build_artifact_classification_read_model(
    inventory: RootSurfaceInventoryReadModel,
) -> ArtifactClassificationReadModel:
    classifications = tuple(
        classify_inventory_entry_location(entry)
        for entry in inventory.entries
    )

    return ArtifactClassificationReadModel.from_entries(
        scanned_root=inventory.scanned_root,
        classifications=classifications,
    )


def classify_inventory_entries(
    entries: Iterable[RootSurfaceInventoryEntry],
    *,
    scanned_root: str,
) -> ArtifactClassificationReadModel:
    return ArtifactClassificationReadModel.from_entries(
        scanned_root=scanned_root,
        classifications=(
            classify_inventory_entry_location(entry)
            for entry in entries
        ),
    )


def _top_level(relative_path: str) -> str:
    parts = Path(relative_path).parts
    if not parts:
        return "."
    return parts[0]


def _expected_audit_or_report_archive(relative_path: str) -> str:
    lower_name = Path(relative_path).name.lower()

    if lower_name.startswith("history_track_"):
        return HISTORY_TRACK_ARCHIVE_ROOT

    if "coverage" in lower_name or "pytest" in lower_name or "report" in lower_name:
        return REPORT_ARCHIVE_ROOT

    return AUDIT_ARCHIVE_ROOT
