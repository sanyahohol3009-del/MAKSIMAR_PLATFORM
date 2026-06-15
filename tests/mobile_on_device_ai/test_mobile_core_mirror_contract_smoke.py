from __future__ import annotations

from MAKSIMAR_CORE_LIB.mobile_bridge.mobile_core_mirror_contract import (
    build_mobile_core_mirror_contract,
)


def test_mobile_core_mirror_contract_is_context_only() -> None:
    read_model = build_mobile_core_mirror_contract().to_read_model()

    assert read_model["mirror_is_read_only"] is True
    assert read_model["mirror_is_app_safe"] is True
    assert read_model["mirror_is_canonical_truth"] is False
    assert read_model["junior_consumes_mirror_as_context"] is True
    assert read_model["junior_cannot_promote_mirror_to_truth"] is True
