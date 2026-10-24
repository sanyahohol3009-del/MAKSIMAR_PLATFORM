from __future__ import annotations

from pathlib import Path
import json

import pytest

from MAKSIMAR_SERVER.WORKFLOW_AUTOMATION_RUNTIME.jarvis_pc_action_adapter_contract import (
    ExistingWindowsEdgeAdapter,
    FALSE_ADAPTER_GATES,
    JARVIS_PC_ACTION_ALLOWLIST_IDS,
    PC_ACTION_OPERATION_CONTRACTS,
    TRUE_ADAPTER_GATES,
    JarvisPcActionAdapterContract,
    build_jarvis_pc_action_adapter_contract,
)
from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import (
    CapabilityRequirement, ExecutionPlan, Goal, OperationRequirement, PlanStep,
    RequestUnderstanding,
)


def test_jarvis_pc_action_adapter_is_direct_owner_gate_contract() -> None:
    read_model = build_jarvis_pc_action_adapter_contract().to_read_model()

    assert read_model["allowed_action_ids"] == JARVIS_PC_ACTION_ALLOWLIST_IDS
    assert read_model["controlled_pc_action_candidate"] is True
    assert read_model["owner_command_required"] is True
    assert read_model["allowlist_required"] is True
    assert read_model["approval_required"] is False
    assert read_model["audit_required"] is True
    assert read_model["screen_context_required"] is False
    assert read_model["explicit_action_preview_required"] is False
    for key in TRUE_ADAPTER_GATES:
        assert read_model[key] is True
    for key in FALSE_ADAPTER_GATES:
        assert read_model[key] is False


def test_jarvis_pc_action_adapter_rejects_dangerous_true_flags() -> None:
    adapter = build_jarvis_pc_action_adapter_contract()
    gates = tuple(
        (key, True if key == "hidden_remote_control_allowed" else value)
        for key, value in adapter.disabled_gates
    )

    with pytest.raises(ValueError, match="must remain disabled"):
        JarvisPcActionAdapterContract(
            adapter_id="jarvis_pc_action_adapter_contract_v1",
            allowed_action_ids=JARVIS_PC_ACTION_ALLOWLIST_IDS,
            disabled_gates=gates,
        )


def test_jarvis_pc_action_adapter_uses_only_the_pinned_windows_owner_process() -> None:
    root = Path(__file__).resolve().parents[2]
    lowered = (
        root
        / "MAKSIMAR_SERVER/WORKFLOW_AUTOMATION_RUNTIME/jarvis_pc_action_adapter_contract.py"
    ).read_text(encoding="utf-8").lower()
    for marker in (
        "pyautogui",
        "pynput",
        "xdotool",
        "keyboard.",
        "mouse.",
        "click(",
        "os.system",
        "powershell",
        "shell=true",
        "webbrowser",
        "socket",
    ):
        assert marker not in lowered
    assert "windows_edge_python" in lowered
    assert "windows_edge_script" in lowered
    assert "shell=false" in lowered
    assert "--execute-json-base64" in lowered


def test_windows_edge_owner_contracts_are_typed_and_dangerous_actions_remain_per_step() -> None:
    assert set(PC_ACTION_OPERATION_CONTRACTS) == set(JARVIS_PC_ACTION_ALLOWLIST_IDS) | {
        "runtime_windows_edge",
    }
    assert PC_ACTION_OPERATION_CONTRACTS["read_screen"][0]["risk_class"] == "READ_ONLY"
    assert PC_ACTION_OPERATION_CONTRACTS["volume_up"][0]["risk_class"] == "MUTATION"
    for capability_id in ("close_opera", "close_all_opera", "type_text", "browser_search"):
        assert PC_ACTION_OPERATION_CONTRACTS[capability_id][0]["risk_class"] == "DANGEROUS"


def test_windows_edge_adapter_returns_matching_evidence_and_receipt(monkeypatch) -> None:
    contract = PC_ACTION_OPERATION_CONTRACTS["read_screen"][0]
    adapter = ExistingWindowsEdgeAdapter()
    monkeypatch.setattr(adapter, "_run_owner", lambda *args, **kwargs: {
        "ok": True, "status": "COMPLETE", "executed": True,
        "evidence": {"screenshot_path": "C:\\MAKSIMAR_EDGE\\screen.png", "sha256": "abc"},
    })
    understanding = RequestUnderstanding(
        request_id="request_pc", original_text="сделай снимок экрана", language="ru",
        goals=(Goal("goal_pc", "capture screen"),),
        required_capabilities=(CapabilityRequirement("read_screen", "capture", True),),
        effect_type="OBSERVE", target_scope="owner_windows_screen",
        reversibility="REVERSIBLE", external_side_effect=False, risk_class="READ_ONLY",
        operation_requirements=(OperationRequirement(
            capability_id="read_screen", operation_id=contract["operation_id"],
            purpose="capture", required=True, required_evidence=contract["evidence_kinds"],
            effect_type="OBSERVE", target_scope="owner_windows_screen",
            reversibility="REVERSIBLE", external_side_effect=False, risk_class="READ_ONLY",
            ),),
        unresolved_capabilities=(), current_topic="screen capture", unresolved_reference="",
        relevant_context_trace_ids=(), confidence=1.0, reason_codes=("typed_test",),
    )
    plan = ExecutionPlan("request_pc", (PlanStep(
        step_id="step_pc", goal_id="goal_pc", capability_id="read_screen",
        operation=contract["operation_id"], required_evidence=contract["evidence_kinds"],
        effect_type="OBSERVE", target_scope="owner_windows_screen",
        reversibility="REVERSIBLE", external_side_effect=False, risk_class="READ_ONLY",
    ),))
    bundle = adapter.collect_evidence(understanding, plan, "trace_pc")
    assert bundle.status == "COMPLETE"
    assert json.loads(bundle.items[0].observation)["executed"] is True
    assert bundle.receipts[0].provider_id == adapter.provider_id
    assert bundle.receipts[0].operation_id == contract["operation_id"]
