from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.runtime_base.runtime_models import RuntimeLoadResult


@dataclass(slots=True)
class RuntimeLoadSummary:
    """Aggregated summary across runtime load results."""

    total_files: int = 0
    valid_files: int = 0
    invalid_files: int = 0

    def register_result(self, result: RuntimeLoadResult) -> None:
        """Accumulate one runtime load result."""
        self.total_files += 1
        if result.is_valid:
            self.valid_files += 1
        else:
            self.invalid_files += 1


def build_runtime_summary(results: list[RuntimeLoadResult]) -> RuntimeLoadSummary:
    """Build aggregated runtime summary.

    Args:
        results: Runtime load results.

    Returns:
        Aggregated summary.
    """
    summary = RuntimeLoadSummary()
    for result in results:
        summary.register_result(result)
    return summary
