from __future__ import annotations

from MAKSIMAR_CORE_LIB.mobile_bridge import (
    MobileRequest,
    MobileRequestContract,
)


def test_mobile_request_models_build() -> None:
    """Mobile request models should build successfully."""
    contract = MobileRequestContract(
        total_requests=1,
        requests=(
            MobileRequest(
                request_id="mobile_req_001",
                client_type="android",
                request_type="query",
                payload_ref="payload_001",
                core_write_allowed=False,
                heavy_execution_allowed=False,
            ),
        ),
    )

    assert contract.total_requests == 1
    assert len(contract.requests) == 1
    assert contract.requests[0].client_type == "android"
    assert contract.requests[0].core_write_allowed is False
    assert contract.requests[0].heavy_execution_allowed is False
