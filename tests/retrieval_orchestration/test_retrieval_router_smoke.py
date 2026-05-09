from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    build_retrieval_route_plan,
)


def test_retrieval_router_smoke() -> None:
    route_plan = build_retrieval_route_plan()

    assert route_plan.route_ready is True
    assert route_plan.policy_gate_passed is True
    assert route_plan.selected_source_count == len(route_plan.selected_sources)
    assert route_plan.evidence_item_count == route_plan.evidence_pack.total_items
