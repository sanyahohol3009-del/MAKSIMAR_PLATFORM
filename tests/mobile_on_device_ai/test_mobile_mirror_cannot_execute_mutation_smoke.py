from __future__ import annotations

from MAKSIMAR_CORE_LIB.mobile_bridge.mobile_core_mirror_contract import (
    build_mobile_core_mirror_contract,
)


def test_mobile_mirror_cannot_execute_or_mutate() -> None:
    read_model = build_mobile_core_mirror_contract().to_read_model()

    assert read_model["mirror_can_execute_actions"] is False
    assert read_model["mirror_can_write_core"] is False
    assert read_model["mirror_can_write_memory"] is False
    assert read_model["mirror_can_mutate_runtime"] is False
    assert read_model["mirror_can_deploy"] is False
    assert read_model["mirror_can_control_pc"] is False
    assert read_model["mirror_can_control_phone"] is False
    assert read_model["mirror_can_bypass_approval"] is False
