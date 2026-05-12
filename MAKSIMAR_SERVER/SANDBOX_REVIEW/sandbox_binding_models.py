from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple

from MAKSIMAR_SERVER.CODEGEN_CONTEXT import build_codegen_preview
from MAKSIMAR_SERVER.SANDBOX_REVIEW.sandbox_review_models import build_sandbox_review_contract


PROJECT_ROOT = Path(__file__).resolve().parents[2]

REQUIRED_SANDBOX_BINDING_SURFACES: Tuple[str, ...] = (
    "MAKSIMAR_CORE_LIB/evolution_debug/sandbox_contract.py",
    "MAKSIMAR_CORE_LIB/evolution_debug/sandbox_models.py",
    "MAKSIMAR_CORE_LIB/evolution_debug/patch_contract.py",
    "MAKSIMAR_CORE_LIB/evolution_debug/patch_models.py",
    "MAKSIMAR_SERVER/CODEGEN_CONTEXT/codegen_preview_builder.py",
    "MAKSIMAR_SERVER/PROPOSAL_AUDIT/proposal_audit_preview_builder.py",
    "MAKSIMAR_SERVER/EXECUTION_CONTROL/artifact_routing/artifact_routing_binding.py",
)


def _missing(paths: Tuple[str, ...]) -> Tuple[str, ...]:
    return tuple(path for path in paths if not (PROJECT_ROOT / path).exists())


def build_sandbox_binding() -> Dict[str, object]:
    contract = build_sandbox_review_contract()
    codegen_preview = build_codegen_preview()
    missing = _missing(REQUIRED_SANDBOX_BINDING_SURFACES)

    sandbox_binding_ready = (
        contract.sandbox_binding_ready
        and codegen_preview["preview_ready"] is True
        and codegen_preview["sandbox_owner_review_allowed_next"] is True
        and missing == ()
    )

    return {
        "sandbox_binding_id": "sandbox_binding_phase_6_4_001",
        "sandbox_binding_ready": sandbox_binding_ready,
        "required_surfaces": REQUIRED_SANDBOX_BINDING_SURFACES,
        "missing_surfaces": missing,
        "source_codegen_preview_id": codegen_preview["preview_id"],
        "sandbox_contract_visible": True,
        "patch_contract_visible": True,
        "artifact_routing_visible": True,
        "sandbox_execution_started_here": False,
        "direct_core_write_allowed": contract.direct_core_write_allowed,
        "deployment_allowed": contract.deployment_allowed,
        "auto_apply_allowed": contract.auto_apply_allowed,
        "runtime_mutation_allowed": False,
    }
