from __future__ import annotations

from MAKSIMAR_CORE_LIB.workers_registry.worker_capability_contract import (
    build_worker_capability_contract,
)
from MAKSIMAR_CORE_LIB.workers_registry.worker_io_contract import (
    build_worker_io_contract,
)
from MAKSIMAR_CORE_LIB.workers_registry.worker_models import (
    WorkerEntry,
    WorkerRegistryContract,
)
from MAKSIMAR_CORE_LIB.workers_registry.worker_shell_models import (
    WorkerRegistryShellContract,
)


def build_worker_registry_contract() -> WorkerRegistryContract:
    """Build canonical worker registry contract."""

    return WorkerRegistryContract(
        total_workers=3,
        workers=(
            WorkerEntry(
                worker_id="worker_ai_001",
                worker_type="ai_worker",
                target_node="home_node",
                active=True,
            ),
            WorkerEntry(
                worker_id="worker_sim_001",
                worker_type="simulation_worker",
                target_node="home_node",
                active=True,
            ),
            WorkerEntry(
                worker_id="worker_voice_001",
                worker_type="voice_worker",
                target_node="dev_node",
                active=True,
            ),
        ),
    )


def build_worker_registry_shell_contract() -> WorkerRegistryShellContract:
    """Build final shell contract for worker registry layer."""
    registry = build_worker_registry_contract()
    capability_contract = build_worker_capability_contract()
    io_contract = build_worker_io_contract()

    return WorkerRegistryShellContract(
        shell_id="worker_registry_shell",
        total_workers=registry.total_workers,
        total_capabilities=capability_contract.total_capabilities,
        total_io_entries=io_contract.total_entries,
    )
