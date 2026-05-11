from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


DENIED_ENV_KEYS = (
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "GOOGLE_API_KEY",
    "GITHUB_TOKEN",
    "HF_TOKEN",
    "HUGGINGFACE_TOKEN",
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY",
    "DATABASE_URL",
    "POSTGRES_PASSWORD",
    "REDIS_PASSWORD",
)


def _load_json(path: Path) -> dict[str, object]:
    if not path.exists():
        raise FileNotFoundError(f"missing required report: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def _build_child_code() -> str:
    return r'''
from __future__ import annotations

import importlib
import json
import os
import socket
import subprocess
import sys
import urllib.request
import shutil


DENIED_ENV_KEYS = (
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "GOOGLE_API_KEY",
    "GITHUB_TOKEN",
    "HF_TOKEN",
    "HUGGINGFACE_TOKEN",
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY",
    "DATABASE_URL",
    "POSTGRES_PASSWORD",
    "REDIS_PASSWORD",
)


def _blocked(*args, **kwargs):
    raise RuntimeError("blocked by MAKSIMAR controlled MemPalace probe")


socket.socket = _blocked
socket.create_connection = _blocked
urllib.request.urlopen = _blocked

subprocess.Popen = _blocked
subprocess.run = _blocked
subprocess.call = _blocked
subprocess.check_output = _blocked

os.system = _blocked
os.remove = _blocked
os.unlink = _blocked
shutil.rmtree = _blocked

result = {
    "import_success": False,
    "module_name": "mempalace",
    "module_file": "",
    "cwd": os.getcwd(),
    "python_executable": sys.executable,
    "denied_env_present_after_scrub": [key for key in DENIED_ENV_KEYS if key in os.environ],
    "network_operations_blocked": True,
    "subprocess_operations_blocked": True,
    "destructive_filesystem_operations_blocked": True,
    "canonical_write_allowed": False,
    "runtime_mutation_allowed": False,
}

try:
    module = importlib.import_module("mempalace")
    result["import_success"] = True
    result["module_file"] = str(getattr(module, "__file__", ""))
except Exception as exc:
    result["import_error"] = repr(exc)

print(json.dumps(result, ensure_ascii=False))
'''


def run_probe(
    *,
    venv_python: Path,
    approval_report: Path,
    sandbox_dir: Path,
    output_report: Path,
) -> int:
    project_root = Path.cwd()

    venv_python = venv_python if venv_python.is_absolute() else project_root / venv_python
    approval_report = approval_report if approval_report.is_absolute() else project_root / approval_report
    sandbox_dir = sandbox_dir if sandbox_dir.is_absolute() else project_root / sandbox_dir
    output_report = output_report if output_report.is_absolute() else project_root / output_report

    approval = _load_json(approval_report)

    if approval.get("controlled_real_backend_probe_allowed") is not True:
        raise RuntimeError("controlled real backend probe is not approved")
    if approval.get("full_real_backend_enablement_allowed") is not False:
        raise RuntimeError("full real backend enablement must remain False")
    if approval.get("general_real_backend_query_allowed") is not False:
        raise RuntimeError("general real backend query must remain False")

    if not venv_python.exists():
        raise FileNotFoundError(f"vendor venv python missing: {venv_python}")

    sandbox_dir.mkdir(parents=True, exist_ok=True)
    output_report.parent.mkdir(parents=True, exist_ok=True)

    env = {
        key: value
        for key, value in os.environ.items()
        if key not in DENIED_ENV_KEYS
    }
    env["PYTHONNOUSERSITE"] = "1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"

    completed = subprocess.run(
        [str(venv_python), "-c", _build_child_code()],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=str(sandbox_dir),
        env=env,
        timeout=120,
        check=False,
    )

    child_payload: dict[str, object]
    try:
        child_payload = json.loads(completed.stdout.strip().splitlines()[-1])
    except Exception:
        child_payload = {
            "import_success": False,
            "parse_error": True,
            "stdout_head": completed.stdout[:1000],
            "stderr_head": completed.stderr[:1000],
        }

    probe_success = (
        completed.returncode == 0
        and child_payload.get("import_success") is True
        and child_payload.get("denied_env_present_after_scrub") == []
        and child_payload.get("network_operations_blocked") is True
        and child_payload.get("subprocess_operations_blocked") is True
        and child_payload.get("destructive_filesystem_operations_blocked") is True
    )

    report = {
        "schema_version": 1,
        "probe_id": "mempalace_controlled_real_backend_probe_001",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "approval_report": str(approval_report),
        "sandbox_dir": str(sandbox_dir),
        "venv_python": str(venv_python),
        "probe_harness_used_subprocess": True,
        "backend_subprocess_allowed": False,
        "backend_network_allowed": False,
        "backend_destructive_filesystem_allowed": False,
        "canonical_write_allowed": False,
        "runtime_mutation_allowed": False,
        "full_real_backend_enablement_allowed": False,
        "general_real_backend_query_allowed": False,
        "controlled_probe_success": probe_success,
        "child_returncode": completed.returncode,
        "child_stdout_head": completed.stdout[:1000],
        "child_stderr_head": completed.stderr[:1000],
        "child_payload": child_payload,
    }

    output_report.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(json.dumps(report, indent=2, ensure_ascii=False))

    return 0 if probe_success else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Run controlled MemPalace real backend probe.")
    parser.add_argument(
        "--venv-python",
        default="EXTERNAL_BACKENDS/mempalace/venv/bin/python",
    )
    parser.add_argument(
        "--approval-report",
        default="EXTERNAL_BACKENDS/mempalace/security_reports/mempalace_real_backend_approval_envelope_report.json",
    )
    parser.add_argument(
        "--sandbox-dir",
        default="EXTERNAL_BACKENDS/mempalace/sandbox_data/controlled_probe",
    )
    parser.add_argument(
        "--output-report",
        default="EXTERNAL_BACKENDS/mempalace/smoke_reports/mempalace_controlled_real_backend_probe_report.json",
    )
    args = parser.parse_args()

    return run_probe(
        venv_python=Path(args.venv_python),
        approval_report=Path(args.approval_report),
        sandbox_dir=Path(args.sandbox_dir),
        output_report=Path(args.output_report),
    )


if __name__ == "__main__":
    raise SystemExit(main())
