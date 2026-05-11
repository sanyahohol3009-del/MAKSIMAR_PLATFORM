from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters import (
    build_mempalace_probe_result_binding,
)


def test_mempalace_probe_result_binding_smoke() -> None:
    binding = build_mempalace_probe_result_binding()

    assert binding.binding_ready is True
    assert binding.controlled_probe_success is True
    assert binding.real_import_verified is True
    assert binding.vendor_venv_used is True
    assert binding.denied_env_scrubbed is True
    assert binding.network_blocked is True
    assert binding.subprocess_blocked is True
    assert binding.destructive_filesystem_blocked is True
    assert binding.read_only_adapter_binding_allowed is True
    assert binding.full_real_backend_enablement_allowed is False
    assert binding.general_real_backend_query_allowed is False
    assert binding.canonical_write_allowed is False
    assert binding.runtime_mutation_allowed is False
