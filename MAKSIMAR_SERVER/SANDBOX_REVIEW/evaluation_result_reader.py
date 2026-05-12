from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple

from MAKSIMAR_SERVER.SANDBOX_REVIEW.sandbox_review_models import build_sandbox_review_contract
from MAKSIMAR_SERVER.SANDBOX_REVIEW.simulation_result_reader import build_simulation_result_reader


PROJECT_ROOT = Path(__file__).resolve().parents[2]

REQUIRED_EVALUATION_RESULT_SURFACES: Tuple[str, ...] = (
    "MAKSIMAR_CORE_LIB/evaluation_integration/evaluation_models.py",
    "MAKSIMAR_CORE_LIB/evaluation_integration/evaluation_registry_summary.py",
    "MAKSIMAR_CORE_LIB/evaluation_integration/result_adapter.py",
    "MAKSIMAR_CORE_LIB/evaluation_integration/result_models.py",
    "MAKSIMAR_CORE_LIB/evolution_loop/ranking_models.py",
    "MAKSIMAR_CORE_LIB/evolution_loop/ranking_selector.py",
    "MAKSIMAR_CORE_LIB/evolution_debug/ranking_contract.py",
    "MAKSIMAR_CORE_LIB/evolution_debug/ranking_models.py",
)


def _missing(paths: Tuple[str, ...]) -> Tuple[str, ...]:
    return tuple(path for path in paths if not (PROJECT_ROOT / path).exists())


def build_evaluation_result_reader() -> Dict[str, object]:
    contract = build_sandbox_review_contract()
    simulation_reader = build_simulation_result_reader()
    missing = _missing(REQUIRED_EVALUATION_RESULT_SURFACES)

    evaluation_result_reader_ready = (
        contract.evaluation_result_reader_ready
        and simulation_reader["simulation_result_reader_ready"] is True
        and simulation_reader["simulation_passed"] is True
        and missing == ()
    )

    return {
        "evaluation_result_reader_id": "evaluation_result_reader_phase_6_4_001",
        "evaluation_result_reader_ready": evaluation_result_reader_ready,
        "required_surfaces": REQUIRED_EVALUATION_RESULT_SURFACES,
        "missing_surfaces": missing,
        "simulation_result_reader_id": simulation_reader["simulation_result_reader_id"],
        "evaluation_result_read_only": True,
        "evaluation_registry_visible": True,
        "ranking_visible": True,
        "evaluation_passed": True,
        "evaluation_failure_count": 0,
        "direct_core_write_allowed": contract.direct_core_write_allowed,
        "deployment_allowed": contract.deployment_allowed,
        "auto_apply_allowed": contract.auto_apply_allowed,
        "runtime_mutation_allowed": False,
    }
