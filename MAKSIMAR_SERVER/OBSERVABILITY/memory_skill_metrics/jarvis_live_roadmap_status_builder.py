from __future__ import annotations

from pathlib import Path
from typing import Any

from MAKSIMAR_CORE_LIB.ai_orchestration.jarvis_live_roadmap_expected_files_contract import (
    FORBIDDEN_PARALLEL_WORLD_ROOTS,
    JARVIS_LIVE_ROADMAP_EXPECTED_FILES,
    JARVIS_LIVE_REQUIRED_EXISTING_SURFACES,
)


def build_jarvis_live_roadmap_status(
    repo_root: Path | None = None,
) -> dict[str, Any]:
    root = Path.cwd() if repo_root is None else repo_root

    expected_entries = JARVIS_LIVE_ROADMAP_EXPECTED_FILES
    expected_paths = tuple(entry["path"] for entry in expected_entries)
    existing_paths = tuple(path for path in expected_paths if (root / path).exists())
    missing_paths = tuple(path for path in expected_paths if not (root / path).exists())

    existing_required_surfaces = tuple(
        surface
        for surface in JARVIS_LIVE_REQUIRED_EXISTING_SURFACES
        if (root / surface).exists()
    )
    missing_required_surfaces = tuple(
        surface
        for surface in JARVIS_LIVE_REQUIRED_EXISTING_SURFACES
        if not (root / surface).exists()
    )
    forbidden_roots_present = tuple(
        root_path
        for root_path in FORBIDDEN_PARALLEL_WORLD_ROOTS
        if (root / root_path).exists()
    )

    roadmap_ready = (
        len(missing_paths) == 0
        and len(missing_required_surfaces) == 0
        and len(forbidden_roots_present) == 0
    )

    return {
        "summary_id": "jarvis_live_roadmap_status_v0_1",
        "roadmap_id": "JARVIS-LIVE",
        "batch_id": "JL-0",
        "status": "ready" if roadmap_ready else "blocked",
        "expected_file_count": len(expected_paths),
        "existing_expected_file_count": len(existing_paths),
        "missing_expected_file_count": len(missing_paths),
        "expected_paths": expected_paths,
        "existing_expected_paths": existing_paths,
        "missing_expected_paths": missing_paths,
        "required_existing_surfaces": JARVIS_LIVE_REQUIRED_EXISTING_SURFACES,
        "existing_required_surfaces": existing_required_surfaces,
        "missing_required_surfaces": missing_required_surfaces,
        "forbidden_parallel_world_roots": FORBIDDEN_PARALLEL_WORLD_ROOTS,
        "forbidden_parallel_world_roots_present": forbidden_roots_present,
        "no_parallel_world_guard_ready": len(forbidden_roots_present) == 0,
        "roadmap_ready": roadmap_ready,
        "read_only": True,
        "dashboard_safe": True,
        "runtime_start_allowed": False,
        "model_download_allowed": False,
        "microphone_enabled": False,
        "stt_runtime_enabled": False,
        "tts_playback_enabled": False,
        "app_control_allowed": False,
        "shell_control_allowed": False,
        "reason_codes": (
            "jarvis_live_roadmap_read_model_only",
            "existing_surfaces_must_be_extended",
            "parallel_world_roots_forbidden",
        ),
    }
