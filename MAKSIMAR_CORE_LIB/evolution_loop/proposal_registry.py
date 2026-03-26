from __future__ import annotations

from MAKSIMAR_CORE_LIB.evolution_loop.proposal_models import (
    ProposalDefinition,
    ProposalRegistrySummary,
)
from MAKSIMAR_CORE_LIB.shared_services.atomic_io import safe_read_yaml
from MAKSIMAR_CORE_LIB.shared_services.path_resolver import PATHS


def build_proposal_registry_summary() -> ProposalRegistrySummary:
    """Build unified proposal registry summary from proposal-like contracts."""
    records: list[ProposalDefinition] = []

    simulation_root = PATHS.contracts_root / "simulation"
    codegen_root = PATHS.contracts_root / "codegen"

    for root in [simulation_root, codegen_root]:
        if not root.exists() or not root.is_dir():
            continue

        for file_path in sorted(root.glob("*proposal*.yaml")):
            if not file_path.is_file():
                continue

            payload = safe_read_yaml(file_path)

            proposal_id = f"{root.name}_{file_path.stem}"
            schema_version = payload.get("schema_version", f"{proposal_id}.v1")

            records.append(
                ProposalDefinition(
                    proposal_id=str(proposal_id),
                    version=str(schema_version),
                    source_definition_id=file_path.stem,
                )
            )

    unique_records: dict[str, ProposalDefinition] = {}
    for record in records:
        unique_records[record.proposal_id] = record

    final_records = list(unique_records.values())

    return ProposalRegistrySummary(
        total_proposals=len(final_records),
        records=final_records,
    )
