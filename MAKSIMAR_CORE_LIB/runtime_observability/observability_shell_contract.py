from __future__ import annotations

from MAKSIMAR_CORE_LIB.runtime_observability.config_boundary_contract import (
    build_typed_config_boundary_contract,
)
from MAKSIMAR_CORE_LIB.runtime_observability.extended_summary_contract import (
    build_extended_observability_summary,
)
from MAKSIMAR_CORE_LIB.runtime_observability.logging_contract import (
    build_structured_logging_contract,
)
from MAKSIMAR_CORE_LIB.runtime_observability.observability_shell_models import (
    RuntimeObservabilityShellContract,
)
from MAKSIMAR_CORE_LIB.runtime_observability.slo_contract import (
    build_slo_alert_semantics_contract,
)
from MAKSIMAR_CORE_LIB.runtime_observability.trace_contract import (
    build_trace_contract,
)
from MAKSIMAR_CORE_LIB.runtime_observability.visual_panel_contract import (
    build_runtime_observability_visual_panel,
)


def build_runtime_observability_shell_contract() -> RuntimeObservabilityShellContract:
    """Build final runtime observability shell contract."""
    summary = build_extended_observability_summary()
    trace_contract = build_trace_contract()
    logging_contract = build_structured_logging_contract()
    config_boundary = build_typed_config_boundary_contract()
    slo_contract = build_slo_alert_semantics_contract()
    visual_panel = build_runtime_observability_visual_panel()

    overall_status = "ok"
    if summary.overall_status == "warning" or visual_panel.overall_status == "warning":
        overall_status = "warning"

    return RuntimeObservabilityShellContract(
        shell_id="runtime_observability_shell",
        total_metrics=summary.total_lines,
        total_spans=trace_contract.total_spans,
        total_log_records=logging_contract.total_records,
        total_config_entries=config_boundary.total_entries,
        total_slo_indicators=slo_contract.total_indicators,
        overall_status=overall_status,
    )
