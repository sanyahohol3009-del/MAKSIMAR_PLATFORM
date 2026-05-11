from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters import (
    build_mempalace_real_backend_approval_envelope,
)


def test_mempalace_real_backend_approval_envelope_smoke() -> None:
    envelope = build_mempalace_real_backend_approval_envelope()

    assert envelope.approval_envelope_ready is True
    assert envelope.hard_gate_passed is True
    assert envelope.security_boundary_ready is True
    assert envelope.classification_ready is True
    assert envelope.manual_security_review_required is True
    assert envelope.manual_security_review_completed is True
    assert envelope.controlled_real_backend_probe_allowed is True

    assert envelope.full_real_backend_enablement_allowed is False
    assert envelope.general_real_backend_query_allowed is False
    assert envelope.network_allowed is False
    assert envelope.subprocess_allowed is False
    assert envelope.shell_execution_allowed is False
    assert envelope.destructive_fs_allowed is False
    assert envelope.secrets_access_allowed is False
    assert envelope.canonical_write_allowed is False
    assert envelope.runtime_mutation_allowed is False
