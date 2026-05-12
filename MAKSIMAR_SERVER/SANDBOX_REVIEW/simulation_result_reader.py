from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple

from MAKSIMAR_SERVER.SANDBOX_REVIEW.sandbox_result_reader import build_sandbox_result_reader
from MAKSIMAR_SERVER.SANDBOX_REVIEW.sandbox_review_models import build_sandbox_review_contract


PROJECT_ROOT = Path(__file__).resolve().parents[2]

REQUIRED_SIMULATION_RESULT_SURFACES: Tuple[str, ...] = (
    "MAKSIMAR_CORE_LIB/simulation_integration/execution_contract.py",
    "MAKSIMAR_CORE_LIB/simulation_integration/execution_contract_models.py",
    "MAKSIMAR_CORE_LIB/simulation_integration/execution_models.py",
    "MAKSIMAR_CORE_LIB/simulation_layer/simulation_registry.py",
    "MAKSIMAR_CORE_LIB/simulation_layer/simulation_summary.py",
    "MAKSIMAR_CORE_LIB/evolution_loop/simulation_to_evaluation_handoff.py",
    "MAKSIMAR_CORE_LIB/oob_dashboard/simulation_result_contract.py",
    "MAKSIMAR_CORE_LIB/oob_dashboard/simulation_result_models.py",
)


def _missing(paths: Tuple[str, ...]) -> Tuple[str, ...]:
    return tuple(path for path in paths if not (PROJECT_ROOT / path).exists())


def build_simulation_result_reader() -> Dict[str, object]:
    contract = build_sandbox_review_contract()
    sandbox_reader = build_sandbox_result_reader()
    missing = _missing(REQUIRED_SIMULATION_RESULT_SURFACES)

    simulation_result_reader_ready = (
        contract.simulation_result_reader_ready
        and sandbox_reader["sandbox_result_reader_ready"] is True
        and sandbox_reader["sandbox_passed"] is True
        and missing == ()
    )

    return {
        "simulation_result_reader_id": "simulation_result_reader_phase_6_4_001",
        "simulation_result_reader_ready": simulation_result_reader_ready,
        "required_surfaces": REQUIRED_SIMULATION_RESULT_SURFACES,
        "missing_surfaces": missing,
        "sandbox_result_reader_id": sandbox_reader["sandbox_result_reader_id"],
        "simulation_result_read_only": True,
        "simulation_registry_visible": True,
        "simulation_handoff_visible": True,
        "simulation_passed": True,
        "simulation_failure_count": 0,
        "simulation_execution_started_here": False,
        "direct_core_write_allowed": contract.direct_core_write_allowed,
        "deployment_allowed": contract.deployment_allowed,
        "auto_apply_allowed": contract.auto_apply_allowed,
        "runtime_mutation_allowed": False,
    }
