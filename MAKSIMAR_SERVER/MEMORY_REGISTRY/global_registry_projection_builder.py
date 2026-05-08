from __future__ import annotations

from MAKSIMAR_CORE_LIB.id_generation import build_canonical_id_generation_contract
from MAKSIMAR_SERVER.MEMORY_REGISTRY.global_registry_projection_models import (
    GlobalRegistryProjectionContract,
    GlobalRegistryProjectionEntry,
)


_GLOBAL_REGISTRY_FLOW = (
    "module_manifest",
    "canonical_id_generation",
    "registry_projection",
    "dashboard_read_only_visibility",
)


def _append_entry(
    entries: list[GlobalRegistryProjectionEntry],
    *,
    entry_kind: str,
    registry_id: str,
    module_slug: str,
    module_id: str,
    source_layer: str,
    dashboard_visible: bool,
    retrieval_visible: bool,
    observability_visible: bool,
) -> None:
    entries.append(
        GlobalRegistryProjectionEntry(
            entry_kind=entry_kind,  # type: ignore[arg-type]
            registry_id=registry_id,
            module_slug=module_slug,
            module_id=module_id,
            source_layer=source_layer,
            dashboard_visible=dashboard_visible,
            retrieval_visible=retrieval_visible,
            observability_visible=observability_visible,
            flow_stages=_GLOBAL_REGISTRY_FLOW,
        )
    )


def build_global_registry_projection_contract() -> GlobalRegistryProjectionContract:
    """Build read-only global registry projection from canonical ID allocations."""

    id_contract = build_canonical_id_generation_contract()
    entries: list[GlobalRegistryProjectionEntry] = []

    for allocation in id_contract.entries:
        _append_entry(
            entries,
            entry_kind="module",
            registry_id=allocation.module_id,
            module_slug=allocation.module_slug,
            module_id=allocation.module_id,
            source_layer="id_generation",
            dashboard_visible=bool(allocation.panel_ids),
            retrieval_visible=bool(allocation.retrieval_source_id),
            observability_visible=True,
        )

        if allocation.skill_id:
            _append_entry(
                entries,
                entry_kind="skill",
                registry_id=allocation.skill_id,
                module_slug=allocation.module_slug,
                module_id=allocation.module_id,
                source_layer="skill_adapter_registry",
                dashboard_visible=bool(allocation.panel_ids),
                retrieval_visible=bool(allocation.retrieval_source_id),
                observability_visible=True,
            )

        if allocation.memory_tier_id:
            _append_entry(
                entries,
                entry_kind="memory_tier",
                registry_id=allocation.memory_tier_id,
                module_slug=allocation.module_slug,
                module_id=allocation.module_id,
                source_layer="memory_registry",
                dashboard_visible=bool(allocation.panel_ids),
                retrieval_visible=bool(allocation.retrieval_source_id),
                observability_visible=True,
            )

        if allocation.worker_id:
            _append_entry(
                entries,
                entry_kind="worker",
                registry_id=allocation.worker_id,
                module_slug=allocation.module_slug,
                module_id=allocation.module_id,
                source_layer="skill_adapter_registry",
                dashboard_visible=False,
                retrieval_visible=False,
                observability_visible=True,
            )

        if allocation.storage_node_id:
            _append_entry(
                entries,
                entry_kind="storage_node",
                registry_id=allocation.storage_node_id,
                module_slug=allocation.module_slug,
                module_id=allocation.module_id,
                source_layer="storage_binding",
                dashboard_visible=True,
                retrieval_visible=bool(allocation.retrieval_source_id),
                observability_visible=True,
            )

        if allocation.retrieval_source_id:
            _append_entry(
                entries,
                entry_kind="retrieval_source",
                registry_id=allocation.retrieval_source_id,
                module_slug=allocation.module_slug,
                module_id=allocation.module_id,
                source_layer="retrieval_binding",
                dashboard_visible=True,
                retrieval_visible=True,
                observability_visible=True,
            )

        for panel_id in allocation.panel_ids:
            _append_entry(
                entries,
                entry_kind="dashboard_view",
                registry_id=panel_id,
                module_slug=allocation.module_slug,
                module_id=allocation.module_id,
                source_layer="dashboard_binding",
                dashboard_visible=True,
                retrieval_visible=False,
                observability_visible=True,
            )

    return GlobalRegistryProjectionContract(
        total_entries=len(entries),
        dashboard_visible_entries=sum(1 for entry in entries if entry.dashboard_visible),
        retrieval_visible_entries=sum(1 for entry in entries if entry.retrieval_visible),
        observability_visible_entries=sum(
            1 for entry in entries if entry.observability_visible
        ),
        entries=tuple(entries),
    )
