from __future__ import annotations

import importlib
from types import SimpleNamespace


def test_snapshot_aggregator_builds_dashboard_state_snapshot() -> None:
    module = importlib.import_module(
        "MAKSIMAR_CORE_LIB.oob_dashboard.snapshot_aggregator"
    )

    live_adapter = importlib.import_module(
        "MAKSIMAR_CORE_LIB.oob_dashboard.foundation_live_status_adapter"
    )

    original_run = live_adapter.subprocess.run
    try:
        live_adapter.subprocess.run = lambda *args, **kwargs: SimpleNamespace(
            stdout="runtime: alive\nkernel: alive\n",
            stderr="",
            returncode=0,
        )

        snapshot = module.build_dashboard_state_snapshot()

        assert snapshot is not None
        assert hasattr(snapshot, "snapshot_id")
        assert hasattr(snapshot, "overall_status")
        assert hasattr(snapshot, "lines")
        assert snapshot.lines
    finally:
        live_adapter.subprocess.run = original_run


def test_snapshot_aggregator_exposes_expected_summary_line_sources() -> None:
    module = importlib.import_module(
        "MAKSIMAR_CORE_LIB.oob_dashboard.snapshot_aggregator"
    )

    live_adapter = importlib.import_module(
        "MAKSIMAR_CORE_LIB.oob_dashboard.foundation_live_status_adapter"
    )

    original_run = live_adapter.subprocess.run
    try:
        live_adapter.subprocess.run = lambda *args, **kwargs: SimpleNamespace(
            stdout="runtime: alive\nkernel: alive\n",
            stderr="",
            returncode=0,
        )

        snapshot = module.build_dashboard_state_snapshot()
        source_names = [line.source_name for line in snapshot.lines]

        assert source_names
        assert "platform_self_check" in source_names
        assert "alert_policy" in source_names
    finally:
        live_adapter.subprocess.run = original_run


def test_snapshot_aggregator_total_lines_matches_line_count() -> None:
    module = importlib.import_module(
        "MAKSIMAR_CORE_LIB.oob_dashboard.snapshot_aggregator"
    )

    live_adapter = importlib.import_module(
        "MAKSIMAR_CORE_LIB.oob_dashboard.foundation_live_status_adapter"
    )

    original_run = live_adapter.subprocess.run
    try:
        live_adapter.subprocess.run = lambda *args, **kwargs: SimpleNamespace(
            stdout="runtime: alive\nkernel: alive\n",
            stderr="",
            returncode=0,
        )

        snapshot = module.build_dashboard_state_snapshot()

        assert snapshot.total_lines == len(snapshot.lines)
    finally:
        live_adapter.subprocess.run = original_run
