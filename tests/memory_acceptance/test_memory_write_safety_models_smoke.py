from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_ACCEPTANCE import build_memory_write_safety_policy


def test_memory_write_safety_models_smoke() -> None:
    policy = build_memory_write_safety_policy()

    assert policy.policy_ready is True
    assert len(policy.rules) == 4
    assert policy.duplicate_write_allowed is False
    assert policy.direct_runtime_to_canonical_write_allowed is False
    assert policy.canonical_write_allowed_without_approval is False
    assert policy.runtime_mutation_allowed is False
    assert all(rule.direct_canonical_write_allowed is False for rule in policy.rules)
    assert all(rule.runtime_mutation_allowed is False for rule in policy.rules)
