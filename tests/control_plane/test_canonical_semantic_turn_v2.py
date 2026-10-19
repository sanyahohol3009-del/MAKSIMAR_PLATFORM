from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def isolate_canonical_session_persistence(monkeypatch, tmp_path):
    """Session unit tests must never append fixture turns into the real user store."""
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import session_memory_store
    monkeypatch.setattr(session_memory_store, "SESSION_MEMORY_ROOT", tmp_path / "session_memory")

import CONTROL_PLANE.canonical_semantic_spine as spine
from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import (
    EvidenceBundle, EvidenceItem, ExecutionReceipt, FinalBrainPort, IdentityContext, ModelUnderstandingPort,
    ProjectUnderstandingPort, utc_observed_at,
)
from MAKSIMAR_CORE_LIB.security_layer.semantic_policy import SemanticPolicyEvaluator
from MAKSIMAR_CORE_LIB.security_layer.semantic_policy import identity_context_from_http_payload
from MAKSIMAR_CORE_LIB.security_layer.jarvis_speaker_profile_resolver import resolve_family_profile
from MAKSIMAR_SERVER.AI_ORCHESTRATION.conversation_evidence_adapter import ExistingConversationEvidenceAdapter
from MAKSIMAR_SERVER.AI_ORCHESTRATION.project_understanding_adapter import ExistingProjectUnderstandingAdapter


CONVERSATION_PROBES = (
    "джарвис привет", "как дела?", "почему ты назвал меня другим именем?", "я пошутил",
    "расскажи коротко, что работает", "ты меня слышишь?", "ответь без технических деталей",
    "а почему так?", "это относилось ко мне?", "я имел в виду предыдущий ответ", "продолжай",
    "спасибо, брат", "кто ты?", "как меня зовут?", "что ты имел в виду до этого?",
)

PROJECT_PROBES = (
    ("что изменилось в рабочем дереве?", ("inspect_git_status", "inspect_changed_files", "inspect_diff_summary")),
    ("покажи незакоммиченные изменения", ("inspect_git_status", "inspect_changed_files", "inspect_diff_summary")),
    ("какие файлы изменены?", ("inspect_changed_files",)), ("есть удалённые или новые файлы?", ("inspect_changed_files",)),
    ("дай сводку текущего diff", ("inspect_diff_summary",)), ("сравни staged и обычный diff", ("inspect_diff_summary",)),
    ("покажи структуру репозитория", ("inspect_structure",)), ("какие верхние каталоги?", ("inspect_structure",)),
    ("найди canonical semantic turn", ("search",)), ("где объявлен EvidenceBundle?", ("search",)),
    ("какие зависимости объявлены?", ("inspect_dependencies",)), ("проверь dependency manifests", ("inspect_dependencies",)),
    ("какие импорты связывают слои?", ("inspect_imports",)), ("покажи импорты runtime", ("inspect_imports",)),
    ("каков результат тестов?", ("inspect_tests",)), ("есть подтверждённые test failures?", ("inspect_tests",)),
    ("что известно о покрытии?", ("inspect_coverage",)), ("какие слабые места coverage?", ("inspect_coverage",)),
    ("покажи архитектурные нарушения", ("inspect_architecture",)), ("каков architecture report?", ("inspect_architecture",)),
)


def evidence_for(operation):
    contract = spine.operation_contract(operation)
    assert contract is not None
    return tuple(contract["evidence_kinds"])


def project_operations(result):
    return tuple(
        operation for operation in result["selected_provider_operation"]
        if operation != "respond"
    )


def project_evidence_kinds(result):
    return {
        item["kind"] for item in result["evidence_bundle"]["items"]
        if item["capability_id"] == "project.read"
    }


def verified_model_output(content):
    return {"final_valid": True,
        "ok": True, "content": content,
        "model_call_attempted": True, "model_call_succeeded": True,
        "model_call_used": False, "raw_output_present": bool(content),
        "requested_num_ctx": 4096, "configured_num_ctx": 4096,
    }


def model_payload(user_prompt, capability, operations, *, topic="", reference="", effect="OBSERVE"):
    request = json.loads(user_prompt)
    risk = "READ_ONLY" if effect == "OBSERVE" else "MUTATION"
    reversibility = "REVERSIBLE" if effect in {"OBSERVE", "MUTATE"} else "UNKNOWN"
    external_side_effect = False
    return verified_model_output(json.dumps({
        "schema_version": "request_understanding.v2", "language": "ru",
        "goals": [{"goal_id": f"g{i}", "description": f"Semantic goal {i}"} for i in range(1, len(operations) + 1)],
        "required_capabilities": [{"capability_id": capability, "purpose": "semantic capability", "required": True}],
        "effect_type": effect, "target_scope": "conversation" if capability == "conversation.respond" else "project",
        "reversibility": reversibility,
        "external_side_effect": external_side_effect, "unresolved_capabilities": [],
        "operation_requirements": [{"capability_id": capability, "operation_id": op,
                                    "purpose": (spine.operation_contract(op) or {}).get("description", "unresolved"),
                                    "required_evidence": list(evidence_for(op)) if spine.operation_contract(op) else ["unknown"],
                                    "effect_type": effect, "target_scope": "conversation" if capability == "conversation.respond" else "project",
                                    "reversibility": reversibility, "external_side_effect": external_side_effect,
                                    "risk_class": risk,
                                    "required": True} for op in operations],
        "current_topic": topic, "unresolved_reference": reference,
        "risk_class": risk,
        "confidence": 0.96,
        "reason_codes": ["model_semantic_interpretation"],
    }, ensure_ascii=False))


class Model(ModelUnderstandingPort):
    def __init__(self, fn, correction=None):
        self.fn = fn
        if correction is not None:
            self.correct_input = correction
    def understand(self, *, system_prompt, user_prompt, deadline): return self.fn(system_prompt, user_prompt)


class Final(FinalBrainPort):
    def __init__(self): self.calls = []
    def answer(self, *, deadline, **payload):
        self.calls.append(payload); name = payload["identity_facts"].get("display_name")
        return {"ok": True, "response_text": f"Ответ для {name}." if name else "Нейтральный ответ.",
                "model_call_attempted": True, "model_call_succeeded": True,
                "model_call_used": True, "raw_output_present": True,
                "done": True, "done_reason": "stop", "truncation": False}


class Project(ProjectUnderstandingPort):
    def __init__(self, status="AVAILABLE"): self.status = status; self.calls = []
    def health(self): return {"status": self.status, "provider_id": "existing_project_workspace_tools"}
    def collect_evidence(self, understanding, plan, trace_id, deadline=None):
        self.calls.append(plan)
        items = tuple(EvidenceItem(kind=kind, source=f"fake:{step.operation}", observation="bounded fact",
            scope="test", confidence=1.0, trace_id=trace_id, observed_at=utc_observed_at(),
            source_reference="test://fixture", request_id=understanding.request_id,
            step_id=step.step_id, capability_id=step.capability_id, operation_id=step.operation,
            provider_id="existing_project_workspace_tools")
            for step in plan.steps for kind in step.required_evidence)
        receipts = tuple(ExecutionReceipt(
            receipt_id=f"{trace_id}:{step.step_id}", request_id=understanding.request_id,
            trace_id=trace_id, step_id=step.step_id, capability_id=step.capability_id,
            operation_id=step.operation, provider_id="existing_project_workspace_tools",
            status="COMPLETE", result="fixture evidence collected",
        ) for step in plan.steps)
        return EvidenceBundle(understanding.request_id, "project.read", trace_id, "COMPLETE", items,
                              ("fixture",), receipts, ())


def run(model, *, text="probe", context=None, identity=None, project=None, final=None,
        input_channel="unknown", input_quality_metadata=None, correction=None):
    return spine.run_canonical_semantic_turn(
        text=text, project_port=project or Project(), conversation_port=ExistingConversationEvidenceAdapter(),
        model_port=Model(model, correction=correction), final_brain_port=final or Final(),
        permission_port=SemanticPolicyEvaluator(),
        identity=identity or IdentityContext("aleksandr", "local_terminal_session", "owner", True, True, "Александр", "JARVIS"),
        session_context=context or {}, input_channel=input_channel,
        input_quality_metadata=input_quality_metadata or {})


@pytest.mark.parametrize("text", CONVERSATION_PROBES)
def test_conversation_turns_use_one_semantic_spine_without_project_tools(text):
    result = run(lambda _, user: model_payload(user, "conversation.respond", ("respond",), topic="conversation"), text=text)
    assert result["orchestration_path"] == "canonical_semantic_turn_v2"
    assert result["selected_capabilities"] == ("conversation.respond",)
    assert result["selected_provider_operation"] == ("respond",)
    assert {item["kind"] for item in result["evidence_bundle"]["items"]} == {
        "identity_facts", "bounded_session_context",
    }
    assert result["project_tools_used"] is False
    assert result["fallback_used"] is False
    assert result["selection_source"] == "model_semantic_registry"
    assert result["trace_id"] == result["evidence_bundle"]["trace_id"] == result["trace"]["trace_id"]


def test_voice_input_uses_existing_helper_only_for_correction_before_main_understanding():
    observed = {}

    def correction(**payload):
        observed["helper"] = payload
        return {"final_valid": True, "ok": True, "content": json.dumps({
            "schema_version": "helper_input_correction.v2",
            "corrected_text": "открой браузер",
            "ambiguity_candidates": [], "confidence": 0.98,
            "reason_codes": ["stt_correction"],
            "preserve_original": True, "no_change_needed": False,
        }, ensure_ascii=False), "model_call_attempted": True, "model_call_succeeded": True,
                "raw_output_present": True, "raw_model_result": {"model": "jarvis:helper3b"}}

    def understanding(_, user_prompt):
        request = json.loads(user_prompt)
        observed["main"] = request
        return model_payload(user_prompt, "conversation.respond", ("respond",))

    result = run(understanding, text="аткрой браузир", input_channel="windows_voice_edge",
                 input_quality_metadata={"stt_confidence": 0.61}, correction=correction)

    assert observed["helper"]["original_text"] == "аткрой браузир"
    assert observed["main"]["original_text"] == "аткрой браузир"
    assert observed["main"]["input_preparation"]["helper_correction_proposal"] == "открой браузер"
    assert result["helper_call_used"] is True
    assert result["helper_call_succeeded"] is True
    assert result["correction_applied"] is True
    assert result["normalized_text"] == "открой браузер"
    assert result["helper_confidence"] == 0.98
    assert result["helper_failure_mode"] == ""
    assert result["helper_parsed_result"]["corrected_text"] == "открой браузер"


def test_helper_failure_does_not_create_keyword_fallback_or_block_main_understanding():
    result = run(
        lambda _, user: model_payload(user, "conversation.respond", ("respond",)),
        text="неполная фраза", input_channel="terminal",
        input_quality_metadata={"input_incomplete": True},
        correction=lambda **_: {"ok": False, "error": "unavailable",
                                "model_call_attempted": True, "model_call_succeeded": False,
                                "raw_output_present": False},
    )

    assert result["operation_status"] == "COMPLETE"
    assert result["helper_call_used"] is False
    assert result["helper_call_attempted"] is True
    assert result["helper_failure_mode"] == "model_unavailable"
    assert result["correction_applied"] is False
    assert result["fallback_used"] is False


def test_clean_terminal_input_skips_helper_by_typed_quality_decision():
    result = run(lambda _, user: model_payload(user, "conversation.respond", ("respond",)),
                 text="обычная беседа", input_channel="terminal")

    assert result["helper_call_used"] is False
    assert result["helper_failure_mode"] == "not_requested"


@pytest.mark.parametrize(("text", "operations"), PROJECT_PROBES)
def test_project_goals_select_contract_operations_and_evidence(text, operations):
    result = run(lambda _, user: model_payload(user, "project.read", operations, topic="project"), text=text)
    assert result["understanding"]["goals"]
    assert result["understanding"]["operation_requirements"]
    assert project_operations(result) == operations
    assert project_evidence_kinds(result) == {
        kind for operation in operations for kind in evidence_for(operation)
    }
    assert result["fallback_used"] is False
    assert result["selection_source"] == "model_semantic_registry"


def test_git_paraphrases_have_equivalent_evidence_sets():
    observed = []
    operations = ("inspect_git_status", "inspect_changed_files", "inspect_diff_summary")
    for text in ("что поменялось локально?", "покажи состояние незаписанных правок", "какие изменения ждут commit?"):
        result = run(lambda _, user: model_payload(user, "project.read", operations), text=text)
        observed.append(project_evidence_kinds(result))
    assert observed == [{"git_status", "changed_files", "diff_summary"}] * 3


def test_follow_up_context_reaches_understanding_and_final_brain():
    context = {
        "bounded_chronological_turns": ({"user_text": "привет", "assistant_text": "ошибочное обращение",
                                          "topic": "greeting", "trace_id": "prior-trace"},),
        "recent_relevant_turns": (),
        "identity_facts": {"identity_id": "aleksandr", "display_name": "Александр"},
        "truncated": False,
    }
    final = Final()

    def understand(_, user):
        assert json.loads(user)["bounded_session_context"]["recent_turns"]
        payload = json.loads(model_payload(user, "conversation.respond", ("respond",),
                                           topic="identity correction", reference="previous assistant address")["content"])
        return verified_model_output(json.dumps(payload, ensure_ascii=False))

    result = run(understand, text="почему ты так меня назвал?", context=context, final=final)
    assert result["understanding"]["unresolved_reference"]
    assert final.calls[0]["session_context"]["recent_relevant_turns"][0]["trace_id"] == "prior-trace"
    assert final.calls[0]["session_context"]["selection_basis"] == "host_bounded_chronological_context"


def test_identity_is_external_ground_truth_and_unknown_identity_is_neutral():
    verified = run(lambda _, user: model_payload(user, "conversation.respond", ("respond",)))
    assert verified["identity"]["identity_id"] == "aleksandr"
    assert verified["identity"]["display_name"] == "Александр"
    assert "Александр" in verified["response_text"]

    anonymous = IdentityContext("anonymous", "http_unverified", "unknown", False, False, "", "JARVIS")
    neutral = run(lambda _, user: model_payload(user, "conversation.respond", ("respond",)), identity=anonymous)
    assert neutral["response_text"] == "Нейтральный ответ."


@pytest.mark.parametrize(("identity_id", "profile", "display_name", "owner"), (
    ("aleksandr", "owner", "Александр", True),
    ("yulia", "trusted_family", "Юля", False),
    ("maksim", "child", "Максим", False),
    ("makar", "child", "Макар", False),
))
def test_family_profiles_share_grounded_identity_contract(identity_id, profile, display_name, owner):
    identity = identity_context_from_http_payload({"identity": {
        "identity_id": identity_id, "source": "authenticated_http_session",
        "profile_type": profile, "verified": True, "trusted_session": True,
    }})
    assert identity.display_name == display_name
    assert identity.owner_authorized is owner
    result = run(lambda _, user: model_payload(user, "conversation.respond", ("respond",)), identity=identity)
    assert result["orchestration_path"] == "canonical_semantic_turn_v2"
    assert display_name in result["response_text"]


def test_model_goal_cannot_replace_resolved_identity_facts():
    def attempted_override(_, user):
        payload = json.loads(model_payload(user, "conversation.respond", ("respond",))["content"])
        payload["goals"][0]["description"] = "Назвать пользователя вымышленным именем Человек-паук"
        return verified_model_output(json.dumps(payload, ensure_ascii=False))

    result = run(attempted_override)
    assert result["identity"]["display_name"] == "Александр"
    assert "Александр" in result["response_text"]
    assert "Человек-паук" not in result["response_text"]


def test_session_context_is_identity_isolated_and_supplies_bounded_chronology_for_model_selection():
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.session_memory_store import CanonicalSessionContextStore

    store = CanonicalSessionContextStore(max_turns=3)
    owner = IdentityContext("aleksandr", "local_terminal_session", "owner", True, True, "Александр", "JARVIS")
    family = IdentityContext("yulia", "authenticated_http_session", "trusted_family", False, True, "Юля", "JARVIS")
    child = IdentityContext("maksim", "authenticated_http_session", "child", False, True, "Максим", "JARVIS")
    store.append("shared", owner, user_text="секрет владельца", assistant_text="owner reply",
                 topic="owner topic", unresolved_reference="предыдущий ответ", trace_id="owner-trace")
    store.append("shared", owner, user_text="другая тема", assistant_text="other reply",
                 topic="other topic", unresolved_reference="", trace_id="other-trace")
    store.append("shared", owner, user_text="вернулись к теме", assistant_text="topic reply",
                 topic="owner topic", unresolved_reference="предыдущий ответ", trace_id="owner-trace-2")

    owner_context = store.read("shared", owner)
    family_context = store.read("shared", family)
    child_context = store.read("shared", child)
    assert owner_context["selection_basis"] == "model_semantic_selection_pending"
    assert [turn["trace_id"] for turn in owner_context["bounded_chronological_turns"]] == [
        "owner-trace", "other-trace", "owner-trace-2",
    ]
    assert owner_context["unresolved_reference"]["present"] is True
    assert family_context["bounded_chronological_turns"] == ()
    assert child_context["bounded_chronological_turns"] == ()
    assert "секрет владельца" not in str(family_context)
    assert "секрет владельца" not in str(child_context)


def test_session_context_has_one_total_prompt_material_bound_not_only_per_turn_limits():
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.session_memory_store import CanonicalSessionContextStore

    store = CanonicalSessionContextStore(
        max_turns=6,
        max_text_chars=1200,
        max_context_chars=900,
        max_turn_context_chars=420,
    )
    owner = IdentityContext(
        "aleksandr", "local_terminal_session", "owner", True, True, "Александр", "JARVIS",
    )
    for index in range(6):
        store.append(
            "bounded",
            owner,
            user_text=f"user-{index}-" + ("я" * 1200),
            assistant_text=f"assistant-{index}-" + ("а" * 1200),
            topic="topic-" + ("т" * 160),
            unresolved_reference="",
            trace_id=f"trace-{index}",
        )
    context = store.read("bounded", owner)
    material = sum(
        len(turn["user_text"]) + len(turn["assistant_text"]) + len(turn["topic"])
        for turn in context["bounded_chronological_turns"]
    )
    assert material <= 900
    assert context["truncated"] is True
    assert context["omitted_turn_count"] > 0
    assert context["bounded_chronological_turns"][-1]["trace_id"] == "trace-5"


def test_bounded_topic_metadata_alone_does_not_claim_conversation_text_was_truncated():
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.session_memory_store import CanonicalSessionContextStore

    store = CanonicalSessionContextStore()
    owner = IdentityContext(
        "aleksandr", "local_terminal_session", "owner", True, True, "Александр", "JARVIS",
    )
    store.append(
        "topic-only-bound",
        owner,
        user_text="у тебя всё хорошо?",
        assistant_text="Да, всё хорошо.",
        topic="длинная служебная тема " * 10,
        unresolved_reference="",
        trace_id="trace-topic",
    )
    context = store.read("topic-only-bound", owner)
    assert context["bounded_chronological_turns"][0]["topic"]
    assert len(context["bounded_chronological_turns"][0]["topic"]) <= 40
    assert context["truncated"] is False
    assert context["omitted_turn_count"] == 0


def test_model_context_projection_keeps_semantics_but_not_host_trace_state():
    context = {
        "bounded_chronological_turns": tuple({
            "user_text": f"user-{index}-" + ("u" * 300),
            "assistant_text": f"assistant-{index}-" + ("a" * 500),
            "topic": f"topic-{index}",
            "trace_id": f"host-trace-{index}",
        } for index in range(6)),
        "unresolved_reference": {"present": True, "description": "previous answer"},
        "truncated": True,
        "omitted_turn_count": 2,
    }
    projected = spine._semantic_context_for_model(context)
    serialized = json.dumps(projected, ensure_ascii=False)

    assert projected["bounded_turn_count"] == 6
    assert len(projected["recent_turns"]) == 2
    assert projected["recent_turns"][-1]["user_text"].startswith("user-5-")
    assert len(projected["recent_turns"][-1]["assistant_text"]) <= 160
    assert "host-trace" not in serialized
    assert len(serialized) < 1000


def test_structure_does_not_invoke_git_and_git_does_not_fall_back_to_structure():
    structure = run(lambda _, user: model_payload(user, "project.read", ("inspect_structure",)))
    git_status = run(lambda _, user: model_payload(user, "project.read", ("inspect_git_status",)))
    assert project_operations(structure) == ("inspect_structure",)
    assert project_evidence_kinds(structure) == {"inspect_structure"}
    assert project_operations(git_status) == ("inspect_git_status",)
    assert "inspect_structure" not in git_status["selected_provider_operation"]


def test_unknown_operation_gets_one_replan_then_truthful_unresolved_status():
    calls = []

    def understand(_, user):
        calls.append(user)
        return model_payload(user, "project.read", ("operation_not_in_registry",))

    result = run(understand)
    assert len(calls) == 2
    assert result["operation_status"] == "UNRESOLVED_OPERATION"
    assert result["evidence_bundle"] is None
    assert result["fallback_used"] is False
    assert "inspect_structure" not in result["selected_provider_operation"]


def test_requested_mutation_is_not_rewritten_as_read_only_project_goal():
    result = run(lambda _, user: model_payload(user, "project.files.write", ("write_file",), effect="MUTATE"))
    assert result["understanding"]["effect_type"] == "MUTATE"
    assert result["selected_capabilities"] != ("project.read",)
    assert result["operation_status"] in {"UNRESOLVED_OPERATION", "UNRESOLVED_CAPABILITY", "DENIED", "APPROVAL_REQUIRED"}


def test_multi_capability_plan_evaluates_each_provider_and_returns_one_trace():
    final = Final()

    def understand(_, user):
        payload = json.loads(model_payload(user, "conversation.respond", ("respond",))["content"])
        payload["goals"] = [
            {"goal_id": "g1", "description": "Respond conversationally"},
            {"goal_id": "g2", "description": "Inspect Git status"},
        ]
        payload["required_capabilities"] = [
            {"capability_id": "conversation.respond", "purpose": "conversation", "required": True},
            {"capability_id": "project.read", "purpose": "project evidence", "required": True},
        ]
        payload["operation_requirements"].append({
            "capability_id": "project.read", "operation_id": "inspect_git_status",
            "purpose": "Git evidence", "required_evidence": ["git_status"],
            "effect_type": "OBSERVE", "target_scope": "project", "reversibility": "REVERSIBLE",
            "external_side_effect": False, "risk_class": "READ_ONLY", "required": True,
        })
        return verified_model_output(json.dumps(payload, ensure_ascii=False))

    result = run(understand, text="ответь и проверь git", final=final)
    assert result["selected_capabilities"] == ("conversation.respond", "project.read")
    assert result["selected_provider_operation"] == ("respond", "inspect_git_status")
    assert {item["kind"] for item in result["evidence_bundle"]["items"]} == {
        "identity_facts", "bounded_session_context", "git_status",
    }
    assert result["evidence_bundle"]["capability_ids"] == ("conversation.respond", "project.read")
    assert len(result["permission_decision"]) == 2
    assert all(item["granted"] for item in result["permission_decision"])
    assert all(item["permissions_granted"] for item in final.calls[0]["capability_state"])
    assert result["trace_id"] == result["trace"]["trace_id"]


def test_missing_required_evidence_replans_once_and_never_calls_final_brain():
    class MissingProject(Project):
        def collect_evidence(self, understanding, plan, trace_id, deadline=None):
            self.calls.append(plan)
            return EvidenceBundle(understanding.request_id, "project.read", trace_id, "UNAVAILABLE", (),
                                  ("required evidence unavailable",), (), ("git_status:unavailable",))

    model_calls = []
    final = Final()

    def understand(_, user):
        model_calls.append(user)
        return model_payload(user, "project.read", ("inspect_git_status",))

    result = run(understand, project=MissingProject(), final=final)
    assert len(model_calls) == 2
    assert result["operation_status"] == "PARTIAL_EVIDENCE"
    assert result["missing_evidence"] == ("git_status",)
    assert result["response_text"]
    assert final.calls == []
    assert result["trace"]["final_brain_status"] == "NOT_CALLED"


def test_structured_safety_uses_typed_understanding_without_rewriting_intent():
    result = run(lambda _, user: model_payload(user, "project.files.write", ("write_file",), effect="MUTATE"))
    assert result["understanding"]["effect_type"] == "MUTATE"
    assert result["understanding"]["risk_class"] == "MUTATION"
    safety = result["safety_validation"]
    assert safety["intent_rewritten"] is False
    assert safety["raw_text_inspected"] is False
    assert safety["approval_decision_deferred_to_step_policy"] is True


def test_inconsistent_understanding_gets_one_model_backed_contract_repair() -> None:
    calls = []

    def understand(system, user):
        calls.append(system)
        if len(calls) == 1:
            payload = model_payload(user, "conversation.respond", ("respond",), effect="MUTATE")
            raw = json.loads(payload["content"])
            raw["risk_class"] = "READ_ONLY"
            raw["operation_requirements"][0]["risk_class"] = "READ_ONLY"
            payload["content"] = json.dumps(raw, ensure_ascii=False)
            return payload
        return model_payload(user, "conversation.respond", ("respond",), effect="OBSERVE")

    result = run(understand, text="обычный разговор")

    assert len(calls) == 2
    assert "Repair typed violations" in calls[1]
    assert "top_level_cannot_hide_side_effect_as_read_only" in calls[1]
    assert result["understanding_repair_succeeded"] is True
    assert result["operation_status"] == "COMPLETE"
    assert result["trace"]["final_brain_status"] == "COMPLETE"


def test_inconsistent_understanding_fails_closed_after_one_failed_repair() -> None:
    calls = []

    def understand(_, user):
        calls.append(user)
        payload = model_payload(user, "project.read", ("inspect_git_status",), effect="MUTATE")
        return payload

    result = run(understand, text="проверь проект")

    assert len(calls) == 2
    assert result["operation_status"] == "SAFETY_VALIDATION_FAILED"
    assert result["understanding_repair_succeeded"] is False
    assert result["trace"]["final_brain_status"] == "NOT_CALLED"


def test_prompt_has_no_request_specific_operation_hint_before_manifest_catalog():
    system, _ = spine.build_request_understanding_prompt(
        request_id="request_test", original_text="новая формулировка",
        identity=IdentityContext("anonymous", "http_unverified", "unknown", False, False),
        session_context={},
    )
    instructions = system.split("CATALOG=", 1)[0]
    for forbidden in (
        "working-tree", "working tree", "git_status", "changed_files", "diff_summary",
        "conversation.respond", "project.read", "inspect_structure",
    ):
        assert forbidden not in instructions


def test_step_policy_preserves_owner_low_risk_reversible_autonomy():
    policy = SemanticPolicyEvaluator()
    owner = IdentityContext("aleksandr", "local_terminal_session", "owner", True, True, "Александр")
    decision = policy.evaluate(
        capability_id="pc.control", operation_id="owner_low_risk_action", effect_type="MUTATE",
        target_scope="owner_desktop", reversibility="REVERSIBLE", external_side_effect=False,
        risk_class="MUTATION", identity=owner, trace_id="trace-owner",
    )
    assert decision.granted is True
    assert decision.approval_required is False


def test_step_policy_separates_dangerous_approval_and_anonymous_denial():
    policy = SemanticPolicyEvaluator()
    owner = IdentityContext("aleksandr", "local_terminal_session", "owner", True, True, "Александр")
    anonymous = IdentityContext("anonymous", "http_unverified", "unknown", False, False)
    dangerous = policy.evaluate(
        capability_id="pc.control", operation_id="irreversible_action", effect_type="EXECUTE",
        target_scope="owner_desktop", reversibility="IRREVERSIBLE", external_side_effect=True,
        risk_class="DANGEROUS", identity=owner, trace_id="trace-dangerous",
    )
    untrusted = policy.evaluate(
        capability_id="pc.control", operation_id="owner_low_risk_action", effect_type="MUTATE",
        target_scope="owner_desktop", reversibility="REVERSIBLE", external_side_effect=False,
        risk_class="MUTATION", identity=anonymous, trace_id="trace-anonymous",
    )
    assert dangerous.granted is False and dangerous.approval_required is True
    assert untrusted.granted is False and untrusted.approval_required is False


def test_canonical_family_resolver_reports_owner_pc_eligibility_truthfully():
    owner = resolve_family_profile(identity_id="aleksandr", profile_type="owner")
    family = resolve_family_profile(identity_id="yulia", profile_type="trusted_family")
    child = resolve_family_profile(identity_id="maksim", profile_type="child")
    assert owner is not None and owner.direct_pc_action_eligible is True
    assert family is not None and family.direct_pc_action_eligible is False
    assert child is not None and child.direct_pc_action_eligible is False


def test_active_hot_path_has_no_legacy_phrase_or_marker_router():
    api_source = Path("CONTROL_PLANE/api_server.py").read_text(encoding="utf-8")
    canonical_source = Path("CONTROL_PLANE/canonical_semantic_spine.py").read_text(encoding="utf-8")
    assert "handle_hot_request" not in api_source
    assert "is_protected_mutation(text)" not in api_source
    tree = ast.parse(canonical_source)
    assert not any(
        isinstance(node, ast.ImportFrom) and node.module and "live_intent" in node.module
        for node in ast.walk(tree)
    )
    for forbidden in ("phrase_map", "marker_map", "token_score", "deterministic_fallback"):
        assert forbidden not in canonical_source


def test_reachable_hot_symbol_graph_excludes_legacy_semantic_routers():
    symbols = {
        "CONTROL_PLANE/api_server.py": ("jarvis_live_hot", "_payload_text", "_payload_session_id"),
        "CONTROL_PLANE/canonical_semantic_spine.py": (
            "run_canonical_semantic_turn", "build_request_understanding_prompt", "load_operation_catalog",
            "operation_contract", "_understand", "_operation_resolution_error", "_execute_evidence",
            "_trace", "_failure", "_degraded_response",
        ),
        "MAKSIMAR_CORE_LIB/security_layer/semantic_policy.py": (
            "identity_context_from_http_payload", "validate_structured_safety",
        ),
        "MAKSIMAR_CORE_LIB/security_layer/jarvis_speaker_profile_resolver.py": ("resolve_family_profile",),
        "MAKSIMAR_CORE_LIB/capability_registry/capability_registry_loader.py": (
            "load_capability_manifests", "discover_capability_providers",
        ),
        "MAKSIMAR_SERVER/AI_ORCHESTRATION/ollama_transport.py": ("grounded_final_brain_call", "ollama_post_json"),
    }
    forbidden = (
        "handle_hot_request", "live_intent_policy", "protected_mutation_gate",
        "autonomous_tool_model_router", "deterministic_fallback", "phrase_map",
        "marker_map", "token_score", "regex_intent",
    )
    checked = []
    for filename, names in symbols.items():
        source = Path(filename).read_text(encoding="utf-8")
        tree = ast.parse(source)
        nodes = {node.name: node for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
        for name in names:
            assert name in nodes, f"missing active graph symbol: {filename}:{name}"
            segment = ast.get_source_segment(source, nodes[name]) or ""
            assert not any(value in segment for value in forbidden), f"forbidden router reachable in {filename}:{name}"
            checked.append(f"{filename}:{name}")
    adapter_source = Path("MAKSIMAR_SERVER/AI_ORCHESTRATION/jarvis_live_brain_loop_server_adapter.py").read_text(encoding="utf-8")
    adapter_tree = ast.parse(adapter_source)
    adapter_class = next(node for node in adapter_tree.body if isinstance(node, ast.ClassDef) and node.name == "ExistingFinalBrainAdapter")
    answer = next(node for node in adapter_class.body if isinstance(node, ast.FunctionDef) and node.name == "answer")
    answer_source = ast.get_source_segment(adapter_source, answer) or ""
    assert "grounded_final_brain_call" in answer_source
    assert "_brain_loop" not in answer_source
    active_dependency_modules = (
        "CONTROL_PLANE/canonical_semantic_spine.py",
        "MAKSIMAR_SERVER/AI_ORCHESTRATION/model_understanding_adapter.py",
        "MAKSIMAR_SERVER/AI_ORCHESTRATION/project_understanding_adapter.py",
        "MAKSIMAR_SERVER/AI_ORCHESTRATION/conversation_evidence_adapter.py",
        "MAKSIMAR_SERVER/AI_ORCHESTRATION/session_memory_store.py",
        "MAKSIMAR_SERVER/AI_ORCHESTRATION/ollama_transport.py",
        "MAKSIMAR_CORE_LIB/security_layer/semantic_policy.py",
        "MAKSIMAR_CORE_LIB/capability_registry/capability_registry_loader.py",
    )
    for filename in active_dependency_modules:
        source = Path(filename).read_text(encoding="utf-8")
        assert not any(value in source for value in forbidden), f"forbidden router import/source in {filename}"
    assert len(checked) >= 20


def test_real_git_evidence_reports_branch_changes_sources_timestamp_and_trace():
    operations = ("inspect_git_status", "inspect_changed_files", "inspect_diff_summary")
    result = run(
        lambda _, user: model_payload(user, "project.read", operations, topic="working tree"),
        text="проверь фактическое состояние рабочего дерева",
        project=ExistingProjectUnderstandingAdapter(),
    )
    items = {
        item["kind"]: item for item in result["evidence_bundle"]["items"]
        if item["capability_id"] == "project.read"
    }
    assert set(items) == {"git_status", "changed_files", "diff_summary"}
    status = json.loads(items["git_status"]["observation"])
    changed = json.loads(items["changed_files"]["observation"])
    diff = json.loads(items["diff_summary"]["observation"])
    assert status["branch"]
    assert {"modified_files", "deleted_files", "untracked_files", "staged_files"} <= set(status)
    assert changed["source_commands"] and changed["observed_at"]
    assert {"diff_name_status", "diff_stat", "cached_diff_stat"} <= set(diff)
    assert all(item["source_reference"].startswith("project://inspect_") for item in items.values())
    assert all(item["observed_at"] and item["trace_id"] == result["trace_id"] for item in items.values())
    assert result["missing_evidence"] == ()


def test_project_provider_uses_shared_turn_deadline_instead_of_local_eight_second_owner(monkeypatch):
    import MAKSIMAR_SERVER.AI_ORCHESTRATION.project_understanding_adapter as adapter_module

    observed_timeouts = []

    class ImmediateFuture:
        def __init__(self, operation):
            self.operation = operation

        def result(self, timeout=None):
            observed_timeouts.append(timeout)
            return self.operation()

    class ImmediateExecutor:
        def __init__(self, **_):
            pass

        def submit(self, operation):
            return ImmediateFuture(operation)

        def shutdown(self, **_):
            pass

    monkeypatch.setattr(adapter_module, "ThreadPoolExecutor", ImmediateExecutor)
    monkeypatch.setattr(
        ExistingProjectUnderstandingAdapter,
        "_inspect_architecture",
        staticmethod(lambda: {"blueprint_id": "fixture", "failed": False, "violations": ()}),
    )
    result = run(
        lambda _, user: model_payload(
            user, "project.read", ("inspect_architecture",), topic="architecture",
        ),
        text="проверь архитектурный отчёт",
        project=ExistingProjectUnderstandingAdapter(),
    )

    assert result["operation_status"] == "COMPLETE"
    assert observed_timeouts and observed_timeouts[0] > 8.0


def test_legacy_project_catalog_does_not_admit_unrelated_memory_instructions():
    system, user = spine.build_request_understanding_prompt(
        request_id="legacy-budget-test", original_text="probe",
        identity=IdentityContext("owner", "local_terminal_session", "owner", True, True),
        session_context={}, registry_projection=None,
    )
    assert "memory_filter: HISTORY" not in system
    assert "CANONICAL_GOAL memory_filter" not in system
    measured = spine.require_prompt_budget(
        system + " Repair typed violations; preserve intent and copy exact source spans: unknown_operation",
        user, reserved_output_tokens=spine.REQUEST_UNDERSTANDING_RESERVED_OUTPUT_TOKENS,
        output_schema=spine.request_understanding_schema_for_projection(None, source_text="probe"),
        num_ctx=spine.REQUEST_UNDERSTANDING_NUM_CTX,
    )
    assert measured["within_budget"]
