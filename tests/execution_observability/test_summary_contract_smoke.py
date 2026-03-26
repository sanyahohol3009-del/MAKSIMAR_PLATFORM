from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_observability import (
    build_execution_summary,
)


def test_execution_summary_builds() -> None:
    summary = build_execution_summary()

    assert summary.total_lines == 5
    assert summary.overall_status == "ok"
