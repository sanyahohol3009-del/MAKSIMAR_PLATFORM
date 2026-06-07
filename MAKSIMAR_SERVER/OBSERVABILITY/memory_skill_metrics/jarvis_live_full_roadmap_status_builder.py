from __future__ import annotations

from pathlib import Path
from typing import Any

from MAKSIMAR_CORE_LIB.ai_orchestration.jarvis_live_full_roadmap_contract import (
    DRIFT_COMMAND_HINT,
    FORBIDDEN_PARALLEL_WORLD_ROOTS,
    FULL_AUTO_COMMAND_HINT,
    XRAY_COMMAND_HINT,
    JarvisLiveRoadmapBatch,
    list_jarvis_live_batches,
)


def build_jarvis_live_full_roadmap_status(
    repo_root: Path | None = None,
) -> dict[str, Any]:
    root = Path.cwd() if repo_root is None else repo_root
    batches = list_jarvis_live_batches()
    per_batch_status = tuple(_build_batch_status(root, batch) for batch in batches)

    ready_batches = tuple(
        entry["batch_id"] for entry in per_batch_status if entry["ready"] is True
    )
    blocked_batches = tuple(
        entry["batch_id"] for entry in per_batch_status if entry["ready"] is False
    )
    next_batch = _resolve_next_batch(per_batch_status)

    expected_file_count_total = sum(
        int(entry["expected_file_count"]) for entry in per_batch_status
    )
    existing_file_count_total = sum(
        int(entry["existing_file_count"]) for entry in per_batch_status
    )
    missing_file_count_total = sum(
        int(entry["missing_file_count"]) for entry in per_batch_status
    )

    forbidden_roots_present = tuple(
        root_path
        for root_path in FORBIDDEN_PARALLEL_WORLD_ROOTS
        if (root / root_path).exists()
    )

    storage_boundary_ready = _batch_ready(per_batch_status, "JL-4")
    vendor_boundary_ready = _batch_ready(per_batch_status, "JL-10")
    voice_smoke_visible = _batch_ready(per_batch_status, "JL-11")
    pc_control_gate_ready = _batch_ready(per_batch_status, "JL-14")
    no_parallel_world_guard_ready = len(forbidden_roots_present) == 0

    return {
        "summary_id": "jarvis_live_full_roadmap_status_v0_1",
        "roadmap_id": "JARVIS-LIVE",
        "total_batches": len(batches),
        "ready_batches": ready_batches,
        "blocked_batches": blocked_batches,
        "next_batch": next_batch,
        "expected_file_count_total": expected_file_count_total,
        "existing_file_count_total": existing_file_count_total,
        "missing_file_count_total": missing_file_count_total,
        "per_batch_status": per_batch_status,
        "download_gate_status": {
            "storage_boundary_ready": storage_boundary_ready,
            "vendor_boundary_ready": vendor_boundary_ready,
            "model_download_allowed_now": storage_boundary_ready and vendor_boundary_ready,
        },
        "voice_gate_status": {
            "voice_smoke_visible": voice_smoke_visible,
            "voice_allowed_now": False,
            "first_voice_batch": "JL-11",
        },
        "pc_control_gate_status": {
            "pc_control_allowed_now": pc_control_gate_ready,
            "first_pc_control_batch": "JL-14",
        },
        "no_parallel_world_guard_status": {
            "ready": no_parallel_world_guard_ready,
            "forbidden_parallel_world_roots": FORBIDDEN_PARALLEL_WORLD_ROOTS,
            "forbidden_parallel_world_roots_present": forbidden_roots_present,
        },
        "model_download_allowed_now": storage_boundary_ready and vendor_boundary_ready,
        "runtime_start_allowed_now": False,
        "voice_allowed_now": False,
        "pc_control_allowed_now": pc_control_gate_ready,
        "required_control_commands": {
            "xray": XRAY_COMMAND_HINT,
            "drift": DRIFT_COMMAND_HINT,
            "full_auto": FULL_AUTO_COMMAND_HINT,
            "jarvis_tests": "TMPDIR=\"$HOME/.tmp\" PYTHONDONTWRITEBYTECODE=1 python -m pytest tests/jarvis_live -q",
        },
        "read_only": True,
        "dashboard_safe": True,
        "runtime_started": False,
        "model_download_started": False,
        "audio_runtime_started": False,
        "pc_control_started": False,
    }


def _build_batch_status(root: Path, batch: JarvisLiveRoadmapBatch) -> dict[str, Any]:
    existing_files = tuple(path for path in batch.expected_files if (root / path).exists())
    missing_files = tuple(path for path in batch.expected_files if not (root / path).exists())
    existing_tests = tuple(path for path in batch.target_tests if (root / path).exists())
    missing_tests = tuple(path for path in batch.target_tests if not (root / path).exists())
    ready = len(missing_files) == 0 and len(missing_tests) == 0

    return {
        "batch_id": batch.batch_id,
        "title": batch.title,
        "purpose": batch.purpose,
        "ready": ready,
        "status": "READY" if ready else "BLOCKED",
        "expected_file_count": len(batch.expected_files),
        "existing_file_count": len(existing_files),
        "missing_file_count": len(missing_files),
        "expected_files": batch.expected_files,
        "existing_files": existing_files,
        "missing_files": missing_files,
        "target_tests": batch.target_tests,
        "existing_target_tests": existing_tests,
        "missing_target_tests": missing_tests,
        "download_allowed": batch.download_allowed,
        "runtime_allowed": batch.runtime_allowed,
        "voice_allowed": batch.voice_allowed,
        "pc_control_allowed": batch.pc_control_allowed,
        "depends_on": batch.depends_on,
        "status_rule": batch.status_rule,
    }


def _resolve_next_batch(per_batch_status: tuple[dict[str, Any], ...]) -> dict[str, Any] | None:
    status_by_id = {str(entry["batch_id"]): entry for entry in per_batch_status}
    for entry in per_batch_status:
        if entry["ready"] is True:
            continue
        dependencies = tuple(entry["depends_on"])
        if all(status_by_id[dependency]["ready"] is True for dependency in dependencies):
            return {
                "batch_id": entry["batch_id"],
                "title": entry["title"],
                "missing_files": entry["missing_files"],
                "target_tests": entry["target_tests"],
            }
    return None


def _batch_ready(per_batch_status: tuple[dict[str, Any], ...], batch_id: str) -> bool:
    return any(
        entry["batch_id"] == batch_id and entry["ready"] is True
        for entry in per_batch_status
    )
