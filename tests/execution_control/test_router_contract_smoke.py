from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_control.router_contract import (
    build_execution_router_contract,
)


def test_router_contract_builds() -> None:
    contract = build_execution_router_contract()

    assert contract.total_routes == 2
    assert len(contract.routes) == 2


def test_router_contract_contains_allowed_route() -> None:
    contract = build_execution_router_contract()

    assert any(route.route_allowed for route in contract.routes)
