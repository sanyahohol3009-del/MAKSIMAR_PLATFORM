from __future__ import annotations

from functools import lru_cache

from MAKSIMAR_CORE_LIB.policy_engine.policy_registry import PolicyRegistry
from MAKSIMAR_CORE_LIB.policy_engine.policy_models import Policy


@lru_cache(maxsize=1)
def _get_registry() -> PolicyRegistry:
    registry = PolicyRegistry()
    registry.load_all()
    return registry


def get_policy(name: str) -> Policy:
    """Get policy by name (strict).

    Raises:
        KeyError if not found.
    """
    policy = _get_registry().get(name)
    if policy is None:
        raise KeyError(f"Policy not found: {name}")
    return policy


def list_policies_by_root(root_name: str) -> list[Policy]:
    return _get_registry().get_by_root(root_name)
