from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters import (
    build_mempalace_read_only_routing_integration,
)


def test_mempalace_read_only_routing_integration_smoke() -> None:
    integration = build_mempalace_read_only_routing_integration()

    assert integration.routing_integration_ready is True
    assert integration.subordinate_backend is True
    assert integration.read_only_routing_enabled is True
    assert integration.query_count == 4
    assert integration.write_request_allowed_count == 0
    assert integration.write_routing_enabled is False
    assert integration.full_real_backend_enablement_allowed is False
    assert integration.general_real_backend_query_allowed is False
    assert integration.canonical_write_allowed is False
    assert integration.runtime_mutation_allowed is False
