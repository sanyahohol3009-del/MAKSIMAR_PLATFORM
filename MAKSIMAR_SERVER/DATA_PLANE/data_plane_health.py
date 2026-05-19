from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.data_plane.data_plane_read_model import DataPlaneHealthReadModel


REQUIRED_DATA_PLANE_PATHS: tuple[str, ...] = (
    "DATA_PLANE",
    "MAKSIMAR_CORE_LIB/data_plane",
    "MAKSIMAR_SERVER/DATA_PLANE",
)


def build_data_plane_health_read_model(project_root: Path) -> DataPlaneHealthReadModel:
    if not isinstance(project_root, Path):
        raise TypeError("project_root must be pathlib.Path")

    checked_paths = tuple(str(project_root / rel_path) for rel_path in REQUIRED_DATA_PLANE_PATHS)
    missing_paths = tuple(
        str(project_root / rel_path)
        for rel_path in REQUIRED_DATA_PLANE_PATHS
        if not (project_root / rel_path).exists()
    )
    health_ok = len(missing_paths) == 0

    return DataPlaneHealthReadModel(
        layer_id="DATA_PLANE",
        status="ready" if health_ok else "degraded",
        checked_paths=checked_paths,
        missing_paths=missing_paths,
        health_ok=health_ok,
        reason_codes=(
            "data_plane_required_paths_present"
            if health_ok
            else "data_plane_required_paths_missing",
        ),
    )
