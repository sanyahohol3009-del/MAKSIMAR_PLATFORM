from __future__ import annotations

from MAKSIMAR_CORE_LIB.platform_integration import run_platform_self_check


def test_platform_self_check_runs() -> None:
    """Platform self-check should run successfully."""
    result = run_platform_self_check()

    assert result.overall_status == "ok"
    assert result.bootstrap_status == "ok"
    assert result.health_status == "ok"
    assert result.total_domains == 13
    assert result.loaded_domains == 13
    assert result.failed_domains == 0
    assert result.total_items >= 1
