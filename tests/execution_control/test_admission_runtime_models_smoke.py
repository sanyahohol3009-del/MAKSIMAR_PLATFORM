from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_control import (
    AdmissionRuntimeContract,
    AdmissionRuntimeState,
)


def test_admission_runtime_models_build() -> None:
    """Admission runtime models should build successfully."""
    contract = AdmissionRuntimeContract(
        total_requests=2,
        requests=(
            AdmissionRuntimeState(
                request_id="req_001",
                admitted=True,
                denial_reason="",
                policy_checked=True,
            ),
            AdmissionRuntimeState(
                request_id="req_002",
                admitted=False,
                denial_reason="queue_pressure",
                policy_checked=True,
            ),
        ),
    )

    assert contract.total_requests == 2
    assert len(contract.requests) == 2
    assert contract.requests[0].admitted is True
    assert contract.requests[-1].denial_reason == "queue_pressure"
