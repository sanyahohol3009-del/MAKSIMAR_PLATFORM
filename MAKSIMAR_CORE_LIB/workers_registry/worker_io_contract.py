from __future__ import annotations

from MAKSIMAR_CORE_LIB.workers_registry.worker_io_models import (
    WorkerIOContract,
    WorkerIOEntry,
)


def build_worker_io_contract() -> WorkerIOContract:
    """Build unified worker input/output contract."""

    entries = (
        WorkerIOEntry(
            worker_id="worker_ai_001",
            input_contract="ai_request",
            output_contract="ai_result",
            artifact_output_supported=True,
        ),
        WorkerIOEntry(
            worker_id="worker_sim_001",
            input_contract="simulation_request",
            output_contract="simulation_result",
            artifact_output_supported=True,
        ),
        WorkerIOEntry(
            worker_id="worker_voice_001",
            input_contract="voice_request",
            output_contract="voice_result",
            artifact_output_supported=False,
        ),
    )

    return WorkerIOContract(
        total_entries=len(entries),
        entries=entries,
    )
