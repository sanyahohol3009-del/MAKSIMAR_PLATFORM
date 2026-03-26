from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.dashboard_models import (
    DashboardStateSnapshot,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.diagnostics_models import (
    DiagnosticsIndex,
    RootCauseHint,
)


def _build_hint_for_source(source_name: str, status: str) -> RootCauseHint:
    """Build root-cause hint for one dashboard source."""
    if source_name == "platform_self_check":
        return RootCauseHint(
            source_name=source_name,
            status=status,
            probable_location="MAKSIMAR_CORE_LIB/platform_integration",
            hint_text="Проверь bootstrap, health и self-check контуры платформы.",
        )

    if source_name == "runtime_observability":
        return RootCauseHint(
            source_name=source_name,
            status=status,
            probable_location="MAKSIMAR_CORE_LIB/runtime_observability",
            hint_text="Проверь snapshot, metrics, summary, incident и alert цепочку.",
        )

    if source_name == "incident_snapshot":
        return RootCauseHint(
            source_name=source_name,
            status=status,
            probable_location="MAKSIMAR_CORE_LIB/runtime_observability/incident_snapshot.py",
            hint_text="Проверь incident signals и согласованность source-of-truth.",
        )

    if source_name == "alert_policy":
        return RootCauseHint(
            source_name=source_name,
            status=status,
            probable_location="MAKSIMAR_CORE_LIB/runtime_observability/alert_policy.py",
            hint_text="Проверь классификацию сигналов и уровни alert semantics.",
        )

    return RootCauseHint(
        source_name=source_name,
        status=status,
        probable_location="unknown",
        hint_text="Проверь соответствующий слой и его источник истины.",
    )


def build_diagnostics_index(
    snapshot: DashboardStateSnapshot,
) -> DiagnosticsIndex:
    """Build diagnostics index from dashboard state snapshot."""
    hints = [
        _build_hint_for_source(
            source_name=line.source_name,
            status=line.status,
        )
        for line in snapshot.lines
    ]

    return DiagnosticsIndex(
        total_hints=len(hints),
        hints=hints,
    )
