from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters import (
    build_mempalace_probe_result_binding_preview,
)


def test_phase_5_1_batch4e_ready_smoke() -> None:
    preview = build_mempalace_probe_result_binding_preview()

    assert preview["binding_ready"] is True
    assert preview["controlled_probe_success"] is True
    assert preview["read_only_adapter_binding_allowed"] is True
    assert preview["full_real_backend_enablement_allowed"] is False
    assert preview["general_real_backend_query_allowed"] is False
