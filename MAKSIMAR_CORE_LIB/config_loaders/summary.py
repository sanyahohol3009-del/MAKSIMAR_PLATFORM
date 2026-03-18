from __future__ import annotations

from MAKSIMAR_CORE_LIB.config_loaders.models import ConfigLoadResult, ConfigLoadSummary


def build_summary(results: list[ConfigLoadResult]) -> ConfigLoadSummary:
    """Build aggregated summary from per-file results.

    Args:
        results: Per-file config load results.

    Returns:
        Aggregated summary.
    """
    summary = ConfigLoadSummary()
    for result in results:
        summary.register_result(result)
    return summary
