from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from MAKSIMAR_CORE_LIB.config_loaders.root_registry import get_config_roots
from MAKSIMAR_CORE_LIB.policy_engine.policy_loader import load_policies_from_root
from MAKSIMAR_CORE_LIB.policy_engine.policy_models import Policy


class PolicyRegistry:
    """In-memory registry of all loaded policies."""

    def __init__(self) -> None:
        self._policies: dict[str, Policy] = {}
        self._by_root: dict[str, list[Policy]] = defaultdict(list)

    def load_all(self) -> None:
        """Load all policies from all config roots."""
        for entry in get_config_roots():
            results = load_policies_from_root(entry.path)

            for result in results:
                if not result.is_valid or result.policy is None:
                    continue

                policy = result.policy

                self._policies[policy.name] = policy
                self._by_root[entry.name].append(policy)

    def get(self, name: str) -> Policy | None:
        return self._policies.get(name)

    def get_by_root(self, root_name: str) -> list[Policy]:
        return self._by_root.get(root_name, [])
