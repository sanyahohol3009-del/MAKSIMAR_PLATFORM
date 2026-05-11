from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters import (
    build_mempalace_real_backend_approval_envelope_preview,
)


def test_mempalace_real_backend_approval_envelope_preview_smoke() -> None:
    preview = build_mempalace_real_backend_approval_envelope_preview()

    assert preview["approval_envelope_ready"] is True
    assert preview["controlled_real_backend_probe_allowed"] is True
    assert preview["full_real_backend_enablement_allowed"] is False
    assert preview["general_real_backend_query_allowed"] is False
    assert preview["network_allowed"] is False
    assert preview["subprocess_allowed"] is False
    assert preview["shell_execution_allowed"] is False
    assert preview["destructive_fs_allowed"] is False
    assert preview["secrets_access_allowed"] is False
    assert preview["canonical_write_allowed"] is False
    assert preview["runtime_mutation_allowed"] is False
    assert preview["allowed_probe_scope"] == "single_controlled_import_and_sandbox_query_probe_only"
