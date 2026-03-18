from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.workflow_engine.workflow_loader import load_workflow_definition


def test_workflow_loader_rejects_missing_workflow_id(tmp_path: Path) -> None:
    """Workflow loader should reject missing workflow_id."""
    file_path = tmp_path / "workflow_definition.v1.yaml"
    file_path.write_text(
        "\n".join(
            [
                "schema_version: workflow_definition.v1",
                "steps:",
                "  - step_id: s1",
                "    action_ref: action.one",
            ]
        ),
        encoding="utf-8",
    )

    result = load_workflow_definition(file_path)

    assert result.is_valid is False
    assert result.definition is None
    assert result.error is not None


def test_workflow_loader_accepts_valid_definition(tmp_path: Path) -> None:
    """Workflow loader should accept valid workflow definition."""
    file_path = tmp_path / "workflow_definition.v1.yaml"
    file_path.write_text(
        "\n".join(
            [
                "workflow_id: wf.sample",
                "schema_version: workflow_definition.v1",
                "trigger_phrases:",
                "  - run sample",
                "steps:",
                "  - step_id: s1",
                "    action_ref: action.one",
            ]
        ),
        encoding="utf-8",
    )

    result = load_workflow_definition(file_path)

    assert result.is_valid is True
    assert result.definition is not None
    assert result.definition.workflow_id == "wf.sample"
    assert len(result.definition.steps) == 1
    assert result.definition.steps[0].step_id == "s1"
