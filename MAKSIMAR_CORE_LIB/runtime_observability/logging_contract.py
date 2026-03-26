from __future__ import annotations

from MAKSIMAR_CORE_LIB.runtime_observability.logging_models import (
    StructuredLogRecord,
    StructuredLoggingContract,
)
from MAKSIMAR_CORE_LIB.runtime_observability.trace_contract import (
    build_trace_contract,
)


def build_structured_logging_contract() -> StructuredLoggingContract:
    """Build unified structured logging contract."""
    trace_contract = build_trace_contract()
    trace_id = trace_contract.root_trace_id

    records = (
        StructuredLogRecord(
            event_name="runtime_snapshot_built",
            level="info",
            trace_id=trace_id,
            message="Runtime snapshot contract built successfully.",
        ),
        StructuredLogRecord(
            event_name="extended_summary_built",
            level="info",
            trace_id=trace_id,
            message="Extended observability summary built successfully.",
        ),
        StructuredLogRecord(
            event_name="trace_contract_built",
            level="info",
            trace_id=trace_id,
            message="Trace contract created successfully.",
        ),
    )

    return StructuredLoggingContract(
        total_records=len(records),
        records=records,
    )
