from __future__ import annotations

from MAKSIMAR_CORE_LIB.platform_integration import (
    build_health_domains,
    build_platform_bootstrap_context,
    build_platform_health_snapshot,
)


def test_platform_health_snapshot_builds() -> None:
    """Platform health snapshot should build successfully."""
    context = build_platform_bootstrap_context()
    snapshot = build_platform_health_snapshot(context)

    assert snapshot.total_domains == 13
    assert snapshot.loaded_domains >= 1
    assert snapshot.failed_domains == 0
    assert snapshot.overall_status == "ok"


def test_platform_health_domains_build() -> None:
    """Platform health domains should build successfully."""
    context = build_platform_bootstrap_context()
    domains = build_health_domains(context)

    assert len(domains) == 13
    assert any(domain.domain_name == "memory_engine" for domain in domains)
    assert any(domain.domain_name == "ai_services" for domain in domains)
