from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.guard_chain_panel_content_contract import (
    ALL_GUARD_CHAIN_PANEL_STATES,
    build_guard_chain_panel_content_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.guard_chain_panel_payload_builder import (
    build_guard_chain_panel_payload,
)


def test_guard_chain_panel_content_contract_builds() -> None:
    """Guard-chain panel content contract should build successfully."""
    contract = build_guard_chain_panel_content_contract()

    assert contract.contract_id == "guard_chain_panel_content_contract_001"
    assert contract.total_entries == 1
    assert contract.read_only_entries == 1
    assert contract.main_dashboard_visible_entries == 1
    assert contract.oob_visible_entries == 1
    assert contract.operator_visible_entries == 1


def test_guard_chain_panel_content_entry_is_canonical() -> None:
    """Guard-chain panel content entry should remain canonical."""
    contract = build_guard_chain_panel_content_contract()
    entry = contract.entries[0]

    assert entry.panel_id == "guard_chain"
    assert entry.panel_state in ALL_GUARD_CHAIN_PANEL_STATES
    assert entry.total_chain_entries >= 0
    assert entry.runtime_entry_present is True
    assert entry.guard_entry_present is True
    assert entry.core_guard_entry_present is True
    assert entry.kernel_guard_entry_present is True
    assert entry.visible_in_main_dashboard is True
    assert entry.visible_in_oob_dashboard is True
    assert entry.read_only is True
    assert entry.operator_visible is True


def test_guard_chain_panel_payload_builder_returns_expected_shape() -> None:
    """Payload builder should return canonical guard-chain payload shape."""
    payload = build_guard_chain_panel_payload()

    assert payload["panel_id"] == "guard_chain"
    assert payload["panel_state"] in ALL_GUARD_CHAIN_PANEL_STATES
    assert "summary" in payload
    assert "chain_health" in payload
    assert "presence" in payload
    assert "state_context" in payload
    assert "visibility" in payload


def test_guard_chain_panel_payload_builder_exposes_presence_semantics() -> None:
    """Payload builder should expose canonical guard-chain presence semantics."""
    payload = build_guard_chain_panel_payload()
    presence = payload["presence"]

    assert presence["runtime_entry_present"] is True
    assert presence["guard_entry_present"] is True
    assert presence["core_guard_entry_present"] is True
    assert presence["kernel_guard_entry_present"] is True


import pytest


@pytest.mark.parametrize("counts,expected", [
    ({"alive_entries": 4, "consistent_entries": 4}, "normal"),
    ({}, "degraded"),
    ({"unknown_entries": 1, "alive_entries": 3, "consistent_entries": 3}, "degraded"),
    ({"unknown_entries": 1, "dead_entries": 1, "warming_up_panels": 1}, "incident"),
    ({"unknown_entries": 1, "broken_entries": 1}, "incident"),
    ({"mismatch_entries": 1, "warming_up_panels": 1}, "stale"),
    ({"partial_entries": 1}, "degraded"),
    ({"degraded_entries": 1}, "degraded"),
    ({"historical_only_panels": 1}, "degraded"),
    ({"warming_up_panels": 1, "alive_entries": 3}, "loading"),
    ({"total_entries": 3, "alive_entries": 3, "consistent_entries": 3}, "degraded"),
    ({"total_entries": 0}, "empty"),
])
def test_guard_chain_truth_decision_table(counts, expected):
    from MAKSIMAR_CORE_LIB.oob_dashboard.guard_chain_panel_content_contract import _derive_guard_chain_panel_state
    args = dict(total_entries=4, broken_entries=0, dead_entries=0, degraded_entries=0,
                mismatch_entries=0, warming_up_panels=0, historical_only_panels=0)
    args.update(counts)
    assert _derive_guard_chain_panel_state(**args) == expected


@pytest.mark.parametrize("family", ["system_status", "topology", "guard_chain"])
@pytest.mark.parametrize("renderer", ["terminal", "web"])
@pytest.mark.parametrize("defect,expected", [
    ("healthy", "normal"), ("missing", "degraded"), ("malformed", "degraded"),
    ("wrong_epoch", "degraded"), ("stale", "degraded"),
    ("unavailable", "degraded"), ("malformed_metadata", "degraded"),
    ("dead_with_unknown", "incident"), ("foreign", "incident"), ("history", "degraded"),
])
def test_all_six_actual_renderers_use_canonical_composition(monkeypatch, capsys, family, renderer, defect, expected):
    import copy
    import importlib
    import importlib.util
    from pathlib import Path
    from tests.runtime.test_preflight_recovery_truth import _observation
    from MAKSIMAR_SERVER.OBSERVABILITY.jarvis_live import jarvis_live_observability_read_model as obs
    from MAKSIMAR_CORE_LIB.oob_dashboard import foundation_live_status_adapter as legacy
    root = Path(__file__).resolve().parents[2]
    snapshot = _observation()
    if defect == "missing":
        snapshot = {}
    elif defect == "malformed":
        snapshot["heartbeats"]["guard"]["fresh"] = "false"
    elif defect == "wrong_epoch":
        snapshot["heartbeats"]["guard"]["boot_id"] = "old-boot"
    elif defect == "stale":
        snapshot["heartbeats"]["guard"]["fresh"] = False
    elif defect == "dead_with_unknown":
        snapshot["heartbeats"]["guard"]["status"] = "stopped"
        snapshot["heartbeats"]["core_guard"] = {}
    elif defect == "foreign":
        snapshot["heartbeats"]["guard"]["source"] = "foreign_owner"
    elif defect == "history":
        snapshot["run_metadata"]["status"] = "shutdown"
    elif defect == "malformed_metadata":
        snapshot["run_metadata"]["status"] = {}
    original = copy.deepcopy(snapshot)
    observed = []
    def collect():
        observed.append(snapshot)
        if defect == "unavailable":
            raise OSError("offline fixture unavailable")
        return snapshot
    monkeypatch.setattr(obs, "observe_runtime_preflight", collect)
    def forbidden(*args, **kwargs):
        raise AssertionError("Legacy status probe is forbidden in canonical Dashboard paths")
    monkeypatch.setattr(legacy, "_run_status_command", forbidden)
    captured = {}
    observation_ids = []
    for name in ("system_status", "topology", "guard_chain"):
        owner = importlib.import_module("MAKSIMAR_CORE_LIB.oob_dashboard." + name + "_panel_payload_builder")
        assert Path(owner.__file__).resolve() == root / "MAKSIMAR_CORE_LIB/oob_dashboard" / (name + "_panel_payload_builder.py")
        real = getattr(owner, "build_" + name + "_panel_payload")
        def traced(*, observation, _name=name, _real=real):
            observation_ids.append(id(observation))
            result = _real(observation=observation)
            captured[_name] = result
            return result
        monkeypatch.setattr(owner, "build_" + name + "_panel_payload", traced)
    path = root / "tools/monitor/runtime_input" / (family + "_panel_" + renderer + "_preview.py")
    spec = importlib.util.spec_from_file_location("offline_renderer_under_test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert Path(module.__file__).resolve() == path
    assert getattr(module, "build_" + family + "_panel_payload").__module__ == obs.__name__
    module.main()
    output = capsys.readouterr().out
    assert len(observed) == 1 and observed[0] is snapshot
    assert len(observation_ids) == 3 and len(set(observation_ids)) == 1
    assert snapshot == original
    assert len(captured) == 3
    for name, payload in captured.items():
        assert payload["panel_state"] == expected
        assert payload["panel_id"] == name
        assert all(payload["visibility"][key] is True for key in ("read_only", "operator_visible"))
        assert payload["raw_entry"]["read_only"] is True
    if renderer == "terminal":
        assert "panel_state=" + expected in output
    else:
        assert "<strong>panel_state:</strong> " + expected in output
        assert '&quot;panel_state&quot;: &quot;' + expected + '&quot;' in output
