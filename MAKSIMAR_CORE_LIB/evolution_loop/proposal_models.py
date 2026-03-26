from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProposalDefinition:
    """Canonical proposal definition for evolution loop foundation."""

    proposal_id: str
    version: str
    source_definition_id: str


@dataclass(frozen=True, slots=True)
class ProposalRegistrySummary:
    """Unified registry summary for proposal definitions."""

    total_proposals: int
    records: list[ProposalDefinition]
