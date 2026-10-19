from __future__ import annotations

import json
import hashlib
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeout
from pathlib import Path
from typing import Any, Callable

from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import (
    EvidenceBundle,
    EvidenceItem,
    ExecutionReceipt,
    ExecutionPlan,
    ProjectUnderstandingPort,
    RequestUnderstanding,
    RequestDeadline,
    utc_observed_at,
)
from MAKSIMAR_CORE_LIB.architecture_map.architecture_radar import build_architecture_report
from MAKSIMAR_CORE_LIB.retrieval_backend import (
    build_retrieval_backend_status_read_model,
    inspect_qdrant_readonly_availability,
)
from MAKSIMAR_SERVER.AI_ORCHESTRATION.project_workspace_tools import (
    PROJECT_ROOT,
    read_file_outline,
    read_file_snippet,
    repo_files,
    repo_git_evidence,
    repo_import_graph,
    repo_search,
    repo_tree,
)
from MAKSIMAR_CORE_LIB.project_read.codegraph_readonly_adapter import (
    build_codegraph_readonly_response,
)
from MAKSIMAR_SERVER.AI_ORCHESTRATION.jarvis_live_read_models import (
    build_jarvis_live_memory_federation_status,
    build_jarvis_live_tool_catalog_read_model,
    build_project_workspace_read_model,
    model_runtime_status,
    status_tools,
)
from MAKSIMAR_CORE_LIB.project_read.jarvis_runtime_library_store import (
    build_flutter_runtime_status_read_model,
    build_runtime_library_store_read_model,
)


PROJECT_READONLY_INVENTORY_CONTRACTS: dict[str, tuple[dict[str, Any], ...]] = {
    "read_file_snippet": ({
        "operation_id": "read_file_snippet",
        "description": "Read a bounded text snippet. The path is relative to the canonical project root unless the source supplies an absolute path inside that root. A root-level filename remains that filename; never invent a project-name or goal-ID prefix.",
        "required_parameters": ("path",), "evidence_kinds": ("file_snippet",),
        "effect_type": "OBSERVE", "target_scope": "local_project_worktree",
        "semantic_owner_id": "project.read",
        "reversibility": "REVERSIBLE", "external_side_effect": False, "risk_class": "READ_ONLY",
    },),
    "read_file_outline": ({
        "operation_id": "read_file_outline",
        "description": "Read the syntax outline. The path is relative to the canonical project root unless the source supplies an absolute path inside that root; never invent a project-name or goal-ID prefix.",
        "required_parameters": ("path",), "evidence_kinds": ("file_outline",),
        "effect_type": "OBSERVE", "target_scope": "local_project_worktree",
        "semantic_owner_id": "project.read",
        "reversibility": "REVERSIBLE", "external_side_effect": False, "risk_class": "READ_ONLY",
    },),
    "project_codegraph_readonly": ({
        "operation_id": "query_codegraph",
        "description": "Query existing read-only codegraph artifacts without rebuilding them.",
        "required_parameters": ("query",), "evidence_kinds": ("codegraph",),
        "effect_type": "OBSERVE", "target_scope": "local_project_worktree",
        "semantic_owner_id": "project.read",
        "reversibility": "REVERSIBLE", "external_side_effect": False, "risk_class": "READ_ONLY",
    },),
    "build_project_workspace_read_model": ({
        "operation_id": "read_project_workspace_model",
        "description": (
            "Read a broad composite project snapshot spanning Git status, repository tree and files, "
            "plus model and runtime status; use narrower evidence operations when that extra scope is unnecessary."
        ),
        "required_parameters": (), "evidence_kinds": ("project_read_model",),
        "effect_type": "OBSERVE", "target_scope": "local_project_worktree",
        "semantic_owner_id": "project.read",
        "reversibility": "REVERSIBLE", "external_side_effect": False, "risk_class": "READ_ONLY",
    },),
    "build_jarvis_live_tool_catalog_read_model": ({
        "operation_id": "read_tool_catalog",
        "description": "Read the existing tools, adapters and runtime-library catalog.",
        "required_parameters": (), "evidence_kinds": ("tool_catalog",),
        "effect_type": "OBSERVE", "target_scope": "local_runtime",
        "semantic_owner_id": "developer.runtime",
        "reversibility": "REVERSIBLE", "external_side_effect": False, "risk_class": "READ_ONLY",
    },),
    "build_jarvis_live_memory_federation_status": ({
        "operation_id": "read_memory_federation_status",
        "description": "Observe live memory owners/layers, physical paths/counts, domain state, session health and Mempalace auxiliary role/authority/index health. Shared JARVIS/UI projection.",
        "required_parameters": (), "evidence_kinds": ("memory_federation",),
        "effect_type": "OBSERVE", "target_scope": "local_memory_runtime",
        "semantic_owner_id": "memory.retrieve",
        "reversibility": "REVERSIBLE", "external_side_effect": False, "risk_class": "READ_ONLY",
    },),
    "status_tools": ({
        "operation_id": "read_project_status_tools",
        "description": (
            "Run existing project readiness and roadmap-drift status scripts; "
            "this is not a Git worktree or changed-file inspection."
        ),
        "required_parameters": (), "evidence_kinds": ("project_status_tools",),
        "effect_type": "OBSERVE", "target_scope": "local_project_worktree",
        "semantic_owner_id": "project.read",
        "reversibility": "REVERSIBLE", "external_side_effect": False, "risk_class": "READ_ONLY",
    },),
    "model_runtime_status": ({
        "operation_id": "read_model_runtime_status",
        "description": "Read current local model and host-resource status.",
        "required_parameters": (), "evidence_kinds": ("model_runtime_status",),
        "effect_type": "OBSERVE", "target_scope": "local_runtime",
        "semantic_owner_id": "developer.runtime",
        "reversibility": "REVERSIBLE", "external_side_effect": False, "risk_class": "READ_ONLY",
    },),
    "qdrant_readonly_status": ({
        "operation_id": "read_qdrant_readonly_status",
        "description": "Read current local Qdrant source and runtime availability without starting a server.",
        "required_parameters": (), "evidence_kinds": ("qdrant_readonly_status",),
        "effect_type": "OBSERVE", "target_scope": "local_project_runtime",
        "semantic_owner_id": "project.read",
        "reversibility": "REVERSIBLE", "external_side_effect": False, "risk_class": "READ_ONLY",
    },),
    "retrieval_backend_status_read_model": ({
        "operation_id": "read_retrieval_backend_status",
        "description": "Read the existing local retrieval-backend adapter status model without executing a backend.",
        "required_parameters": (), "evidence_kinds": ("retrieval_backend_status",),
        "effect_type": "OBSERVE", "target_scope": "local_project_runtime",
        "semantic_owner_id": "project.read",
        "reversibility": "REVERSIBLE", "external_side_effect": False, "risk_class": "READ_ONLY",
    },),
    "jarvis_runtime_library:agents": ({
        "operation_id": "read_runtime_library_agents",
        "description": "Read installed agent packages from the existing runtime library store.",
        "required_parameters": (), "evidence_kinds": ("runtime_library_agents",),
        "effect_type": "OBSERVE", "target_scope": "local_runtime_library",
        "semantic_owner_id": "developer.runtime",
        "reversibility": "REVERSIBLE", "external_side_effect": False, "risk_class": "READ_ONLY",
    },),
    "jarvis_runtime_library:skills": ({
        "operation_id": "read_runtime_library_skills",
        "description": "Read installed skill and retrieval packages from the existing runtime library store.",
        "required_parameters": (), "evidence_kinds": ("runtime_library_skills",),
        "effect_type": "OBSERVE", "target_scope": "local_runtime_library",
        "semantic_owner_id": "developer.runtime",
        "reversibility": "REVERSIBLE", "external_side_effect": False, "risk_class": "READ_ONLY",
    },),
    "jarvis_runtime_library:tools": ({
        "operation_id": "read_runtime_library_tools",
        "description": "Read installed tool and browser packages from the existing runtime library store.",
        "required_parameters": (), "evidence_kinds": ("runtime_library_tools",),
        "effect_type": "OBSERVE", "target_scope": "local_runtime_library",
        "semantic_owner_id": "developer.runtime",
        "reversibility": "REVERSIBLE", "external_side_effect": False, "risk_class": "READ_ONLY",
    },),
    "jarvis_runtime_library:manifests": ({
        "operation_id": "read_runtime_library_manifests",
        "description": "Read package manifests and import-probe truth from the existing runtime library store.",
        "required_parameters": (), "evidence_kinds": ("runtime_library_manifests",),
        "effect_type": "OBSERVE", "target_scope": "local_runtime_library",
        "semantic_owner_id": "developer.runtime",
        "reversibility": "REVERSIBLE", "external_side_effect": False, "risk_class": "READ_ONLY",
    },),
    "runtime_tooling:flutter": ({
        "operation_id": "read_flutter_runtime_status",
        "description": "Read installed Flutter path and cached version truth without running build, deploy, or device commands.",
        "required_parameters": (), "evidence_kinds": ("flutter_runtime_status",),
        "effect_type": "OBSERVE", "target_scope": "local_runtime_tooling",
        "semantic_owner_id": "developer.runtime",
        "reversibility": "REVERSIBLE", "external_side_effect": False, "risk_class": "READ_ONLY",
    },),
}


class ExistingProjectUnderstandingAdapter(ProjectUnderstandingPort):
    """Bounded, local and read-only facade over the existing project tools."""

    provider_id = "existing_project_workspace_tools"

    def __init__(self, *, available: bool = True) -> None:
        self.available = available

    def health(self) -> dict[str, Any]:
        return {
            "provider_id": self.provider_id,
            "status": "AVAILABLE" if self.available and PROJECT_ROOT.exists() else "UNAVAILABLE",
            "filesystem_read_only": True,
            "network_required": False,
            "degradation": "conversation_continues",
        }

    def collect_evidence(
        self,
        understanding: RequestUnderstanding,
        plan: ExecutionPlan,
        trace_id: str,
        deadline: RequestDeadline | None = None,
    ) -> EvidenceBundle:
        if self.health()["status"] != "AVAILABLE":
            return EvidenceBundle(
                request_id=understanding.request_id, capability_id="project.read", trace_id=trace_id,
                status="UNAVAILABLE", items=(), limitations=("project provider is unavailable",),
                receipts=(), errors=("provider_unavailable",),
            )
        git_cache: dict[str, Any] = {}
        runtime_library_cache: dict[str, Any] = {}
        current_step_parameters: dict[str, str] = {}

        def git_evidence() -> dict[str, Any]:
            if not git_cache:
                git_cache.update(repo_git_evidence())
            return dict(git_cache)

        def runtime_library() -> dict[str, Any]:
            if not runtime_library_cache:
                runtime_library_cache.update(build_runtime_library_store_read_model())
            return runtime_library_cache

        operations: dict[str, Callable[[], Any]] = {
            "inspect_git_status": lambda: {"git_status": git_evidence()},
            "inspect_changed_files": lambda: {"changed_files": {
                key: git_evidence().get(key) for key in (
                    "branch", "modified_files", "deleted_files", "untracked_files", "staged_files",
                    "modified_file_count", "deleted_file_count", "untracked_file_count", "staged_file_count",
                    "source_commands", "observed_at",
                )
            }},
            "inspect_diff_summary": lambda: {"diff_summary": {
                key: git_evidence().get(key) for key in (
                    "branch", "diff_name_status", "diff_stat", "cached_diff_stat",
                    "source_commands", "observed_at",
                )
            }},
            "inspect_structure": lambda: {"tree": repo_tree(depth=2, max_entries=120), "files": repo_files(page=1, page_size=40)},
            "search": lambda: repo_search(
                current_step_parameters.get("query", understanding.original_text), max_results=20
            ),
            "read_file_snippet": lambda: {
                "file_snippet": read_file_snippet(current_step_parameters["path"])
            },
            "read_file_outline": lambda: {
                "file_outline": read_file_outline(current_step_parameters["path"])
            },
            "inspect_dependencies": self._inspect_dependencies,
            "inspect_imports": lambda: repo_import_graph(max_edges=60),
            "inspect_tests": self._inspect_tests,
            "inspect_coverage": self._inspect_coverage,
            "inspect_architecture": self._inspect_architecture,
            "query_codegraph": lambda: {
                "codegraph": build_codegraph_readonly_response(
                    current_step_parameters.get("query", understanding.original_text)
                )
            },
            "read_project_workspace_model": lambda: {
                "project_read_model": build_project_workspace_read_model()
            },
            "read_tool_catalog": lambda: {
                "tool_catalog": build_jarvis_live_tool_catalog_read_model()
            },
            "read_memory_federation_status": lambda: {
                "memory_federation": build_jarvis_live_memory_federation_status()
            },
            "read_project_status_tools": lambda: {
                "project_status_tools": status_tools()
            },
            "read_model_runtime_status": lambda: {
                "model_runtime_status": model_runtime_status()
            },
            "read_qdrant_readonly_status": lambda: {
                "qdrant_readonly_status": inspect_qdrant_readonly_availability(
                    PROJECT_ROOT
                ).to_read_model()
            },
            "read_retrieval_backend_status": lambda: {
                "retrieval_backend_status": build_retrieval_backend_status_read_model().to_read_model()
            },
            "read_runtime_library_agents": lambda: {
                "runtime_library_agents": runtime_library().get("agents", ())
            },
            "read_runtime_library_skills": lambda: {
                "runtime_library_skills": runtime_library().get("skills_rag", ())
            },
            "read_runtime_library_tools": lambda: {
                "runtime_library_tools": runtime_library().get("tools_browser", ())
            },
            "read_runtime_library_manifests": lambda: {
                "runtime_library_manifests": {
                    key: runtime_library().get(key)
                    for key in (
                        "store_root", "manifest_dir", "probe_report_dir", "packages",
                        "available_count", "unavailable_count", "probe_reports_read",
                        "probe_reports_loaded", "source_observations", "source_errors",
                        "probe_observation_only", "current_execution_verified", "probe_freshness",
                    )
                }
            },
            "read_flutter_runtime_status": lambda: {
                "flutter_runtime_status": build_flutter_runtime_status_read_model()
            },
        }
        items: list[EvidenceItem] = []
        errors: list[str] = []
        receipts: list[ExecutionReceipt] = []
        for step in plan.steps:
            if deadline is not None and deadline.cancelled:
                errors.append(f"{step.operation}:total_deadline")
                break
            operation = operations[step.operation]
            current_step_parameters = dict(step.parameters)
            executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix=f"project-read-{step.operation}")
            try:
                # The canonical turn deadline is the authority for provider work.
                # A second local eight-second owner made the real architecture
                # report fail despite ample safe read-only turn budget.
                timeout = deadline.remaining() if deadline is not None else None
                payload = executor.submit(operation).result(timeout=timeout)
            except FutureTimeout:
                errors.append(f"{step.operation}:timeout")
                receipts.append(ExecutionReceipt(
                    receipt_id=f"{trace_id}:{step.step_id}:timeout", request_id=understanding.request_id,
                    trace_id=trace_id, step_id=step.step_id, capability_id=step.capability_id,
                    operation_id=step.operation, provider_id=self.provider_id,
                    status="TIMEOUT", result="provider operation timed out",
                ))
                continue
            except Exception as exc:
                errors.append(f"{step.operation}:{type(exc).__name__}")
                continue
            finally:
                executor.shutdown(wait=False, cancel_futures=True)
            failure_payload = None
            if isinstance(payload, dict) and payload.get("allowed") is False:
                failure_payload = payload
            elif isinstance(payload, dict):
                failure_payload = next((
                    value for key, value in payload.items()
                    if key in step.required_evidence
                    and isinstance(value, dict)
                    and value.get("allowed") is False
                ), None)
            if failure_payload is not None:
                failure = str(failure_payload.get("error") or "operation_not_allowed")
                errors.append(f"{step.operation}:{failure}")
                receipts.append(ExecutionReceipt(
                    receipt_id=f"{trace_id}:{step.step_id}:failed",
                    request_id=understanding.request_id,
                    trace_id=trace_id,
                    step_id=step.step_id,
                    capability_id=step.capability_id,
                    operation_id=step.operation,
                    provider_id=self.provider_id,
                    status="FAILED",
                    result=f"project operation returned no usable evidence: {failure}",
                ))
                continue
            evidence_payloads = payload if isinstance(payload, dict) and set(payload).intersection(step.required_evidence) else {step.operation: payload}
            for evidence_kind, evidence_value in evidence_payloads.items():
                bounded, omitted = self._bounded_payload(evidence_value)
                observation = json.dumps(bounded, ensure_ascii=False, default=str, sort_keys=True)
                digest = hashlib.sha256(observation.encode("utf-8")).hexdigest()
                items.append(EvidenceItem(
                    kind=str(evidence_kind), source=f"{self.provider_id}:{step.operation}", observation=observation,
                    scope=str(PROJECT_ROOT), confidence=1.0, trace_id=trace_id, observed_at=utc_observed_at(),
                    content_hash=f"sha256:{digest}", source_reference=f"project://{step.operation}",
                    truncated=omitted > 0, omitted_count=omitted,
                    request_id=understanding.request_id, step_id=step.step_id,
                    capability_id=step.capability_id, operation_id=step.operation,
                    provider_id=self.provider_id,
                ))
            receipts.append(ExecutionReceipt(
                receipt_id=f"{trace_id}:{step.step_id}", request_id=understanding.request_id,
                trace_id=trace_id, step_id=step.step_id, capability_id=step.capability_id,
                operation_id=step.operation, provider_id=self.provider_id,
                status="COMPLETE", result="required project evidence collected",
            ))
        status = "COMPLETE" if items and not errors else "PARTIAL" if items else "UNAVAILABLE"
        return EvidenceBundle(
            request_id=understanding.request_id, capability_id="project.read", trace_id=trace_id,
            status=status, items=tuple(items),
            limitations=(
                () if status == "COMPLETE" else
                ("project evidence incomplete; large collections retain explicit counts and bounded samples",)
            ),
            receipts=tuple(receipts), errors=tuple(errors),
        )

    @classmethod
    def _bounded_payload(cls, value: Any, *, max_items: int = 40, max_text: int = 2000) -> tuple[Any, int]:
        omitted = 0
        if isinstance(value, dict):
            output: dict[str, Any] = {}
            entries = list(value.items())
            omitted += max(0, len(entries) - max_items)
            for key, item in entries[:max_items]:
                output[str(key)], child = cls._bounded_payload(item, max_items=max_items, max_text=max_text)
                omitted += child
            return output, omitted
        if isinstance(value, (list, tuple)):
            omitted += max(0, len(value) - max_items)
            result = []
            for item in value[:max_items]:
                bounded, child = cls._bounded_payload(item, max_items=max_items, max_text=max_text)
                result.append(bounded); omitted += child
            return result, omitted
        if isinstance(value, str) and len(value) > max_text:
            return value[:max_text], omitted + 1
        return value, omitted

    @staticmethod
    def _latest_test_audit() -> Path | None:
        candidates = sorted(Path.home().glob("MAKSIMAR_TEST_TRUTH_*"), key=lambda path: path.stat().st_mtime, reverse=True)
        return candidates[0] if candidates else None

    def _inspect_tests(self) -> dict[str, Any]:
        audit = self._latest_test_audit()
        if audit is None:
            return {"status": "UNAVAILABLE", "reason": "test audit not found"}
        summary = audit / "TEST_TRUTH_SUMMARY.json"
        return json.loads(summary.read_text(encoding="utf-8")) if summary.exists() else {"status": "UNAVAILABLE"}

    def _inspect_coverage(self) -> dict[str, Any]:
        audit = self._latest_test_audit()
        if audit is None or not (audit / "coverage.json").exists():
            return {"status": "UNAVAILABLE", "reason": "coverage audit not found"}
        payload = json.loads((audit / "coverage.json").read_text(encoding="utf-8"))
        return {"totals": payload.get("totals", {}), "source": str(audit / "coverage.json")}

    @staticmethod
    def _inspect_dependencies() -> dict[str, Any]:
        dependency_files = (
            "pyproject.toml", "requirements.txt", "package.json", "pubspec.yaml", "Cargo.toml",
        )
        found: dict[str, str] = {}
        for relative in dependency_files:
            path = PROJECT_ROOT / relative
            if path.exists() and path.is_file():
                found[relative] = path.read_text(encoding="utf-8", errors="replace")[:4000]
        return {"dependency_manifests": found, "read_only": True}

    @staticmethod
    def _inspect_architecture() -> dict[str, Any]:
        report = build_architecture_report(project_root=PROJECT_ROOT)
        return {
            "blueprint_id": report.blueprint_id,
            "failed": report.failed,
            "violations": tuple(item.render() for item in report.violations[:80]),
        }

    @staticmethod
    def _model_understood_project_path(understanding: RequestUnderstanding) -> str:
        """Use the model-owned semantic target; never classify request text here."""
        target = str(understanding.target_scope or "").strip()
        for prefix in ("project://", "file://"):
            if target.startswith(prefix):
                target = target[len(prefix):]
        return target


__all__ = [
    "ExistingProjectUnderstandingAdapter",
    "PROJECT_READONLY_INVENTORY_CONTRACTS",
]
