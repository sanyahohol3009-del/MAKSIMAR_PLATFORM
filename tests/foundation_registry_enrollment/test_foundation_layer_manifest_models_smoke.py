from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.foundation_registry_enrollment.foundation_layer_manifest_models import (
    FOUNDATION_LAYER_IDS,
    FoundationLayerManifestModel,
    build_default_foundation_layer_manifests,
    build_foundation_layer_manifest_model,
)


def test_default_foundation_layer_manifests_cover_all_layers() -> None:
    manifests = build_default_foundation_layer_manifests()

    assert tuple(item.layer_id for item in manifests) == FOUNDATION_LAYER_IDS
    assert all(item.registry_enrollment_required is True for item in manifests)
    assert all(item.closed_before_registry_enrollment is True for item in manifests)
    assert all(item.runtime_mutation_allowed is False for item in manifests)
    assert all(item.registry_write_allowed is False for item in manifests)
    assert all(item.auto_enrollment_write_allowed is False for item in manifests)
    assert all(item.dashboard_safe is True for item in manifests)
    assert all(item.read_only is True for item in manifests)


def test_foundation_layer_manifest_builder_returns_expected_layer() -> None:
    manifest = build_foundation_layer_manifest_model("ai_orchestration")

    assert manifest.layer_id == "ai_orchestration"
    assert manifest.title == "AI Orchestration"
    assert manifest.canonical_path == "MAKSIMAR_CORE_LIB/ai_orchestration"
    assert manifest.phase_id == "PHASE_5_AI_ORCHESTRATION"
    assert manifest.foundation_sequence == 5


def test_foundation_layer_manifest_rejects_runtime_mutation() -> None:
    with pytest.raises(ValueError, match="runtime_mutation_allowed"):
        FoundationLayerManifestModel(
            layer_id="ai_orchestration",
            title="AI Orchestration",
            canonical_path="MAKSIMAR_CORE_LIB/ai_orchestration",
            phase_id="PHASE_5_AI_ORCHESTRATION",
            foundation_sequence=5,
            registry_enrollment_required=True,
            closed_before_registry_enrollment=True,
            runtime_mutation_allowed=True,
            registry_write_allowed=False,
            auto_enrollment_write_allowed=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )


def test_foundation_layer_manifest_rejects_registry_write() -> None:
    with pytest.raises(ValueError, match="registry_write_allowed"):
        FoundationLayerManifestModel(
            layer_id="security_layer",
            title="Security Layer",
            canonical_path="MAKSIMAR_CORE_LIB/security_layer",
            phase_id="PHASE_1_SECURITY_LAYER",
            foundation_sequence=1,
            registry_enrollment_required=True,
            closed_before_registry_enrollment=True,
            runtime_mutation_allowed=False,
            registry_write_allowed=True,
            auto_enrollment_write_allowed=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )
