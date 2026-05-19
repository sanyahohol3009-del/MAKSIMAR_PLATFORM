from __future__ import annotations

import argparse
import ast
import fnmatch
import json
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BLUEPRINT_PATH = PROJECT_ROOT / "MAKSIMAR_CORE_LIB" / "architecture_map" / "architecture_blueprint.json"


IGNORED_DIR_NAMES = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".pymon",
    "node_modules",
    "dist",
    "build",
}


IGNORED_PATH_GLOBS = (
    ".git/**",
    ".venv/**",
    "venv/**",
    "__pycache__/**",
    ".pytest_cache/**",
    ".mypy_cache/**",
    ".ruff_cache/**",
    ".pymon/**",
    "node_modules/**",
    "dist/**",
    "build/**",
    "*.egg-info/**",
    "EXTERNAL_BACKENDS/**/.git/**",
    "EXTERNAL_BACKENDS/**/.venv/**",
    "EXTERNAL_BACKENDS/**/venv/**",
    "EXTERNAL_BACKENDS/**/sandbox_data/**",
    "EXTERNAL_BACKENDS/**/__pycache__/**",
)


@dataclass(frozen=True)
class LawSpec:
    law_id: str
    title: str
    tokens: tuple[str, ...]


@dataclass(frozen=True)
class LayerSpec:
    layer_id: str
    title: str
    phase: str
    path_candidates: tuple[str, ...]
    expected_laws: tuple[LawSpec, ...]
    deep_scan_default: bool = True


@dataclass
class FileAstMetrics:
    file_path: str
    classes: int = 0
    functions: int = 0
    methods: int = 0
    imports: int = 0
    contract_imports: int = 0
    parse_errors: int = 0
    symbol_names: list[str] = field(default_factory=list)
    imported_modules: list[str] = field(default_factory=list)
    text_tokens: str = ""


@dataclass
class LayerReport:
    spec: LayerSpec
    status: str
    existing_paths: list[str] = field(default_factory=list)
    missing_paths: list[str] = field(default_factory=list)
    files: int = 0
    parsed_files: int = 0
    classes: int = 0
    functions: int = 0
    methods: int = 0
    imports: int = 0
    contract_imports: int = 0
    parse_errors: int = 0
    present_laws: list[LawSpec] = field(default_factory=list)
    missing_laws: list[LawSpec] = field(default_factory=list)
    readiness_percent: float = 0.0
    code_weight_percent: float = 0.0
    law_percent: float = 0.0
    deep_scan_skipped: bool = False


def law(law_id: str, title: str, *tokens: str) -> LawSpec:
    return LawSpec(
        law_id=law_id,
        title=title,
        tokens=tuple(token.lower() for token in tokens if token.strip()),
    )


VFINAL_LAYERS: tuple[LayerSpec, ...] = (
    LayerSpec(
        layer_id="01_GLOBAL_CORE_ROOT",
        title="Global / Immutable Core Safety Root",
        phase="FOUNDATION",
        path_candidates=(
            "GLOBAL_CORE_ROOT",
            "CORE_ROOT",
        ),
        expected_laws=(
            law("stop_gate", "STOP-GATE emergency halt", "stop_gate", "StopGate"),
            law("core_guard", "Core guard integrity chain", "core_guard", "CoreGuard"),
            law("watchdog", "Kernel/watchdog safety monitor", "watchdog", "kernel_watchdog"),
            law("heartbeat", "Heartbeat freshness truth", "heartbeat", "heartbeat_io"),
            law("immutable_core", "Immutable core boundary", "immutable", "CORE_ROOT"),
            law("no_upward_write", "No upward write into core", "no direct core write", "canonical_write_allowed"),
        ),
    ),
    LayerSpec(
        layer_id="02_NODE_CORE_ROOT",
        title="Node Core / Existing MAKSIMAR_CORE Root",
        phase="FOUNDATION",
        path_candidates=(
            "NODE_CORE_ROOT",
            "MAKSIMAR_CORE",
        ),
        expected_laws=(
            law("shared_services", "Shared services exist", "shared_services"),
            law("contracts_root", "Core contracts root exists", "contracts"),
            law("path_resolver", "Canonical path resolver", "path_resolver"),
            law("atomic_io", "Atomic IO utilities", "atomic_io"),
            law("capability_resolver", "Capability resolver", "capability_resolver"),
            law("policy_loader", "Policy loader", "policy_loader"),
        ),
    ),
    LayerSpec(
        layer_id="03_CORE_LIB_CONTRACTS",
        title="MAKSIMAR_CORE_LIB canonical contracts / validators / builders",
        phase="FOUNDATION",
        path_candidates=(
            "MAKSIMAR_CORE_LIB",
        ),
        expected_laws=(
            law("contracts", "Canonical contracts", "contract", "contracts"),
            law("validators", "Validators / validation policy", "validator", "validation"),
            law("builders", "Builders / preview builders", "builder", "preview_builder"),
            law("id_generation", "Canonical ID generation", "id_generation", "canonical_id"),
            law("module_manifest", "Module manifest schema", "module_manifest", "manifest"),
            law("policy_models", "Policy models", "policy"),
            law("approval_models", "Approval models", "approval"),
            law("audit_models", "Audit models", "audit"),
            law("rollback_models", "Rollback models", "rollback"),
            law("root_artifact_hygiene", "Root artifact hygiene", "root_artifact_hygiene", "RootArtifact"),
            law("semantic_duplicate_scan", "Semantic duplicate scan", "semantic_duplicate", "SemanticDuplicate"),
            law("root_artifact_report", "Root artifact report builder", "root_artifact_report", "RootArtifactReport"),
        ),
    ),
    LayerSpec(
        layer_id="04_BOOTSTRAP_ENTRYPOINTS",
        title="Boot, bootstrap and local entrypoints",
        phase="FOUNDATION",
        path_candidates=(
            "BOOT",
            "run_context.py",
            "refactor.py",
        ),
        expected_laws=(
            law("system_bootstrap", "System bootstrap", "system_bootstrap", "bootstrap"),
            law("run_context", "Run context", "run_context"),
            law("maintenance_entrypoint", "Maintenance/refactor entrypoint", "refactor"),
        ),
    ),
    LayerSpec(
        layer_id="05_SECURITY_LAYER",
        title="Security: RBAC, policy, approval, vault, signatures, quarantine",
        phase="FOUNDATION/HARDENED",
        path_candidates=(
            "SECURITY_LAYER",
            "SECURITY",
            "MAKSIMAR_SERVER/SECURITY",
            "MAKSIMAR_SERVER/AUTH",
            "MAKSIMAR_SERVER/APPROVAL",
            "MAKSIMAR_SERVER/VAULT",
            "MAKSIMAR_CORE/contracts/security",
            "MAKSIMAR_CORE_LIB/security_layer",
            "MAKSIMAR_SERVER/SECURITY_LAYER",
        ),
        expected_laws=(
            law("security_layer_surface", "Security layer surface", "SECURITY_LAYER", "security_layer_surface", "layer_manifest"),
            law("rbac", "RBAC service", "rbac", "role", "permission"),
            law("policy_enforcer", "Policy enforcer", "policy_enforcer", "policy engine"),
            law("execution_bundle_verifier", "Execution bundle verifier", "execution_bundle_verifier", "bundle_verifier"),
            law("approval_service", "Approval service / gate", "approval", "approval_service"),
            law("voice_identity", "Voice identity high-risk check", "voice_identity", "biometric"),
            law("vault", "Vault / secrets", "vault", "secret"),
            law("signature_verifier", "Signature verification", "signature_verifier", "signature"),
            law("usb_guard", "USB guard", "usb_guard", "usb"),
            law("media_quarantine", "Media quarantine", "media_quarantine", "quarantine"),
        ),
    ),
    LayerSpec(
        layer_id="06_GOVERNANCE_LAYER",
        title="Governance: risk, ethics, anti-scam, consent, retention, legal adaptability",
        phase="FOUNDATION/HARDENED",
        path_candidates=(
            "GOVERNANCE_LAYER",
            "GOVERNANCE",
            "MAKSIMAR_SERVER/GOVERNANCE",
            "MAKSIMAR_CORE/governance",
            "MAKSIMAR_CORE_LIB/memory_policy",
            "MAKSIMAR_SERVER/REGULATORY_MEMORY_FOUNDATION",
        ),
        expected_laws=(
            law("risk_engine", "Risk classification engine", "risk_engine", "risk classification", "RiskLevel"),
            law("ethical_guard", "Ethical guard", "ethical_guard", "ethic"),
            law("anti_scam", "Anti-scam service", "anti_scam", "scam"),
            law("consent_registry", "Consent registry", "consent"),
            law("retention_policy", "Retention policy", "retention"),
            law("legal_adaptability", "Legal adaptability layer", "legal_adaptability", "jurisdiction"),
            law("regulatory_source_version", "Regulatory source versioning", "source_version", "effective_date"),
            law("no_auto_truth_update", "No automatic canonical truth update", "canonical_truth_update_allowed", "auto_apply_allowed"),
        ),
    ),
    LayerSpec(
        layer_id="07_CONTROL_PLANE",
        title="Control Plane: API gateway, routing, validation, intent and orchestration",
        phase="FOUNDATION/HARDENED",
        path_candidates=(
            "CONTROL_PLANE",
            "MAKSIMAR_SERVER/CONTROL_PLANE",
            "MAKSIMAR_SERVER/API_GATEWAY",
            "MAKSIMAR_SERVER/INTENT_NORMALIZATION",
        ),
        expected_laws=(
            law("api_gateway", "API gateway", "api_gateway", "gateway"),
            law("contract_validator", "Contract validator", "contract_validator", "validation_gate"),
            law("flow_router", "Flow/router layer", "flow_router", "router", "routing"),
            law("execution_engine", "Execution engine orchestration", "execution_engine", "orchestration"),
            law("runtime_controller", "Runtime controller", "runtime_controller"),
            law("intent_normalization", "Intent normalization", "intent_normalization", "intent"),
            law("policy_handoff", "Policy-aware handoff", "policy", "approval"),
        ),
    ),
    LayerSpec(
        layer_id="08_EXECUTION_RUNTIME",
        title="Execution Runtime: supervisor, runtime state, pressure, admission, workers boundary",
        phase="FOUNDATION/HARDENED",
        path_candidates=(
            "SUPERVISOR",
            "RUNTIME",
            "MAKSIMAR_SERVER/EXECUTION_CONTROL",
            "MAKSIMAR_SERVER/RUNTIME",
            "MAKSIMAR_SERVER/SUPERVISOR",
        ),
        expected_laws=(
            law("process_supervisor", "Process supervisor", "process_supervisor", "supervisor"),
            law("runtime_state", "Runtime state", "RUNTIME/state", "runtime_state"),
            law("execution_pressure", "Execution pressure policy", "pressure", "backpressure"),
            law("degraded_mode", "Degraded mode", "degraded"),
            law("admission_control", "Admission control", "admission"),
            law("node_runtime", "Node runtime health", "node_runtime", "health"),
            law("no_ui_execution", "No UI direct execution", "operator", "policy"),
        ),
    ),
    LayerSpec(
        layer_id="09_DATA_PLANE",
        title="Data Plane: append-only log, ledger, DB, vector store, object storage",
        phase="FOUNDATION/HARDENED",
        path_candidates=(
            "DATA_PLANE",
            "MAKSIMAR_SERVER/DATA_PLANE",
            "MAKSIMAR_CORE_LIB/data_plane",
            "storage",
            "STORAGE",
            "MAKSIMAR_SERVER/STORAGE",
            "RUNTIME/state",
        ),
        expected_laws=(
            law("data_plane_surface", "Data plane surface", "DATA_PLANE", "data_plane_surface", "layer_manifest"),
            law("append_only_log", "Append-only log", "append_only", "event_journal", "jsonl"),
            law("immutable_ledger", "Immutable ledger", "immutable_ledger", "ledger"),
            law("postgres_main", "Postgres main", "postgres", "postgres_main"),
            law("vector_store", "Vector store", "vector_store", "qdrant", "sqlite_vec"),
            law("object_storage", "Object storage", "object_storage", "artifact"),
            law("memory_index", "Memory index", "memory_index"),
            law("no_direct_canonical_write", "No direct canonical write", "NoDirectCanonicalWriteContract", "DATA_PLANE_NO_DIRECT_CANONICAL_WRITE_CONTRACT", "no_direct_canonical_write_contract", "data_plane_never_writes_directly_to_canonical_store"),
        ),
    ),
    LayerSpec(
        layer_id="10_MEMORY_KNOWLEDGE_HUB",
        title="Memory + Knowledge Hub: retrieval, evidence, regulatory memory, source chain",
        phase="FOUNDATION CLOSED / NEXT HARDENING",
        path_candidates=(
            "MEMORY",
            "KNOWLEDGE_HUB",
            "MAKSIMAR_CORE_LIB/memory_engine",
            "MAKSIMAR_CORE_LIB/memory_domains",
            "MAKSIMAR_SERVER/MEMORY",
            "MAKSIMAR_SERVER/MEMORY_REGISTRY",
            "MAKSIMAR_SERVER/REGULATORY_MEMORY_FOUNDATION",
        ),
        expected_laws=(
            law("memory_routing", "Memory routing", "memory_routing", "retrieval"),
            law("evidence_pack", "Evidence pack", "evidence", "source_chain"),
            law("regulatory_memory", "Regulatory memory", "regulatory", "jurisdiction"),
            law("tenant_isolation", "Tenant isolation", "tenant", "same_tenant_only"),
            law("drift_detection", "Memory drift detection", "drift", "contradiction"),
            law("self_readability", "Self-readability", "self_readability", "explain"),
            law("backend_adapter", "Memory backend adapter", "backend_adapter", "adapter"),
        ),
    ),
    LayerSpec(
        layer_id="11_AI_SERVICES_ORCHESTRATION",
        title="AI services: model router, local LLM, embeddings, provenance, feedback",
        phase="FIRST WORKING PLATFORM",
        path_candidates=(
            "AI_SERVICES",
            "WORKERS",
            "MAKSIMAR_SERVER/AI_SERVICES",
            "MAKSIMAR_SERVER/WORKERS",
            "MAKSIMAR_SERVER/POLYGLOT_MODEL_WORKER_BRIDGE",
            "MAKSIMAR_CORE_LIB/real_ai_services_model_adapters",
        ),
        expected_laws=(
            law("model_router", "Model router", "model_router", "router"),
            law("local_llm_runtime", "Local LLM runtime", "local_llm", "llm_runtime"),
            law("coder_model", "Coder model service", "coder_model", "code"),
            law("reasoning_model", "Reasoning model service", "reasoning_model", "reasoning"),
            law("vision_model", "Vision model service", "vision_model", "vision"),
            law("embedding_service", "Embedding service", "embedding"),
            law("feedback_engine", "Feedback engine", "feedback"),
            law("model_provenance", "Model provenance", "provenance"),
            law("finops", "FinOps / GPU / token budget", "finops", "budget", "gpu"),
        ),
    ),
    LayerSpec(
        layer_id="12_SANDBOX_EVOLUTION_ENGINE",
        title="Sandbox + Evolution: proposal, simulation, codegen, owner review, self-expansion gate",
        phase="ADVANCED LOCAL PLATFORM",
        path_candidates=(
            "SANDBOX",
            "EVOLUTION_ENGINE",
            "MAKSIMAR_SERVER/SANDBOX",
            "MAKSIMAR_SERVER/SANDBOX_REVIEW",
            "MAKSIMAR_SERVER/SELF_EXPANSION_GATE",
            "MAKSIMAR_SERVER/PROPOSAL_AUDIT",
            "MAKSIMAR_SERVER/CODEGEN_CONTEXT",
            "MAKSIMAR_CORE_LIB/code_generation",
            "MAKSIMAR_CORE_LIB/sandboxing",
            "MAKSIMAR_CORE_LIB/simulation_review",
        ),
        expected_laws=(
            law("proposal_flow", "Proposal flow", "proposal", "audit"),
            law("sandbox_first", "Sandbox-first execution", "sandbox"),
            law("diff_review", "Diff/review before apply", "diff", "review"),
            law("owner_review", "Owner review", "owner_review", "approval"),
            law("self_expansion_gate", "Self-expansion gate", "self_expansion"),
            law("no_auto_deploy", "No auto deploy", "auto_deploy", "deployment_allowed_now"),
            law("rollback_reference", "Rollback reference", "rollback"),
            law("synthetic_benchmarks", "Synthetic benchmarks", "benchmark", "synthetic"),
        ),
    ),
    LayerSpec(
        layer_id="13_OBSERVABILITY_DASHBOARD",
        title="Observability + dashboards: metrics, logs, tracing, panels, read-only views",
        phase="FOUNDATION/HARDENED",
        path_candidates=(
            "OBSERVABILITY",
            "DASHBOARD",
            "DASHBOARDS",
            "MAKSIMAR_SERVER/OBSERVABILITY",
            "MAKSIMAR_SERVER/DASHBOARD",
            "MAKSIMAR_SERVER/DASHBOARDS",
            "MAKSIMAR_SERVER/DASHBOARD_READ_ONLY_VIEWS",
            "MAKSIMAR_SERVER/OPERATOR_UI",
            "MAKSIMAR_SERVER/VISUAL_OPERATOR",
        ),
        expected_laws=(
            law("metrics_collector", "Metrics collector", "metrics", "metrics_collector"),
            law("log_aggregator", "Log aggregator", "log_aggregator", "logs"),
            law("tracing", "Tracing service", "trace", "correlation"),
            law("dashboard_service", "Dashboard service", "dashboard"),
            law("alert_manager", "Alert manager", "alert"),
            law("incident_model", "Incident model", "incident"),
            law("read_only_views", "Read-only views", "read_only", "DASHBOARD_READ_ONLY_VIEWS"),
            law("panel_registry", "Panel registry", "panel_registry", "panel"),
            law("display_resolver", "Display resolver", "display", "resolver"),
        ),
    ),
    LayerSpec(
        layer_id="14_UPDATE_RECOVERY_INFRA",
        title="Update / Recovery / Infrastructure: snapshots, rollback, signed updates, queues, namespace",
        phase="HARDENED FOUNDATION",
        path_candidates=(
            "UPDATE_RECOVERY",
            "UPDATE_CHANNEL",
            "RECOVERY",
            "INFRA",
            "INFRASTRUCTURE",
            "MAKSIMAR_SERVER/UPDATE_RECOVERY",
            "MAKSIMAR_CORE_LIB/update_recovery",
            "MAKSIMAR_SERVER/UPDATE_CHANNEL",
            "MAKSIMAR_SERVER/RECOVERY",
            "MAKSIMAR_SERVER/ROADMAP_CLOSURE",
        ),
        expected_laws=(
            law("signed_update", "Signed update service", "signed_update", "update_service"),
            law("signature_verifier", "Signature verifier", "signature_verifier", "signature"),
            law("snapshot_manager", "Snapshot manager", "snapshot"),
            law("rollback_manager", "Rollback manager", "rollback"),
            law("recovery_service", "Recovery service", "recovery"),
            law("offline_import_gate", "Offline import gate", "offline_import", "air_gapped"),
            law("redis_bus", "Redis bus", "redis"),
            law("message_queue", "Message queue", "queue"),
            law("namespace_manager", "Namespace manager", "namespace"),
        ),
    ),
    LayerSpec(
        layer_id="15_HARDWARE_EDGE_LAYER",
        title="Hardware / Edge: industrial bus, telemetry, power, TPM, secure boot, HSM",
        phase="FULL SYSTEM / COMPANY SCALE",
        path_candidates=(
            "HARDWARE_LAYER",
            "HARDWARE",
            "EDGE",
            "MAKSIMAR_SERVER/HARDWARE",
            "MAKSIMAR_SERVER/EDGE",
            "MAKSIMAR_SERVER/HARDWARE_EDGE",
        ),
        expected_laws=(
            law("industrial_bus", "Industrial bus", "industrial_bus", "opc", "plc"),
            law("power_stability", "Power stability monitor", "power_stability", "power"),
            law("telemetry_probes", "Telemetry probes", "telemetry", "gpu", "temperature"),
            law("tpm_binding", "TPM binding", "tpm"),
            law("secure_boot", "Secure boot", "secure_boot"),
            law("hsm_module", "HSM module", "hsm"),
            law("gesture_device", "External gesture/sensor node", "gesture", "sensor"),
        ),
    ),
    LayerSpec(
        layer_id="PRODUCT_RUNTIME",
        title="Product Runtime: loader, registry, isolation, quota, versions",
        phase="HARDENED FOUNDATION / FIRST WORKING PLATFORM",
        path_candidates=(
            "PRODUCT_RUNTIME",
            "MAKSIMAR_SERVER/PRODUCT_RUNTIME",
            "MAKSIMAR_SERVER/PRODUCT_REGISTRY",
            "MAKSIMAR_SERVER/REGISTRY_AUTO_ENROLLMENT",
            "MAKSIMAR_CORE_LIB/product_governance",
            "MAKSIMAR_CORE_LIB/product_hardening_onboarding_packaging",
        ),
        expected_laws=(
            law("product_loader", "Product loader", "product_loader", "loader"),
            law("product_registry", "Product registry", "product_registry", "registry"),
            law("isolation_manager", "Isolation manager", "isolation"),
            law("quota_manager", "Quota manager", "quota"),
            law("version_controller", "Version controller", "version"),
            law("module_manifest", "Module manifest", "module_manifest", "manifest"),
            law("permission_matrix", "Permission matrix", "permission", "capability"),
        ),
    ),
    LayerSpec(
        layer_id="PRODUCTS_CUBES",
        title="Product Cubes: blogger/content, ERP, CAD, robotics, gravure, industrial suite",
        phase="FIRST WORKING PLATFORM / PRODUCT SCALE",
        path_candidates=(
            "PRODUCTS",
            "PRODUCT_CUBES",
            "CUBES",
            "MODULES",
            "BLOGGER_CONTENT_CUBE",
            "MAKSIMAR_SERVER/PRODUCTS",
            "MAKSIMAR_SERVER/CUBES",
            "MAKSIMAR_SERVER/MODULES",
            "MAKSIMAR_SERVER/PRODUCTIZATION",
        ),
        expected_laws=(
            law("stone_erp", "Stone ERP service", "stone_erp", "erp"),
            law("content_saas", "Content SaaS / Blogger cube", "content_saas", "blogger", "content"),
            law("cad_platform", "CAD platform", "cad_platform", "cad"),
            law("robotics_service", "Robotics service", "robotics_service", "robotics"),
            law("gravure_service", "Gravure / engraving service", "gravure", "engraving"),
            law("industrial_suite", "Industrial suite", "industrial_suite"),
            law("anti_scam_binding", "Anti-scam content binding", "anti_scam", "content_safety"),
        ),
    ),
    LayerSpec(
        layer_id="CLIENTS_MOBILE",
        title="Clients / Mobile bridge: Android, iOS, task envelope, notifications",
        phase="ADVANCED LOCAL PLATFORM",
        path_candidates=(
            "CLIENTS",
            "clients",
            "MOBILE",
            "mobile",
            "ANDROID_CLIENT",
            "IOS_CLIENT",
            "JARVIS_MOBILE",
            "MOBILE_BRIDGE",
            "MAKSIMAR_SERVER/MOBILE_BRIDGE",
            "MAKSIMAR_CORE_LIB/real_dashboard_clients_mobile",
        ),
        expected_laws=(
            law("mobile_request", "MobileRequest", "MobileRequest", "mobile_request"),
            law("task_envelope", "TaskEnvelope", "TaskEnvelope", "task_envelope"),
            law("task_result", "TaskResult", "TaskResult", "task_result"),
            law("notifications", "Notifications", "notification"),
            law("dashboard_proxy", "Dashboard proxy", "dashboard_proxy", "mobile dashboard"),
            law("no_heavy_mobile", "No heavy execution on mobile", "heavy_execution_allowed", "mobile"),
            law("no_core_write", "No core write from mobile", "core write", "mobile"),
        ),
    ),
    LayerSpec(
        layer_id="SIMULATION_ROBOTICS_CAD",
        title="Simulation / Physics / Robotics / CAD / CAM / Digital Twin",
        phase="FULL SYSTEM / COMPANY SCALE",
        path_candidates=(
            "SIMULATION_LAYER",
            "PHYSICS_RUNTIME",
            "DIGITAL_TWIN",
            "ROBOTICS_MODULE",
            "CAD_3D_CAM_LAYER",
            "ENGRAVING_BLOCK",
            "MAKSIMAR_SERVER/SIMULATION_LAYER",
            "MAKSIMAR_SERVER/PHYSICS_RUNTIME",
            "MAKSIMAR_SERVER/DIGITAL_TWIN",
            "MAKSIMAR_SERVER/ROBOTICS",
            "MAKSIMAR_SERVER/CAD_3D_CAM",
            "MAKSIMAR_SERVER/ENGRAVING_BLOCK",
        ),
        expected_laws=(
            law("simulation_engine", "Simulation engine", "simulation", "engine"),
            law("physics_runtime", "Physics runtime", "physics"),
            law("surface_intelligence", "Surface intelligence", "surface", "height_map"),
            law("material_registry", "Material registry", "material_registry", "material"),
            law("sensor_simulation", "Sensor simulation", "sensor_simulation", "noise_model"),
            law("validation_gate", "Physics validation gate", "validation", "feasibility"),
            law("robotics_queue", "Robotics safe command queue", "command_queue", "robotics"),
            law("estop", "E-Stop / safety stop", "e_stop", "estop"),
            law("cad_backend", "CAD backend", "freecad", "openscad", "step", "stl"),
        ),
    ),
    LayerSpec(
        layer_id="NETWORK_CONTAINERIZATION",
        title="Network segmentation + container deployment spec",
        phase="HARDENED FOUNDATION / DEPLOYMENT",
        path_candidates=(
            "NETWORK",
            "NETWORK_SEGMENTATION",
            "CONTAINER_DEPLOYMENT",
            "DEPLOYMENT",
            "docker",
            "compose",
            "infra",
            "infrastructure",
            "docker-compose.yml",
            "compose.yaml",
            "compose.yml",
        ),
        expected_laws=(
            law("net_core_safety", "net_core_safety", "net_core_safety"),
            law("net_control", "net_control", "net_control"),
            law("net_security", "net_security", "net_security"),
            law("net_governance", "net_governance", "net_governance"),
            law("net_data", "net_data", "net_data"),
            law("net_ai", "net_ai", "net_ai"),
            law("net_products", "net_products", "net_products"),
            law("net_observability", "net_observability", "net_observability"),
            law("net_update", "net_update", "net_update"),
            law("healthcheck", "Healthcheck declared", "healthcheck", "/health"),
            law("restart_policy", "Restart policy declared", "restart", "unless-stopped", "on-failure"),
            law("no_public_exposure", "No public exposure by default", "localhost", "expose outside"),
        ),
    ),
    LayerSpec(
        layer_id="EXTERNAL_BACKENDS_VENDOR_GATE",
        title="External backends + vendor security gate",
        phase="ADVANCED LOCAL PLATFORM",
        path_candidates=(
            "EXTERNAL_BACKENDS",
            "tools/vendor_security_gate.py",
        ),
        expected_laws=(
            law("vendor_security_gate", "Vendor security gate", "vendor_security_gate"),
            law("official_remote", "Official remote verification", "official_remote", "commit_seen"),
            law("pip_audit", "pip-audit", "pip-audit", "pip_audit"),
            law("bandit", "Bandit SAST", "bandit"),
            law("clamscan", "ClamAV scan", "clamscan"),
            law("sandbox_only", "Sandbox-only external backend", "sandbox-only", "sandbox_only"),
            law("no_core_access", "No core access", "canonical_memory_access", "runtime_mutation_allowed"),
        ),
        deep_scan_default=True,
    ),
    LayerSpec(
        layer_id="TOOLS_TESTS_DOCS",
        title="Tools, tests, docs and acceptance records",
        phase="ALL",
        path_candidates=(
            "tools",
            "tests",
            "docs",
        ),
        expected_laws=(
            law("pytest", "Pytest tests", "pytest", "test_"),
            law("architecture_radar", "Architecture radar", "architecture_radar"),
            law("drift_guard", "Drift guard", "drift_guard", "semantic drift"),
            law("roadmap_index", "Roadmap index", "roadmap_index"),
            law("acceptance_docs", "Acceptance docs", "acceptance", "closure"),
            law("foundation_roadmap_machine_check", "Foundation roadmap machine check", "foundation_roadmap_ci_check", "batched_foundation_roadmap"),
            law("smoke_tests", "Smoke tests", "smoke"),
        ),
    ),
)


def main() -> int:
    args = parse_args()

    project_root = Path(args.root).resolve()
    blueprint_path = Path(args.blueprint).resolve() if args.blueprint else DEFAULT_BLUEPRINT_PATH

    layer_specs = build_layer_specs(
        project_root=project_root,
        blueprint_path=blueprint_path,
        use_blueprint=not args.no_blueprint,
    )

    reports = build_reports(
        project_root=project_root,
        layer_specs=layer_specs,
        include_external=not args.skip_external,
        max_files_per_layer=args.max_files_per_layer,
    )

    print_dashboard(
        reports=reports,
        project_root=project_root,
        blueprint_path=blueprint_path,
        details=args.details,
        show_missing_laws=args.show_missing_laws,
    )

    if args.json:
        write_json_report(
            reports=reports,
            output_path=Path(args.json),
            project_root=project_root,
            blueprint_path=blueprint_path,
        )

    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "MAKSIMAR Super Radar / Project X-Ray. "
            "Read-only architecture analytics; never fails CI by design."
        )
    )
    parser.add_argument(
        "--root",
        default=str(PROJECT_ROOT),
        help="Project root. Default: auto-detected repository root.",
    )
    parser.add_argument(
        "--blueprint",
        default=str(DEFAULT_BLUEPRINT_PATH),
        help="Optional architecture_blueprint.json path.",
    )
    parser.add_argument(
        "--no-blueprint",
        action="store_true",
        help="Use embedded vFINAL skeleton only.",
    )
    parser.add_argument(
        "--details",
        action="store_true",
        help="Show detailed laws/functions per layer.",
    )
    parser.add_argument(
        "--show-missing-laws",
        action="store_true",
        help="Show missing expected laws even without --details.",
    )
    parser.add_argument(
        "--skip-external",
        action="store_true",
        help="Skip deep AST scan for EXTERNAL_BACKENDS layer.",
    )
    parser.add_argument(
        "--max-files-per-layer",
        type=int,
        default=0,
        help="Optional safety limit. 0 = no limit.",
    )
    parser.add_argument(
        "--json",
        default="",
        help="Write machine-readable JSON report to this path.",
    )
    return parser.parse_args()


def build_layer_specs(
    project_root: Path,
    blueprint_path: Path,
    use_blueprint: bool,
) -> list[LayerSpec]:
    specs = list(VFINAL_LAYERS)

    if not use_blueprint:
        return specs

    blueprint = safe_load_blueprint(blueprint_path)
    if not blueprint:
        return specs

    known_ids = {spec.layer_id for spec in specs}

    for layer in blueprint.get("layers", []):
        layer_id = str(layer.get("id", "")).strip()
        if not layer_id:
            continue

        if layer_id in known_ids:
            continue

        path_prefixes = tuple(str(item) for item in layer.get("path_prefixes", []) if str(item).strip())
        if not path_prefixes:
            continue

        imported_law_tokens = []
        for key in ("allowed_import_layer_ids", "forbidden_import_layer_ids", "module_prefixes"):
            for value in layer.get(key, []):
                imported_law_tokens.append(str(value))

        specs.append(
            LayerSpec(
                layer_id=f"BP::{layer_id}",
                title=str(layer.get("title", layer_id)),
                phase=str(layer.get("status", "BLUEPRINT")),
                path_candidates=path_prefixes,
                expected_laws=(
                    law("blueprint_import_policy", "Blueprint import policy exists", *imported_law_tokens),
                ),
                deep_scan_default=bool(layer.get("import_guard", True)),
            )
        )

    return specs


def safe_load_blueprint(blueprint_path: Path) -> dict[str, Any] | None:
    try:
        if not blueprint_path.exists():
            return None

        with blueprint_path.open("r", encoding="utf-8") as handle:
            loaded = json.load(handle)

        if not isinstance(loaded, dict):
            return None

        return loaded
    except Exception:
        return None


def build_reports(
    project_root: Path,
    layer_specs: list[LayerSpec],
    include_external: bool,
    max_files_per_layer: int,
) -> list[LayerReport]:
    reports: list[LayerReport] = []

    for spec in layer_specs:
        report = scan_layer(
            project_root=project_root,
            spec=spec,
            include_external=include_external,
            max_files_per_layer=max_files_per_layer,
        )
        reports.append(report)

    return reports


def scan_layer(
    project_root: Path,
    spec: LayerSpec,
    include_external: bool,
    max_files_per_layer: int,
) -> LayerReport:
    existing_paths: list[str] = []
    missing_paths: list[str] = []
    py_files: list[Path] = []

    for raw_candidate in spec.path_candidates:
        path = project_root / raw_candidate

        if path.exists():
            existing_paths.append(raw_candidate)
            py_files.extend(collect_python_files(path, project_root))
        else:
            missing_paths.append(raw_candidate)

    py_files = unique_paths(py_files)

    if max_files_per_layer > 0:
        py_files = py_files[:max_files_per_layer]

    if not existing_paths:
        status = "MISSING/ПЛАН"
    elif not py_files:
        status = "EMPTY DIR/ПУСТОЙ ГАРАЖ"
    else:
        non_init_files = [path for path in py_files if path.name != "__init__.py"]
        status = "READY/КОД ЕСТЬ" if non_init_files else "SKELETON/КАРКАС"

    report = LayerReport(
        spec=spec,
        status=status,
        existing_paths=existing_paths,
        missing_paths=missing_paths,
        files=len(py_files),
    )

    if should_skip_deep_scan(spec, include_external):
        report.deep_scan_skipped = True
        compute_laws_and_readiness(report, corpus="")
        return report

    corpus_parts: list[str] = []

    for py_file in py_files:
        metrics = scan_python_file(py_file, project_root)
        report.parsed_files += 1 if metrics.parse_errors == 0 else 0
        report.classes += metrics.classes
        report.functions += metrics.functions
        report.methods += metrics.methods
        report.imports += metrics.imports
        report.contract_imports += metrics.contract_imports
        report.parse_errors += metrics.parse_errors

        corpus_parts.append(metrics.file_path.lower())
        corpus_parts.extend(name.lower() for name in metrics.symbol_names)
        corpus_parts.extend(module.lower() for module in metrics.imported_modules)
        corpus_parts.append(metrics.text_tokens)

    compute_laws_and_readiness(report, corpus="\n".join(corpus_parts))
    return report


def collect_python_files(path: Path, project_root: Path) -> list[Path]:
    if path.is_file():
        if path.suffix == ".py" and not should_ignore_path(path, project_root):
            return [path]
        return []

    result: list[Path] = []

    for dirpath, dirnames, filenames in os.walk(path):
        current = Path(dirpath)

        dirnames[:] = [
            name
            for name in dirnames
            if name not in IGNORED_DIR_NAMES and not should_ignore_path(current / name, project_root)
        ]

        for filename in filenames:
            if not filename.endswith(".py"):
                continue

            file_path = current / filename
            if should_ignore_path(file_path, project_root):
                continue

            result.append(file_path)

    return result


def scan_python_file(path: Path, project_root: Path) -> FileAstMetrics:
    rel_path = relative_posix(path, project_root)

    metrics = FileAstMetrics(file_path=rel_path)

    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        metrics.parse_errors += 1
        return metrics

    metrics.text_tokens = make_light_text_corpus(text)

    try:
        tree = ast.parse(text, filename=rel_path)
    except SyntaxError:
        metrics.parse_errors += 1
        return metrics
    except Exception:
        metrics.parse_errors += 1
        return metrics

    class_stack: list[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            metrics.classes += 1
            metrics.symbol_names.append(node.name)

        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            metrics.functions += 1
            metrics.symbol_names.append(node.name)

        elif isinstance(node, ast.Import):
            metrics.imports += len(node.names)
            for alias in node.names:
                metrics.imported_modules.append(alias.name)
                if is_contract_import(alias.name):
                    metrics.contract_imports += 1

        elif isinstance(node, ast.ImportFrom):
            metrics.imports += len(node.names)
            if node.module:
                metrics.imported_modules.append(node.module)
                if is_contract_import(node.module):
                    metrics.contract_imports += 1

    for class_node in [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]:
        for child in class_node.body:
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                metrics.methods += 1

    return metrics


def make_light_text_corpus(text: str) -> str:
    lowered = text.lower()
    interesting_lines: list[str] = []

    markers = (
        "stop_gate",
        "core_guard",
        "watchdog",
        "heartbeat",
        "policy",
        "approval",
        "risk",
        "ethic",
        "scam",
        "consent",
        "retention",
        "jurisdiction",
        "tenant",
        "evidence",
        "snapshot",
        "rollback",
        "sandbox",
        "proposal",
        "router",
        "registry",
        "dashboard",
        "display",
        "observability",
        "metric",
        "trace",
        "incident",
        "container",
        "docker",
        "healthcheck",
        "network",
        "vault",
        "signature",
        "vector",
        "memory",
        "runtime",
        "execution",
        "robotics",
        "cad",
        "simulation",
        "physics",
        "mobile",
        "product",
    )

    for line in lowered.splitlines():
        if any(marker in line for marker in markers):
            interesting_lines.append(line.strip())

    return "\n".join(interesting_lines[:300])


def compute_laws_and_readiness(report: LayerReport, corpus: str) -> None:
    present: list[LawSpec] = []
    missing: list[LawSpec] = []

    for expected in report.spec.expected_laws:
        if law_is_present(expected, corpus):
            present.append(expected)
        else:
            missing.append(expected)

    report.present_laws = present
    report.missing_laws = missing

    if not report.spec.expected_laws:
        report.law_percent = 0.0
    else:
        report.law_percent = (len(present) / len(report.spec.expected_laws)) * 100.0

    report.code_weight_percent = compute_code_weight_percent(report)

    if report.status == "MISSING/ПЛАН":
        report.readiness_percent = 0.0
        return

    if report.status == "EMPTY DIR/ПУСТОЙ ГАРАЖ":
        report.readiness_percent = 5.0
        return

    if not report.spec.expected_laws:
        report.readiness_percent = report.code_weight_percent
        return

    report.readiness_percent = round(
        (report.code_weight_percent * 0.35) + (report.law_percent * 0.65),
        1,
    )


def law_is_present(expected: LawSpec, corpus: str) -> bool:
    if not expected.tokens:
        return False

    lowered = corpus.lower()
    return any(token.lower() in lowered for token in expected.tokens)


def compute_code_weight_percent(report: LayerReport) -> float:
    if report.status == "MISSING/ПЛАН":
        return 0.0

    if report.status == "EMPTY DIR/ПУСТОЙ ГАРАЖ":
        return 5.0

    if report.files == 0:
        return 0.0

    score = 0.0
    score += min(report.files * 3.0, 30.0)
    score += min(report.classes * 1.5, 25.0)
    score += min((report.functions + report.methods) * 0.25, 30.0)
    score += min(report.contract_imports * 1.0, 10.0)
    score += 5.0 if report.parse_errors == 0 else 0.0

    return round(min(score, 100.0), 1)


def should_skip_deep_scan(spec: LayerSpec, include_external: bool) -> bool:
    if spec.layer_id == "EXTERNAL_BACKENDS_VENDOR_GATE" and not include_external:
        return True

    return not spec.deep_scan_default


def is_contract_import(module_name: str) -> bool:
    lowered = module_name.lower()
    return (
        "contract" in lowered
        or "contracts" in lowered
        or "models" in lowered
        or "policy" in lowered
        or "validator" in lowered
    )


def unique_paths(paths: list[Path]) -> list[Path]:
    seen: set[str] = set()
    result: list[Path] = []

    for path in paths:
        key = str(path.resolve())
        if key in seen:
            continue
        seen.add(key)
        result.append(path)

    return result


def should_ignore_path(path: Path, project_root: Path) -> bool:
    rel = relative_posix(path, project_root)
    return any(fnmatch.fnmatch(rel, pattern) for pattern in IGNORED_PATH_GLOBS)


def relative_posix(path: Path, project_root: Path) -> str:
    try:
        return path.resolve().relative_to(project_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def print_dashboard(
    reports: list[LayerReport],
    project_root: Path,
    blueprint_path: Path,
    details: bool,
    show_missing_laws: bool,
) -> None:
    total_layers = len(reports)
    present_dirs = sum(1 for report in reports if report.status != "MISSING/ПЛАН")
    code_layers = sum(1 for report in reports if report.files > 0)
    ready_layers = sum(1 for report in reports if report.status == "READY/КОД ЕСТЬ")
    empty_layers = sum(1 for report in reports if report.status == "EMPTY DIR/ПУСТОЙ ГАРАЖ")
    missing_layers = sum(1 for report in reports if report.status == "MISSING/ПЛАН")

    total_files = sum(report.files for report in reports)
    total_classes = sum(report.classes for report in reports)
    total_functions = sum(report.functions for report in reports)
    total_methods = sum(report.methods for report in reports)
    total_imports = sum(report.imports for report in reports)
    total_contract_imports = sum(report.contract_imports for report in reports)
    total_parse_errors = sum(report.parse_errors for report in reports)

    average_readiness = (
        sum(report.readiness_percent for report in reports) / total_layers if total_layers else 0.0
    )

    physical_percent = (present_dirs / total_layers) * 100.0 if total_layers else 0.0
    code_percent = (code_layers / total_layers) * 100.0 if total_layers else 0.0
    ready_percent = (ready_layers / total_layers) * 100.0 if total_layers else 0.0

    print()
    print("MAKSIMAR SUPER RADAR / PROJECT X-RAY")
    print("=" * 118)
    print(f"Project root : {project_root}")
    print(f"Blueprint    : {blueprint_path if blueprint_path.exists() else 'not found / embedded vFINAL only'}")
    print("Mode         : read-only analytics; does not fail CI")
    print("-" * 118)
    print(
        f"{'LAYER':<34} {'STATUS':<24} {'READY%':>7} "
        f"{'FILES':>7} {'CLS':>6} {'FUNC':>7} {'METH':>7} {'IMP':>7} {'LAW':>9}"
    )
    print("-" * 118)

    for report in reports:
        laws_total = len(report.spec.expected_laws)
        laws_present = len(report.present_laws)
        law_cell = f"{laws_present}/{laws_total}" if laws_total else "n/a"

        print(
            f"{report.spec.layer_id:<34} "
            f"{report.status:<24} "
            f"{report.readiness_percent:>6.1f}% "
            f"{report.files:>7} "
            f"{report.classes:>6} "
            f"{report.functions:>7} "
            f"{report.methods:>7} "
            f"{report.imports:>7} "
            f"{law_cell:>9}"
        )

    print("-" * 118)
    print("SUMMARY")
    print("-" * 118)
    print(f"Physical layers present : {present_dirs}/{total_layers} = {physical_percent:.1f}%")
    print(f"Layers with Python code : {code_layers}/{total_layers} = {code_percent:.1f}%")
    print(f"READY code layers       : {ready_layers}/{total_layers} = {ready_percent:.1f}%")
    print(f"Empty garage layers     : {empty_layers}/{total_layers}")
    print(f"Missing/planned layers  : {missing_layers}/{total_layers}")
    print(f"X-Ray readiness average : {average_readiness:.1f}%")
    print()
    print(f"Total .py files         : {total_files}")
    print(f"Total classes           : {total_classes}")
    print(f"Total functions         : {total_functions}")
    print(f"Total methods           : {total_methods}")
    print(f"Total imports           : {total_imports}")
    print(f"Contract/model imports  : {total_contract_imports}")
    print(f"AST parse errors        : {total_parse_errors}")
    print()

    print("READING RULE")
    print("-" * 118)
    print("READY% is a heuristic X-Ray score: 35% code weight + 65% expected law/function markers.")
    print("It is not a production acceptance score and not a security guarantee.")
    print("Drift enforcement remains in the pytest Architecture Drift Guard.")
    print()

    if details or show_missing_laws:
        print("LAW / FUNCTION MARKER DETAILS")
        print("=" * 118)

        for report in reports:
            print()
            print(f"{report.spec.layer_id} — {report.spec.title}")
            print(f"Status: {report.status} | X-Ray readiness: {report.readiness_percent:.1f}%")
            print(f"Existing paths: {', '.join(report.existing_paths) if report.existing_paths else '-'}")
            print(f"Missing paths : {', '.join(report.missing_paths) if report.missing_paths else '-'}")

            if report.deep_scan_skipped:
                print("Deep scan     : skipped")

            if details:
                if report.present_laws:
                    print("Present laws/functions:")
                    for item in report.present_laws:
                        print(f"  + {item.law_id}: {item.title}")

            if report.missing_laws:
                print("Missing laws/functions:")
                for item in report.missing_laws:
                    print(f"  - {item.law_id}: {item.title}")
            else:
                print("Missing laws/functions: none")


def write_json_report(
    reports: list[LayerReport],
    output_path: Path,
    project_root: Path,
    blueprint_path: Path,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "project_root": str(project_root),
        "blueprint_path": str(blueprint_path),
        "mode": "read_only_xray_analytics",
        "layers": [
            {
                "layer_id": report.spec.layer_id,
                "title": report.spec.title,
                "phase": report.spec.phase,
                "status": report.status,
                "readiness_percent": report.readiness_percent,
                "code_weight_percent": report.code_weight_percent,
                "law_percent": report.law_percent,
                "existing_paths": report.existing_paths,
                "missing_paths": report.missing_paths,
                "files": report.files,
                "parsed_files": report.parsed_files,
                "classes": report.classes,
                "functions": report.functions,
                "methods": report.methods,
                "imports": report.imports,
                "contract_imports": report.contract_imports,
                "parse_errors": report.parse_errors,
                "present_laws": [
                    {
                        "law_id": law_spec.law_id,
                        "title": law_spec.title,
                        "tokens": list(law_spec.tokens),
                    }
                    for law_spec in report.present_laws
                ],
                "missing_laws": [
                    {
                        "law_id": law_spec.law_id,
                        "title": law_spec.title,
                        "tokens": list(law_spec.tokens),
                    }
                    for law_spec in report.missing_laws
                ],
                "deep_scan_skipped": report.deep_scan_skipped,
            }
            for report in reports
        ],
    }

    output_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"JSON report written: {output_path}")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\nInterrupted by operator.")
        raise SystemExit(130)
    except Exception as exc:
        print()
        print("MAKSIMAR SUPER RADAR INTERNAL ERROR")
        print("=" * 80)
        print(str(exc))
        print()
        print("This tool is analytics-only. It reports its own failure but does not mutate the project.")
        raise SystemExit(0)
