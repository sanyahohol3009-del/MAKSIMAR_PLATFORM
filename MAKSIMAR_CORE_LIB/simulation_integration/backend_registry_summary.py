from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.shared_services.atomic_io import safe_read_yaml
from MAKSIMAR_CORE_LIB.shared_services.path_resolver import PATHS
from MAKSIMAR_CORE_LIB.simulation_integration.backend_models import (
    SimulationBackendRecord,
    SimulationBackendSummary,
)


def _collect_backend_files() -> list[Path]:
    """Collect simulation backend config files."""
    root = PATHS.simulation_layer / "config"
    if not root.exists() or not root.is_dir():
        return []

    return sorted(
        [
            path
            for path in root.glob("backend_*.yaml")
            if path.is_file()
        ]
    )


def _extract_backend_id(payload: dict, file_path: Path) -> str:
    """Extract canonical backend id from payload or filename."""
    schema_version = payload.get("schema_version")
    if isinstance(schema_version, str) and schema_version.strip():
        return schema_version.strip().split(".v", maxsplit=1)[0]

    return f"simulation_{file_path.stem}"


def build_simulation_backend_summary() -> SimulationBackendSummary:
    """Build unified simulation backend summary from backend config files."""
    records: list[SimulationBackendRecord] = []

    for file_path in _collect_backend_files():
        payload = safe_read_yaml(file_path)
        backend_id = _extract_backend_id(payload, file_path)
        version = payload.get("schema_version", f"{backend_id}.v1")

        records.append(
            SimulationBackendRecord(
                backend_id=backend_id,
                version=version,
                source_definition_id=file_path.stem,
            )
        )

    return SimulationBackendSummary(
        total_backends=len(records),
        records=records,
    )
