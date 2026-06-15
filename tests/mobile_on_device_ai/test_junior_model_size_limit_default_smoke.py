from __future__ import annotations

from MAKSIMAR_CORE_LIB.mobile_bridge.junior_model_policy_contract import (
    build_junior_model_policy_contract,
)


def test_junior_model_size_limit_default_is_conservative() -> None:
    read_model = build_junior_model_policy_contract().to_read_model()

    assert read_model["junior_model_size_limit_default_enabled"] is True
    assert isinstance(read_model["junior_model_size_limit_mb"], int)
    assert read_model["junior_model_size_limit_mb"] > 0
    assert read_model["junior_model_size_limit_mb"] <= 1024
    assert read_model["model_download_allowed"] is False
