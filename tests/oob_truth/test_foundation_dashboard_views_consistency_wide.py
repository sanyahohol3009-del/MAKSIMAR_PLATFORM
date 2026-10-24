from __future__ import annotations

import importlib
from types import SimpleNamespace


def _patch_live_status_run():
    live_adapter = importlib.import_module(
        "MAKSIMAR_CORE_LIB.oob_dashboard.foundation_live_status_adapter"
    )
    original_run = live_adapter.subprocess.run
    live_adapter.subprocess.run = lambda *args, **kwargs: SimpleNamespace(
        stdout="runtime: alive\nkernel: alive\nguard: alive\n",
        stderr="",
        returncode=0,
    )
    return live_adapter, original_run


def test_foundation_dashboard_views_have_non_empty_content() -> None:
    live_adapter, original_run = _patch_live_status_run()
    try:
        builders = [
            (
                "MAKSIMAR_CORE_LIB.oob_dashboard.foundation_unified_dashboard_view",
                "build_foundation_unified_dashboard_view",
            ),
            (
                "MAKSIMAR_CORE_LIB.oob_dashboard.foundation_incident_dashboard_view",
                "build_foundation_incident_dashboard_view",
            ),
            (
                "MAKSIMAR_CORE_LIB.oob_dashboard.foundation_incident_failure_localization_view",
                "build_foundation_incident_failure_localization_view",
            ),
            (
                "MAKSIMAR_CORE_LIB.oob_dashboard.foundation_live_historical_state_split_view",
                "build_foundation_live_historical_state_split_view",
            ),
        ]

        for module_name, builder_name in builders:
            module = importlib.import_module(module_name)
            builder = getattr(module, builder_name)
            view = builder()

            view_dict = view if isinstance(view, dict) else getattr(view, "__dict__", {})
            assert len(view_dict) > 0 or hasattr(view, "entries") or hasattr(view, "summary")
    finally:
        live_adapter.subprocess.run = original_run


def test_foundation_incident_dashboard_view_builds_under_failed_status_command_too() -> None:
    live_adapter = importlib.import_module(
        "MAKSIMAR_CORE_LIB.oob_dashboard.foundation_live_status_adapter"
    )
    original_run = live_adapter.subprocess.run
    try:
        live_adapter.subprocess.run = lambda *args, **kwargs: SimpleNamespace(
            stdout="",
            stderr="boom",
            returncode=1,
        )

        module = importlib.import_module(
            "MAKSIMAR_CORE_LIB.oob_dashboard.foundation_incident_dashboard_view"
        )
        view = module.build_foundation_incident_dashboard_view()
        assert view is not None
    finally:
        live_adapter.subprocess.run = original_run


def test_foundation_live_historical_split_view_builds_under_failed_status_command_too() -> None:
    live_adapter = importlib.import_module(
        "MAKSIMAR_CORE_LIB.oob_dashboard.foundation_live_status_adapter"
    )
    original_run = live_adapter.subprocess.run
    try:
        live_adapter.subprocess.run = lambda *args, **kwargs: SimpleNamespace(
            stdout="",
            stderr="boom",
            returncode=1,
        )

        module = importlib.import_module(
            "MAKSIMAR_CORE_LIB.oob_dashboard.foundation_live_historical_state_split_view"
        )
        view = module.build_foundation_live_historical_state_split_view()
        assert view is not None
    finally:
        live_adapter.subprocess.run = original_run
