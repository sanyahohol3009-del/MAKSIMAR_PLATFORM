from __future__ import annotations

import argparse
from pathlib import Path

from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.jarvis_live_full_roadmap_status_builder import (
    build_jarvis_live_full_roadmap_status,
)


def render_status(status: dict[str, object]) -> str:
    lines = [
        "JARVIS-LIVE FULL ROADMAP STATUS",
        f"total_batches={status['total_batches']}",
        f"ready_batches={', '.join(status['ready_batches'])}",
        f"blocked_batches={', '.join(status['blocked_batches'])}",
    ]

    next_batch = status["next_batch"]
    if isinstance(next_batch, dict):
        lines.append(f"next_batch={next_batch['batch_id']} {next_batch['title']}")
        lines.append("missing_files:")
        for path in next_batch["missing_files"]:
            lines.append(f"- {path}")
        lines.append("target_tests:")
        for path in next_batch["target_tests"]:
            lines.append(f"- {path}")
    else:
        lines.append("next_batch=None")

    commands = status["required_control_commands"]
    assert isinstance(commands, dict)
    lines.extend(
        (
            "commands:",
            f"- xray: {commands['xray']}",
            f"- drift: {commands['drift']}",
            f"- full_auto: {commands['full_auto']}",
            f"- jarvis_tests: {commands['jarvis_tests']}",
        )
    )

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Print JARVIS-LIVE full roadmap status.")
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()

    status = build_jarvis_live_full_roadmap_status(Path(args.repo_root))
    print(render_status(status), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
