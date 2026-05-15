from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.architecture_map.architecture_radar import (
    DEFAULT_BLUEPRINT_PATH,
    PROJECT_ROOT,
    assert_architecture_is_clean,
    build_architecture_report,
    load_blueprint,
)


def test_architecture_blueprint_json_is_valid() -> None:
    blueprint = load_blueprint(DEFAULT_BLUEPRINT_PATH)

    assert blueprint["blueprint_id"] == "MAKSIMAR_PLATFORM_FULL_CONSOLIDATED_SKELETON_vFINAL_FREEZE"
    assert isinstance(blueprint["layers"], list)
    assert len(blueprint["layers"]) >= 12


def test_architecture_radar_can_build_report() -> None:
    report = build_architecture_report(
        project_root=PROJECT_ROOT,
        blueprint_path=DEFAULT_BLUEPRINT_PATH,
    )

    assert report.blueprint_id == "MAKSIMAR_PLATFORM_FULL_CONSOLIDATED_SKELETON_vFINAL_FREEZE"
    assert report.layer_statuses

    layer_ids = {layer.layer_id for layer in report.layer_statuses}
    assert "CORE_ROOT" in layer_ids
    assert "MAKSIMAR_CORE_LIB" in layer_ids
    assert "PRODUCTS_CUBES" in layer_ids


def test_architecture_structure_and_semantic_drift_guard() -> None:
    assert Path(DEFAULT_BLUEPRINT_PATH).exists()
    assert_architecture_is_clean(
        project_root=PROJECT_ROOT,
        blueprint_path=DEFAULT_BLUEPRINT_PATH,
    )
