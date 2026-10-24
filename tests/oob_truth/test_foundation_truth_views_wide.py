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


def test_foundation_truth_views_build_major_views() -> None:
    live_adapter, original_run = _patch_live_status_run()
    try:
        builders = [
            (
                "MAKSIMAR_CORE_LIB.oob_dashboard.foundation_guard_chain_truth_view",
                "build_foundation_guard_chain_truth_view",
            ),
            (
                "MAKSIMAR_CORE_LIB.oob_dashboard.foundation_diagnostics_correlation_view",
                "build_foundation_diagnostics_correlation_view",
            ),
            (
                "MAKSIMAR_CORE_LIB.oob_dashboard.foundation_stalled_stage_command_flow_view",
                "build_foundation_stalled_stage_command_flow_view",
            ),
            (
                "MAKSIMAR_CORE_LIB.oob_dashboard.foundation_truth_consistency_view",
                "build_foundation_truth_consistency_view",
            ),
        ]

        for module_name, builder_name in builders:
            module = importlib.import_module(module_name)
            builder = getattr(module, builder_name)
            view = builder()
            assert view is not None
    finally:
        live_adapter.subprocess.run = original_run


def test_foundation_truth_views_expose_identity_or_summary_shape() -> None:
    live_adapter, original_run = _patch_live_status_run()
    try:
        builders = [
            (
                "MAKSIMAR_CORE_LIB.oob_dashboard.foundation_guard_chain_truth_view",
                "build_foundation_guard_chain_truth_view",
            ),
            (
                "MAKSIMAR_CORE_LIB.oob_dashboard.foundation_diagnostics_correlation_view",
                "build_foundation_diagnostics_correlation_view",
            ),
            (
                "MAKSIMAR_CORE_LIB.oob_dashboard.foundation_stalled_stage_command_flow_view",
                "build_foundation_stalled_stage_command_flow_view",
            ),
            (
                "MAKSIMAR_CORE_LIB.oob_dashboard.foundation_truth_consistency_view",
                "build_foundation_truth_consistency_view",
            ),
        ]

        for module_name, builder_name in builders:
            module = importlib.import_module(module_name)
            builder = getattr(module, builder_name)
            view = builder()

            view_dict = view if isinstance(view, dict) else getattr(view, "__dict__", {})
            assert view_dict or hasattr(view, "view_id") or hasattr(view, "summary") or hasattr(view, "entries")
    finally:
        live_adapter.subprocess.run = original_run


def test_foundation_truth_views_repeatable_shape() -> None:
    live_adapter, original_run = _patch_live_status_run()
    try:
        module = importlib.import_module(
            "MAKSIMAR_CORE_LIB.oob_dashboard.foundation_guard_chain_truth_view"
        )
        builder = getattr(module, "build_foundation_guard_chain_truth_view")

        first = builder()
        second = builder()

        first_dict = first if isinstance(first, dict) else getattr(first, "__dict__", {})
        second_dict = second if isinstance(second, dict) else getattr(second, "__dict__", {})

        assert type(first) is type(second)
        if first_dict and second_dict:
            assert set(first_dict.keys()) == set(second_dict.keys())
    finally:
        live_adapter.subprocess.run = original_run
