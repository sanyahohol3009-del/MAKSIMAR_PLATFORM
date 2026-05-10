from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters import (
    build_mempalace_adapter_contract,
    build_mempalace_capability_contract,
    build_mempalace_query_contract,
    build_mempalace_write_request_contract,
)


def test_phase_5_1_batch1_ready_smoke() -> None:
    adapter = build_mempalace_adapter_contract()
    capabilities = build_mempalace_capability_contract()
    queries = build_mempalace_query_contract()
    writes = build_mempalace_write_request_contract()

    assert adapter.source_of_truth_adapters == 0
    assert adapter.canonical_write_allowed_adapters == 0
    assert capabilities.canonical_truth_allowed_capabilities == 0
    assert capabilities.regulatory_memory_allowed_capabilities == 0
    assert capabilities.enterprise_policy_memory_allowed_capabilities == 0
    assert queries.canonical_truth_allowed_queries == 0
    assert writes.canonical_write_allowed_write_requests == 0
    assert writes.approval_granted_write_requests == 0
