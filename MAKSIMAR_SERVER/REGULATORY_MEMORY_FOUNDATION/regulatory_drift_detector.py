from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Literal, Tuple

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.regulatory_conflict_models import (
    build_regulatory_conflict_registry,
)
from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.regulatory_source_version_models import (
    build_regulatory_source_version_registry,
)


RegulatoryDriftKind = Literal[
    "draft_source_pending_review",
    "jurisdiction_precedence_recheck_required",
    "conflict_candidate_detected",
    "supersession_candidate_detected",
]

RegulatoryDriftSeverity = Literal["low", "medium", "high", "critical"]


@dataclass(frozen=True, slots=True)
class RegulatoryDriftSignal:
    signal_id: str
    drift_kind: RegulatoryDriftKind
    severity: RegulatoryDriftSeverity
    source_refs: Tuple[str, ...]
    tenant_id: str
    jurisdiction_ids: Tuple[str, ...]
    source_version_present: bool
    effective_date_present: bool
    human_review_required: bool
    automatic_resolution_allowed: bool
    canonical_truth_update_allowed: bool
    runtime_mutation_allowed: bool
    signal_ready: bool

    def __post_init__(self) -> None:
        if not self.signal_id:
            raise ValueError("signal_id must be non-empty")
        if not self.source_refs:
            raise ValueError("source_refs must be non-empty")
        if not self.tenant_id:
            raise ValueError("tenant_id must be non-empty")
        if not self.jurisdiction_ids:
            raise ValueError("jurisdiction_ids must be non-empty")
        if self.source_version_present is not True:
            raise ValueError("source_version_present must be True")
        if self.effective_date_present is not True:
            raise ValueError("effective_date_present must be True")
        if self.human_review_required is not True:
            raise ValueError("human_review_required must be True")
        if self.automatic_resolution_allowed:
            raise ValueError("automatic_resolution_allowed must be False")
        if self.canonical_truth_update_allowed:
            raise ValueError("canonical_truth_update_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.signal_ready is not True:
            raise ValueError("signal_ready must be True")


@dataclass(frozen=True, slots=True)
class RegulatoryDriftReport:
    report_id: str
    signals: Tuple[RegulatoryDriftSignal, ...]
    conflict_registry_ready: bool
    drift_detection_ready: bool
    human_review_required: bool
    automatic_resolution_allowed: bool
    canonical_truth_update_allowed: bool
    runtime_mutation_allowed: bool

    def __post_init__(self) -> None:
        if not self.report_id:
            raise ValueError("report_id must be non-empty")
        if not self.signals:
            raise ValueError("signals must be non-empty")
        signal_ids = {signal.signal_id for signal in self.signals}
        if len(signal_ids) != len(self.signals):
            raise ValueError("signal_id values must be unique")
        if self.conflict_registry_ready is not True:
            raise ValueError("conflict_registry_ready must be True")
        if self.drift_detection_ready is not True:
            raise ValueError("drift_detection_ready must be True")
        if self.human_review_required is not True:
            raise ValueError("human_review_required must be True")
        if self.automatic_resolution_allowed:
            raise ValueError("automatic_resolution_allowed must be False")
        if self.canonical_truth_update_allowed:
            raise ValueError("canonical_truth_update_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if not all(signal.signal_ready for signal in self.signals):
            raise ValueError("all drift signals must be ready")


def build_regulatory_drift_report() -> RegulatoryDriftReport:
    conflict_registry = build_regulatory_conflict_registry()
    source_registry = build_regulatory_source_version_registry()

    draft_sources = tuple(source for source in source_registry.sources if source.source_status == "draft")
    de_tenant_sources = tuple(source for source in source_registry.sources if source.tenant_id == "tenant_demo_de_001")

    signals = (
        RegulatoryDriftSignal(
            signal_id="regulatory_drift_draft_source_pending_review_001",
            drift_kind="draft_source_pending_review",
            severity="low",
            source_refs=tuple(source.source_ref for source in draft_sources),
            tenant_id="tenant_demo_ua_001",
            jurisdiction_ids=tuple(source.jurisdiction_id for source in draft_sources),
            source_version_present=True,
            effective_date_present=True,
            human_review_required=True,
            automatic_resolution_allowed=False,
            canonical_truth_update_allowed=False,
            runtime_mutation_allowed=False,
            signal_ready=True,
        ),
        RegulatoryDriftSignal(
            signal_id="regulatory_drift_precedence_recheck_de_eu_001",
            drift_kind="jurisdiction_precedence_recheck_required",
            severity="medium",
            source_refs=tuple(source.source_ref for source in de_tenant_sources),
            tenant_id="tenant_demo_de_001",
            jurisdiction_ids=tuple(source.jurisdiction_id for source in de_tenant_sources),
            source_version_present=True,
            effective_date_present=True,
            human_review_required=True,
            automatic_resolution_allowed=False,
            canonical_truth_update_allowed=False,
            runtime_mutation_allowed=False,
            signal_ready=True,
        ),
        RegulatoryDriftSignal(
            signal_id="regulatory_drift_conflict_candidate_detected_001",
            drift_kind="conflict_candidate_detected",
            severity="medium",
            source_refs=conflict_registry.candidates[0].source_refs,
            tenant_id=conflict_registry.candidates[0].tenant_id,
            jurisdiction_ids=conflict_registry.candidates[0].jurisdiction_ids,
            source_version_present=True,
            effective_date_present=True,
            human_review_required=True,
            automatic_resolution_allowed=False,
            canonical_truth_update_allowed=False,
            runtime_mutation_allowed=False,
            signal_ready=True,
        ),
    )

    return RegulatoryDriftReport(
        report_id="regulatory_drift_report_step_5_001",
        signals=signals,
        conflict_registry_ready=conflict_registry.conflict_detection_ready,
        drift_detection_ready=conflict_registry.conflict_detection_ready,
        human_review_required=True,
        automatic_resolution_allowed=False,
        canonical_truth_update_allowed=False,
        runtime_mutation_allowed=False,
    )


def build_regulatory_drift_preview() -> Dict[str, object]:
    report = build_regulatory_drift_report()

    return {
        "preview_id": "regulatory_drift_preview_step_5_001",
        "preview_ready": report.drift_detection_ready,
        "report_id": report.report_id,
        "signal_count": len(report.signals),
        "signal_ids": tuple(signal.signal_id for signal in report.signals),
        "drift_kinds": tuple(signal.drift_kind for signal in report.signals),
        "conflict_registry_ready": report.conflict_registry_ready,
        "human_review_required": report.human_review_required,
        "automatic_resolution_allowed": report.automatic_resolution_allowed,
        "canonical_truth_update_allowed": report.canonical_truth_update_allowed,
        "runtime_mutation_allowed": report.runtime_mutation_allowed,
    }
