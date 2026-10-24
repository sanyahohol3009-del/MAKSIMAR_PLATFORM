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


def test_oob_payload_builders_build_all_major_payloads() -> None:
    live_adapter, original_run = _patch_live_status_run()
    try:
        builders = [
            (
                "MAKSIMAR_CORE_LIB.oob_dashboard.guard_chain_panel_payload_builder",
                "build_guard_chain_panel_payload",
            ),
            (
                "MAKSIMAR_CORE_LIB.oob_dashboard.logs_panel_payload_builder",
                "build_logs_panel_payload",
            ),
            (
                "MAKSIMAR_CORE_LIB.oob_dashboard.incidents_panel_payload_builder",
                "build_incidents_panel_payload",
            ),
            (
                "MAKSIMAR_CORE_LIB.oob_dashboard.system_status_panel_payload_builder",
                "build_system_status_panel_payload",
            ),
            (
                "MAKSIMAR_CORE_LIB.oob_dashboard.topology_panel_payload_builder",
                "build_topology_panel_payload",
            ),
        ]

        for module_name, builder_name in builders:
            module = importlib.import_module(module_name)
            builder = getattr(module, builder_name)
            payload = builder()

            assert payload is not None
    finally:
        live_adapter.subprocess.run = original_run


def test_oob_payload_builders_expose_panel_identity_or_summary_shape() -> None:
    live_adapter, original_run = _patch_live_status_run()
    try:
        builders = [
            (
                "MAKSIMAR_CORE_LIB.oob_dashboard.guard_chain_panel_payload_builder",
                "build_guard_chain_panel_payload",
            ),
            (
                "MAKSIMAR_CORE_LIB.oob_dashboard.logs_panel_payload_builder",
                "build_logs_panel_payload",
            ),
            (
                "MAKSIMAR_CORE_LIB.oob_dashboard.incidents_panel_payload_builder",
                "build_incidents_panel_payload",
            ),
            (
                "MAKSIMAR_CORE_LIB.oob_dashboard.system_status_panel_payload_builder",
                "build_system_status_panel_payload",
            ),
            (
                "MAKSIMAR_CORE_LIB.oob_dashboard.topology_panel_payload_builder",
                "build_topology_panel_payload",
            ),
        ]

        for module_name, builder_name in builders:
            module = importlib.import_module(module_name)
            builder = getattr(module, builder_name)
            payload = builder()

            payload_dict = payload if isinstance(payload, dict) else getattr(payload, "__dict__", {})
            assert payload_dict or hasattr(payload, "panel_id") or hasattr(payload, "raw_entry")
    finally:
        live_adapter.subprocess.run = original_run


def test_oob_payload_builders_are_deterministic_enough_for_repeat_builds() -> None:
    live_adapter, original_run = _patch_live_status_run()
    try:
        module = importlib.import_module(
            "MAKSIMAR_CORE_LIB.oob_dashboard.topology_panel_payload_builder"
        )
        builder = getattr(module, "build_topology_panel_payload")

        first = builder()
        second = builder()

        first_dict = first if isinstance(first, dict) else getattr(first, "__dict__", {})
        second_dict = second if isinstance(second, dict) else getattr(second, "__dict__", {})

        assert type(first) is type(second)
        if first_dict and second_dict:
            assert set(first_dict.keys()) == set(second_dict.keys())
    finally:
        live_adapter.subprocess.run = original_run
