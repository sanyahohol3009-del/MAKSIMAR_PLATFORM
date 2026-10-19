from __future__ import annotations

import ast
import json
from pathlib import Path
from types import SimpleNamespace
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeout
import hashlib

import pytest

from MAKSIMAR_CORE_LIB.project_read import jarvis_runtime_library_store as library
from MAKSIMAR_SERVER.AI_ORCHESTRATION import project_workspace_tools as workspace
from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import (
    EvidenceBundle, EvidenceItem, ExecutionReceipt, utc_observed_at,
)

ROOT = Path(__file__).resolve().parents[2]


def fixture_store(tmp_path, packages=None, manifest_extra=None):
    root = tmp_path / "library"
    (root / "manifests").mkdir(parents=True)
    (root / "probe_reports").mkdir()
    report = root / "probe_reports/agents_import_probe.json"
    report.write_text(json.dumps({"observed_at": "2000-01-01T00:00:00Z", "packages": packages if packages is not None else [
        {"pip_name": "package_a", "module_name": "module_a", "import_ok": True, "version": "1.2"}
    ]}))
    manifest = {"manifest_id": "package_a", "category": "agents", **(manifest_extra or {})}
    (root / "manifests/a.json").write_text(json.dumps(manifest))
    return root, report


@pytest.mark.parametrize("value,available", [(True, 1), (False, 0), ("false", 0), ("true", 0), (1, 0), (None, 0)])
def test_import_observation_is_typed_not_truthy(tmp_path, value, available):
    root, _ = fixture_store(tmp_path, [{"pip_name": "package_a", "import_ok": value}])
    view = library.build_runtime_library_store_read_model(root)
    assert view["available_count"] == available
    assert view["current_execution_verified"] is False
    assert view["direct_execution_allowed"] is False
    assert view["canonical_write_allowed"] is False


@pytest.mark.parametrize("kind", ["package", "manifest"])
def test_ambiguous_identity_cannot_select_first_success(tmp_path, kind):
    rows = [{"pip_name": "package_a", "import_ok": True}, {"pip_name": "package_a", "import_ok": False}]
    root, _ = fixture_store(tmp_path, rows if kind == "package" else None)
    if kind == "manifest":
        (root / "manifests/b.json").write_text((root / "manifests/a.json").read_text())
    view = library.build_runtime_library_store_read_model(root)
    assert view["available_count"] == 0
    assert all(row["error"] == "ambiguous_package_identity" for row in view["packages"])


@pytest.mark.parametrize("kind", ["absolute", "relative", "symlink"])
def test_report_cannot_cross_store_boundary(tmp_path, kind):
    foreign = tmp_path / "foreign.json"
    foreign.write_text(json.dumps({"packages": [{"pip_name": "package_a", "import_ok": True, "version": "FOREIGN"}]}))
    ref = str(foreign) if kind == "absolute" else "../foreign.json" if kind == "relative" else "escape.json"
    root, _ = fixture_store(tmp_path, manifest_extra={"report_file": ref})
    if kind == "symlink":
        (root / "escape.json").symlink_to(foreign)
    view = library.build_runtime_library_store_read_model(root)
    assert view["available_count"] == 0
    assert view["packages"][0]["version"] == ""
    assert any(row["status"] == "PATH_DENIED" for row in view["source_errors"])
    assert view["probe_reports_loaded"] == ()


@pytest.mark.parametrize("kind", ["missing", "malformed", "permission_denied"])
def test_unreadable_evidence_is_explicit_not_success(tmp_path, monkeypatch, kind):
    root, report = fixture_store(tmp_path)
    if kind == "missing":
        report.unlink()
    elif kind == "malformed":
        report.write_text("not-json")
    else:
        original = Path.read_text
        def read(path, *args, **kwargs):
            if path == report:
                raise PermissionError("synthetic fixture denial")
            return original(path, *args, **kwargs)
        monkeypatch.setattr(Path, "read_text", read)
    view = library.build_runtime_library_store_read_model(root)
    assert view["available_count"] == 0
    assert view["probe_reports_loaded"] == ()
    assert view["source_errors"]
    assert str(report) in view["probe_reports_read"]  # retained legacy attempted-path field


def test_historical_probe_is_not_current_execution_or_freshness(tmp_path):
    root, _ = fixture_store(tmp_path)
    view = library.build_runtime_library_store_read_model(root)
    row = view["packages"][0]
    assert row["import_ok"] is True  # historical observation only
    assert row["probe_observed_at"] == "2000-01-01T00:00:00Z"
    assert row["probe_freshness"] == "UNASSESSED"
    assert row["current_execution_verified"] is False
    assert row["probe_observation_only"] is True


def test_relative_report_resolves_against_selected_store(tmp_path):
    root, report = fixture_store(tmp_path, manifest_extra={"report_file": "probe_reports/agents_import_probe.json"})
    view = library.build_runtime_library_store_read_model(root)
    assert view["available_count"] == 1
    assert view["probe_reports_loaded"] == (str(report),)


def test_report_schema_mismatch_and_missing_store_fail_safely(tmp_path):
    root, report = fixture_store(tmp_path)
    report.write_text(json.dumps({"packages": 7}))
    assert library.build_runtime_library_store_read_model(root)["available_count"] == 0
    assert library.build_runtime_library_store_read_model(tmp_path / "missing")["packages"] == ()


def test_project_references_are_exact_scoped_and_read_only(tmp_path, monkeypatch):
    project = tmp_path / "project"
    for part in ["a", "b"]:
        (project / part).mkdir(parents=True)
        (project / part / "same.py").write_text("VALUE = " + repr(part))
    monkeypatch.setattr(workspace, "PROJECT_ROOT", project)
    assert workspace.read_file_snippet("a/same.py")["allowed"] is True
    assert workspace.read_file_snippet("same.py")["error"] == "file_not_found"
    assert workspace.read_file_snippet("../outside.py")["error"] == "path_denied"
    assert workspace.read_file_snippet(str(tmp_path / "outside.py"))["allowed"] is False
    assert (project / "a/same.py").read_text() == "VALUE = 'a'"


def test_project_understanding_preserves_library_evidence_and_denies_foreign_path(tmp_path, monkeypatch):
    root, _ = fixture_store(tmp_path)
    monkeypatch.setattr(workspace, "PROJECT_ROOT", tmp_path)
    source = (ROOT / "MAKSIMAR_SERVER/AI_ORCHESTRATION/project_understanding_adapter.py").read_text()
    node = next(n for n in ast.parse(source).body if isinstance(n, ast.ClassDef) and n.name == "ExistingProjectUnderstandingAdapter")
    ns = {"ProjectUnderstandingPort": object, "PROJECT_ROOT": tmp_path, "build_runtime_library_store_read_model": lambda: library.build_runtime_library_store_read_model(root),
          "ThreadPoolExecutor": ThreadPoolExecutor, "FutureTimeout": FutureTimeout, "json": json, "hashlib": hashlib,
          "EvidenceBundle": EvidenceBundle, "EvidenceItem": EvidenceItem, "ExecutionReceipt": ExecutionReceipt,
          "utc_observed_at": utc_observed_at, "read_file_snippet": workspace.read_file_snippet}
    module = ast.Module(body=[ast.ImportFrom(module="__future__", names=[ast.alias(name="annotations")], level=0), node], type_ignores=[])
    exec(compile(ast.fix_missing_locations(module), source, "exec"), ns)
    adapter = ns["ExistingProjectUnderstandingAdapter"]()
    understanding = SimpleNamespace(request_id="synthetic", original_text="fixture")
    def collect(operation, parameters, required):
        step = SimpleNamespace(step_id="s1", operation=operation, parameters=parameters, required_evidence=required, capability_id="project.read")
        return adapter.collect_evidence(understanding, SimpleNamespace(steps=[step]), "synthetic_trace")
    result = collect("read_runtime_library_agents", {}, ("runtime_library_agents",))
    assert result.status == "COMPLETE"
    data = json.loads(result.items[0].observation)
    assert data[0]["package_name"] == "package_a"
    assert data[0]["current_execution_verified"] is False
    assert result.receipts[0].status == "COMPLETE"  # receipt of metadata read, not package execution
    manifests = collect("read_runtime_library_manifests", {}, ("runtime_library_manifests",))
    meta = json.loads(manifests.items[0].observation)
    assert meta["probe_freshness"] == "UNASSESSED"
    assert meta["current_execution_verified"] is False
    assert meta["source_errors"] == []
    assert len(meta["probe_reports_loaded"]) == 1
    denied = collect("read_file_snippet", {"path": "../foreign.py"}, ("file_snippet",))
    assert denied.status == "UNAVAILABLE"
    assert denied.items == ()
    assert denied.receipts[0].status == "FAILED"


def _existing_functions(path, names, namespace):
    source = (ROOT / path).read_text()
    nodes = [n for n in ast.parse(source).body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in names]
    assert {n.name for n in nodes} == set(names)
    namespace.setdefault("__name__", __name__)
    future = ast.ImportFrom(module="__future__", names=[ast.alias(name="annotations")], level=0)
    exec(compile(ast.fix_missing_locations(ast.Module(body=[future, *nodes], type_ignores=[])), path, "exec"), namespace)
    return namespace


def test_core_server_registry_visibility_share_one_inventory_without_effects(tmp_path):
    from collections import Counter
    from dataclasses import dataclass, asdict
    root, _ = fixture_store(tmp_path)
    reader = lambda: library.build_runtime_library_store_read_model(root)
    memory = {"surfaces": (), "disabled_memory_surfaces": (), "active_retrieval_surfaces": (),
              "sandbox_only_memory_surfaces": (), "inventory_coverage": "SYNTHETIC_SCOPE"}
    external = {"active_adapter_ids": (), "adapters": (), "unavailable_adapter_ids": (), "legacy_adapter_ids": (),
                "runtime_python": "", "probe": {}, "registry": {"tools": (), "safe_direct_tool_ids": (), "risk_gated_tool_ids": ()}}
    read_model = lambda: SimpleNamespace(to_read_model=lambda: {})
    ns = {"PROJECT_ROOT": tmp_path, "build_runtime_library_store_read_model": reader,
          "build_jarvis_live_memory_federation_status": lambda: memory,
          "build_jarvis_external_adapter_visibility_read_model": lambda: external,
          "inspect_mgrep_readonly_availability": lambda *a: read_model(),
          "inspect_sqlite_vec_readonly_availability": lambda *a: read_model(),
          "inspect_qdrant_readonly_availability": lambda *a: read_model(),
          "list_memory_definitions": lambda: (), "build_enterprise_memory_preview": lambda: {},
          "build_regulatory_routing_preview": lambda: {}}
    server = _existing_functions("MAKSIMAR_SERVER/AI_ORCHESTRATION/jarvis_live_read_models.py",
        {"build_jarvis_live_tool_catalog_read_model", "_operator_capability_flags"}, ns)
    catalog = server["build_jarvis_live_tool_catalog_read_model"]()
    assert catalog["runtime_library_packages"] == reader()["packages"]
    assert catalog["direct_execution_allowed"] is False
    assert catalog["runtime_library_current_execution_verified"] is False
    assert catalog["runtime_library_source_observations"] == reader()["source_observations"]
    registry = _existing_functions("MAKSIMAR_SERVER/SKILL_ADAPTER_REGISTRY/existing_capability_inventory.py",
        {"CapabilityRecord", "_build_record", "_scan_runtime_library_sources"},
        {"Path": Path, "dataclass": dataclass, "asdict": asdict, "JARVIS_LIBRARY_DIRS": {"library:agents": root},
         "build_runtime_library_store_read_model": reader})
    record = registry["_scan_runtime_library_sources"]()[0].to_read_model()
    assert record["read_only"] is True
    assert record["executed"] is False
    assert record["execution_receipt_present"] is False
    assert record["policy_execution_allowed"] is None
    ns = {"Counter": Counter, "build_jarvis_live_tool_catalog_read_model": lambda: catalog,
          "build_jarvis_live_memory_federation_status": lambda: memory,
          "build_action_capability_inventory_read_model": lambda: SimpleNamespace(to_read_model=lambda: {
              "capabilities": (), "safe_direct_capabilities": (), "risk_gated_capabilities": ()}),
          "build_jarvis_external_adapter_visibility_read_model": lambda: external,
          "build_runtime_library_store_read_model": reader,
          "build_default_capability_activation_matrix": lambda: SimpleNamespace(to_read_model=lambda: {"entries": ()}),
          "build_default_swarm_agent_role_contracts": lambda: (), "_scan_visible_skills": lambda: (),
          "_ROUTER_VISIBLE_TOOLS": ()}
    visibility = _existing_functions("tools/jarvis_live_runtime/jarvis_skill_visibility.py",
        {"build_jarvis_skill_visibility_read_model", "build_jarvis_agent_catalog_read_model", "_operator_capability_flags", "_normalize_tool_name"}, ns)
    view = visibility["build_jarvis_skill_visibility_read_model"]()
    assert view["runtime_library_packages"] == catalog["runtime_library_packages"]
    assert view["runtime_library_available_package_names"] == ("package_a",)
    assert view["runtime_library_source_observations"] == catalog["runtime_library_source_observations"]
    assert view["runtime_library_probe_freshness"] == "UNASSESSED"
    assert view["runtime_library_packages"][0]["current_execution_verified"] is False
    assert view["canonical_write_allowed"] is False
