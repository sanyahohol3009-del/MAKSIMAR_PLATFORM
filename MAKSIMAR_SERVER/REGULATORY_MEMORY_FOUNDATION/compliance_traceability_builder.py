from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.regulatory_audit_read_model import (
    build_regulatory_audit_read_model_preview,
)
from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.regulatory_conflict_preview_builder import (
    build_regulatory_conflict_drift_supersession_preview,
)


@dataclass(frozen=True, slots=True)
class ComplianceTraceabilityChain:
    chain_id: str
    trace_steps: Tuple[str, ...]
    audit_read_model_ready: bool
    conflict_drift_supersession_ready: bool
    source_to_decision_trace_ready: bool
    operator_visible: bool
    read_only: bool
    mutation_allowed: bool
    chain_ready: bool

    def __post_init__(self) -> None:
        if not self.chain_id:
            raise ValueError("chain_id must be non-empty")
        if not self.trace_steps:
            raise ValueError("trace_steps must be non-empty")
        required_steps = {
            "source_ref",
            "source_version",
            "effective_date",
            "tenant_scope",
            "jurisdiction_scope",
            "conflict_drift_supersession",
            "audit_read_model",
            "human_review",
        }
        if not required_steps.issubset(set(self.trace_steps)):
            raise ValueError("trace_steps missing required compliance trace steps")
        if self.audit_read_model_ready is not True:
            raise ValueError("audit_read_model_ready must be True")
        if self.conflict_drift_supersession_ready is not True:
            raise ValueError("conflict_drift_supersession_ready must be True")
        if self.source_to_decision_trace_ready is not True:
            raise ValueError("source_to_decision_trace_ready must be True")
        if self.operator_visible is not True:
            raise ValueError("operator_visible must be True")
        if self.read_only is not True:
            raise ValueError("read_only must be True")
        if self.mutation_allowed:
            raise ValueError("mutation_allowed must be False")
        if self.chain_ready is not True:
            raise ValueError("chain_ready must be True")


def build_compliance_traceability_chain() -> ComplianceTraceabilityChain:
    audit = build_regulatory_audit_read_model_preview()
    conflict = build_regulatory_conflict_drift_supersession_preview()

    trace_steps = (
        "source_ref",
        "source_version",
        "effective_date",
        "tenant_scope",
        "jurisdiction_scope",
        "precedence",
        "conflict_drift_supersession",
        "audit_read_model",
        "human_review",
    )

    return ComplianceTraceabilityChain(
        chain_id="compliance_traceability_chain_step_6_001",
        trace_steps=trace_steps,
        audit_read_model_ready=audit["preview_ready"],
        conflict_drift_supersession_ready=conflict["preview_ready"],
        source_to_decision_trace_ready=audit["preview_ready"] is True and conflict["preview_ready"] is True,
        operator_visible=True,
        read_only=True,
        mutation_allowed=False,
        chain_ready=audit["preview_ready"] is True and conflict["preview_ready"] is True,
    )


def build_compliance_traceability_preview() -> Dict[str, object]:
    chain = build_compliance_traceability_chain()

    return {
        "preview_id": "compliance_traceability_preview_step_6_001",
        "preview_ready": chain.chain_ready,
        "chain_id": chain.chain_id,
        "trace_steps": chain.trace_steps,
        "trace_step_count": len(chain.trace_steps),
        "audit_read_model_ready": chain.audit_read_model_ready,
        "conflict_drift_supersession_ready": chain.conflict_drift_supersession_ready,
        "source_to_decision_trace_ready": chain.source_to_decision_trace_ready,
        "operator_visible": chain.operator_visible,
        "read_only": chain.read_only,
        "mutation_allowed": chain.mutation_allowed,
    }
