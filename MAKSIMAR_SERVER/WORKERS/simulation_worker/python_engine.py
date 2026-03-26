from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_SERVER.WORKERS.simulation_worker.io_contracts import (
    SimulationEngineRequest,
    SimulationEngineResult,
)


@dataclass(frozen=True, slots=True)
class PythonSimulationEngine:
    """Reference Python backend for simulation workloads."""

    backend_kind: str = "python"

    def run(self, request: SimulationEngineRequest) -> SimulationEngineResult:
        """Execute deterministic Python simulation backend."""
        normalized_budget = max(request.iteration_budget, 1)

        base_score = min(normalized_budget / 100.0, 1.0)

        if request.scenario_type == "control_validation":
            score = min(base_score + 0.10, 1.0)
            summary = "control_validation_completed"
        elif request.scenario_type == "safety_regression":
            score = min(base_score + 0.05, 1.0)
            summary = "safety_regression_completed"
        else:
            score = min(base_score, 1.0)
            summary = "runtime_pressure_probe_completed"

        output_payload_ref = f"artifact://simulation/{request.task_id}/result"

        return SimulationEngineResult(
            task_id=request.task_id,
            backend_kind="python",
            status="completed",
            score=score,
            output_payload_ref=output_payload_ref,
            summary=summary,
            trace_id=request.trace_id,
        )
