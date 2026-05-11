from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters import (
    build_mempalace_real_backend_approval_envelope_preview,
)


def test_phase_5_1_batch4c_ready_smoke() -> None:
    preview = build_mempalace_real_backend_approval_envelope_preview()

    assert preview["approval_envelope_ready"] is True
    assert preview["manual_security_review_completed"] is True
    assert preview["controlled_real_backend_probe_allowed"] is True
    assert preview["full_real_backend_enablement_allowed"] is False
    assert preview["general_real_backend_query_allowed"] is False
