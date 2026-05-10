from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters.mempalace_adapter import (
    build_mempalace_adapter_surface,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters.mempalace_capability_builder import (
    build_mempalace_capability_contract,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters.mempalace_guard_validators import (
    build_mempalace_guard_validation_report,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters.mempalace_query_models import (
    build_mempalace_query_contract,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters.mempalace_summary_builder import (
    build_mempalace_summary,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters.mempalace_write_models import (
    build_mempalace_write_request_contract,
)


_MEMPALACE_PREVIEW_FLOW = (
    "mempalace_adapter_contract",
    "mempalace_capability_contract",
    "mempalace_query_contract",
    "mempalace_write_request_guard",
    "mempalace_guard_validators",
    "mempalace_adapter_surface",
    "mempalace_summary",
    "mempalace_preview",
)


def build_mempalace_preview() -> Dict[str, object]:
    capabilities = build_mempalace_capability_contract()
    queries = build_mempalace_query_contract()
    writes = build_mempalace_write_request_contract()
    guards = build_mempalace_guard_validation_report()
    surface = build_mempalace_adapter_surface()
    summary = build_mempalace_summary()

    return {
        "flow": _MEMPALACE_PREVIEW_FLOW,
        "preview_ready": bool(summary["summary_ready"]) and surface.adapter_surface_ready,
        "summary_ready": summary["summary_ready"],
        "guard_validation_ready": guards.guard_validation_ready,
        "adapter_surface_ready": surface.adapter_surface_ready,
        "allowed_domains": guards.allowed_domains,
        "forbidden_domains": guards.forbidden_domains,
        "capability_domains": tuple(entry.domain for entry in capabilities.entries),
        "query_ids": tuple(entry.query_id for entry in queries.entries),
        "write_request_ids": tuple(entry.write_request_id for entry in writes.entries),
        "external_backend_connected": surface.external_backend_connected,
        "vendor_acquisition_required": surface.vendor_acquisition_required,
        "download_performed": surface.download_performed,
        "real_backend_enabled": surface.real_backend_enabled,
        "source_of_truth_adapters": summary["source_of_truth_adapters"],
        "canonical_truth_allowed_capabilities": summary["canonical_truth_allowed_capabilities"],
        "regulatory_memory_allowed_capabilities": summary["regulatory_memory_allowed_capabilities"],
        "enterprise_policy_memory_allowed_capabilities": summary["enterprise_policy_memory_allowed_capabilities"],
        "technical_truth_allowed_capabilities": summary["technical_truth_allowed_capabilities"],
        "audit_truth_allowed_capabilities": summary["audit_truth_allowed_capabilities"],
        "approval_truth_allowed_capabilities": summary["approval_truth_allowed_capabilities"],
        "canonical_write_allowed": summary["canonical_write_allowed"],
        "auto_promotion_allowed": summary["auto_promotion_allowed"],
        "auto_conflict_resolution_allowed": summary["auto_conflict_resolution_allowed"],
        "runtime_mutation_allowed": summary["runtime_mutation_allowed"],
    }
