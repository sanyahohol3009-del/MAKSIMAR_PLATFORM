from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_SERVER.WORKERS.simulation_worker.engine_adapter import (
    SimulationEngineAdapter,
)
from MAKSIMAR_SERVER.WORKERS.simulation_worker.io_contracts import (
    SimulationEngineRequest,
    SimulationEngineResult,
)
from MAKSIMAR_SERVER.WORKERS.simulation_worker.python_engine import (
    PythonSimulationEngine,
)


@dataclass(frozen=True, slots=True)
class SimulationWorkerRuntime:
    """Worker orchestration shell for simulation workloads."""

    worker_id: str
    adapter: SimulationEngineAdapter

    def execute_task(self, request: SimulationEngineRequest) -> SimulationEngineResult:
        """Execute simulation task through engine adapter boundary."""
        return self.adapter.execute(request)


def build_simulation_worker_runtime() -> SimulationWorkerRuntime:
    """Build simulation worker runtime with Python engine backend."""
    adapter = SimulationEngineAdapter(engine=PythonSimulationEngine())

    return SimulationWorkerRuntime(
        worker_id="worker_sim_001",
        adapter=adapter,
    )
