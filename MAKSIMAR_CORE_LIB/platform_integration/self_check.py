from __future__ import annotations

from MAKSIMAR_CORE_LIB.platform_integration.bootstrap_loader import (
    build_platform_bootstrap_context,
)
from MAKSIMAR_CORE_LIB.platform_integration.health_snapshot import (
    build_platform_health_snapshot,
)
from MAKSIMAR_CORE_LIB.platform_integration.self_check_models import (
    PlatformSelfCheckResult,
)


def run_platform_self_check() -> PlatformSelfCheckResult:
    """Run unified self-check for the whole platform."""
    context = build_platform_bootstrap_context()
    health = build_platform_health_snapshot(context)

    bootstrap_status = "ok"
    health_status = health.overall_status
    overall_status = "ok" if bootstrap_status == "ok" and health_status == "ok" else "failed"

    return PlatformSelfCheckResult(
        overall_status=overall_status,
        bootstrap_status=bootstrap_status,
        health_status=health_status,
        total_domains=health.total_domains,
        loaded_domains=health.loaded_domains,
        failed_domains=health.failed_domains,
        total_items=health.total_items,
    )
