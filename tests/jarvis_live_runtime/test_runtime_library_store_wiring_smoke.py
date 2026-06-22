from __future__ import annotations

import json

from tools.jarvis_live_runtime.jarvis_live_read_models import build_jarvis_live_tool_catalog_read_model
from tools.jarvis_live_runtime.jarvis_runtime_library_store import build_runtime_library_store_read_model
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
    assert catalog["runtime_library_execution_allowed"] is False


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
    assert visibility["runtime_library_execution_allowed"] is False
    assert visibility["runtime_library_install_allowed"] is False
    assert visibility["runtime_library_download_allowed"] is False
