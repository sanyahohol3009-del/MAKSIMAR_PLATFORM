from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.config_loaders.loader import load_config_root
from MAKSIMAR_CORE_LIB.policy_engine.policy_models import Policy, PolicyLoadResult


def _extract_policy_name(file_path: Path) -> str:
    return file_path.name.removesuffix(".yaml")


def load_policies_from_root(root: Path) -> list[PolicyLoadResult]:
    """Load policies from one config root.

    Args:
        root: Config root directory.

    Returns:
        List of policy load results.
    """
    results, _ = load_config_root(root)

    policy_results: list[PolicyLoadResult] = []

    for result in results:
        if not result.is_valid:
            policy_results.append(
                PolicyLoadResult(
                    policy=None,
                    is_valid=False,
                    error="Config validation failed",
                )
            )
            continue

        payload = result.payload  # <-- важно: если у тебя нет payload в result — скажи
        if payload is None:
            policy_results.append(
                PolicyLoadResult(
                    policy=None,
                    is_valid=False,
                    error="Missing payload",
                )
            )
            continue

        policy = Policy(
            name=_extract_policy_name(result.file_path),
            version=str(payload.get("schema_version", "unknown")),
            file_path=result.file_path,
            payload=payload,
        )

        policy_results.append(
            PolicyLoadResult(
                policy=policy,
                is_valid=True,
            )
        )

    return policy_results
