from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_chart_backend_contract import (
    build_visual_chart_backend_contract,
)


def test_visual_chart_backend_contract_builds() -> None:
    contract = build_visual_chart_backend_contract()

    assert contract.contract_id == "visual_chart_backend_contract_001"
    assert contract.backend_id == "visual_backend_chart_001"
    assert contract.chart_backend_name == "echarts_adapter_backend"
    assert contract.supports_line_series is True
    assert contract.supports_status_series is True
    assert contract.supports_multi_series is True
    assert contract.supports_responsive_rendering is True
