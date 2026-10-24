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


def test_oob_panel_content_contracts_build_all_major_contracts() -> None:
    live_adapter, original_run = _patch_live_status_run()
    try:
        builders = [
            (
                "MAKSIMAR_CORE_LIB.oob_dashboard.guard_chain_panel_content_contract",
                "build_guard_chain_panel_content_contract",
            ),
            (
                "MAKSIMAR_CORE_LIB.oob_dashboard.logs_panel_content_contract",
                "build_logs_panel_content_contract",
            ),
            (
                "MAKSIMAR_CORE_LIB.oob_dashboard.incidents_panel_content_contract",
                "build_incidents_panel_content_contract",
            ),
            (
                "MAKSIMAR_CORE_LIB.oob_dashboard.system_status_panel_content_contract",
                "build_system_status_panel_content_contract",
            ),
            (
                "MAKSIMAR_CORE_LIB.oob_dashboard.topology_panel_content_contract",
                "build_topology_panel_content_contract",
            ),
        ]

        for module_name, builder_name in builders:
            module = importlib.import_module(module_name)
            builder = getattr(module, builder_name)
            contract = builder()

            assert contract is not None
    finally:
        live_adapter.subprocess.run = original_run


def test_oob_panel_content_contracts_expose_major_identity_fields() -> None:
    live_adapter, original_run = _patch_live_status_run()
    try:
        builders = [
            (
                "MAKSIMAR_CORE_LIB.oob_dashboard.guard_chain_panel_content_contract",
                "build_guard_chain_panel_content_contract",
            ),
            (
                "MAKSIMAR_CORE_LIB.oob_dashboard.logs_panel_content_contract",
                "build_logs_panel_content_contract",
            ),
            (
                "MAKSIMAR_CORE_LIB.oob_dashboard.incidents_panel_content_contract",
                "build_incidents_panel_content_contract",
            ),
            (
                "MAKSIMAR_CORE_LIB.oob_dashboard.system_status_panel_content_contract",
                "build_system_status_panel_content_contract",
            ),
            (
                "MAKSIMAR_CORE_LIB.oob_dashboard.topology_panel_content_contract",
                "build_topology_panel_content_contract",
            ),
        ]

        for module_name, builder_name in builders:
            module = importlib.import_module(module_name)
            builder = getattr(module, builder_name)
            contract = builder()

            contract_dict = contract if isinstance(contract, dict) else getattr(contract, "__dict__", {})
            assert contract_dict or hasattr(contract, "panel_id") or hasattr(contract, "contract_id") or hasattr(contract, "description")
    finally:
        live_adapter.subprocess.run = original_run


def test_oob_panel_content_contracts_preserve_repeatable_shape() -> None:
    live_adapter, original_run = _patch_live_status_run()
    try:
        module = importlib.import_module(
            "MAKSIMAR_CORE_LIB.oob_dashboard.system_status_panel_content_contract"
        )
        builder = getattr(module, "build_system_status_panel_content_contract")

        first = builder()
        second = builder()

        first_dict = first if isinstance(first, dict) else getattr(first, "__dict__", {})
        second_dict = second if isinstance(second, dict) else getattr(second, "__dict__", {})

        assert type(first) is type(second)
        if first_dict and second_dict:
            assert set(first_dict.keys()) == set(second_dict.keys())
    finally:
        live_adapter.subprocess.run = original_run
