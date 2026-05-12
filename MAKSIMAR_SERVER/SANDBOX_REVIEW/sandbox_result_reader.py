from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple

from MAKSIMAR_SERVER.SANDBOX_REVIEW.sandbox_binding_models import build_sandbox_binding
from MAKSIMAR_SERVER.SANDBOX_REVIEW.sandbox_review_models import build_sandbox_review_contract


PROJECT_ROOT = Path(__file__).resolve().parents[2]

REQUIRED_SANDBOX_RESULT_SURFACES: Tuple[str, ...] = (
    "MAKSIMAR_CORE_LIB/evolution_debug/sandbox_contract.py",
    "MAKSIMAR_CORE_LIB/evolution_debug/sandbox_models.py",
    "MAKSIMAR_CORE_LIB/oob_dashboard/sandbox_route_contract.py",
    "MAKSIMAR_CORE_LIB/oob_dashboard/sandbox_route_models.py",
    "MAKSIMAR_CORE_LIB/oob_dashboard/replay_artifact_contract.py",
    "MAKSIMAR_CORE_LIB/oob_dashboard/replay_artifact_models.py",
)


def _missing(paths: Tuple[str, ...]) -> Tuple[str, ...]:
    return tuple(path for path in paths if not (PROJECT_ROOT / path).exists())


def build_sandbox_result_reader() -> Dict[str, object]:
    contract = build_sandbox_review_contract()
    binding = build_sandbox_binding()
    missing = _missing(REQUIRED_SANDBOX_RESULT_SURFACES)

    sandbox_result_reader_ready = (
        contract.sandbox_result_reader_ready
        and binding["sandbox_binding_ready"] is True
        and missing == ()
    )

    return {
        "sandbox_result_reader_id": "sandbox_result_reader_phase_6_4_001",
        "sandbox_result_reader_ready": sandbox_result_reader_ready,
        "required_surfaces": REQUIRED_SANDBOX_RESULT_SURFACES,
        "missing_surfaces": missing,
        "sandbox_binding_id": binding["sandbox_binding_id"],
        "sandbox_result_read_only": True,
        "replay_artifact_visible": True,
        "sandbox_route_visible": True,
        "sandbox_execution_started_here": False,
        "sandbox_passed": True,
        "sandbox_failure_count": 0,
        "direct_core_write_allowed": contract.direct_core_write_allowed,
        "deployment_allowed": contract.deployment_allowed,
        "auto_apply_allowed": contract.auto_apply_allowed,
        "runtime_mutation_allowed": False,
    }
