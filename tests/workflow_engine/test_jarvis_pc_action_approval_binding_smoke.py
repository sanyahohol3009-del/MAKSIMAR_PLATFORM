from __future__ import annotations

import pytest

from MAKSIMAR_SERVER.WORKFLOW_AUTOMATION_RUNTIME.jarvis_pc_action_approval_binding import (
    FALSE_APPROVAL_GATES,
    TRUE_APPROVAL_GATES,
    JarvisPcActionApprovalBinding,
    build_jarvis_pc_action_approval_binding,
)


def test_jarvis_pc_action_approval_binding_requires_owner_approval_and_audit() -> None:
    read_model = build_jarvis_pc_action_approval_binding().to_read_model()

    for key in TRUE_APPROVAL_GATES:
        assert read_model[key] is True
    assert read_model["owner_approval_required"] is True
    assert read_model["action_preview_required"] is True
    assert read_model["allowlist_match_required"] is True
    assert read_model["audit_record_required"] is True
    assert read_model["refusal_on_unknown_action"] is True
    assert read_model["refusal_on_missing_screen_context"] is True
    assert read_model["refusal_on_missing_owner_command"] is True
    for key in FALSE_APPROVAL_GATES:
        assert read_model[key] is False


def test_jarvis_pc_action_approval_binding_rejects_bypass_flags() -> None:
    binding = build_jarvis_pc_action_approval_binding()
    gates = tuple(
        (key, True if key == "bypass_approval_allowed" else value)
        for key, value in binding.disabled_gates
    )

    with pytest.raises(ValueError, match="must remain disabled"):
        JarvisPcActionApprovalBinding(
            binding_id="jarvis_pc_action_approval_binding_v0_1",
            disabled_gates=gates,
        )

