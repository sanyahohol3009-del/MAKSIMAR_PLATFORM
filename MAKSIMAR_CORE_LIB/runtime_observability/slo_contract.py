from __future__ import annotations

from MAKSIMAR_CORE_LIB.runtime_observability.slo_models import (
    SLOAlertSemanticsContract,
    SLOIndicator,
)


def build_slo_alert_semantics_contract() -> SLOAlertSemanticsContract:
    """Build unified SLO / alert semantics contract."""

    indicators = (
        SLOIndicator(
            indicator_name="runtime_snapshot_health",
            alert_level="info",
            service_impact="System snapshot built successfully.",
        ),
        SLOIndicator(
            indicator_name="failed_domains_presence",
            alert_level="warning",
            service_impact="Some monitored domains are degraded or unavailable.",
        ),
        SLOIndicator(
            indicator_name="consistency_failure",
            alert_level="critical",
            service_impact="Dashboard source-of-truth is inconsistent.",
        ),
    )

    return SLOAlertSemanticsContract(
        total_indicators=len(indicators),
        indicators=indicators,
    )
