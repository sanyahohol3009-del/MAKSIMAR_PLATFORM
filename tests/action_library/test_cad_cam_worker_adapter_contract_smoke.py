from __future__ import annotations

from MAKSIMAR_CORE_LIB.action_library_adapters.cad_cam_worker_adapter_contract import (
    build_cad_cam_worker_adapter_contract,
)


def test_cad_cam_worker_adapter_contract_smoke() -> None:
    contract = build_cad_cam_worker_adapter_contract().to_read_model()

    assert contract["capability_id"] == "cad_cam_worker"
    assert contract["risk_class"] == "risk_gate"
    assert "machine_control" in contract["side_effects"]
