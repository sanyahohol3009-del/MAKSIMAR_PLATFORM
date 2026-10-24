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


def test_foundation_status_bridge_builds_major_bridge_contracts() -> None:
    live_adapter, original_run = _patch_live_status_run()
    try:
        builders = [
            (
                "MAKSIMAR_CORE_LIB.oob_dashboard.foundation_status_dashboard_bridge_contract",
                "build_foundation_status_dashboard_bridge_contract",
            ),
            (
                "MAKSIMAR_CORE_LIB.oob_dashboard.foundation_status_panel_summary_contract",
                "build_foundation_status_panel_summary_contract",
            ),
            (
                "MAKSIMAR_CORE_LIB.oob_dashboard.foundation_live_status_derived_view_contract",
                "build_foundation_live_status_derived_view_contract",
            ),
        ]

        for module_name, builder_name in builders:
            module = importlib.import_module(module_name)
            builder = getattr(module, builder_name)
            contract = builder()
            assert contract is not None
    finally:
        live_adapter.subprocess.run = original_run


def test_foundation_status_bridge_exposes_identity_or_content_shape() -> None:
    live_adapter, original_run = _patch_live_status_run()
    try:
        builders = [
            (
                "MAKSIMAR_CORE_LIB.oob_dashboard.foundation_status_dashboard_bridge_contract",
                "build_foundation_status_dashboard_bridge_contract",
            ),
            (
                "MAKSIMAR_CORE_LIB.oob_dashboard.foundation_status_panel_summary_contract",
                "build_foundation_status_panel_summary_contract",
            ),
            (
                "MAKSIMAR_CORE_LIB.oob_dashboard.foundation_live_status_derived_view_contract",
                "build_foundation_live_status_derived_view_contract",
            ),
        ]

        for module_name, builder_name in builders:
            module = importlib.import_module(module_name)
            builder = getattr(module, builder_name)
            contract = builder()

            contract_dict = contract if isinstance(contract, dict) else getattr(contract, "__dict__", {})
            assert contract_dict or hasattr(contract, "contract_id") or hasattr(contract, "view_id") or hasattr(contract, "summary")
    finally:
        live_adapter.subprocess.run = original_run


def test_foundation_status_bridge_repeatable_shape() -> None:
    live_adapter, original_run = _patch_live_status_run()
    try:
        module = importlib.import_module(
            "MAKSIMAR_CORE_LIB.oob_dashboard.foundation_status_dashboard_bridge_contract"
        )
        builder = getattr(module, "build_foundation_status_dashboard_bridge_contract")

        first = builder()
        second = builder()

        first_dict = first if isinstance(first, dict) else getattr(first, "__dict__", {})
        second_dict = second if isinstance(second, dict) else getattr(second, "__dict__", {})

        assert type(first) is type(second)
        if first_dict and second_dict:
            assert set(first_dict.keys()) == set(second_dict.keys())
    finally:
        live_adapter.subprocess.run = original_run
