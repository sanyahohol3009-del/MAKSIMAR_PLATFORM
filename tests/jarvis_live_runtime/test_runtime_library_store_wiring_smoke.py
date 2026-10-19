from __future__ import annotations

import json

import pytest

from tools.jarvis_live_runtime.jarvis_live_read_models import build_jarvis_live_tool_catalog_read_model
from MAKSIMAR_CORE_LIB.project_read.jarvis_runtime_library_store import build_runtime_library_store_read_model
from tools.jarvis_live_runtime.jarvis_skill_visibility import build_jarvis_skill_visibility_read_model


def test_runtime_library_store_reads_probe_reports_smoke(tmp_path) -> None:
    store_root = tmp_path / "jarvis_library"
    manifests_dir = store_root / "manifests"
    reports_dir = store_root / "probe_reports"
    manifests_dir.mkdir(parents=True)
    reports_dir.mkdir(parents=True)

    report_path = reports_dir / "agent_tooling_import_probe.json"
    report_path.write_text(
        json.dumps(
            {
                "venv_name": "agent_tooling",
                "python": "/tmp/venvs/agent_tooling/bin/python",
                "packages": [
                    {
                        "pip_name": "autogen-agentchat",
                        "module_name": "autogen_agentchat",
                        "category": "agents",
                        "import_ok": True,
                        "version": "0.7.5",
                        "error": "",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    (manifests_dir / "autogen-agentchat.json").write_text(
        json.dumps(
            {
                "manifest_id": "autogen-agentchat",
                "category": "agents",
                "runtime_only": True,
                "direct_execution_allowed": False,
                "approval_required_for_write_or_action": True,
                "report_file": str(report_path),
            }
        ),
        encoding="utf-8",
    )

    payload = build_runtime_library_store_read_model(store_root)

    assert payload["probe_reports_read"] == (str(report_path),)
    assert payload["available_package_names"] == ("autogen-agentchat",)
    assert payload["agents"][0]["module_name"] == "autogen_agentchat"
    assert payload["agents"][0]["version"] == "0.7.5"
    assert payload["agents"][0]["import_ok"] is True
    assert payload["agents"][0]["runtime_only"] is True
    assert payload["agents"][0]["runtime_probe_allowed"] is True
    assert payload["agents"][0]["sandbox_execution_allowed"] is True
    assert payload["agents"][0]["direct_execution_allowed"] is False


def test_tool_catalog_exposes_runtime_library_packages_smoke(monkeypatch) -> None:
    runtime_payload = {
        "packages": (
            {
                "package_name": "autogen-agentchat",
                "module_name": "autogen_agentchat",
                "version": "0.7.5",
                "import_ok": True,
                "category": "agents",
                "runtime_only": True,
            },
            {
                "package_name": "llama-index",
                "module_name": "llama_index",
                "version": "0.14.22",
                "import_ok": True,
                "category": "skills_rag",
                "runtime_only": True,
            },
            {
                "package_name": "playwright",
                "module_name": "playwright",
                "version": "1.60.0",
                "import_ok": True,
                "category": "tools_browser",
                "runtime_only": True,
            },
        ),
        "available_packages": (
            {
                "package_name": "autogen-agentchat",
                "module_name": "autogen_agentchat",
                "version": "0.7.5",
                "import_ok": True,
                "category": "agents",
                "runtime_only": True,
            },
        ),
        "package_names": ("autogen-agentchat", "llama-index", "playwright"),
        "available_package_names": ("autogen-agentchat", "llama-index", "playwright"),
        "module_names": ("autogen_agentchat", "llama_index", "playwright"),
        "agents": (
            {
                "package_name": "autogen-agentchat",
                "module_name": "autogen_agentchat",
                "version": "0.7.5",
                "import_ok": True,
                "category": "agents",
                "runtime_only": True,
            },
        ),
        "skills_rag": (
            {
                "package_name": "llama-index",
                "module_name": "llama_index",
                "version": "0.14.22",
                "import_ok": True,
                "category": "skills_rag",
                "runtime_only": True,
            },
        ),
        "tools_browser": (
            {
                "package_name": "playwright",
                "module_name": "playwright",
                "version": "1.60.0",
                "import_ok": True,
                "category": "tools_browser",
                "runtime_only": True,
            },
        ),
        "categories": ("agents", "skills_rag", "tools_browser"),
        "probe_reports_read": ("/tmp/agent_tooling_import_probe.json",),
    }
    monkeypatch.setattr(
        "tools.jarvis_live_runtime.jarvis_live_read_models.build_runtime_library_store_read_model",
        lambda: runtime_payload,
    )

    catalog = build_jarvis_live_tool_catalog_read_model()

    assert "autogen-agentchat" in catalog["runtime_library_package_names"]
    assert "llama-index" in catalog["runtime_library_package_names"]
    assert "playwright" in catalog["runtime_library_package_names"]
    assert catalog["runtime_library_categories"] == ("agents", "skills_rag", "tools_browser")
    assert catalog["runtime_library_execution_allowed"] is True
    assert catalog["runtime_probe_allowed"] is True
    assert catalog["sandbox_execution_allowed"] is True


def test_skill_visibility_runtime_library_store_stays_proposal_only_smoke(monkeypatch) -> None:
    runtime_payload = {
        "packages": (
            {
                "package_name": "browser-use",
                "module_name": "browser_use",
                "version": "0.13.1",
                "import_ok": True,
                "category": "tools_browser",
                "runtime_only": True,
            },
        ),
        "available_packages": (
            {
                "package_name": "browser-use",
                "module_name": "browser_use",
                "version": "0.13.1",
                "import_ok": True,
                "category": "tools_browser",
                "runtime_only": True,
            },
        ),
        "package_names": ("browser-use",),
        "available_package_names": ("browser-use",),
        "module_names": ("browser_use",),
        "agents": (),
        "skills_rag": (),
        "tools_browser": (
            {
                "package_name": "browser-use",
                "module_name": "browser_use",
                "version": "0.13.1",
                "import_ok": True,
                "category": "tools_browser",
                "runtime_only": True,
            },
        ),
        "categories": ("agents", "skills_rag", "tools_browser"),
        "probe_reports_read": ("/tmp/browser_tooling_import_probe.json",),
    }
    monkeypatch.setattr(
        "tools.jarvis_live_runtime.jarvis_live_read_models.build_runtime_library_store_read_model",
        lambda: runtime_payload,
    )
    monkeypatch.setattr(
        "tools.jarvis_live_runtime.jarvis_skill_visibility.build_runtime_library_store_read_model",
        lambda: runtime_payload,
    )

    visibility = build_jarvis_skill_visibility_read_model()

    assert visibility["runtime_library_package_names"] == ("browser-use",)
    assert visibility["runtime_library_execution_allowed"] is True
    assert visibility["runtime_probe_allowed"] is True
    assert visibility["sandbox_execution_allowed"] is True
    assert visibility["runtime_library_install_allowed"] is False
    assert visibility["runtime_library_download_allowed"] is False


@pytest.mark.parametrize("report_setting", [None, "", "   ", "explicit", "explicit_missing", "malformed"])
def test_runtime_library_report_path_binding_preserves_observed_availability(tmp_path, report_setting):
    store = tmp_path / "library"
    (store / "manifests").mkdir(parents=True)
    (store / "probe_reports").mkdir()
    fallback = store / "probe_reports" / "agents_import_probe.json"
    report = {"venv_name": "observed_venv", "python": "/observed/python", "packages": [
        {"pip_name": "observed-package", "module_name": "observed_module", "import_ok": True, "version": "1.2"},
        {"pip_name": "different-package", "module_name": "other", "import_ok": False},
    ]}
    fallback.write_text(json.dumps(report), encoding="utf-8")
    manifest = {"manifest_id": "observed-package", "category": "agents"}
    chosen = fallback
    expected = True
    if report_setting == "explicit":
        chosen = store / "custom_report.json"
        chosen.write_text(json.dumps({**report, "venv_name": "explicit_venv"}), encoding="utf-8")
        manifest["report_file"] = str(chosen)
    elif report_setting == "explicit_missing":
        chosen = store / "missing_report.json"
        manifest["report_file"] = str(chosen)
        expected = False  # A supplied missing path must not silently use the available fallback.
    elif report_setting == "malformed":
        fallback.write_text("not-json", encoding="utf-8")
        expected = False
    elif report_setting is not None:
        manifest["report_file"] = report_setting
    (store / "manifests" / "observed-package.json").write_text(json.dumps(manifest), encoding="utf-8")
    payload = build_runtime_library_store_read_model(store)
    package = payload["packages"][0]
    assert package["import_ok"] is expected
    assert package["probe_report_file"] == str(chosen)
    assert payload["probe_reports_read"] == (str(chosen),)
    assert payload["available_count"] == int(expected)
    assert payload["unavailable_count"] == int(not expected)
    assert payload["available_package_names"] == (("observed-package",) if expected else ())
    assert package["direct_execution_allowed"] is False
    assert package["approval_required_for_runtime_execution"] is True
    assert payload["install_allowed"] is False
    if expected:
        assert package["module_name"] == "observed_module"
        assert package["runtime_python"] == "/observed/python"
        assert package["venv_name"] == ("explicit_venv" if report_setting == "explicit" else "observed_venv")
