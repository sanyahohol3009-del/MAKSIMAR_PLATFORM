from __future__ import annotations

from MAKSIMAR_CORE_LIB.platform_integration import (
    build_platform_bootstrap_context,
    build_platform_summary,
)


def test_platform_bootstrap_context_builds() -> None:
    """Platform bootstrap context should build successfully."""
    context = build_platform_bootstrap_context()

    assert context.snapshot.contract_count >= 1
    assert context.snapshot.config_count >= 1
    assert context.contract_validation.is_loaded is True
    assert context.config_loaders.is_loaded is True


def test_platform_summary_builds() -> None:
    """Platform summary should build successfully."""
    context = build_platform_bootstrap_context()
    summary = build_platform_summary(context)

    assert len(summary) >= 5
    assert any(line.domain_name == "memory_engine" for line in summary)
    assert any(line.domain_name == "ai_services" for line in summary)
