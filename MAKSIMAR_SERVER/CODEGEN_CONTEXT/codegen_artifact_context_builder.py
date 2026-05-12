from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple

from MAKSIMAR_SERVER.CODEGEN_CONTEXT.codegen_boundary_models import build_codegen_boundary_contract
from MAKSIMAR_SERVER.CODEGEN_CONTEXT.codegen_intent_models import build_codegen_intent_contract
from MAKSIMAR_SERVER.CODEGEN_CONTEXT.controlled_codegen_models import (
    build_controlled_codegen_context_contract,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

REQUIRED_ARTIFACT_SURFACES: Tuple[str, ...] = (
    "MAKSIMAR_CORE_LIB/artifact_reference_models.py",
    "MAKSIMAR_CORE_LIB/data_plane/artifact_ownership_contract.py",
    "MAKSIMAR_CORE_LIB/data_plane/artifact_retention_contract.py",
    "MAKSIMAR_CORE_LIB/data_plane/artifact_cleanup_contract.py",
    "MAKSIMAR_SERVER/EXECUTION_CONTROL/artifact_routing/artifact_routing_binding.py",
    "MAKSIMAR_SERVER/EXECUTION_CONTROL/artifact_routing/artifact_routing_models.py",
    "MAKSIMAR_SERVER/PROPOSAL_AUDIT/proposal_audit_preview_builder.py",
)


def _missing(paths: Tuple[str, ...]) -> Tuple[str, ...]:
    return tuple(path for path in paths if not (PROJECT_ROOT / path).exists())


def build_codegen_artifact_context() -> Dict[str, object]:
    contract = build_controlled_codegen_context_contract()
    intent = build_codegen_intent_contract()
    boundary = build_codegen_boundary_contract()
    missing = _missing(REQUIRED_ARTIFACT_SURFACES)

    artifact_context_ready = (
        contract.artifact_context_ready
        and intent.intent_contract_ready
        and boundary.artifact_reference_required
        and missing == ()
    )

    return {
        "artifact_context_id": "codegen_artifact_context_phase_6_3_001",
        "artifact_context_ready": artifact_context_ready,
        "required_surfaces": REQUIRED_ARTIFACT_SURFACES,
        "missing_surfaces": missing,
        "artifact_reference_required": boundary.artifact_reference_required,
        "artifact_ownership_required": True,
        "artifact_retention_required": True,
        "artifact_cleanup_required": True,
        "artifact_routing_visible": True,
        "direct_core_write_allowed": contract.direct_core_write_allowed,
        "deployment_allowed": contract.deployment_allowed,
        "sandbox_execution_allowed_now": contract.sandbox_execution_allowed_now,
        "runtime_mutation_allowed": False,
    }
