from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.project_read import codegraph_readonly_adapter as adapter


def test_codegraph_missing_returns_graceful_unavailable(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(adapter, "CODEGRAPH_OUT_ROOT", tmp_path / "codegraph-out")
    monkeypatch.setattr(adapter, "CODEGRAPH_GRAPH_JSON", tmp_path / "codegraph-out" / "graph.json")
    monkeypatch.setattr(adapter, "CODEGRAPH_GRAPH_REPORT", tmp_path / "codegraph-out" / "GRAPH_REPORT.md")
    monkeypatch.setattr(adapter, "CODEGRAPH_WIKI_INDEX", tmp_path / "codegraph-out" / "wiki" / "index.md")
    monkeypatch.setattr(adapter, "CODEGRAPH_EXECUTABLE", tmp_path / ".venv" / "bin" / "codegraph")

    payload = adapter.build_codegraph_readonly_response("dependency graph")

    assert payload["graph_available"] is False
    assert payload["response_text"] == "Codegraph is installed but graph.json is not built yet."
    assert payload["error_kind"] == ""


def test_codegraph_present_reads_report_with_cap(monkeypatch, tmp_path: Path) -> None:
    root = tmp_path / "codegraph-out"
    root.mkdir(parents=True)
    (root / "graph.json").write_text("{}", encoding="utf-8")
    (root / "GRAPH_REPORT.md").write_text("# Report\ncentral nodes: jarvis_live_brain_loop.py\n" + ("x" * 5000), encoding="utf-8")
    monkeypatch.setattr(adapter, "CODEGRAPH_OUT_ROOT", root)
    monkeypatch.setattr(adapter, "CODEGRAPH_GRAPH_JSON", root / "graph.json")
    monkeypatch.setattr(adapter, "CODEGRAPH_GRAPH_REPORT", root / "GRAPH_REPORT.md")
    monkeypatch.setattr(adapter, "CODEGRAPH_WIKI_INDEX", root / "wiki" / "index.md")
    monkeypatch.setattr(adapter, "CODEGRAPH_EXECUTABLE", tmp_path / ".venv" / "bin" / "codegraph")
    monkeypatch.setattr(adapter, "_resolve_codegraph_executable", lambda: None)

    payload = adapter.build_codegraph_readonly_response("central nodes", output_budget=200)

    assert payload["graph_available"] is True
    assert payload["report_available"] is True
    assert len(payload["response_text"]) <= 200
    assert str(root / "GRAPH_REPORT.md") in payload["source_files"]


def test_codegraph_query_uses_cli_read_only_with_timeout(monkeypatch, tmp_path: Path) -> None:
    root = tmp_path / "codegraph-out"
    root.mkdir(parents=True)
    (root / "graph.json").write_text("{}", encoding="utf-8")
    executable = tmp_path / ".venv" / "bin" / "codegraph"
    executable.parent.mkdir(parents=True)
    executable.write_text("", encoding="utf-8")
    monkeypatch.setattr(adapter, "CODEGRAPH_OUT_ROOT", root)
    monkeypatch.setattr(adapter, "CODEGRAPH_GRAPH_JSON", root / "graph.json")
    monkeypatch.setattr(adapter, "CODEGRAPH_GRAPH_REPORT", root / "GRAPH_REPORT.md")
    monkeypatch.setattr(adapter, "CODEGRAPH_WIKI_INDEX", root / "wiki" / "index.md")
    monkeypatch.setattr(adapter, "CODEGRAPH_EXECUTABLE", executable)

    called: dict[str, object] = {}

    class Completed:
        returncode = 0
        stdout = "node: tools/jarvis_live_runtime/live_intent_policy.py\nedge: api_server -> handle_hot_request\n"

    def fake_run(command, **kwargs):
        called["command"] = command
        called["timeout"] = kwargs.get("timeout")
        return Completed()

    monkeypatch.setattr(adapter.subprocess, "run", fake_run)

    payload = adapter.build_codegraph_readonly_response("call chain", output_budget=120)

    assert payload["cli_used"] is True
    assert payload["error_kind"] == ""
    assert called["command"][1] == "query"
    assert called["timeout"] == 5.0
    assert len(payload["response_text"]) <= 120


def test_codegraph_adapter_does_not_rebuild_in_hotpath() -> None:
    source = Path("MAKSIMAR_CORE_LIB/project_read/codegraph_readonly_adapter.py").read_text(encoding="utf-8")

    assert "_rebuild_code" not in source


def test_generated_codegraph_output_remains_ignored() -> None:
    gitignore = Path(".gitignore").read_text(encoding="utf-8")
    assert "codegraph-out/" in gitignore


def test_root_agents_is_canonical_entrypoint_not_second_constitution() -> None:
    source = Path("AGENTS.md").read_text(encoding="utf-8")

    for marker in (
        "PERSONAL_JARVIS_RECOVERY", "P2 / Phase 1B", "PENDING", "Do not start P3",
        "REUSE → EXTEND → MIGRATE → DELETE", "Parallel worlds are forbidden", "Phrase, keyword, regex",
        "correction-only", "one canonical Semantic Spine", "one Final Brain",
        "Preserve existing tests", "Do not commit or push",
    ):
        assert marker in source
    for reference in (
        "PHASE_1B_PLAN.md", "PHASE_1B_FINAL_REPORT.md",
        "CANONICAL_SEMANTIC_PROJECT_READ_SPINE_v1.md", "PERSONAL_OWNER_AUTONOMY_POLICY.md",
        "PHASE_1_DEPENDENCY_MAP.md", "PHASE_1A_TEST_REPLACEMENT_LEDGER.md",
    ):
        assert reference in source
    assert "Codegraph rebuild is a separate acceptance gate" in source
    assert "shell exit code of zero is insufficient" in source
    assert "_rebuild_code" not in source


def test_existing_codegraph_identity_keeps_same_basename_owners_distinct(tmp_path):
    from codegraph.extract import extract_python
    (tmp_path / ".git").mkdir()
    results = []
    for folder in ("android", "ios", "A-B", "A_B"):
        path = tmp_path / folder / "store.py"
        path.parent.mkdir()
        path.write_text("class Store:\n    def append(self): pass\n")
        results.append(extract_python(path))
    ids = [node["id"] for result in results for node in result["nodes"]]
    assert len(ids) == len(set(ids))
    for result in results:
        assert any(node["label"] == "Store" for node in result["nodes"])


def test_existing_codegraph_identity_is_stable_for_relative_and_absolute_paths(tmp_path, monkeypatch):
    from codegraph.extract import extract_python
    (tmp_path / ".git").mkdir()
    path = tmp_path / "store.py"
    path.write_text("class Store: pass\n")
    monkeypatch.chdir(tmp_path)
    assert [n["id"] for n in extract_python(path)["nodes"]] == [n["id"] for n in extract_python(Path("store.py"))["nodes"]]


def test_existing_codegraph_resolves_full_and_relative_module_identity(tmp_path):
    from codegraph.extract import extract_python, _resolve_cross_file_imports
    (tmp_path / ".git").mkdir()
    paths = []
    for folder in ("android", "ios"):
        root = tmp_path / folder
        root.mkdir()
        store = root / "store.py"
        store.write_text("class Store: pass\n")
        caller = root / "caller.py"
        caller.write_text("from .store import Store as CurrentStore\nclass Reader: pass\n")
        paths.extend((store, caller))
    external = tmp_path / "reader.py"
    external.write_text("from android.store import Store\nclass Reader: pass\n")
    paths.append(external)
    results = [extract_python(p) for p in paths]
    edges = _resolve_cross_file_imports(results, paths)
    owners = {n["id"]: n["source_file"] for r in results for n in r["nodes"]}
    uses = [e for e in edges if e["relation"] == "uses"]
    assert len(uses) == 3
    for edge in uses:
        source = Path(owners[edge["source"]])
        target = Path(owners[edge["target"]])
        expected = "android" if source == external else source.parent.name
        assert target.parent.name == expected
        assert edge["confidence"] == "INFERRED"


def test_existing_codegraph_cache_does_not_reuse_pre_identity_migration_entries(tmp_path):
    import hashlib, json
    from codegraph.cache import cache_dir, file_hash, load_cached, save_cached
    path = tmp_path / "store.py"
    path.write_text("class Store: pass\n")
    old = hashlib.sha256(path.read_bytes() + b"\x00" + str(path.resolve()).encode()).hexdigest()
    legacy = cache_dir(tmp_path) / (old + ".json")
    legacy.write_text(json.dumps({"nodes": [{"id": "store"}], "edges": []}))
    assert file_hash(path) != old
    assert load_cached(path, tmp_path) is None
    current = {"nodes": [{"id": "current_scoped_identity"}], "edges": []}
    save_cached(path, current, tmp_path)
    assert load_cached(path, tmp_path) == current
    assert legacy.exists()



def test_existing_codegraph_preserves_function_local_and_nested_import_sites(tmp_path):
    from codegraph.extract import extract_python
    (tmp_path / ".git").mkdir()
    source = "from native.store import Store\ndef outer():\n    from native.store import Store\n    def inner():\n        from native.store import Store\n    return inner\nclass Reader:\n    async def read(self):\n        try:\n            from native.store import Store\n        except ImportError:\n            import native.store\n"
    path = tmp_path / "caller.py"
    path.write_text(source)
    result = extract_python(path)
    imports = [edge for edge in result["edges"] if edge["relation"] in {"imports", "imports_from"}]
    assert len(imports) == 5
    assert {edge["source_location"] for edge in imports} == {"L1", "L3", "L5", "L10", "L12"}
    assert len({(edge["source"], edge["target"], edge["relation"], edge["source_location"]) for edge in imports}) == 5
    assert all(edge["confidence"] == "EXTRACTED" for edge in imports)


def test_existing_codegraph_local_import_upgrade_keeps_old_cache_as_evidence(tmp_path):
    import hashlib, json
    from codegraph.cache import cache_dir, file_hash, load_cached
    path = tmp_path / "store.py"
    path.write_text("def read():\n    from native.store import Store\n")
    old = hashlib.sha256(b"project-relative-symbol-v1\x00" + path.read_bytes() + b"\x00" + str(path.resolve()).encode()).hexdigest()
    legacy = cache_dir(tmp_path) / (old + ".json")
    legacy.write_text(json.dumps({"nodes": [{"id": "same_source_identity"}], "edges": []}))
    assert file_hash(path) != old
    assert load_cached(path, tmp_path) is None
    assert legacy.exists()


def test_existing_codegraph_decorated_methods_keep_exact_class_owner(tmp_path):
    from codegraph.extract import extract_python
    (tmp_path / ".git").mkdir()
    source = "class First:\n    @classmethod\n    def generation_schema(cls):\n        \"\"\"A schema belongs to its exact class, including rationale ownership.\"\"\"\n        return {}\nclass Second:\n    @staticmethod\n    def generation_schema():\n        return {}\n"
    path = tmp_path / "owners.py"
    path.write_text(source)
    result = extract_python(path)
    nodes = {n["id"]: n for n in result["nodes"]}
    classes = {n["label"]: n["id"] for n in result["nodes"] if n["label"] in {"First", "Second"}}
    methods = [e for e in result["edges"] if e["relation"] == "method"]
    assert {e["source"] for e in methods} == set(classes.values())
    assert len({e["target"] for e in methods}) == 2
    assert all(nodes[e["target"]]["label"] == ".generation_schema()" for e in methods)
    assert all(e["source"] in nodes and e["target"] in nodes for e in result["edges"])


def test_existing_codegraph_python_calls_do_not_borrow_another_receiver_owner(tmp_path):
    from codegraph.extract import extract_python
    (tmp_path / ".git").mkdir()
    path = tmp_path / "receivers.py"
    path.write_text("class First:\n    def append(self, value): pass\n    def run(self):\n        values = []\n        values.append(1)\n        self.append(2)\nclass Second:\n    def append(self, value): pass\n    def run(self):\n        self.append(3)\ndef collect(values):\n    values.append(4)\n")
    result = extract_python(path)
    nodes = {n["id"]: n for n in result["nodes"]}
    ownership = {e["target"]: nodes[e["source"]]["label"] for e in result["edges"] if e["relation"] == "method"}
    calls = [e for e in result["edges"] if e["relation"] == "calls"]
    assert len(calls) == 2
    assert {e["source_location"] for e in calls} == {"L6", "L10"}
    assert all(ownership[e["source"]] == ownership[e["target"]] for e in calls)


def test_existing_codegraph_module_references_are_scoped_and_not_installation_claims(tmp_path):
    from codegraph.extract import extract
    from codegraph.validate import validate_extraction
    (tmp_path / ".git").mkdir()
    paths = []
    for package in ("first", "second", "regular"):
        folder = tmp_path / package
        folder.mkdir()
        if package == "regular":
            init = folder / "__init__.py"
            init.write_text("")
            paths.append(init)
        store = folder / "store.py"
        store.write_text("class Store: pass\n")
        caller = folder / "caller.py"
        caller.write_text("from . import store\nimport entirely_unconfigured_provider\nclass Reader: pass\n")
        paths.extend((store, caller))
    result = extract(paths)
    assert validate_extraction(result) == []
    refs = [n for n in result["nodes"] if n.get("entity_kind") == "module_reference"]
    assert {n["label"] for n in refs} == {"first", "second", "entirely_unconfigured_provider"}
    assert len({n["id"] for n in refs}) == 3
    assert all(n["runtime_import_status"] == "NOT_PROBED" for n in refs)
    nodes = {n["id"]: n for n in result["nodes"]}
    children = [e for e in result["edges"] if e["relation"] == "imports_from" and nodes[e["target"]].get("source_file", "").endswith("store.py")]
    assert len(children) == 3
    assert all(Path(nodes[e["source"]]["source_file"]).parent == Path(nodes[e["target"]]["source_file"]).parent for e in children)
