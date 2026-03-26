from __future__ import annotations

from MAKSIMAR_CORE_LIB.observability_contracts import (
    build_observability_shapes_contract,
)


def test_observability_shapes_contract_builds() -> None:
    """Observability shapes contract should build successfully."""
    contract = build_observability_shapes_contract()

    assert contract.total_shapes == 3
    assert len(contract.shapes) == 3


def test_observability_shapes_contract_contains_expected_event_kinds() -> None:
    """Observability shapes contract should expose expected event kinds."""
    contract = build_observability_shapes_contract()

    assert contract.shapes[0].event_kind == "validation_event"
    assert contract.shapes[1].event_kind == "pressure_event"
    assert contract.shapes[2].event_kind == "payload_event"


def test_observability_shapes_contract_preserves_expected_requirements() -> None:
    """Observability shapes should preserve expected trace/timestamp semantics."""
    contract = build_observability_shapes_contract()

    validation = contract.shapes[0]
    pressure = contract.shapes[1]
    payload = contract.shapes[2]

    assert validation.requires_trace_id is True
    assert validation.requires_timestamp is True
    assert validation.supports_alerting is True

    assert pressure.requires_trace_id is True
    assert pressure.requires_timestamp is True
    assert pressure.supports_alerting is True

    assert payload.requires_trace_id is True
    assert payload.requires_timestamp is True
    assert payload.supports_alerting is False
