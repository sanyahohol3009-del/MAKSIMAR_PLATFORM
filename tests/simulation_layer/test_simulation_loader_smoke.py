from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.simulation_layer.simulation_loader import (
    load_simulation_definition,
)


def test_simulation_loader_rejects_missing_schema_version(tmp_path: Path) -> None:
    """Simulation loader should reject missing schema_version."""
    file_path = tmp_path / "simulation_request.v1.yaml"
    file_path.write_text(
        "\n".join(
            [
                "contract_name: simulation_request",
                "description: test",
            ]
        ),
        encoding="utf-8",
    )

    result = load_simulation_definition(file_path)

    assert result.is_valid is False
    assert result.definition is None
    assert result.error is not None


def test_simulation_loader_accepts_valid_definition(tmp_path: Path) -> None:
    """Simulation loader should accept valid simulation definition."""
    file_path = tmp_path / "simulation_request.v1.yaml"
    file_path.write_text(
        "\n".join(
            [
                "contract_name: simulation_request",
                "schema_version: simulation_request.v1",
                "description: test",
            ]
        ),
        encoding="utf-8",
    )

    result = load_simulation_definition(file_path)

    assert result.is_valid is True
    assert result.definition is not None
    assert result.definition.request_id == "simulation_request"
    assert result.definition.version == "simulation_request.v1"
