from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.end_to_end_dry_run_models import (
    EndToEndDryRunProof,
)


def validate_end_to_end_dry_run_ready(
    proof: EndToEndDryRunProof,
) -> None:
    if not proof.route_ready:
        raise ValueError("End-to-end dry-run must be route_ready")

    if not proof.dry_run_only:
        raise ValueError("End-to-end proof must stay dry_run_only")

    if proof.normalized_record.canonical_truth:
        raise ValueError("Normalized record must remain non-canonical")

    if not proof.portable_reference.portable:
        raise ValueError("Portable reference must be portable")
