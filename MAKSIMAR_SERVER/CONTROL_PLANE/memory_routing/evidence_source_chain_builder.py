from __future__ import annotations

import re

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.evidence_source_chain_models import (
    EvidenceSourceChainContract,
    EvidenceSourceChainEntry,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.retrieval_phase_readiness_gate import (
    build_retrieval_phase_readiness,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.retrieval_preview_builder import (
    build_retrieval_preview,
)


def _chain_id_from_evidence_id(evidence_id: str) -> str:
    suffix = evidence_id.removeprefix("evidence_")
    suffix = re.sub(r"[^a-zA-Z0-9_]+", "_", suffix.strip().lower()).strip("_")
    if not suffix:
        raise ValueError("evidence_id must produce a non-empty chain id suffix")
    if not suffix[0].isalpha():
        suffix = f"item_{suffix}"
    return f"evidence_chain_{suffix}"


def build_evidence_source_chain_contract() -> EvidenceSourceChainContract:
    from MAKSIMAR_CORE_LIB.memory_engine.media_memory import (
        build_media_memory_phase_readiness,
    )
    from MAKSIMAR_CORE_LIB.memory_engine.storage_registry import (
        build_storage_registry_phase_readiness,
    )
    from MAKSIMAR_SERVER.architecture_map_runtime import (
        build_architecture_control_phase_readiness,
    )

    retrieval_preview = build_retrieval_preview()
    retrieval_readiness = build_retrieval_phase_readiness()
    storage_readiness = build_storage_registry_phase_readiness()
    media_readiness = build_media_memory_phase_readiness()
    architecture_readiness = build_architecture_control_phase_readiness()

    selected_sources = {
        str(source["source_id"]): source
        for source in retrieval_preview["selected_sources"]
    }

    source_contract_ready = (
        retrieval_readiness.phase_ready
        and storage_readiness.phase_core_ready
        and media_readiness.phase_core_ready
        and architecture_readiness.phase_ready
    )

    provenance_bound = (
        storage_readiness.phase_core_ready
        and media_readiness.provenance_traceability_ready
        and media_readiness.phase_core_ready
    )

    trace_bound = (
        retrieval_readiness.trace_ready
        and architecture_readiness.phase_ready
        and architecture_readiness.read_only
    )

    dashboard_visible = (
        architecture_readiness.dashboard_read_only_ready
        and architecture_readiness.no_mutation_surface
    )

    entries = tuple(
        EvidenceSourceChainEntry(
            chain_id=_chain_id_from_evidence_id(str(item["evidence_id"])),
            evidence_id=str(item["evidence_id"]),
            source_id=str(item["source_id"]),
            source_layer=str(selected_sources[str(item["source_id"])]["source_kind"]),
            artifact_ref=str(item["artifact_ref"]),
            citation_required=bool(item["citation_required"]),
            conflict_marker=str(item["conflict_marker"]),
            source_bound=(
                str(item["source_id"]) in selected_sources
                and source_contract_ready
            ),
            provenance_bound=provenance_bound,
            trace_bound=trace_bound,
            dashboard_visible=dashboard_visible,
            chain_ready=(
                str(item["source_id"]) in selected_sources
                and source_contract_ready
                and provenance_bound
                and trace_bound
                and dashboard_visible
                and bool(item["citation_required"])
                and not str(item["conflict_marker"])
            ),
        )
        for item in retrieval_preview["evidence_pack"]
    )

    return EvidenceSourceChainContract(
        total_items=len(entries),
        source_bound_items=sum(1 for entry in entries if entry.source_bound),
        provenance_bound_items=sum(1 for entry in entries if entry.provenance_bound),
        trace_bound_items=sum(1 for entry in entries if entry.trace_bound),
        citation_required_items=sum(1 for entry in entries if entry.citation_required),
        conflict_marked_items=sum(1 for entry in entries if entry.conflict_marker),
        dashboard_visible_items=sum(1 for entry in entries if entry.dashboard_visible),
        ready_items=sum(1 for entry in entries if entry.chain_ready),
        retrieval_phase_ready=retrieval_readiness.phase_ready,
        storage_phase_ready=storage_readiness.phase_core_ready,
        media_phase_ready=media_readiness.phase_core_ready,
        architecture_control_ready=architecture_readiness.phase_ready,
        mgrep_blocked=retrieval_readiness.mgrep_blocked,
        sqlite_vec_blocked=retrieval_readiness.sqlite_vec_blocked,
        backend_execution_allowed=retrieval_readiness.backend_execution_allowed,
        entries=entries,
    )
