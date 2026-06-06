from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.jarvis_live_full_roadmap_status_builder import (
    build_jarvis_live_full_roadmap_status,
)


def render_jarvis_live_ci_status(status: dict[str, Any]) -> str:
    guard_status = status["no_parallel_world_guard_status"]
    assert isinstance(guard_status, dict)
    forbidden_present = tuple(guard_status["forbidden_parallel_world_roots_present"])
    drift_guard_ok = len(forbidden_present) == 0

    next_batch = status["next_batch"]
    if isinstance(next_batch, dict):
        next_batch_id = str(next_batch["batch_id"])
        next_missing_files = tuple(str(path) for path in next_batch["missing_files"])
    else:
        next_batch_id = "NONE"
        next_missing_files = ()

    commands = status["required_control_commands"]
    assert isinstance(commands, dict)

    lines = [
        "JARVIS_LIVE_CI_STATUS",
        f"JARVIS_DRIFT_GUARD_OK={str(drift_guard_ok).lower()}",
        f"READY_BATCHES={','.join(str(batch) for batch in status['ready_batches'])}",
        f"NEXT_BATCH={next_batch_id}",
        "NEXT_BATCH_MISSING_FILES="
        + (";".join(next_missing_files) if next_missing_files else "NONE"),
        f"MODEL_DOWNLOAD_ALLOWED={str(status['model_download_allowed_now']).lower()}",
        f"RUNTIME_START_ALLOWED={str(status['runtime_start_allowed_now']).lower()}",
        f"VOICE_ALLOWED={str(status['voice_allowed_now']).lower()}",
        f"PC_CONTROL_ALLOWED={str(status['pc_control_allowed_now']).lower()}",
        f"XRAY_COMMAND={commands['xray']}",
        f"DRIFT_COMMAND={commands['drift']}",
        f"FULL_AUTO_COMMAND={commands['full_auto']}",
    ]

    if forbidden_present:
        lines.append("FORBIDDEN_PARALLEL_WORLD_ROOTS_PRESENT=" + ";".join(forbidden_present))
    else:
        lines.append("FORBIDDEN_PARALLEL_WORLD_ROOTS_PRESENT=NONE")

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Print JARVIS-LIVE CI guard status.")
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()

    status = build_jarvis_live_full_roadmap_status(Path(args.repo_root))
    output = render_jarvis_live_ci_status(status)
    print(output, end="")

    guard_status = status["no_parallel_world_guard_status"]
    assert isinstance(guard_status, dict)
    forbidden_present = tuple(guard_status["forbidden_parallel_world_roots_present"])
    return 1 if forbidden_present else 0


if __name__ == "__main__":
    raise SystemExit(main())
