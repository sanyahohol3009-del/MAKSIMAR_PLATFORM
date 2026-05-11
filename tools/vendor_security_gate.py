from __future__ import annotations

import argparse
import ast
import hashlib
import json
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RISKY_IMPORTS = {
    "subprocess",
    "socket",
    "requests",
    "urllib",
    "httpx",
    "ftplib",
    "paramiko",
    "pickle",
}

RISKY_CALLS = {
    "eval",
    "exec",
    "compile",
    "os.system",
    "subprocess.Popen",
    "subprocess.run",
    "subprocess.call",
    "subprocess.check_output",
    "shutil.rmtree",
    "os.remove",
    "os.unlink",
}

FORBIDDEN_COUPLING_MARKERS = (
    "CORE_ROOT",
    "RUNTIME",
    "SUPERVISOR",
    "MAKSIMAR_SERVER.EXECUTION_CONTROL",
)


@dataclass(frozen=True, slots=True)
class CommandResult:
    command: tuple[str, ...]
    available: bool
    returncode: int | None
    stdout_head: str
    stderr_head: str
    output_path: str | None
    skipped_reason: str | None


@dataclass(frozen=True, slots=True)
class VendorGateReport:
    schema_version: int
    vendor_name: str
    timestamp_utc: str
    source_dir: str
    expected_remote: str
    observed_remote: str
    official_remote_verified: bool
    commit: str
    commit_seen_in_remote_refs: bool
    commit_in_remote_ref_tips: bool
    commit_matches_version_lock: bool
    version_lock_paths: tuple[str, ...]
    tree_sha: str
    archive_sha256: str
    tracked_file_count: int
    python_file_count: int
    required_files_present: dict[str, bool]
    non_empty_project: bool
    external_code_not_committed: bool
    canonical_memory_access: bool
    runtime_mutation_allowed: bool
    forbidden_coupling_findings_count: int
    forbidden_coupling_findings: tuple[dict[str, str], ...]
    risky_static_findings_count: int
    risky_static_findings: tuple[dict[str, str], ...]
    scanner_results: dict[str, dict[str, Any]]
    hard_gate_passed: bool
    manual_security_review_required: bool
    hard_blockers: tuple[str, ...]
    manual_review_reasons: tuple[str, ...]


def _run(
    command: list[str],
    *,
    timeout: int = 120,
    output_path: Path | None = None,
) -> CommandResult:
    binary = shutil.which(command[0])
    if binary is None:
        return CommandResult(
            command=tuple(command),
            available=False,
            returncode=None,
            stdout_head="",
            stderr_head="",
            output_path=str(output_path) if output_path else None,
            skipped_reason=f"{command[0]} not installed",
        )

    completed = subprocess.run(
        command,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
        check=False,
    )

    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(
                {
                    "command": command,
                    "returncode": completed.returncode,
                    "stdout": completed.stdout,
                    "stderr": completed.stderr,
                },
                indent=2,
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )

    return CommandResult(
        command=tuple(command),
        available=True,
        returncode=completed.returncode,
        stdout_head=completed.stdout[:1000],
        stderr_head=completed.stderr[:1000],
        output_path=str(output_path) if output_path else None,
        skipped_reason=None,
    )


def _git(source_dir: Path, args: list[str]) -> str:
    return subprocess.check_output(
        ["git", "-C", str(source_dir), *args],
        text=True,
    ).strip()


def _project_git(args: list[str]) -> str:
    return subprocess.check_output(["git", *args], text=True).strip()


def _archive_sha256(source_dir: Path) -> str:
    archive_bytes = subprocess.check_output(
        ["git", "-C", str(source_dir), "archive", "--format=tar", "HEAD"]
    )
    return hashlib.sha256(archive_bytes).hexdigest()


def _version_lock_commit_matches(source_dir: Path, commit: str) -> tuple[str, ...]:
    manifests_dir = source_dir.parent / "manifests"

    if not manifests_dir.exists():
        return ()

    matches: list[str] = []

    for lock_path in sorted(manifests_dir.glob("*version_lock*.json")):
        try:
            payload = json.loads(lock_path.read_text(encoding="utf-8"))
        except Exception:
            continue

        if payload.get("git_commit") == commit:
            matches.append(str(lock_path))

    return tuple(matches)


def _scan_python_ast(source_dir: Path, python_files: list[str]) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    risky_findings: list[dict[str, str]] = []
    coupling_findings: list[dict[str, str]] = []

    for rel in python_files:
        path = source_dir / rel
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
            tree = ast.parse(text)
        except Exception as exc:
            risky_findings.append({"file": rel, "kind": "parse_error", "detail": repr(exc)})
            continue

        for marker in FORBIDDEN_COUPLING_MARKERS:
            if marker in text:
                coupling_findings.append({"file": rel, "kind": "forbidden_marker", "detail": marker})

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    base = alias.name.split(".")[0]
                    if base in RISKY_IMPORTS:
                        risky_findings.append({"file": rel, "kind": "risky_import", "detail": alias.name})

            if isinstance(node, ast.ImportFrom):
                module = node.module or ""
                base = module.split(".")[0]
                if base in RISKY_IMPORTS:
                    risky_findings.append({"file": rel, "kind": "risky_import_from", "detail": module})

            if isinstance(node, ast.Call):
                name = _call_name(node)
                if name in RISKY_CALLS:
                    risky_findings.append({"file": rel, "kind": "risky_call", "detail": name})

    return risky_findings, coupling_findings


def _call_name(node: ast.Call) -> str | None:
    if isinstance(node.func, ast.Name):
        return node.func.id

    if isinstance(node.func, ast.Attribute):
        parts: list[str] = []
        current: ast.AST = node.func

        while isinstance(current, ast.Attribute):
            parts.append(current.attr)
            current = current.value

        if isinstance(current, ast.Name):
            parts.append(current.id)

        return ".".join(reversed(parts))

    return None


def _run_optional_scanners(
    *,
    source_dir: Path,
    reports_dir: Path,
    venv_python: Path | None,
) -> dict[str, dict[str, Any]]:
    reports_dir.mkdir(parents=True, exist_ok=True)
    results: dict[str, CommandResult] = {}

    results["bandit"] = _run(
        [
            sys.executable,
            "-m",
            "bandit",
            "-r",
            str(source_dir),
            "-f",
            "json",
            "-o",
            str(reports_dir / "vendor_bandit_report.json"),
        ],
        timeout=300,
    )

    if venv_python and venv_python.exists():
        results["pip_audit"] = _run(
            [
                str(venv_python),
                "-m",
                "pip_audit",
                "-f",
                "json",
                "-o",
                str(reports_dir / "vendor_pip_audit_report.json"),
            ],
            timeout=300,
        )
    else:
        results["pip_audit"] = CommandResult(
            command=(),
            available=False,
            returncode=None,
            stdout_head="",
            stderr_head="",
            output_path=str(reports_dir / "vendor_pip_audit_report.json"),
            skipped_reason="vendor venv python not provided or missing",
        )

    results["clamscan"] = _run(
        ["clamscan", "-r", str(source_dir)],
        timeout=300,
        output_path=reports_dir / "vendor_clamscan_report.json",
    )

    results["detect_secrets"] = _run(
        [
            sys.executable,
            "-m",
            "detect_secrets",
            "scan",
            str(source_dir),
        ],
        timeout=300,
        output_path=reports_dir / "vendor_detect_secrets_report.json",
    )

    results["semgrep"] = _run(
        [
            sys.executable,
            "-m",
            "semgrep",
            "scan",
            "--json",
            str(source_dir),
        ],
        timeout=300,
        output_path=reports_dir / "vendor_semgrep_report.json",
    )

    results["gitleaks"] = _run(
        [
            "gitleaks",
            "detect",
            "--source",
            str(source_dir),
            "--report-format",
            "json",
            "--report-path",
            str(reports_dir / "vendor_gitleaks_report.json"),
            "--no-banner",
        ],
        timeout=300,
    )

    results["trufflehog"] = _run(
        [
            "trufflehog",
            "filesystem",
            str(source_dir),
            "--json",
        ],
        timeout=300,
        output_path=reports_dir / "vendor_trufflehog_report.json",
    )

    results["osv_scanner"] = _run(
        [
            "osv-scanner",
            "scan",
            "source",
            "-r",
            str(source_dir),
            "--format",
            "json",
        ],
        timeout=300,
        output_path=reports_dir / "vendor_osv_scanner_report.json",
    )

    results["syft"] = _run(
        [
            "syft",
            str(source_dir),
            "-o",
            "json",
        ],
        timeout=300,
        output_path=reports_dir / "vendor_syft_sbom.json",
    )

    results["grype"] = _run(
        [
            "grype",
            str(source_dir),
            "-o",
            "json",
        ],
        timeout=300,
        output_path=reports_dir / "vendor_grype_report.json",
    )

    return {name: asdict(result) for name, result in results.items()}


def build_vendor_gate_report(
    *,
    vendor_name: str,
    source_dir: Path,
    expected_remote: str,
    reports_dir: Path,
    required_files: tuple[str, ...],
    venv_python: Path | None,
) -> VendorGateReport:
    if not source_dir.exists():
        raise FileNotFoundError(f"source_dir not found: {source_dir}")

    observed_remote = _git(source_dir, ["remote", "get-url", "origin"])
    commit = _git(source_dir, ["rev-parse", "HEAD"])
    tree_sha = _git(source_dir, ["rev-parse", "HEAD^{tree}"])
    tracked_files = _git(source_dir, ["ls-tree", "-r", "--name-only", "HEAD"]).splitlines()
    remote_refs = subprocess.check_output(["git", "ls-remote", expected_remote], text=True)

    python_files = [item for item in tracked_files if item.endswith(".py")]
    required_files_present = {name: (source_dir / name).exists() for name in required_files}

    risky_findings, coupling_findings = _scan_python_ast(source_dir, python_files)

    source_dir_posix = source_dir.as_posix().rstrip("/")
    tracked_external = _project_git(
        [
            "ls-files",
            f"{source_dir_posix}",
            f"{source_dir_posix}/../venv",
            f"{source_dir_posix}/../sandbox_data",
        ]
    )

    scanner_results = _run_optional_scanners(
        source_dir=source_dir,
        reports_dir=reports_dir,
        venv_python=venv_python,
    )

    version_lock_paths = _version_lock_commit_matches(source_dir, commit)
    commit_in_remote_ref_tips = commit in remote_refs
    commit_matches_version_lock = bool(version_lock_paths)

    official_remote_verified = observed_remote == expected_remote
    commit_seen_in_remote_refs = commit_in_remote_ref_tips or commit_matches_version_lock
    non_empty_project = len(tracked_files) > 20 and len(python_files) > 5 and all(required_files_present.values())
    external_code_not_committed = tracked_external.strip() == ""

    canonical_memory_access = False
    runtime_mutation_allowed = False

    hard_blockers: list[str] = []
    if not official_remote_verified:
        hard_blockers.append("official_remote_verified=False")
    if not commit_seen_in_remote_refs:
        hard_blockers.append("commit_seen_in_remote_refs=False")
    if not non_empty_project:
        hard_blockers.append("non_empty_project=False")
    if not external_code_not_committed:
        hard_blockers.append("external_code_not_committed=False")
    if canonical_memory_access:
        hard_blockers.append("canonical_memory_access=True")
    if runtime_mutation_allowed:
        hard_blockers.append("runtime_mutation_allowed=True")
    if coupling_findings:
        hard_blockers.append("forbidden_CORE_RUNTIME_SUPERVISOR_EXECUTION_CONTROL_coupling_detected")

    manual_review_reasons: list[str] = []
    if risky_findings:
        manual_review_reasons.append("risky_static_findings_present")
    for scanner_name, scanner in scanner_results.items():
        if not scanner["available"]:
            manual_review_reasons.append(f"{scanner_name}_skipped")
        elif scanner["returncode"] not in (0, None):
            manual_review_reasons.append(f"{scanner_name}_returned_{scanner['returncode']}")

    hard_gate_passed = not hard_blockers
    manual_security_review_required = bool(manual_review_reasons)

    return VendorGateReport(
        schema_version=1,
        vendor_name=vendor_name,
        timestamp_utc=datetime.now(timezone.utc).isoformat(),
        source_dir=str(source_dir),
        expected_remote=expected_remote,
        observed_remote=observed_remote,
        official_remote_verified=official_remote_verified,
        commit=commit,
        commit_seen_in_remote_refs=commit_seen_in_remote_refs,
        commit_in_remote_ref_tips=commit_in_remote_ref_tips,
        commit_matches_version_lock=commit_matches_version_lock,
        version_lock_paths=version_lock_paths,
        tree_sha=tree_sha,
        archive_sha256=_archive_sha256(source_dir),
        tracked_file_count=len(tracked_files),
        python_file_count=len(python_files),
        required_files_present=required_files_present,
        non_empty_project=non_empty_project,
        external_code_not_committed=external_code_not_committed,
        canonical_memory_access=canonical_memory_access,
        runtime_mutation_allowed=runtime_mutation_allowed,
        forbidden_coupling_findings_count=len(coupling_findings),
        forbidden_coupling_findings=tuple(coupling_findings[:200]),
        risky_static_findings_count=len(risky_findings),
        risky_static_findings=tuple(risky_findings[:200]),
        scanner_results=scanner_results,
        hard_gate_passed=hard_gate_passed,
        manual_security_review_required=manual_security_review_required,
        hard_blockers=tuple(hard_blockers),
        manual_review_reasons=tuple(manual_review_reasons),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Run MAKSIMAR vendor security gate.")
    parser.add_argument("--vendor-name", required=True)
    parser.add_argument("--source-dir", required=True)
    parser.add_argument("--expected-remote", required=True)
    parser.add_argument("--reports-dir", required=True)
    parser.add_argument("--venv-python", default="")
    parser.add_argument("--required-file", action="append", default=["README.md", "pyproject.toml"])
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    venv_python = Path(args.venv_python) if args.venv_python else None

    report = build_vendor_gate_report(
        vendor_name=args.vendor_name,
        source_dir=Path(args.source_dir),
        expected_remote=args.expected_remote,
        reports_dir=Path(args.reports_dir),
        required_files=tuple(args.required_file),
        venv_python=venv_python,
    )

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(asdict(report), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(json.dumps(asdict(report), indent=2, ensure_ascii=False))

    if not report.hard_gate_passed:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
