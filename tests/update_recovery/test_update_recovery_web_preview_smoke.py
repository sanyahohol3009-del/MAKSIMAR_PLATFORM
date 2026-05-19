from __future__ import annotations

from pathlib import Path

from tools.monitor.runtime_input.update_recovery_web_preview import (
    render_update_recovery_web_preview,
    write_update_recovery_web_preview,
)


def test_update_recovery_web_preview_is_dashboard_safe_html(tmp_path: Path) -> None:
    html = render_update_recovery_web_preview(project_root=Path.cwd())

    assert "<!doctype html>" in html
    assert "UPDATE_RECOVERY Runtime Preview" in html
    assert "Dashboard-safe read-only preview" in html
    assert "runtime_apply_allowed" in html

    output_path = write_update_recovery_web_preview(
        output_path=tmp_path / "update_recovery_preview.html",
        project_root=Path.cwd(),
    )

    assert output_path.exists()
    assert "UPDATE_RECOVERY Runtime Preview" in output_path.read_text(encoding="utf-8")
