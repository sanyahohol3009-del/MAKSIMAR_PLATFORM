from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.regulatory_update_approval_gate import (
    build_regulatory_update_approval_gate_preview,
)
from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.regulatory_update_approval_models import (
    build_regulatory_update_approval_registry,
)


@dataclass(frozen=True, slots=True)
class RegulatoryUpdateDiffEntry:
    diff_id: str
    proposal_id: str
    source_ref: str
    tenant_id: str
    jurisdiction_id: str
    previous_version: str
    proposed_version: str
    previous_effective_date: str
    proposed_effective_date: str
    approval_required: bool
    approval_granted: bool
    auto_apply_allowed: bool
    diff_ready: bool

    def __post_init__(self) -> None:
        if not self.diff_id:
            raise ValueError("diff_id must be non-empty")
        if not self.proposal_id:
            raise ValueError("proposal_id must be non-empty")
        if not self.source_ref:
            raise ValueError("source_ref must be non-empty")
        if not self.tenant_id:
            raise ValueError("tenant_id must be non-empty")
        if not self.jurisdiction_id:
            raise ValueError("jurisdiction_id must be non-empty")
        if self.approval_required is not True:
            raise ValueError("approval_required must be True")
        if self.approval_granted:
            raise ValueError("approval_granted must be False")
        if self.auto_apply_allowed:
            raise ValueError("auto_apply_allowed must be False")
        if self.diff_ready is not True:
            raise ValueError("diff_ready must be True")


@dataclass(frozen=True, slots=True)
class RegulatoryUpdateDiffPack:
    diff_pack_id: str
    diff_entries: Tuple[RegulatoryUpdateDiffEntry, ...]
    approval_gate_ready: bool
    diff_pack_ready: bool
    approval_required: bool
    approval_granted: bool
    auto_apply_allowed: bool
    canonical_truth_update_allowed: bool
    runtime_mutation_allowed: bool

    def __post_init__(self) -> None:
        if not self.diff_pack_id:
            raise ValueError("diff_pack_id must be non-empty")
        if not self.diff_entries:
            raise ValueError("diff_entries must be non-empty")
        diff_ids = {entry.diff_id for entry in self.diff_entries}
        if len(diff_ids) != len(self.diff_entries):
            raise ValueError("diff_id values must be unique")
        if self.approval_gate_ready is not True:
            raise ValueError("approval_gate_ready must be True")
        if self.diff_pack_ready is not True:
            raise ValueError("diff_pack_ready must be True")
        if self.approval_required is not True:
            raise ValueError("approval_required must be True")
        if self.approval_granted:
            raise ValueError("approval_granted must be False")
        if self.auto_apply_allowed:
            raise ValueError("auto_apply_allowed must be False")
        if self.canonical_truth_update_allowed:
            raise ValueError("canonical_truth_update_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if not all(entry.diff_ready for entry in self.diff_entries):
            raise ValueError("all diff entries must be ready")


def build_regulatory_update_diff_pack() -> RegulatoryUpdateDiffPack:
    registry = build_regulatory_update_approval_registry()
    gate = build_regulatory_update_approval_gate_preview()

    entries = tuple(
        RegulatoryUpdateDiffEntry(
            diff_id=f"regulatory_update_diff_{proposal.proposal_id}",
            proposal_id=proposal.proposal_id,
            source_ref=proposal.source_ref,
            tenant_id=proposal.tenant_id,
            jurisdiction_id=proposal.jurisdiction_id,
            previous_version=proposal.previous_version,
            proposed_version=proposal.proposed_version,
            previous_effective_date=proposal.previous_effective_date,
            proposed_effective_date=proposal.proposed_effective_date,
            approval_required=proposal.approval_required,
            approval_granted=proposal.approval_granted,
            auto_apply_allowed=proposal.auto_apply_allowed,
            diff_ready=True,
        )
        for proposal in registry.proposals
    )

    return RegulatoryUpdateDiffPack(
        diff_pack_id="regulatory_update_diff_pack_step_7_001",
        diff_entries=entries,
        approval_gate_ready=gate["preview_ready"],
        diff_pack_ready=gate["preview_ready"] is True,
        approval_required=registry.approval_required,
        approval_granted=registry.approval_granted,
        auto_apply_allowed=registry.auto_apply_allowed,
        canonical_truth_update_allowed=registry.canonical_truth_update_allowed,
        runtime_mutation_allowed=registry.runtime_mutation_allowed,
    )


def build_regulatory_update_diff_preview() -> Dict[str, object]:
    pack = build_regulatory_update_diff_pack()

    return {
        "preview_id": "regulatory_update_diff_preview_step_7_001",
        "preview_ready": pack.diff_pack_ready,
        "diff_pack_id": pack.diff_pack_id,
        "diff_entry_count": len(pack.diff_entries),
        "proposal_ids": tuple(entry.proposal_id for entry in pack.diff_entries),
        "source_refs": tuple(entry.source_ref for entry in pack.diff_entries),
        "approval_gate_ready": pack.approval_gate_ready,
        "approval_required": pack.approval_required,
        "approval_granted": pack.approval_granted,
        "auto_apply_allowed": pack.auto_apply_allowed,
        "canonical_truth_update_allowed": pack.canonical_truth_update_allowed,
        "runtime_mutation_allowed": pack.runtime_mutation_allowed,
    }
