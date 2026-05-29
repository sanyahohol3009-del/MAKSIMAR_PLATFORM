from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DECISION_DOC = PROJECT_ROOT / "docs/architecture/workflow_engine/phase_6_mobile_local_workflow_semantic_decision_v1.md"
RECONCILIATION_DOC = PROJECT_ROOT / "docs/architecture/workflow_engine/phase_6_workflow_automation_registry_reconciliation_v1.md"


def test_phase_6_mobile_local_workflow_decision_contains_required_boundaries() -> None:
    text = DECISION_DOC.read_text(encoding="utf-8")

    required_markers = (
        "mobile app = local-first JARVIS node",
        "server = optional senior/accelerator hub",
        "n8n = external server adapter/container/runtime, not immutable core",
        "Mobile Local Workflow Engine = first-class local mobile automation layer",
        "n8n-compatible graph semantics",
        "Android/iOS capability profiles modeled separately",
        "local AI workflow proposal is not execution authority",
        "no hidden remote control",
        "no direct phone control without explicit permission and approval",
        "no direct core/server canonical write",
        "dashboard/preview read-only",
        "OSS download/install only after vendor gate + sandbox boundary",
        "Mobile local workflow automation is a first-class local mobile automation layer.",
        "The mobile app acts as a local-first JARVIS node.",
        "n8n remains an external server adapter, container, and runtime.",
        "A proposal is not execution authority.",
        "direct phone control without explicit user permission and approval",
        "Android and iOS capability limits must be modeled separately",
        "direct core write",
        "direct server canonical write",
    )

    for marker in required_markers:
        assert marker in text


def test_phase_6_registry_reconciliation_contains_active_batch_scope() -> None:
    text = RECONCILIATION_DOC.read_text(encoding="utf-8")

    assert "6.0 PHASE 6 Registry Reconciliation / Mobile Local Workflow Correction" in text
    assert "6.1 Workflow Graph Contracts" in text
    assert "6.6 PHASE 6 Acceptance" in text
    assert "MAKSIMAR_CORE_LIB/workflow_engine/" in text
    assert "ANDROID_SHELL/workflow_adapter/" in text
    assert "IOS_SHELL/workflow_adapter/" in text
    assert "batches 6.1 through 6.6 as active missing product scope" in text
