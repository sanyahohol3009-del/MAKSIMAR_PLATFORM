from __future__ import annotations

import importlib.util
import os
import sys
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from types import ModuleType

from MAKSIMAR_CORE_LIB.architecture_map.architecture_radar import (
    build_architecture_report,
)
from MAKSIMAR_CORE_LIB.architecture_map.pytest_report_gate import (
    is_maksimar_full_platform_report_enabled,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
XRAY_PATH = PROJECT_ROOT / "tools" / "architecture_xray_radar.py"


def pytest_terminal_summary(terminalreporter, exitstatus, config) -> None:
    if not is_maksimar_full_platform_report_enabled(config):
        return

    _render_architecture_radar(terminalreporter)
    _render_project_xray(terminalreporter)


def _render_architecture_radar(terminalreporter) -> None:
    try:
        report = build_architecture_report()
    except Exception as exc:  # pragma: no cover
        terminalreporter.write_sep(
            "=",
            "MAKSIMAR ARCHITECTURE RADAR FAILED TO RENDER",
        )
        terminalreporter.write_line(str(exc))
        return

    terminalreporter.write_line(report.terminal_text())


def _render_project_xray(terminalreporter) -> None:
    if os.environ.get("MAKSIMAR_XRAY_DISABLED") == "1":
        terminalreporter.write_sep("=", "MAKSIMAR PROJECT X-RAY SKIPPED")
        terminalreporter.write_line("Reason: MAKSIMAR_XRAY_DISABLED=1")
        return

    if not XRAY_PATH.exists():
        terminalreporter.write_sep("=", "MAKSIMAR PROJECT X-RAY NOT FOUND")
        terminalreporter.write_line(str(XRAY_PATH))
        return

    try:
        module = _load_xray_module(XRAY_PATH)
        layer_specs = module.build_layer_specs(
            project_root=PROJECT_ROOT,
            blueprint_path=PROJECT_ROOT
            / "MAKSIMAR_CORE_LIB"
            / "architecture_map"
            / "architecture_blueprint.json",
            use_blueprint=True,
        )
        reports = module.build_reports(
            project_root=PROJECT_ROOT,
            layer_specs=layer_specs,
            include_external=True,
            max_files_per_layer=0,
        )
        buffer = StringIO()
        with redirect_stdout(buffer):
            module.print_dashboard(
                reports=reports,
                project_root=PROJECT_ROOT,
                blueprint_path=PROJECT_ROOT
                / "MAKSIMAR_CORE_LIB"
                / "architecture_map"
                / "architecture_blueprint.json",
                details=False,
                show_missing_laws=True,
            )
        terminalreporter.write_line(buffer.getvalue())
    except Exception as exc:  # pragma: no cover
        terminalreporter.write_sep(
            "=",
            "MAKSIMAR PROJECT X-RAY FAILED TO RENDER",
        )
        terminalreporter.write_line(str(exc))
        terminalreporter.write_line(
            "X-Ray is analytics-only. Pytest result is controlled by tests and Drift Guard."
        )


def _load_xray_module(path: Path) -> ModuleType:
    module_name = "maksimar_architecture_xray_radar"
    spec = importlib.util.spec_from_file_location(
        module_name,
        path,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load X-Ray module from {path}")

    module = importlib.util.module_from_spec(spec)
    # Required for dataclasses: dataclass internals resolve cls.__module__
    # through sys.modules[module_name].__dict__ during class creation.
    sys.modules[module_name] = module

    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(module_name, None)
        raise

    return module
