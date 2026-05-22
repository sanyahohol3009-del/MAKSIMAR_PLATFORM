from __future__ import annotations

from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_layers_final_acceptance_read_model import (
    build_foundation_layers_final_acceptance_read_model,
)


def test_all_foundation_layers_have_dashboard_visibility() -> None:
    read_model = build_foundation_layers_final_acceptance_read_model()

    assert read_model.total_layers == 5
    assert read_model.dashboard_visible_layers == 5
    assert read_model.all_foundation_layers_have_dashboard_visibility is True
    assert read_model.dashboard_visibility.dashboard_visibility_mandatory is True
    assert read_model.dashboard_visibility.all_foundation_layers_dashboard_visible is True
    assert read_model.dashboard_mutation_allowed is False
    assert read_model.dashboard_visibility.dashboard_control_allowed is False

    for entry in read_model.acceptance_entries:
        assert entry.has_dashboard_visibility is True
        assert entry.dashboard_mutation_allowed is False
