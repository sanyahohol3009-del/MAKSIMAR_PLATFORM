from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple

from MAKSIMAR_SERVER.PROPOSAL_AUDIT.proposal_audit_spine_models import (
    build_proposal_audit_spine_contract,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

REQUIRED_AUDIT_SURFACES: Tuple[str, ...] = (
    "MAKSIMAR_CORE_LIB/evolution_debug/ranking_contract.py",
    "MAKSIMAR_CORE_LIB/evolution_debug/ranking_models.py",
    "MAKSIMAR_CORE_LIB/evolution_debug/patch_contract.py",
    "MAKSIMAR_CORE_LIB/evolution_debug/patch_models.py",
    "MAKSIMAR_CORE_LIB/evolution_debug/sandbox_contract.py",
    "MAKSIMAR_CORE_LIB/evolution_debug/sandbox_models.py",
    "docs/security_governance/governed_action_model/PROPOSAL_TO_ACTION_TRANSITION_v1.md",
    "docs/security_governance/governed_action_model/WRITE_APPLY_BOUNDARY_v1.md",
)


def _missing(paths: Tuple[str, ...]) -> Tuple[str, ...]:
    return tuple(path for path in paths if not (PROJECT_ROOT / path).exists())


def build_audit_inspector_binding() -> Dict[str, object]:
    contract = build_proposal_audit_spine_contract()
    missing = _missing(REQUIRED_AUDIT_SURFACES)

    binding_ready = (
        contract.audit_visible is True
        and missing == ()
        and contract.sandbox_execution_allowed_now is False
        and contract.code_write_allowed is False
    )

    return {
        "binding_id": "audit_inspector_binding_phase_6_2_001",
        "binding_ready": binding_ready,
        "required_surfaces": REQUIRED_AUDIT_SURFACES,
        "missing_surfaces": missing,
        "audit_visible": contract.audit_visible,
        "ranking_visible": True,
        "patch_contract_visible": True,
        "sandbox_contract_visible_read_only": True,
        "sandbox_execution_allowed_now": contract.sandbox_execution_allowed_now,
        "code_write_allowed": contract.code_write_allowed,
        "action_execution_allowed": contract.action_execution_allowed,
        "runtime_mutation_allowed": False,
    }
