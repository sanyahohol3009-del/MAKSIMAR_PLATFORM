from __future__ import annotations

from pathlib import Path
from typing import Any

from MAKSIMAR_CORE_LIB.shared_services.atomic_io import AtomicIOError, safe_read_yaml
from MAKSIMAR_CORE_LIB.shared_services.path_resolver import PATHS
from MAKSIMAR_CORE_LIB.simulation_layer.simulation_models import (
    SimulationLoadResult,
    SimulationRequestDefinition,
)


def collect_simulation_files() -> list[Path]:
    """Collect simulation contract files."""
    root = PATHS.simulation_contracts
    if not root.exists() or not root.is_dir():
        return []

    return sorted(
        [
            path
            for path in root.glob("*.yaml")
            if path.is_file()
        ]
    )


def _extract_request_id(payload: dict[str, Any], file_path: Path) -> str | None:
    """Extract canonical simulation request id from payload or filename."""
    request_id = payload.get("request_id")
    if isinstance(request_id, str) and request_id.strip():
        return request_id.strip()

    contract_name = payload.get("contract_name")
    if isinstance(contract_name, str) and contract_name.strip():
        return contract_name.strip()

    return file_path.name.removesuffix(".yaml")


def load_simulation_definition(file_path: Path) -> SimulationLoadResult:
    """Load one simulation definition from contract YAML."""
    try:
        payload = safe_read_yaml(file_path)
    except AtomicIOError as exc:
        return SimulationLoadResult(
            definition=None,
            is_valid=False,
            error=f"Failed to read simulation file: {exc}",
        )

    schema_version = payload.get("schema_version")
    if not isinstance(schema_version, str) or not schema_version.strip():
        return SimulationLoadResult(
            definition=None,
            is_valid=False,
            error="Simulation definition must contain non-empty 'schema_version'.",
        )

    request_id = _extract_request_id(payload, file_path)
    if request_id is None:
        return SimulationLoadResult(
            definition=None,
            is_valid=False,
            error="Unable to derive request_id.",
        )

    definition = SimulationRequestDefinition(
        request_id=request_id,
        version=schema_version.strip(),
        file_path=file_path,
        payload=payload,
    )

    return SimulationLoadResult(
        definition=definition,
        is_valid=True,
    )


def load_all_simulation_definitions() -> list[SimulationLoadResult]:
    """Load all simulation definitions."""
    return [load_simulation_definition(file_path) for file_path in collect_simulation_files()]
