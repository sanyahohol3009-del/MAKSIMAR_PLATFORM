from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    build_default_retrieval_scope,
)


def test_retrieval_scope_models_smoke() -> None:
    scope = build_default_retrieval_scope()

    assert scope.tenant_boundary_required is True
    assert scope.policy_gate_required is True
    assert "project_history" in scope.allowed_memory_domains
    assert "raw_binary_payload" in scope.forbidden_source_kinds
