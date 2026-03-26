from __future__ import annotations

from MAKSIMAR_CORE_LIB.mobile_bridge.bridge_shell_models import (
    MobileBridgeShellContract,
)
from MAKSIMAR_CORE_LIB.mobile_bridge.request_models import (
    MobileRequestContract,
)
from MAKSIMAR_CORE_LIB.mobile_bridge.result_contract import (
    build_task_result_contract,
)
from MAKSIMAR_CORE_LIB.mobile_bridge.task_contract import (
    build_task_envelope_contract,
)


def build_mobile_request_contract() -> MobileRequestContract:
    """Build canonical mobile request contract."""
    from MAKSIMAR_CORE_LIB.mobile_bridge.request_models import MobileRequest

    requests = (
        MobileRequest(
            request_id="mobile_req_001",
            client_type="android",
            request_type="query",
            payload_ref="payload_001",
            core_write_allowed=False,
            heavy_execution_allowed=False,
        ),
        MobileRequest(
            request_id="mobile_req_002",
            client_type="android",
            request_type="status_check",
            payload_ref="payload_002",
            core_write_allowed=False,
            heavy_execution_allowed=False,
        ),
    )

    return MobileRequestContract(
        total_requests=len(requests),
        requests=requests,
    )


def build_mobile_bridge_shell_contract() -> MobileBridgeShellContract:
    """Build final mobile bridge shell contract."""
    request_contract = build_mobile_request_contract()
    envelope_contract = build_task_envelope_contract()
    result_contract = build_task_result_contract()

    return MobileBridgeShellContract(
        shell_id="mobile_bridge_shell",
        total_requests=request_contract.total_requests,
        total_envelopes=envelope_contract.total_envelopes,
        total_results=result_contract.total_results,
        core_write_allowed=False,
        heavy_execution_allowed_on_mobile=False,
    )
