from __future__ import annotations

from pathlib import Path

import pytest

from MAKSIMAR_CORE_LIB.capability_registry.capability_registry_loader import (
    DEFAULT_CAPABILITY_REGISTRY_YAML_PATH,
    load_canonical_capability_registry,
)


def test_capability_registry_loader_smoke() -> None:
    result = load_canonical_capability_registry()

    assert result.source_path == DEFAULT_CAPABILITY_REGISTRY_YAML_PATH.as_posix()
    assert result.schema_version == "canonical_capability_registry.v1"
    assert result.registry_id == "phase_1_canonical_capability_registry"
    assert result.contract.total_capabilities >= 6
    assert result.missing_from_yaml == ()
    assert result.extra_in_yaml == ()

    assert result.direct_core_import_allowed is False
    assert result.source_of_truth_override_allowed is False
    assert result.runtime_mutation_allowed is False
    assert result.dashboard_read_only is True
    assert result.active_deployment_created is False
    assert result.ports_opened is False
    assert result.containers_started is False
    assert result.read_only_load is True


def test_capability_registry_loader_rejects_noncanonical_source_by_default(
    tmp_path: Path,
) -> None:
    candidate = tmp_path / "canonical_capability_registry_v1.yaml"
    candidate.write_text(
        DEFAULT_CAPABILITY_REGISTRY_YAML_PATH.read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        load_canonical_capability_registry(candidate)


def test_capability_registry_loader_rejects_missing_yaml_capability(
    tmp_path: Path,
) -> None:
    text = DEFAULT_CAPABILITY_REGISTRY_YAML_PATH.read_text(encoding="utf-8")
    text = text.replace(
        "  - capability_id: cap_worker_runtime_surface\n",
        "",
    )

    candidate = tmp_path / "canonical_capability_registry_v1.yaml"
    candidate.write_text(text, encoding="utf-8")

    with pytest.raises(ValueError):
        load_canonical_capability_registry(
            candidate,
            allow_noncanonical_source=True,
        )


def test_capability_registry_loader_rejects_pyc_source() -> None:
    with pytest.raises(ValueError):
        load_canonical_capability_registry(Path("__pycache__/bad.pyc"))
