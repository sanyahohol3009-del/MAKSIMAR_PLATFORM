from __future__ import annotations

import argparse
import html
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.monitor.runtime_input.data_plane_terminal_preview import (  # noqa: E402
    build_preview_runtime_read_model,
)


def render_html() -> str:
    runtime_read_model = build_preview_runtime_read_model()
    rows = (
        ("Runtime read model", runtime_read_model.runtime_read_model_id),
        ("Layer", runtime_read_model.layer_id),
        ("Append log records", str(runtime_read_model.telemetry.append_log.record_count)),
        ("Ledger entries", str(runtime_read_model.telemetry.ledger.entry_count)),
        ("Health", runtime_read_model.telemetry.health.status),
        ("Dashboard safe", str(runtime_read_model.dashboard_safe)),
        ("Preview safe", str(runtime_read_model.preview_safe)),
        ("Execution from preview", str(runtime_read_model.execution_allowed_from_preview)),
    )

    row_html = "\n".join(
        f"<tr><th>{html.escape(key)}</th><td>{html.escape(value)}</td></tr>"
        for key, value in rows
    )

    return (
        "<!doctype html>\n"
        "<html lang=\"en\">\n"
        "<head><meta charset=\"utf-8\"><title>DATA_PLANE Preview</title></head>\n"
        "<body>\n"
        "<h1>DATA_PLANE RUNTIME READ MODEL</h1>\n"
        "<table>\n"
        f"{row_html}\n"
        "</table>\n"
        "</body>\n"
        "</html>\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Render DATA_PLANE web preview.")
    parser.add_argument("--output", required=True, help="Output HTML file path.")
    args = parser.parse_args()

    output_path = Path(args.output)
    if ".." in output_path.parts:
        raise ValueError("output path must not contain parent traversal")
    if output_path.suffix != ".html":
        raise ValueError("output path must use .html suffix")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_html(), encoding="utf-8")

    print(f"WROTE: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
