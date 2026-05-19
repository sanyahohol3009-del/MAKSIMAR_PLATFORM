from __future__ import annotations

import html
from pathlib import Path

from tools.monitor.runtime_input.update_recovery_terminal_preview import (
    render_update_recovery_terminal_preview,
)


def render_update_recovery_web_preview(project_root: Path | None = None) -> str:
    payload = render_update_recovery_terminal_preview(project_root=project_root)
    escaped_payload = html.escape(payload)
    return (
        "<!doctype html>\n"
        "<html lang=\"en\">\n"
        "<head>\n"
        "  <meta charset=\"utf-8\">\n"
        "  <title>UPDATE_RECOVERY Runtime Preview</title>\n"
        "</head>\n"
        "<body>\n"
        "  <main>\n"
        "    <h1>UPDATE_RECOVERY Runtime Preview</h1>\n"
        "    <p>Dashboard-safe read-only preview. Runtime apply is disabled.</p>\n"
        f"    <pre>{escaped_payload}</pre>\n"
        "  </main>\n"
        "</body>\n"
        "</html>\n"
    )


def write_update_recovery_web_preview(
    *,
    output_path: Path,
    project_root: Path | None = None,
) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_update_recovery_web_preview(project_root=project_root), encoding="utf-8")
    return output_path


def main() -> None:
    print(render_update_recovery_web_preview())


if __name__ == "__main__":
    main()
