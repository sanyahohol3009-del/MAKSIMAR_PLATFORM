import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import (
    CapabilityRequirement, ExecutionPlan, Goal, OperationRequirement, PlanStep,
    RequestDeadline, RequestUnderstanding,
)
from MAKSIMAR_SERVER.AI_ORCHESTRATION import n8n_adapter


OFFICIAL_SKILLS = (
    "using-n8n-skills-official", "n8n-workflow-lifecycle-official",
    "n8n-node-configuration-official", "n8n-agents-official", "n8n-extending-mcp-official",
)


@pytest.fixture
def private_skills(monkeypatch, tmp_path):
    monkeypatch.setattr(n8n_adapter, "_PROJECT_ROOT", tmp_path)
    contents = {}
    for skill_id in OFFICIAL_SKILLS:
        path = tmp_path / "RUNTIME/n8n/authoring/.agents/skills" / skill_id / "SKILL.md"
        path.parent.mkdir(parents=True)
        contents[skill_id] = skill_id + "\n" + "Я" * 900
        path.write_text(contents[skill_id], encoding="utf-8")
    return tmp_path, contents


@pytest.mark.parametrize("operation", ("create_workflow", "build_workflow"))
def test_n8n_provider_consumes_bounded_private_skill_context(monkeypatch, private_skills, operation) -> None:
    spec = json.dumps({"trigger": {"catalog_query": "manual"}, "steps": [{"action": "set_field", "step_id": "x"}]})
    understanding = RequestUnderstanding(
        request_id="skill-path", original_text="create a local workflow", language="en",
        goals=(Goal("g1", "create workflow"),),
        required_capabilities=(CapabilityRequirement("workflow_automation:n8n", "create", True),),
        effect_type="MUTATE", target_scope="local_workflow_automation", reversibility="REVERSIBLE",
        external_side_effect=False, unresolved_capabilities=(), operation_requirements=(OperationRequirement(
            capability_id="workflow_automation:n8n", operation_id=operation, purpose="create",
            required_evidence=("n8n_workflow",), effect_type="MUTATE", target_scope="local_workflow_automation",
            reversibility="REVERSIBLE", external_side_effect=False, risk_class="MUTATION", required=True,
            parameters=(("logical_spec", spec),),
        ),), current_topic="workflow", unresolved_reference="", relevant_context_trace_ids=(),
        risk_class="MUTATION", confidence=1.0, reason_codes=("typed_test",),
    )
    plan = ExecutionPlan("skill-path", (PlanStep(
        step_id="s1", goal_id="g1", capability_id="workflow_automation:n8n", operation=operation,
        required_evidence=("n8n_workflow",), effect_type="MUTATE", target_scope="local_workflow_automation",
        reversibility="REVERSIBLE", external_side_effect=False, risk_class="MUTATION", parameters=(("logical_spec", spec),),
    ),))
    monkeypatch.setattr(n8n_adapter, "_compiled_workflow_spec", lambda *a, **k: ({"name": "local", "nodes": [], "connections": {}}, None))
    monkeypatch.setattr(n8n_adapter, "_architect_logical_spec", lambda *a, **k: json.loads(spec))
    calls = []
    reader = n8n_adapter.load_automation_n8n_private_skill_context
    def capture_reader(selected):
        calls.append(selected)
        return reader(selected)
    monkeypatch.setattr(n8n_adapter, "load_automation_n8n_private_skill_context", capture_reader)
    monkeypatch.setattr(n8n_adapter, "_n8n_request", lambda method, path, payload=None: {"id": "wf-local", "name": "local", "active": False})
    evidence = n8n_adapter.ExistingN8nAdapter().collect_evidence(understanding, plan, "trace-skill")
    assert evidence.status == "COMPLETE"
    observation = json.loads(evidence.items[0].observation)
    assert observation["authoring_skill_ids"] == [
        "using-n8n-skills-official", "n8n-node-configuration-official"
    ]
    assert calls == [("using-n8n-skills-official", "n8n-node-configuration-official")]


def test_private_reader_preserves_all_five_order_dedupe_and_character_bound(private_skills):
    root, contents = private_skills
    selected = tuple(reversed(OFFICIAL_SKILLS)) + OFFICIAL_SKILLS
    result = n8n_adapter.load_automation_n8n_private_skill_context(selected)
    assert result["skill_ids"] == tuple(reversed(OFFICIAL_SKILLS))
    assert len(result["entries"]) == 5
    for entry in result["entries"]:
        assert entry["content"] == contents[entry["skill_id"]][:800]
        assert len(entry["content"]) == 800
        assert not Path(entry["path"]).is_absolute()
        assert (root / entry["path"]).is_file()
    assert result["organ_id"] == "automation"
    assert result["provider_policy_evidence_owned_by_host"] is True
    assert result["direct_execution_allowed"] is False


def test_private_reader_never_reads_unapproved_or_missing_skills(monkeypatch, private_skills):
    root, _ = private_skills
    missing = root / "RUNTIME/n8n/authoring/.agents/skills" / OFFICIAL_SKILLS[1] / "SKILL.md"
    missing.unlink()
    original_read = Path.read_text
    reads = []
    def read(path, *args, **kwargs):
        reads.append(path)
        return original_read(path, *args, **kwargs)
    monkeypatch.setattr(Path, "read_text", read)
    result = n8n_adapter.load_automation_n8n_private_skill_context((
        "../../outside", "unknown-skill", OFFICIAL_SKILLS[1], OFFICIAL_SKILLS[0], OFFICIAL_SKILLS[0],
    ))
    assert result["skill_ids"] == (OFFICIAL_SKILLS[0],)
    assert reads == [root / "RUNTIME/n8n/authoring/.agents/skills" / OFFICIAL_SKILLS[0] / "SKILL.md"]
    assert n8n_adapter.load_automation_n8n_private_skill_context(())["entries"] == ()


def test_private_reader_does_not_hide_read_failure(monkeypatch, private_skills):
    def denied(*args, **kwargs):
        raise PermissionError("controlled skill read denial")
    monkeypatch.setattr(Path, "read_text", denied)
    with pytest.raises(PermissionError, match="controlled skill read denial"):
        n8n_adapter.load_automation_n8n_private_skill_context(OFFICIAL_SKILLS)


@pytest.mark.parametrize("operation", ("create_workflow", "build_workflow"))
def test_cancelled_authoring_does_not_read_skills_compile_or_call_provider(monkeypatch, operation):
    deadline = RequestDeadline(5)
    deadline.cancel()
    def forbidden(*args, **kwargs):
        pytest.fail("cancelled authoring must stop before skills, compiler, model or provider")
    for name in ("load_automation_n8n_private_skill_context", "_compiled_workflow_spec",
                 "_architect_logical_spec", "_n8n_request"):
        monkeypatch.setattr(n8n_adapter, name, forbidden)
    step = PlanStep(step_id="cancelled", goal_id="g1", capability_id="workflow_automation:n8n",
        operation=operation, required_evidence=("n8n_workflow",), effect_type="MUTATE",
        target_scope="local_workflow_automation", reversibility="REVERSIBLE",
        external_side_effect=False, risk_class="MUTATION")
    evidence = n8n_adapter.ExistingN8nAdapter().collect_evidence(
        SimpleNamespace(request_id="cancelled"), ExecutionPlan("cancelled", (step,)),
        "trace-cancelled", deadline=deadline)
    assert evidence.status == "UNAVAILABLE"
    assert evidence.errors == (operation + ":total_deadline",)
    assert evidence.items == evidence.receipts == ()
