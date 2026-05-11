from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters import (
    build_mempalace_read_only_routing_integration_preview,
)


def test_phase_5_1_batch4f_ready_smoke() -> None:
    preview = build_mempalace_read_only_routing_integration_preview()

    assert preview["routing_integration_ready"] is True
    assert preview["read_only_routing_enabled"] is True
    assert preview["query_count"] == 4
    assert preview["write_routing_enabled"] is False
    assert preview["full_real_backend_enablement_allowed"] is False
    assert preview["general_real_backend_query_allowed"] is False
