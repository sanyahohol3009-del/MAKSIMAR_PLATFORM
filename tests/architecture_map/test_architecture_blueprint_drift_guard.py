from __future__ import annotations

from pathlib import Path
import ast
import json

import pytest

from MAKSIMAR_CORE_LIB.architecture_map import architecture_radar as radar

from MAKSIMAR_CORE_LIB.architecture_map.architecture_radar import (
    DEFAULT_BLUEPRINT_PATH,
    PROJECT_ROOT,
    assert_architecture_is_clean,
    build_architecture_report,
    load_blueprint,
)


def test_architecture_blueprint_json_is_valid() -> None:
    blueprint = load_blueprint(DEFAULT_BLUEPRINT_PATH)

    assert blueprint["blueprint_id"] == "MAKSIMAR_PLATFORM_FULL_CONSOLIDATED_SKELETON_vFINAL_FREEZE"
    assert isinstance(blueprint["layers"], list)
    assert len(blueprint["layers"]) >= 12


def test_architecture_radar_can_build_report() -> None:
    report = build_architecture_report(
        project_root=PROJECT_ROOT,
        blueprint_path=DEFAULT_BLUEPRINT_PATH,
    )

    assert report.blueprint_id == "MAKSIMAR_PLATFORM_FULL_CONSOLIDATED_SKELETON_vFINAL_FREEZE"
    assert report.layer_statuses

    layer_ids = {layer.layer_id for layer in report.layer_statuses}
    assert "CORE_ROOT" in layer_ids
    assert "MAKSIMAR_CORE_LIB" in layer_ids
    assert "PRODUCTS_CUBES" in layer_ids


def test_architecture_structure_and_semantic_drift_guard() -> None:
    assert Path(DEFAULT_BLUEPRINT_PATH).exists()
    assert_architecture_is_clean(
        project_root=PROJECT_ROOT,
        blueprint_path=DEFAULT_BLUEPRINT_PATH,
    )


def test_historical_n8n_snapshot_is_excluded_but_live_adapter_is_scanned(tmp_path: Path) -> None:
    snapshot_rule = "RUNTIME/n8n/rollback-snapshots/pre-2.42.6-20261011/**"
    archived = "RUNTIME/n8n/rollback-snapshots/pre-2.42.6-20261011/project/MAKSIMAR_SERVER/AI_ORCHESTRATION/n8n_adapter.py"
    live = "MAKSIMAR_SERVER/AI_ORCHESTRATION/n8n_adapter.py"
    for relative in (archived, live):
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("from tools.jarvis_live_runtime import jarvis_skill_visibility\n", encoding="utf-8")

    blueprint = load_blueprint(DEFAULT_BLUEPRINT_PATH)
    assert snapshot_rule in blueprint["ignored_path_globs"]
    blueprint_path = tmp_path / "blueprint.json"
    blueprint_path.write_text(json.dumps(blueprint), encoding="utf-8")
    after = build_architecture_report(tmp_path, blueprint_path)
    scanned = {p.relative_to(tmp_path).as_posix() for p in radar._iter_python_files(
        tmp_path, tuple(blueprint["ignored_path_globs"]),
    )}
    assert archived not in scanned and live in scanned
    assert not any(v.file_path == archived for v in after.violations)
    live_after = [v for v in after.violations if v.file_path == live]
    assert len(live_after) == 1 and live_after[0].code == "IMPORT_NOT_ALLOWED"
    assert live_after[0].target_layer == "TOOLS"

    # Removing only this classification rule must expose the same archived import.
    blueprint["ignored_path_globs"].remove(snapshot_rule)
    blueprint_path.write_text(json.dumps(blueprint), encoding="utf-8")
    before = build_architecture_report(tmp_path, blueprint_path)
    archived_before = [v for v in before.violations if v.file_path == archived]
    assert len(archived_before) == 1 and archived_before[0].code == "IMPORT_NOT_ALLOWED"
    assert archived_before[0].source_layer == "EXECUTION_CONTROL"
    assert [v for v in before.violations if v.file_path == live] == live_after


@pytest.mark.parametrize("relative", (
    "RUNTIME/n8n/live_adapter.py",
    "RUNTIME/active_source.py",
    "RUNTIME/n8n/rollback-snapshots/unclassified/active_source.py",
    "RUNTIME/n8n/rollback-snapshots/pre-2.42.6-20261011-extra/active_source.py",
    "MAKSIMAR_SERVER/AI_ORCHESTRATION/n8n_adapter.py",
    "MAKSIMAR_SERVER/active_source.py",
    "SUPERVISOR/runtime_preflight.py",
    "tools/active_source.py",
))
def test_snapshot_ignore_does_not_hide_active_or_unclassified_sources(tmp_path: Path, relative: str) -> None:
    ignored = tuple(load_blueprint(DEFAULT_BLUEPRINT_PATH)["ignored_path_globs"])
    assert not {"RUNTIME/**", "RUNTIME/n8n/**", "MAKSIMAR_SERVER/**", "SUPERVISOR/**"}.intersection(ignored)
    assert not radar._matches_any_glob(relative, ignored)
    source = tmp_path / relative
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text("pass\n", encoding="utf-8")
    assert source in radar._iter_python_files(tmp_path, ignored)


def test_snapshot_classification_preserves_active_import_enforcement(tmp_path: Path) -> None:
    sources = {
        "CORE_ROOT/stop_gate.py": "from SUPERVISOR import runtime_preflight\nimport UnregisteredLocal\n",
        "SUPERVISOR/runtime_preflight.py": "pass\n",
        "UnregisteredLocal/source.py": "pass\n",
    }
    for relative, text in sources.items():
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    report = build_architecture_report(tmp_path, DEFAULT_BLUEPRINT_PATH)
    assert report.failed
    assert any(v.code == "FORBIDDEN_IMPORT" and v.file_path == "CORE_ROOT/stop_gate.py"
               and v.target_layer == "EXECUTION_CONTROL" for v in report.violations)
    assert any(v.code == "UNKNOWN_LOCAL_IMPORT" and v.imported_module == "UnregisteredLocal"
               for v in report.violations)
    assert any(v.code == "UNREGISTERED_SOURCE_FILE" and v.file_path == "UnregisteredLocal/source.py"
               for v in report.violations)


def test_snapshot_classification_keeps_existing_enforcement_enabled() -> None:
    enforcement = load_blueprint(DEFAULT_BLUEPRINT_PATH)["enforcement"]
    for key in ("fail_on_forbidden_import", "fail_on_unknown_local_import",
                "fail_on_unregistered_source_file", "fail_on_missing_mandatory_paths"):
        assert enforcement[key] is True


@pytest.mark.parametrize("relative,module,expected_layer", (
    ("CORE_ROOT/run_context.py", "CORE_ROOT.run_context", "CORE_ROOT"),
    ("BOOT/system_bootstrap.py", "BOOT.system_bootstrap", "BOOTSTRAP_ENTRYPOINTS"),
    ("refactor.py", "refactor", "BOOTSTRAP_ENTRYPOINTS"),
))
def test_run_context_and_bootstrap_file_namespace_owners(relative: str, module: str, expected_layer: str) -> None:
    layers = load_blueprint(DEFAULT_BLUEPRINT_PATH)["layers"]
    assert radar._resolve_file_layer(relative, layers)["id"] == expected_layer
    assert radar._resolve_import_layer(module, layers)["id"] == expected_layer


@pytest.mark.parametrize("caller,source_layer,expected_code", (
    ("CORE_ROOT/heartbeat_io.py", "CORE_ROOT", None),
    ("MAKSIMAR_SERVER/AI_ORCHESTRATION/ollama_transport.py", "MAKSIMAR_SERVER_ROOT", None),
    ("SUPERVISOR/runtime_preflight.py", "EXECUTION_CONTROL", None),
    ("CONTROL_PLANE/api_server.py", "CONTROL_PLANE", "FORBIDDEN_IMPORT"),
    ("MAKSIMAR_CORE_LIB/action_library_adapters/agent_tooling_runtime_probe.py", "MAKSIMAR_CORE_LIB", "IMPORT_NOT_ALLOWED"),
    ("MAKSIMAR_SERVER/OBSERVABILITY/jarvis_live/jarvis_live_observability_read_model.py", "OBSERVABILITY", "IMPORT_NOT_ALLOWED"),
))
def test_run_context_imports_obey_each_existing_layer_policy(
    tmp_path: Path, caller: str, source_layer: str, expected_code: str | None,
) -> None:
    sources = {
        "CORE_ROOT/run_context.py": "from CORE_ROOT.runtime_paths import RUN_METADATA_FILE\n",
        "CORE_ROOT/runtime_paths.py": "RUN_METADATA_FILE = None\n",
        caller: "from CORE_ROOT.run_context import model_free_startup\n",
    }
    for relative, text in sources.items():
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    blueprint = load_blueprint(DEFAULT_BLUEPRINT_PATH)
    layer = next(layer for layer in blueprint["layers"] if layer["id"] == source_layer)
    assert layer["import_guard"] is True
    report = build_architecture_report(tmp_path, DEFAULT_BLUEPRINT_PATH)
    assert not any(v.code in {"UNREGISTERED_SOURCE_FILE", "UNKNOWN_LOCAL_IMPORT"} for v in report.violations)
    assert not any(v.file_path == "CORE_ROOT/run_context.py" for v in report.violations)
    violations = [v for v in report.violations if v.file_path == caller]
    if expected_code is None:
        assert "CORE_ROOT" in layer["allowed_import_layer_ids"]
        assert "CORE_ROOT" not in layer["forbidden_import_layer_ids"]
        assert violations == []
    else:
        assert "CORE_ROOT" not in layer["allowed_import_layer_ids"]
        assert ("CORE_ROOT" in layer["forbidden_import_layer_ids"]) == (expected_code == "FORBIDDEN_IMPORT")
        assert len(violations) == 1
        violation = violations[0]
        assert violation.code == expected_code
        assert violation.source_layer == source_layer and violation.target_layer == "CORE_ROOT"
        assert violation.imported_module == "CORE_ROOT.run_context"


def test_run_context_classification_preserves_bootstrap_and_mandatory_core_roots() -> None:
    layers = load_blueprint(DEFAULT_BLUEPRINT_PATH)["layers"]
    core = next(layer for layer in layers if layer["id"] == "CORE_ROOT")
    bootstrap = next(layer for layer in layers if layer["id"] == "BOOTSTRAP_ENTRYPOINTS")
    assert {"path": "CORE_ROOT", "mandatory": True} in core["expected_paths"]
    assert bootstrap["import_guard"] is True
    assert {"BOOT", "refactor.py"}.issubset(bootstrap["path_prefixes"])
    assert {"BOOT", "refactor"}.issubset(bootstrap["module_prefixes"])
    assert {entry["path"] for entry in bootstrap["expected_paths"]} >= {"BOOT", "refactor.py"}
    assert "CORE_ROOT/run_context.py" not in bootstrap["path_prefixes"]
    assert "CORE_ROOT.run_context" not in bootstrap["module_prefixes"]
    assert all(entry["path"] != "CORE_ROOT/run_context.py" for entry in bootstrap["expected_paths"])


def test_n8n_private_skill_reader_uses_production_owner_without_tools_import(tmp_path: Path) -> None:
    live = "MAKSIMAR_SERVER/AI_ORCHESTRATION/n8n_adapter.py"
    compatibility = "tools/jarvis_live_runtime/jarvis_skill_visibility.py"
    text = (PROJECT_ROOT / live).read_text(encoding="utf-8")
    tree = ast.parse(text)
    imports = [node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]
    assert not any((isinstance(node, ast.ImportFrom) and (node.module or "").split(".")[0] == "tools")
        or (isinstance(node, ast.Import) and any(alias.name.split(".")[0] == "tools" for alias in node.names))
        for node in imports)
    assert sum(isinstance(node, ast.FunctionDef) and node.name == "load_automation_n8n_private_skill_context"
               for node in tree.body) == 1
    assert not any(isinstance(node, ast.Name) and node.id == "select_skills_for_tools" for node in ast.walk(tree))

    for relative, source in ((live, text), (compatibility, (PROJECT_ROOT / compatibility).read_text(encoding="utf-8"))):
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(source, encoding="utf-8")
    after = build_architecture_report(tmp_path, DEFAULT_BLUEPRINT_PATH)
    assert not any(v.file_path == live and v.target_layer == "TOOLS" for v in after.violations)
    assert not any(v.file_path == compatibility for v in after.violations)
    # Counterfactual import remains forbidden: migration does not relax the scanner.
    (tmp_path / live).write_text(text + "\nfrom tools.jarvis_live_runtime.jarvis_skill_visibility import load_automation_n8n_private_skill_context\n", encoding="utf-8")
    before = build_architecture_report(tmp_path, DEFAULT_BLUEPRINT_PATH)
    violations = [v for v in before.violations if v.file_path == live and v.target_layer == "TOOLS"]
    assert len(violations) == 1 and violations[0].code == "IMPORT_NOT_ALLOWED"
def test_g8c3_existing_owner_boundaries_and_counterfactuals(tmp_path: Path) -> None:
    paths = (
        "CONTROL_PLANE/api_server.py",
        "MAKSIMAR_CORE_LIB/action_library_adapters/agent_tooling_runtime_probe.py",
        "MAKSIMAR_CORE_LIB/oob_dashboard/foundation_truth_consistency_contract.py",
        "MAKSIMAR_SERVER/AI_ORCHESTRATION/jarvis_live_read_models.py",
        "MAKSIMAR_SERVER/AI_ORCHESTRATION/ollama_transport.py",
        "MAKSIMAR_SERVER/OBSERVABILITY/jarvis_live/jarvis_live_observability_read_model.py",
        "MAKSIMAR_SERVER/EXECUTION_CONTROL/node_runtime/hardware_detection_adapter.py",
    )
    for relative in paths:
        source = PROJECT_ROOT / relative
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    report = build_architecture_report(tmp_path, DEFAULT_BLUEPRINT_PATH)
    assert not any(v.code in {"FORBIDDEN_IMPORT", "IMPORT_NOT_ALLOWED", "UNKNOWN_LOCAL_IMPORT"}
                   and v.file_path in paths for v in report.violations)
    # The removed edges still fail the unchanged blueprint/scanner.
    counterfactuals = {
        paths[0]: "from CORE_ROOT.run_context import model_free_startup\n",
        paths[1]: "from CORE_ROOT.run_context import model_free_startup\n",
        paths[2]: "from SUPERVISOR.runtime_preflight import inspect_runtime_state\nfrom CORE_ROOT.heartbeat_io import safe_read_json\nfrom CORE_ROOT import runtime_paths\n",
        paths[4]: "from SUPERVISOR.runtime_preflight import inspect_runtime_state\nfrom MAKSIMAR_SERVER.EXECUTION_CONTROL.node_runtime import hardware_detection_adapter\n",
    }
    for relative, imports in counterfactuals.items():
        with (tmp_path / relative).open("a", encoding="utf-8") as target:
            target.write("\n" + imports)
    before = build_architecture_report(tmp_path, DEFAULT_BLUEPRINT_PATH)
    violations = [v for v in before.violations if v.code in {"FORBIDDEN_IMPORT", "IMPORT_NOT_ALLOWED"}]
    assert len(violations) == 7


def test_s1_uses_one_supervisor_entrypoint_and_keeps_reverse_edge_forbidden(tmp_path):
    core = (PROJECT_ROOT / "CORE_ROOT/stop_gate.py").read_text()
    supervisor = ast.parse((PROJECT_ROOT / "SUPERVISOR/runtime_preflight.py").read_text())
    entries = [n for n in supervisor.body if isinstance(n, ast.FunctionDef) and n.name == "recover_previous_run_degradation"]
    assert len(entries) == 1 and not entries[0].args.args and not entries[0].args.kwonlyargs
    assert "def recover_previous_run_degradation" not in core
    assert not any((n.module or "").split(".")[0] == "SUPERVISOR" for n in ast.walk(ast.parse(core)) if isinstance(n, ast.ImportFrom))
    for path in ("tools/work", "RUNTIME/recovery_manager.py"):
        text = (PROJECT_ROOT / path).read_text()
        assert "from SUPERVISOR.runtime_preflight import recover_previous_run_degradation" in text
        assert "from CORE_ROOT.stop_gate import recover_previous_run_degradation" not in text
    target = tmp_path / "CORE_ROOT/stop_gate.py"
    target.parent.mkdir(parents=True)
    target.write_text(core + "\nfrom SUPERVISOR.runtime_preflight import inspect_runtime_state\n")
    active = tmp_path / "SUPERVISOR/runtime_preflight.py"
    active.parent.mkdir()
    active.write_text("pass\n")
    report = build_architecture_report(tmp_path, DEFAULT_BLUEPRINT_PATH)
    assert any(v.file_path == "CORE_ROOT/stop_gate.py" and v.code == "FORBIDDEN_IMPORT" for v in report.violations)
