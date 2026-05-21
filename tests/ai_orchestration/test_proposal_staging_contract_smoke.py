from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.ai_orchestration.proposal_staging_contract import (
    ProposalStagingContract,
    build_default_proposal_staging_contract,
)


def test_default_proposal_staging_contract_is_proposal_only() -> None:
    contract = build_default_proposal_staging_contract()

    assert contract.proposal_id == "ai_orchestration_proposal_v1"
    assert contract.proposal_only is True
    assert contract.owner_approval_required is True
    assert contract.apply_allowed is False
    assert contract.auto_apply_allowed is False
    assert contract.execution_allowed is False
    assert contract.runtime_mutation_allowed is False
    assert contract.dashboard_safe is True
    assert contract.read_only is True


def test_proposal_staging_contract_rejects_apply_allowed() -> None:
    with pytest.raises(ValueError, match="apply_allowed"):
        ProposalStagingContract(
            proposal_id="bad",
            source_request_id="model_request_v1",
            proposal_payload_ref="payload",
            proposal_only=True,
            owner_approval_required=True,
            apply_allowed=True,
            auto_apply_allowed=False,
            execution_allowed=False,
            runtime_mutation_allowed=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )


def test_proposal_staging_contract_rejects_auto_apply_allowed() -> None:
    with pytest.raises(ValueError, match="auto_apply_allowed"):
        ProposalStagingContract(
            proposal_id="bad",
            source_request_id="model_request_v1",
            proposal_payload_ref="payload",
            proposal_only=True,
            owner_approval_required=True,
            apply_allowed=False,
            auto_apply_allowed=True,
            execution_allowed=False,
            runtime_mutation_allowed=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )
