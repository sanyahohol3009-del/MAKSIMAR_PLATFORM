from __future__ import annotations

from functools import lru_cache

from MAKSIMAR_CORE_LIB.policy_engine.policy_models import Policy
from MAKSIMAR_CORE_LIB.policy_engine.policy_registry import PolicyRegistry


@lru_cache(maxsize=1)
def _get_registry() -> PolicyRegistry:
    """Build cached policy registry."""
    registry = PolicyRegistry()
    registry.load_all()
    return registry


def get_policy(name: str) -> Policy:
    """Get policy by canonical name.

    Raises:
        KeyError: If policy is not found.
    """
    policy = _get_registry().get(name)
    if policy is None:
        raise KeyError(f"Policy not found: {name}")
    return policy


def get_policy_definition(name: str) -> Policy:
    """Unified public accessor for one policy definition.

    Raises:
        KeyError: If policy is not found.
    """
    return get_policy(name)


def list_policies_by_root(root_name: str) -> list[Policy]:
    """List policies for one config root."""
    return _get_registry().get_by_root(root_name)


def list_policy_definitions() -> list[Policy]:
    """Unified public accessor for all policy definitions."""
    registry = _get_registry()
    all_policies: list[Policy] = []

    for policies in registry._by_root.values():
        all_policies.extend(policies)

    unique: dict[str, Policy] = {}
    for policy in all_policies:
        unique[policy.name] = policy

    return list(unique.values())
