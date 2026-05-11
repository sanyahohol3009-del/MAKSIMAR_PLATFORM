from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters import (
    build_mempalace_runtime_sandbox_policy,
)


def test_mempalace_runtime_sandbox_models_smoke() -> None:
    policy = build_mempalace_runtime_sandbox_policy()

    assert policy.sandbox_policy_ready is True
    assert policy.hard_gate_passed is True
    assert policy.manual_security_review_required is True
    assert policy.fake_backend_required is True
    assert policy.fake_backend_allowed is True
    assert policy.real_backend_candidate_allowed is True
    assert policy.real_backend_enablement_allowed is False
    assert policy.query_only_allowed is True
    assert policy.read_only_allowed is True
    assert policy.canonical_write_allowed is False
    assert policy.runtime_mutation_allowed is False
