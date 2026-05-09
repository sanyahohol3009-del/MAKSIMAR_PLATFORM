from __future__ import annotations

from MAKSIMAR_CORE_LIB.skill_domain_binding import (
    build_shell_adapter_binding_contract,
    build_skill_domain_preview,
    build_skill_domain_summary,
    build_skill_to_dashboard_binding_contract,
    build_skill_to_memory_binding_contract,
    build_skill_to_retrieval_binding_contract,
)


def test_phase_2_4_batch2_ready_smoke() -> None:
    shells = build_shell_adapter_binding_contract()
    memory = build_skill_to_memory_binding_contract()
    retrieval = build_skill_to_retrieval_binding_contract()
    dashboard = build_skill_to_dashboard_binding_contract()
    summary = build_skill_domain_summary()
    preview = build_skill_domain_preview()

    assert shells.ready_bindings == shells.total_bindings
    assert shells.action_execution_allowed_bindings == 0
    assert memory.ready_bindings == memory.total_bindings
    assert retrieval.ready_bindings == retrieval.total_bindings
    assert retrieval.backend_execution_allowed_bindings == 0
    assert dashboard.ready_bindings == dashboard.total_bindings
    assert dashboard.action_execution_allowed_bindings == 0
    assert summary["summary_ready"] is True
    assert preview["preview_ready"] is True
    assert preview["batch1_ready"] is True
