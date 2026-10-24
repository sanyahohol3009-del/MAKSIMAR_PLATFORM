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


def test_foundation_dashboard_views_build_major_views() -> None:
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
            assert view is not None
    finally:
        live_adapter.subprocess.run = original_run


def test_foundation_dashboard_views_expose_identity_or_content_shape() -> None:
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
            assert view_dict or hasattr(view, "view_id") or hasattr(view, "entries") or hasattr(view, "summary")
    finally:
        live_adapter.subprocess.run = original_run


def test_foundation_unified_dashboard_view_repeatable_shape() -> None:
    live_adapter, original_run = _patch_live_status_run()
    try:
        module = importlib.import_module(
            "MAKSIMAR_CORE_LIB.oob_dashboard.foundation_unified_dashboard_view"
        )
        builder = getattr(module, "build_foundation_unified_dashboard_view")

        first = builder()
        second = builder()

        first_dict = first if isinstance(first, dict) else getattr(first, "__dict__", {})
        second_dict = second if isinstance(second, dict) else getattr(second, "__dict__", {})

        assert type(first) is type(second)
        if first_dict and second_dict:
            assert set(first_dict.keys()) == set(second_dict.keys())
    finally:
        live_adapter.subprocess.run = original_run
