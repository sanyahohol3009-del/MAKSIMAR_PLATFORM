from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple

from MAKSIMAR_SERVER.PROPOSAL_AUDIT.proposal_audit_spine_models import (
    build_proposal_audit_spine_contract,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

REQUIRED_PROPOSAL_SURFACES: Tuple[str, ...] = (
    "MAKSIMAR_CORE_LIB/evolution_loop/proposal_models.py",
    "MAKSIMAR_CORE_LIB/evolution_loop/proposal_package_models.py",
    "MAKSIMAR_CORE_LIB/evolution_loop/proposal_package_builder.py",
    "MAKSIMAR_CORE_LIB/evolution_loop/proposal_registry.py",
    "MAKSIMAR_CORE_LIB/evolution_debug/proposal_models.py",
    "MAKSIMAR_CORE_LIB/evolution_debug/proposal_contract.py",
)


def _missing(paths: Tuple[str, ...]) -> Tuple[str, ...]:
    return tuple(path for path in paths if not (PROJECT_ROOT / path).exists())


def build_proposal_inspector_binding() -> Dict[str, object]:
    contract = build_proposal_audit_spine_contract()
    missing = _missing(REQUIRED_PROPOSAL_SURFACES)

    binding_ready = (
        contract.proposal_visible is True
        and contract.code_write_allowed is False
        and contract.action_execution_allowed is False
        and missing == ()
    )

    return {
        "binding_id": "proposal_inspector_binding_phase_6_2_001",
        "binding_ready": binding_ready,
        "required_surfaces": REQUIRED_PROPOSAL_SURFACES,
        "missing_surfaces": missing,
        "proposal_visible": contract.proposal_visible,
        "proposal_package_readable": True,
        "proposal_registry_readable": True,
        "proposal_execution_allowed": False,
        "code_write_allowed": contract.code_write_allowed,
        "action_execution_allowed": contract.action_execution_allowed,
        "runtime_mutation_allowed": False,
    }
