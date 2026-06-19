from __future__ import annotations

from MAKSIMAR_CORE_LIB.action_library_adapters.action_capability_inventory_read_model import (
    build_action_capability_inventory_read_model,
)


def test_action_capability_inventory_read_model_smoke() -> None:
    inventory = build_action_capability_inventory_read_model().to_read_model()
    capability_ids = tuple(capability["capability_id"] for capability in inventory["capabilities"])

    assert capability_ids == ("browser_worker", "gui_worker", "cli_worker", "cad_cam_worker")
    assert inventory["safe_direct_capabilities"] == ("browser_worker",)
    assert "cli_worker" in inventory["risk_gated_capabilities"]
