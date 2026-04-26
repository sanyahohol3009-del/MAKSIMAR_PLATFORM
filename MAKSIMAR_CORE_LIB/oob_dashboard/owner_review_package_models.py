from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


OwnerReviewPackageState = Literal[
    "owner_review_package_ready",
]

OwnerReviewPackageClass = Literal[
    "read_only_review_package",
    "approval_bound_review_package",
]

OwnerReviewEvidenceMode = Literal[
    "preview_and_audit_evidence",
    "preview_approval_and_audit_evidence",
]

ALL_OWNER_REVIEW_PACKAGE_STATES: tuple[OwnerReviewPackageState, ...] = (
    "owner_review_package_ready",
)

ALL_OWNER_REVIEW_PACKAGE_CLASSES: tuple[OwnerReviewPackageClass, ...] = (
    "read_only_review_package",
    "approval_bound_review_package",
)

ALL_OWNER_REVIEW_EVIDENCE_MODES: tuple[OwnerReviewEvidenceMode, ...] = (
    "preview_and_audit_evidence",
    "preview_approval_and_audit_evidence",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class OwnerReviewPackageEntry:
    """Canonical owner review package entry."""

    owner_review_package_id: str
    operator_intent_id: str
    panel_id: str
    workspace_id: str
    owner_review_package_state: OwnerReviewPackageState
    owner_review_package_class: OwnerReviewPackageClass
    owner_review_evidence_mode: OwnerReviewEvidenceMode
    approval_required: bool
    handoff_ready: bool
    audit_visible: bool
    operator_visible: bool
    trace_id: str
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.owner_review_package_id, "owner_review_package_id")
        _require_non_empty(self.operator_intent_id, "operator_intent_id")
        _require_non_empty(self.panel_id, "panel_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.trace_id, "trace_id")
        _require_non_empty(self.description, "description")

        if self.owner_review_package_state not in ALL_OWNER_REVIEW_PACKAGE_STATES:
            raise ValueError(
                "owner_review_package_state must be one of "
                f"{ALL_OWNER_REVIEW_PACKAGE_STATES}, got {self.owner_review_package_state!r}."
            )

        if self.owner_review_package_class not in ALL_OWNER_REVIEW_PACKAGE_CLASSES:
            raise ValueError(
                "owner_review_package_class must be one of "
                f"{ALL_OWNER_REVIEW_PACKAGE_CLASSES}, got {self.owner_review_package_class!r}."
            )

        if self.owner_review_evidence_mode not in ALL_OWNER_REVIEW_EVIDENCE_MODES:
            raise ValueError(
                "owner_review_evidence_mode must be one of "
                f"{ALL_OWNER_REVIEW_EVIDENCE_MODES}, got {self.owner_review_evidence_mode!r}."
            )

        if not self.handoff_ready:
            raise ValueError(
                "handoff_ready must remain true for canonical owner review packages."
            )

        if not self.audit_visible:
            raise ValueError(
                "audit_visible must remain true for canonical owner review packages."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical owner review packages."
            )

        if (
            self.owner_review_package_class == "approval_bound_review_package"
            and not self.approval_required
        ):
            raise ValueError(
                "approval_bound_review_package must have approval_required=True."
            )

        if (
            self.owner_review_package_class == "read_only_review_package"
            and self.approval_required
        ):
            raise ValueError(
                "read_only_review_package must have approval_required=False."
            )

        if (
            self.owner_review_package_class == "approval_bound_review_package"
            and self.owner_review_evidence_mode != "preview_approval_and_audit_evidence"
        ):
            raise ValueError(
                "approval_bound_review_package must use preview_approval_and_audit_evidence."
            )

        if (
            self.owner_review_package_class == "read_only_review_package"
            and self.owner_review_evidence_mode != "preview_and_audit_evidence"
        ):
            raise ValueError(
                "read_only_review_package must use preview_and_audit_evidence."
            )


@dataclass(frozen=True, slots=True)
class OwnerReviewPackageContract:
    """Canonical owner review package contract."""

    contract_id: str
    total_entries: int
    read_only_review_entries: int
    approval_bound_review_entries: int
    audit_visible_entries: int
    operator_visible_entries: int
    entries: tuple[OwnerReviewPackageEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")

        if self.read_only_review_entries != sum(
            1
            for entry in self.entries
            if entry.owner_review_package_class == "read_only_review_package"
        ):
            raise ValueError(
                "read_only_review_entries must match read_only_review_package count."
            )

        if self.approval_bound_review_entries != sum(
            1
            for entry in self.entries
            if entry.owner_review_package_class == "approval_bound_review_package"
        ):
            raise ValueError(
                "approval_bound_review_entries must match approval_bound_review_package count."
            )

        if self.audit_visible_entries != sum(
            1 for entry in self.entries if entry.audit_visible
        ):
            raise ValueError(
                "audit_visible_entries must match audit_visible count."
            )

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )
