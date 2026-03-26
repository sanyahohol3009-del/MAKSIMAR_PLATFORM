from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_control.admission_models import (
    AdmissionContract,
    AdmissionDecision,
)


def build_admission_contract() -> AdmissionContract:
    """Build unified admission control contract."""

    decisions = (
        AdmissionDecision(
            request_id="req_001",
            admitted=True,
            reason="resources_available",
            policy_checked=True,
        ),
        AdmissionDecision(
            request_id="req_002",
            admitted=False,
            reason="queue_pressure",
            policy_checked=True,
        ),
    )

    return AdmissionContract(
        total_decisions=len(decisions),
        decisions=decisions,
    )
