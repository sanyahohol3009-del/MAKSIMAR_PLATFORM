from __future__ import annotations

from MAKSIMAR_CORE_LIB.mobile_bridge.task_models import (
    TaskEnvelope,
    TaskEnvelopeContract,
)


def build_task_envelope_contract() -> TaskEnvelopeContract:
    """Build unified mobile bridge task envelope contract."""

    envelopes = (
        TaskEnvelope(
            envelope_id="task_env_001",
            request_id="mobile_req_001",
            envelope_type="query_task",
            execution_target="home_node",
            core_write_allowed=False,
            mobile_executes_task=False,
        ),
        TaskEnvelope(
            envelope_id="task_env_002",
            request_id="mobile_req_002",
            envelope_type="status_task",
            execution_target="dev_node",
            core_write_allowed=False,
            mobile_executes_task=False,
        ),
    )

    return TaskEnvelopeContract(
        total_envelopes=len(envelopes),
        envelopes=envelopes,
    )
