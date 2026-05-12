from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.SANDBOX_REVIEW.evaluation_result_reader import build_evaluation_result_reader
from MAKSIMAR_SERVER.SANDBOX_REVIEW.owner_review_package_builder import build_owner_review_package
from MAKSIMAR_SERVER.SANDBOX_REVIEW.sandbox_binding_models import build_sandbox_binding
from MAKSIMAR_SERVER.SANDBOX_REVIEW.sandbox_result_reader import build_sandbox_result_reader
from MAKSIMAR_SERVER.SANDBOX_REVIEW.sandbox_review_models import build_sandbox_review_contract
from MAKSIMAR_SERVER.SANDBOX_REVIEW.simulation_result_reader import build_simulation_result_reader


def build_sandbox_owner_review_preview() -> Dict[str, object]:
    contract = build_sandbox_review_contract()
    binding = build_sandbox_binding()
    sandbox = build_sandbox_result_reader()
    simulation = build_simulation_result_reader()
    evaluation = build_evaluation_result_reader()
    owner_review = build_owner_review_package()

    preview_path = (
        "sandbox_binding",
        "sandbox_result_reader",
        "simulation_result_reader",
        "evaluation_result_reader",
        "owner_review_package",
        "self_expansion_next_only",
    )

    preview_ready = (
        contract.sandbox_review_ready
        and binding["sandbox_binding_ready"] is True
        and sandbox["sandbox_result_reader_ready"] is True
        and simulation["simulation_result_reader_ready"] is True
        and evaluation["evaluation_result_reader_ready"] is True
        and owner_review["owner_review_package_ready"] is True
    )

    return {
        "preview_id": "sandbox_owner_review_preview_phase_6_4_001",
        "preview_ready": preview_ready,
        "preview_path": preview_path,
        "sandbox_binding": binding,
        "sandbox_result": sandbox,
        "simulation_result": simulation,
        "evaluation_result": evaluation,
        "owner_review": owner_review,
        "direct_core_write_allowed": contract.direct_core_write_allowed,
        "deployment_allowed": contract.deployment_allowed,
        "auto_apply_allowed": contract.auto_apply_allowed,
        "self_expansion_allowed_now": contract.self_expansion_allowed_now,
        "productization_allowed_now": contract.productization_allowed_now,
        "self_expansion_allowed_next": preview_ready,
    }
