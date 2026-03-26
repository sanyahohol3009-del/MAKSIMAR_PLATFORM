from __future__ import annotations

from MAKSIMAR_CORE_LIB.mobile_bridge.result_models import (
    TaskResult,
    TaskResultContract,
)


def build_task_result_contract() -> TaskResultContract:
    """Build unified mobile bridge task result contract."""

    results = (
        TaskResult(
            result_id="task_result_001",
            envelope_id="task_env_001",
            status="completed",
            payload_ref="result_payload_001",
            core_write_performed=False,
        ),
        TaskResult(
            result_id="task_result_002",
            envelope_id="task_env_002",
            status="completed",
            payload_ref="result_payload_002",
            core_write_performed=False,
        ),
    )

    return TaskResultContract(
        total_results=len(results),
        results=results,
    )
