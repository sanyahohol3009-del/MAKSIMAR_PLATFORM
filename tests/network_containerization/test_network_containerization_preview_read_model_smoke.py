from __future__ import annotations

import pytest

from tools.monitor.runtime_input.network_containerization_terminal_preview import (
    NetworkContainerizationPreviewReadModel,
    build_network_containerization_preview_read_model,
)


def test_network_containerization_preview_read_model_shows_blocked_edges_and_missing_contracts() -> None:
    preview = build_network_containerization_preview_read_model()

    assert "production_deployment" in preview.blocked_edges
    assert "public_exposure" in preview.blocked_edges
    assert isinstance(preview.missing_contract_paths, tuple)
    assert preview.xray_layer_id == "NETWORK_CONTAINERIZATION"
    assert preview.xray_non_regression_required is True
    assert preview.drift_guard_required is True


def test_network_containerization_preview_read_model_rejects_deployment_allowed_now() -> None:
    preview = build_network_containerization_preview_read_model()

    with pytest.raises(ValueError, match="deployment_allowed_now"):
        NetworkContainerizationPreviewReadModel(
            read_model_id=preview.read_model_id,
            layer_id=preview.layer_id,
            dashboard_safe=True,
            read_only=True,
            deployment_allowed_now=True,
            public_exposure_allowed=False,
            runtime_network_mutation_allowed=False,
            active_docker_deployment_allowed=False,
            active_compose_deployment_allowed=False,
            blocked_edges=preview.blocked_edges,
            expected_contract_paths=preview.expected_contract_paths,
            present_contract_paths=preview.present_contract_paths,
            missing_contract_paths=preview.missing_contract_paths,
            xray_layer_id=preview.xray_layer_id,
            xray_non_regression_required=True,
            drift_guard_required=True,
            provenance_index_update_considered=True,
            reason_codes=("bad",),
        )
