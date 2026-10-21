from __future__ import annotations

from MAKSIMAR_SERVER.SKILL_ADAPTER_REGISTRY.existing_capability_inventory import (
    build_existing_capability_catalog,
)
from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import (
    CapabilityRequirement, ExecutionPlan, Goal, PlanStep, RequestUnderstanding,
)


def test_restored_memory_dialogue_keeps_context_inside_real_understanding_budget():
    from CONTROL_PLANE import canonical_semantic_spine as spine
    from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import IdentityContext
    from MAKSIMAR_SERVER.SKILL_ADAPTER_REGISTRY.existing_capability_inventory import build_semantic_capability_registry_projection
    projection = build_semantic_capability_registry_projection()
    details = spine.select_semantic_projection_details(projection, ("mempalace_search",))
    context = {"bounded_chronological_turns": tuple({
        "user_text": "Найди документ с правилами владельца. " * 5,
        "assistant_text": "Найден документ POLICY.md в /project/docs/POLICY.md. " * 5,
        "topic": "memory provenance",
    } for _ in range(2)), "truncated": True, "omitted_turn_count": 4}
    text = "Какой документ ты только что нашёл? Назови его и путь."
    prompt = spine.build_request_understanding_prompt(request_id="restart_budget",
        original_text=text, identity=IdentityContext("owner", "local_terminal_session", "owner", True, True),
        session_context=context, registry_projection=details)
    budget = spine.measure_prompt_budget(*prompt,
        reserved_output_tokens=spine.REQUEST_UNDERSTANDING_RESERVED_OUTPUT_TOKENS,
        output_schema=spine.request_understanding_schema_for_projection(details, source_text=text),
        num_ctx=spine.REQUEST_UNDERSTANDING_NUM_CTX)
    assert budget["within_budget"] is True
    assert "POLICY.md" in prompt[1]
    assert "logical_spec is" not in prompt[0]
    assert "Typed memory_filter" not in prompt[0]
    assert spine.REQUEST_UNDERSTANDING_RESERVED_OUTPUT_TOKENS == spine.REQUEST_UNDERSTANDING_NUM_PREDICT


def test_goalframe_identifiers_are_opaque_labels_not_source_paths():
    from CONTROL_PLANE import canonical_semantic_spine as spine
    for role in ("PRIMARY_OUTCOME", "SUBGOAL"):
        fields = spine._goalframe_item_schema(role)["properties"]
        assert fields["goal_id"]["enum"] == ["g1", "g2", "g3", "g4"]
        if role == "SUBGOAL":
            assert fields["parent_goal_id"]["enum"] == fields["goal_id"]["enum"]


def test_operation_discovery_reserves_the_actual_structured_output(monkeypatch):
    from CONTROL_PLANE import canonical_semantic_spine as spine
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.model_understanding_adapter import ExistingOllamaModelUnderstandingAdapter
    from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import RequestDeadline
    schema = {"properties":{"selection_justifications":{}}}
    adapter = ExistingOllamaModelUnderstandingAdapter(json_schema={}, candidate_json_schema=schema)
    calls = []
    monkeypatch.setattr(adapter, "_main_model_call", lambda **kwargs:calls.append(kwargs) or {})
    adapter.discover_candidates(system_prompt="typed operation selection", user_prompt="request",
                               deadline=RequestDeadline(10), output_schema=schema)
    assert calls[0]["num_predict"] == spine.OPERATION_DISCOVERY_RESERVED_OUTPUT_TOKENS
    assert calls[0]["num_ctx"] == spine.SEMANTIC_SELECTION_NUM_CTX


def test_enterprise_examples_and_empty_vector_directory_do_not_claim_live_data(monkeypatch, tmp_path):
    import json
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import memory_context_sources as sources
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.memory_retrieval_adapter import _contract_memory_preview, build_enterprise_memory_preview
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.ollama_transport import _bounded_observation
    monkeypatch.setattr(sources, "RUNTIME_VECTOR_INDEX_ROOT", tmp_path)
    surfaces = {item["surface_id"]:item for item in sources._build_memory_surface_inventory()}
    assert surfaces["vector_runtime_indexes"]["status"] == "not_connected"
    assert surfaces["enterprise_business_memory"]["persisted_dataset_available"] is False
    assert surfaces["regulatory_memory_foundation"]["runtime_status"] == "CONTRACT_PREVIEW"
    projection = _bounded_observation("enterprise_business_memory",
        json.dumps(_contract_memory_preview(build_enterprise_memory_preview)))
    assert projection["contract_examples_only"] is True
    assert projection["persisted_dataset_available"] is False
    assert projection["data_status"] == "NOT_CONFIGURED"
    assert projection["contract_flow"]


def test_memory_and_retrieval_capabilities_are_visible_in_existing_inventory() -> None:
    catalog = build_existing_capability_catalog()
    memory_ids = {item["capability_id"] for item in catalog["memory_tools"]}
    retrieval_ids = {item["capability_id"] for item in catalog["retrieval_tools"]}

    assert "session_memory" in memory_ids
    assert "runtime_history_store" in memory_ids
    assert "memory_engine_registry" in memory_ids
    assert "mempalace_search" in memory_ids
    assert len(retrieval_ids) >= 1


def test_failed_real_mempalace_search_has_no_authoritative_receipt(monkeypatch) -> None:
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import memory_retrieval_adapter as adapter_module

    monkeypatch.setattr(adapter_module, "_run_mempalace_search", lambda query: {
        "query": query, "returncode": 1, "stdout": "No palace found", "stderr": "",
    })
    understanding = RequestUnderstanding(
        request_id="mempalace_test", original_text="search external memory for semantic spine", language="en",
        goals=(Goal("g1", "retrieve external memory"),),
        required_capabilities=(CapabilityRequirement("mempalace_search", "retrieve", True),),
        effect_type="OBSERVE", target_scope="local_memory_runtime", reversibility="REVERSIBLE",
        external_side_effect=False, unresolved_capabilities=(), operation_requirements=(),
        current_topic="memory", unresolved_reference="", relevant_context_trace_ids=(),
        risk_class="READ_ONLY", confidence=1.0, reason_codes=("typed_test",),
    )
    step = PlanStep(
        step_id="memory", goal_id="g1", capability_id="mempalace_search", operation="search_mempalace",
        required_evidence=("mempalace_search",), effect_type="OBSERVE", target_scope="local_memory_runtime",
        reversibility="REVERSIBLE", external_side_effect=False, risk_class="READ_ONLY",
        parameters=(("query", "semantic spine"),),
    )
    bundle = adapter_module.ExistingMemoryRetrievalAdapter().collect_evidence(
        understanding, ExecutionPlan(request_id="mempalace_test", steps=(step,)), "trace_memory",
    )
    assert bundle.status == "UNAVAILABLE"
    assert bundle.items == ()
    assert bundle.receipts == ()
    assert "No palace found" in bundle.errors[0]


def test_external_memory_search_is_reachable_from_both_semantic_retrieval_domains():
    from CONTROL_PLANE.canonical_semantic_spine import _goalframe_projection
    from MAKSIMAR_SERVER.SKILL_ADAPTER_REGISTRY.existing_capability_inventory import build_semantic_capability_registry_projection
    registry = build_semantic_capability_registry_projection()
    for domain in ("memory", "retrieval"):
        candidates = _goalframe_projection(registry, semantic_domain=domain, effect_intent="retrieve")
        assert "mempalace_search" in candidates
        assert "open_project_workbench" not in candidates


def test_document_source_and_text_survive_final_brain_prompt_compaction():
    import json
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    source_text = "Owner authorization is identity resolver plus trusted session policy. " * 16
    observation = {"palace": "/home/owner/.mempalace", "retrieval": {"query": "owner policy",
        "results": [{"text": source_text, "source_file": "POLICY.md", "wing": "architecture",
        "source_readback": [{"path": "/project/docs/POLICY.md", "sha256": "a" * 64}],
        "distance": 0.2}]}, "derived_index_only": True, "runtime_authority": False}
    payload = transport._grounded_final_brain_payload(original_text="Найди правила владельца через Mempalace",
        understanding={"goals": (), "operation_requirements": ()},
        execution_plan={"steps": ()}, capability_state=(), identity_facts={}, session_context={},
        evidence_bundle={"status": "COMPLETE", "items": [{"kind": "mempalace_search",
        "observation": json.dumps(observation)}], "receipts": ()}, stream=False)
    prompt = "".join(message["content"] for message in payload["messages"])
    assert "Owner authorization is identity resolver plus trusted session policy" in prompt
    assert "/project/docs/POLICY.md" in prompt
    assert '"runtime_authority":false' in prompt
    assert transport._final_brain_prompt_budget(payload)["within_budget"] is True


def test_large_retrieval_compaction_preserves_structured_provenance_and_marks_excerpt():
    import json
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.ollama_transport import _bounded_evidence_items_for_prompt
    value = {"results": [{"text": "retrieved source excerpt " * 400,
        "source_readback": [{"path": "/project/POLICY.md", "drawer_id": "drawer_native_id",
                             "indexed_sha256": "a" * 64, "sha256": "b" * 64, "freshness": "STALE"}]}]}
    bounded = _bounded_evidence_items_for_prompt((("mempalace_search", value),), aggregate_character_limit=1500)
    hit = bounded[0][1]["results"][0]
    assert hit["source_readback"] == value["results"][0]["source_readback"]
    assert hit["excerpt_truncated"] is True
    assert hit["text"].startswith("retrieved source excerpt")
    assert "grounded_excerpt" not in bounded[0][1]
    assert len(json.dumps(bounded[0][1], separators=(",", ":"))) <= 1500


def test_final_memory_map_and_jarvis_share_live_child_archive_owner(monkeypatch):
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import memory_context_sources as sources
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.jarvis_live_read_models import build_jarvis_live_memory_federation_status
    from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.final_memory_map.final_memory_preview_builder import build_final_memory_preview
    health = {"status": "ENVIRONMENT_BLOCKED", "storage_path": "/test/chroma.sqlite3", "freshness": "STALE", "duplicate_chunk_count": 0,
              "logical_role": "AUXILIARY_PROJECT_DOCUMENT_REFERENCE_RETRIEVAL",
              "native_memory_authority": {role: False for role in ("business", "regulatory", "session", "experience", "evidence", "learning", "skills", "user", "device")}}
    monkeypatch.setattr(sources, "_mempalace_live_read_model", lambda: dict(health))
    jarvis = build_jarvis_live_memory_federation_status()
    dashboard = build_final_memory_preview()
    child = next(s for s in jarvis["surfaces"] if s["surface_id"] == "mempalace_search")
    assert dashboard["mempalace"] == child["health"]
    assert dashboard["mempalace"]["status"] == "ENVIRONMENT_BLOCKED"
    node = next(n for n in dashboard["graph"]["nodes"] if n["node_id"] == "mempalace_search")
    assert node["runtime_status"] == "ENVIRONMENT_BLOCKED"
    assert node["classification"] == "CHILD_BACKEND"
    assert node["node_ready"] is True  # definition readiness never claims store health
    assert dashboard["canonical_write_allowed"] is False


def test_live_health_counts_survive_budget_with_many_view_descriptions():
    import json
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.ollama_transport import _bounded_observation, _bounded_evidence_items_for_prompt
    observation = {"federation": {"memory_surfaces_detected_count":11, "physical_store_count":2,
        "live_physical_store_count":2, "runtime_history_store_exists":True,
        "physical_stores":[{"path":"/project/history.jsonl","owner":"CanonicalSessionContextStore"},
                           {"path":"/home/owner/.mempalace/chroma.sqlite3","owner":"ExistingMemoryRetrievalAdapter"}],
        "surfaces":[{"surface_id":"existing_memory_surface_"+str(i),"classification":"READ_MODEL","runtime_status":"READ_MODEL_ONLY"} for i in range(9)]},
        "mempalace":{"status":"LIVE_READ_ONLY","freshness":"FRESH","drawer_count":45,
                     "source_count":17,"duplicate_chunk_count":0,"storage_path":"/home/owner/.mempalace/chroma.sqlite3"}}
    projected = _bounded_observation("memory_federation", json.dumps(observation))
    bounded = _bounded_evidence_items_for_prompt((("memory_federation",projected),))
    assert bounded[0][0] == "memory_federation"
    assert bounded[0][1]["physical_store_count"] == 2
    assert bounded[0][1]["mempalace"]["source_count"] == 17
    assert bounded[0][1]["mempalace"]["duplicate_chunk_count"] == 0
    assert bounded[0][1]["omitted_registered_views"] == 2


def test_native_refresh_source_boundary_rejects_non_document_and_escape(monkeypatch, tmp_path):
    import pytest
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import memory_retrieval_adapter as adapter
    monkeypatch.setattr(adapter, "PROJECT_ROOT", tmp_path)
    docs = tmp_path / "docs"
    docs.mkdir()
    source = docs / "CANON.md"
    source.write_text("canonical existing source")
    assert adapter._mempalace_refresh_source(str(source)) == source
    for path in (tmp_path / "private.md", docs / "settings.json", docs / "missing.md"):
        with pytest.raises(ValueError):
            adapter._mempalace_refresh_source(str(path))
    outside = tmp_path / "outside.md"
    outside.write_text("not reviewed documentation")
    link = docs / "escape.md"
    link.symlink_to(outside)
    with pytest.raises(ValueError):
        adapter._mempalace_refresh_source(str(link))


def test_native_refresh_has_mutation_policy_and_requires_verified_effect(monkeypatch):
    import json
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import memory_retrieval_adapter as adapter
    from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import IdentityContext
    from MAKSIMAR_CORE_LIB.security_layer.semantic_policy import SemanticPolicyEvaluator
    contract = next(c for c in adapter.MEMORY_CAPABILITY_OPERATION_CONTRACTS["mempalace_search"]
                    if c["operation_id"] == "refresh_mempalace_source")
    assert contract["effect_type"] == "MUTATE" and contract["risk_class"] == "MUTATION"
    policy = SemanticPolicyEvaluator()
    kwargs = {k:contract[k] for k in ("operation_id", "risk_class", "effect_type", "target_scope", "reversibility", "external_side_effect")}
    anonymous = IdentityContext("anonymous", "http_unverified", "unknown", False, False)
    assert policy.evaluate(capability_id="mempalace_search", identity=anonymous, trace_id="refresh", **kwargs).granted is False
    understanding = RequestUnderstanding(request_id="refresh", original_text="Refresh the existing document index",
        language="en", goals=(Goal("g1", "refresh derived index"),),
        required_capabilities=(CapabilityRequirement("mempalace_search", "refresh", True),),
        effect_type="MUTATE", target_scope="local_memory_runtime", reversibility="REVERSIBLE",
        external_side_effect=False, unresolved_capabilities=(), operation_requirements=(), current_topic="memory",
        unresolved_reference="", relevant_context_trace_ids=(), risk_class="MUTATION", confidence=1.0, reason_codes=())
    step = PlanStep(step_id="refresh", goal_id="g1", capability_id="mempalace_search", operation="refresh_mempalace_source",
        required_evidence=("mempalace_index_refresh",), effect_type="MUTATE", target_scope="local_memory_runtime",
        reversibility="REVERSIBLE", external_side_effect=False, risk_class="MUTATION",
        parameters=(("source_path", "/project/docs/CANON.md"),))
    plan = ExecutionPlan(request_id="refresh", steps=(step,))
    monkeypatch.setattr(adapter, "_run_mempalace_refresh", lambda path: {"returncode":0,"effect_readback_verified":False})
    failed = adapter.ExistingMemoryRetrievalAdapter().collect_evidence(understanding, plan, "refresh_trace")
    assert failed.status == "UNAVAILABLE" and not failed.receipts
    monkeypatch.setattr(adapter, "_run_mempalace_refresh", lambda path: {
        "returncode":0,"effect_readback_verified":True,"source_path":path,"freshness":"FRESH"})
    completed = adapter.ExistingMemoryRetrievalAdapter().collect_evidence(understanding, plan, "refresh_trace")
    assert completed.status == "COMPLETE" and completed.receipts[0].operation_id == "refresh_mempalace_source"
    assert json.loads(completed.items[0].observation)["effect_readback_verified"] is True


def test_file_source_facts_and_path_survive_final_brain_prompt_compaction():
    import json
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    observation = {"path": "docs/current_scope.md", "allowed": True, "read_only": True,
        "start_line": 1, "end_line": 30, "page": 1, "line_count": 30,
        "snippet": ["1: # Current scope", "2: Track: RECOVERY_ALPHA",
            "3: Phase: P2 / Phase 1B; P3 is pending owner acceptance."] +
            [f"{n}: Existing architecture context " + "x" * 120 for n in range(4, 31)]}
    payload = transport._grounded_final_brain_payload(original_text="Read the current track and phase from the source",
        understanding={"goals": (), "operation_requirements": ()},
        execution_plan={"steps": ()}, capability_state=(), identity_facts={}, session_context={},
        evidence_bundle={"status": "COMPLETE", "items": [{"kind": "file_snippet",
        "observation": json.dumps(observation)}], "receipts": ()}, stream=False)
    prompt = "".join(message["content"] for message in payload["messages"])
    assert "docs/current_scope.md" in prompt
    assert "RECOVERY_ALPHA" in prompt
    assert "P2 / Phase 1B; P3 is pending owner acceptance." in prompt
    assert '\"excerpt_truncated\":true' in prompt
    assert transport._final_brain_prompt_budget(payload)["within_budget"] is True


def test_memory_provenance_stays_available_without_mandatory_full_record_dump():
    import json
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    record = {"experience_id": "devexp_proved", "observed_at": "2026-10-11T16:00:00Z",
        "verification_status": "VERIFIED", "review_status": "EXECUTION_RECEIPTS_VERIFIED",
        "trace_id": "trace_proved", "session_id": "session_proved", "review_ref": "receipt://proved",
        "evidence_refs": ["evidence://proved"], "execution_receipt_refs": ["proved:step_1"],
        "task_ref": "Refresh the existing derived archive index"}
    payload = transport._grounded_final_brain_payload(original_text="What verified work and evidence?",
        understanding={"goals": (), "operation_requirements": ()}, execution_plan={"steps": ()},
        capability_state=(), identity_facts={}, session_context={}, evidence_bundle={"status": "COMPLETE",
        "items": [{"kind": "history_search", "observation": json.dumps({"history_query": {
        "query_kind": "VERIFIED_EXPERIENCE", "match_count": 1, "matches": [record]}})}], "receipts": ()}, stream=False)
    prompt = "".join(message["content"] for message in payload["messages"])
    for value in record.values():
        if isinstance(value, str): assert value in prompt
    assert "only requested provenance fields" in prompt or "only the requested provenance fields" in prompt
    assert payload["options"]["num_predict"] == 512
    assert payload["options"]["num_ctx"] == transport.OLLAMA_FAST_CHAT_NUM_CTX
    assert "first describe the concrete work in task_ref" in payload["messages"][-1]["content"]
    assert "every supplied provenance field" not in prompt
    assert transport._final_brain_prompt_budget(payload)["within_budget"] is True


def test_long_history_proof_is_not_dropped_for_duplicate_context_metadata():
    import json
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    trace = "activation_" + "native_refresh_" * 3 + "trace"
    record = {"experience_id": "devexp_" + "a" * 24, "trace_id": trace,
        "session_id": trace[:-6], "observed_at": "2026-10-11T16:58:17Z",
        "created_at": "2026-10-11T16:58:17Z", "persisted_at": "2026-10-11T16:58:23Z",
        "timestamp_status": "KNOWN", "verification_status": "VERIFIED",
        "review_status": "EXECUTION_RECEIPTS_VERIFIED", "review_ref": "receipt://" + trace + ":step_1",
        "evidence_refs": ["evidence://" + trace + "/step_1/sha256:" + "b" * 64],
        "provenance_refs": ["trace://" + trace, "audit_verdict=EXECUTION_RECEIPTS_VERIFIED"],
        "execution_receipt_refs": [trace + ":step_1", trace + ":step_2:final_brain"],
        "learning_bundle_id": "bundle_devexp_" + "a" * 24, "learning_bundle_hash": "sha256:" + "c" * 64,
        "task_ref": "Update the existing derived archive from source bytes. " * 6,
        "experience_kind": "INTEGRATION", "artifact_kind": "provider_execution_experience"}
    evidence = {"status": "COMPLETE", "items": [
        {"kind": "history_search", "observation": json.dumps({"history_query": {
            "query_kind": "VERIFIED_EXPERIENCE", "time_basis": "TODAY_UTC", "match_count": 15,
            "matches": [record]}})},
        {"kind": "identity_facts", "observation": json.dumps({"identity_id": "owner"})},
        {"kind": "bounded_session_context", "observation": json.dumps({"context": "x" * 1000})}], "receipts": ()}
    payload = transport._grounded_final_brain_payload(original_text="Show verified work and its evidence",
        understanding={"goals": (), "operation_requirements": ()}, execution_plan={"steps": ()},
        capability_state=(), identity_facts={"identity_id": "owner"}, session_context={},
        evidence_bundle=evidence, stream=False)
    prompt = "".join(message["content"] for message in payload["messages"])
    for field in ("trace_id", "session_id", "observed_at", "review_ref", "learning_bundle_id", "learning_bundle_hash"):
        assert record[field] in prompt
    for field in ("evidence_refs", "execution_receipt_refs"):
        assert all(value in prompt for value in record[field])
    assert "Update the existing derived archive" in prompt
    assert transport._final_brain_prompt_budget(payload)["within_budget"] is True


def test_recorded_task_is_never_cut_into_a_fake_source_path():
    import json
    import pytest
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    path = "/home/owner/project/docs/architecture/" + "long_canonical_name_" * 6 + ".md"
    record = {"experience_id": "devexp_source", "observed_at": "2026-10-11T16:00:00Z",
        "verification_status": "VERIFIED", "review_status": "EXECUTION_RECEIPTS_VERIFIED",
        "task_ref": "Update the derived index of " + path + " without changing source bytes.",
        "evidence_refs": ["evidence://source"], "execution_receipt_refs": ["trace:step_1"]}
    def payload():
        return transport._grounded_final_brain_payload(original_text="What work was done?",
            understanding={"goals": (), "operation_requirements": ()}, execution_plan={"steps": ()},
            capability_state=(), identity_facts={}, session_context={}, evidence_bundle={"status": "COMPLETE",
            "items": [{"kind": "history_search", "observation": json.dumps({"history_query": {
            "query_kind": "VERIFIED_EXPERIENCE", "match_count": 1, "matches": [record]}})}], "receipts": ()}, stream=False)
    prompt = "".join(message["content"] for message in payload()["messages"])
    assert path in prompt
    assert record["task_ref"] in prompt
    record["task_ref"] += " Long original task." * 200
    with pytest.raises(ValueError, match="primary_history_evidence_exceeds_prompt_budget"):
        payload()


def test_oversized_primary_history_returns_transport_failure_without_model_call(monkeypatch):
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    def unavailable(**kwargs):
        raise ValueError("primary_history_evidence_exceeds_prompt_budget")
    def must_not_call(*args, **kwargs):
        raise AssertionError("No model call may occur without primary evidence")
    monkeypatch.setattr(transport, "_grounded_final_brain_payload", unavailable)
    monkeypatch.setattr(transport, "ollama_post_json", must_not_call)
    inputs = dict(original_text="Retrieve work", understanding={}, execution_plan={},
        evidence_bundle={}, capability_state=())
    result = transport.grounded_final_brain_call(**inputs)
    assert result["error"] == "primary_history_evidence_exceeds_prompt_budget"
    assert result["ok"] is False and result["model_call_attempted"] is False
    events = list(transport.grounded_final_brain_stream(**inputs))
    assert len(events) == 1 and events[0]["event"] == "error"
    assert events[0]["error_kind"] == result["error"]
    assert events[0]["model_call_attempted"] is False


def test_positive_current_history_result_cannot_be_shadowed_by_past_assistant_failure():
    import json
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    record = {"user_text": "Read my earlier actual question", "assistant_text": "No records found",
        "persisted_at": "2026-10-11T22:35:22Z"}
    payload = transport._grounded_final_brain_payload(original_text="Show an earlier question and its saved time",
        understanding={"goals": (), "operation_requirements": ()}, execution_plan={"steps": ()},
        capability_state=(), identity_facts={}, session_context={}, evidence_bundle={"status": "COMPLETE",
        "items": [{"kind": "history_search", "observation": json.dumps({"history_query": {
        "query_kind": "HISTORY", "match_count": 24, "matches": [record]}})}], "receipts": ()}, stream=False)
    current = payload["messages"][-1]["content"]
    assert '\"current_history_match_count\":24' in current
    assert record["user_text"] in current and record["persisted_at"] in current
    assert "A past assistant_text failure" in current
    assert "No records found" not in current
    assert transport._final_brain_prompt_budget(payload)["within_budget"] is True


def test_same_live_memory_owner_survives_both_existing_evidence_envelopes():
    import json
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    child = {"status": "LIVE_READ_ONLY", "logical_role": "AUXILIARY_PROJECT_DOCUMENT_REFERENCE_RETRIEVAL",
        "native_memory_authority": {"business": False, "regulatory": False, "session": False},
        "freshness": "FRESH", "drawer_count": 12, "source_count": 3, "duplicate_chunk_count": 0,
        "storage_path": "/native/palace/chroma.sqlite3"}
    federation = {"memory_surfaces_detected_count": 1, "physical_store_count": 1,
        "live_physical_store_count": 1, "physical_stores": ({"path": child["storage_path"]},),
        "surfaces": ({"surface_id": "mempalace_search", "classification": "CHILD_BACKEND",
            "runtime_status": "LIVE_READ_ONLY", "health": child},),
        "canonical_session_health": {"status": "LIVE_READ_ONLY", "record_count": 7}}
    direct = transport._bounded_observation("memory_federation", json.dumps({"memory_federation": federation}))
    aggregate = transport._bounded_observation("memory_federation", json.dumps({"federation": federation, "mempalace": child}))
    flat = transport._bounded_observation("memory_federation", json.dumps(federation))
    assert flat == direct == aggregate
    assert direct["physical_store_count"] == 1
    assert direct["mempalace"]["logical_role"] == child["logical_role"]
    assert direct["mempalace"]["native_memory_authority"]["session"] is False


def test_existing_direct_memory_aggregate_is_bindable_in_memory_observe_domain():
    from CONTROL_PLANE import canonical_semantic_spine as spine
    from MAKSIMAR_SERVER.SKILL_ADAPTER_REGISTRY.existing_capability_inventory import build_semantic_capability_registry_projection
    registry = build_semantic_capability_registry_projection()
    candidates = spine._goalframe_projection(registry, semantic_domain="memory", effect_intent="observe")
    assert "build_jarvis_live_memory_federation_status" in candidates
    detail = spine.select_semantic_projection_details(registry, ("build_jarvis_live_memory_federation_status",))
    catalog = spine.load_operation_catalog(detail)
    assert len(catalog) == 1
    assert catalog[0]["operation_id"] == "read_memory_federation_status"
    assert catalog[0]["target_scope"] == "local_memory_runtime"
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.project_understanding_adapter import PROJECT_READONLY_INVENTORY_CONTRACTS
    assert PROJECT_READONLY_INVENTORY_CONTRACTS["build_jarvis_live_memory_federation_status"][0]["semantic_owner_id"] == "memory.retrieve"


def test_memory_aggregate_compaction_retains_actual_role_owner_and_domain_qualification():
    import json
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    federation = {"surfaces": [
        {"surface_id": "native_chat", "owner": "CanonicalSessionContextStore",
            "logical_roles": ["conversation", "developer experience", "LearningBundle references"]},
        {"surface_id": "native_domain", "owner": "native_domain_preview",
            "data_status": "NOT_CONFIGURED", "persisted_dataset_available": False}]}
    bounded = transport._bounded_observation("memory_federation", json.dumps(federation))
    assert bounded["logical_role_owners"] == [("native_chat", "CanonicalSessionContextStore",
        ["conversation", "developer experience", "LearningBundle references"])]
    assert bounded["domain_data_states"] == [("native_domain", "native_domain_preview", "NOT_CONFIGURED", False)]


def test_live_memory_roles_and_paths_are_lifted_once_into_mandatory_evidence():
    import json
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    federation = {"physical_store_count": 1, "physical_stores": [{"path": "/native/history.jsonl"}],
        "surfaces": [{"surface_id": "native_chat", "owner": "CanonicalSessionContextStore",
            "logical_roles": ["conversation", "developer experience"]},
            {"surface_id": "domain", "owner": "native_domain", "data_status": "NOT_CONFIGURED",
             "persisted_dataset_available": False}]}
    _, _, bounded, _, _ = transport._bounded_final_brain_inputs(understanding={}, execution_plan=_typed_memory_self_knowledge_plan(),
        evidence_bundle={"status": "COMPLETE", "items": [{"kind": "memory_federation",
            "observation": json.dumps(federation)}]}, capability_state=(), session_context={})
    facts = bounded["mandatory_answer_facts"]["live_memory_health"]
    assert facts["physical_stores"][0]["path"] == "/native/history.jsonl"
    assert facts["logical_role_owners"][0][2] == ["conversation", "developer experience"]
    assert facts["domain_data_states"][0][2:] == ("NOT_CONFIGURED", False)
    assert not any(kind == "memory_federation" for kind, _ in bounded["items"])


def test_live_readonly_health_does_not_erase_actual_native_capture_writer():
    import json
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    writer = "CONTROL_PLANE.api_server._capture_canonical_turn_memory -> CanonicalSessionContextStore.append"
    federation = {"canonical_session_health": {"status": "LIVE_READ_ONLY"}, "surfaces": [
        {"surface_id": "local_chat_memory", "classification": "CANONICAL_STORE",
         "owner": "CanonicalSessionContextStore", "writer": writer}]}
    evidence = {"status": "COMPLETE", "items": [{"kind": "memory_federation",
        "observation": json.dumps(federation)}]}
    for stream in (False, True):
        payload = transport._grounded_final_brain_payload(original_text="Explain current memory", understanding={},
            execution_plan=_typed_memory_self_knowledge_plan(), capability_state=(), identity_facts={}, session_context={},
            evidence_bundle=evidence, stream=stream, compact=True)
        current = payload["messages"][-1]["content"]
        assert writer in current
        assert payload["options"]["temperature"] == 0
        assert "not a ban on the native writer" in "\n".join(message["content"] for message in payload["messages"])
        assert transport._final_brain_prompt_budget(payload)["within_budget"] is True


def test_live_memory_literal_paths_preserve_punctuation_in_both_final_modes():
    import json
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    paths = ["/home/example/.native.palace/chroma.sqlite3", "/project/session_memory/user_turns.jsonl"]
    evidence = {"status": "COMPLETE", "items": [{"kind": "memory_federation", "observation": json.dumps({
        "physical_stores": [{"path": path} for path in paths]})}]}
    for stream in (False, True):
        payload = transport._grounded_final_brain_payload(original_text="Explain live memory", understanding={},
            execution_plan=_typed_memory_self_knowledge_plan(), capability_state=(), identity_facts={}, session_context={},
            evidence_bundle=evidence, stream=stream, compact=True)
        current = payload["messages"][-1]["content"]
        raw = current.split("MANDATORY GROUNDED FACTS FOR THIS ANSWER: ", 1)[1].split("\nMemory:", 1)[0]
        restored = _restore_live_health_fact_groups(json.loads(raw)["mandatory_answer_facts"]["live_memory_health"])
        assert [store["path"] for store in restored["physical_stores"]] == paths
        assert all(current.count(path) == 1 for path in paths)
        assert transport._final_brain_prompt_budget(payload)["within_budget"] is True


def test_duplicate_utterances_keep_primary_record_date_separate_from_old_assistant_claim():
    import json
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    text = "My previous actual question"
    records = [{"user_text": text, "persisted_at": "2026-10-11T23:09:44Z",
        "assistant_text": "The earlier saved time was 2026-10-11T22:50:07Z"},
        {"user_text": text, "persisted_at": "2026-10-11T22:50:07Z"}]
    evidence = {"status": "COMPLETE", "items": [{"kind": "history_search", "observation": json.dumps({
        "history_query": {"query_kind": "HISTORY", "match_count": 2, "matches": records}})}]}
    _, _, bounded, _, _ = transport._bounded_final_brain_inputs(understanding={}, execution_plan={},
        evidence_bundle=evidence, capability_state=(), session_context={})
    primary = bounded["mandatory_answer_facts"]["retrieved_conversation_record"]
    assert primary == {"user_text": text, "persisted_at": "2026-10-11T23:09:44Z"}
    payload = transport._grounded_final_brain_payload(original_text="Show an earlier question and its saved date",
        understanding={}, execution_plan={}, capability_state=(), identity_facts={}, session_context={},
        evidence_bundle=evidence, stream=False)
    assert "never borrow another match's date" in payload["messages"][-1]["content"]
    assert transport._final_brain_prompt_budget(payload)["within_budget"] is True


def test_historical_assistant_claim_keeps_dialogue_but_has_no_record_metadata_authority():
    import json
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    old_claim = "This was saved 2026-10-11T22:50:07Z"
    observation = {"history_query": {"query_kind": "HISTORY", "match_count": 1,
        "matches": [{"user_text": "actual earlier question", "persisted_at": "2026-10-11T23:53:37Z",
            "assistant_text": old_claim}]}}
    projection = transport._bounded_observation("history_search", observation)
    record = projection["matches"][0]
    assert "assistant_text" not in record
    assert record["historical_assistant_utterance"] == {"text": old_claim,
        "authority": "quoted_dialogue_only_not_record_metadata"}
    assert record["persisted_at"] == observation["history_query"]["matches"][0]["persisted_at"]
    for stream in (False, True):
        payload = transport._grounded_final_brain_payload(original_text="Show earlier dialogue and saved date",
            understanding={}, execution_plan={}, capability_state=(), session_context={}, identity_facts={},
            evidence_bundle={"items": [{"kind": "history_search", "observation": json.dumps(observation)}]},
            stream=stream)
        assert "PRIMARY NATIVE RECORD PERSISTED_AT LITERAL: 2026-10-11T23:53:37Z" in payload["messages"][-1]["content"]
        assert payload["options"]["temperature"] == 0
        assert transport._final_brain_prompt_budget(payload)["within_budget"] is True
    assert observation["history_query"]["matches"][0]["assistant_text"] == old_claim


def test_native_journal_readback_preserves_bytes_and_does_not_create_missing_layout(tmp_path):
    import json
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import memory_context_sources as sources
    absent = tmp_path / "missing" / "incident_history.jsonl"
    assert sources._native_runtime_journal_health(absent, "incident")["status"] == "NOT_CONFIGURED"
    assert not absent.parent.exists()
    journal = tmp_path / "events.jsonl"
    records = [{"event_id": "e1", "event_type": "runtime.child.started", "source": "process_supervisor",
        "created_at": "2026-10-12T14:00:00+00:00", "payload": {"private": "do_not_project_payload"}},
        {"event_id": "e2", "event_type": "runtime.child.started", "source": "process_supervisor",
        "created_at": "2026-10-12T15:00:00Z", "payload": {}}]
    original = ("\n".join(json.dumps(x) for x in records) + "\n").encode()
    journal.write_bytes(original)
    health = sources._native_runtime_journal_health(journal, "event")
    assert health["status"] == "LIVE_READ_ONLY" and health["record_count"] == 2
    assert health["latest_event_at"] == "2026-10-12T15:00:00+00:00"
    assert "do_not_project_payload" not in json.dumps(health)
    assert journal.read_bytes() == original
    journal.write_bytes(original + b"invalid\n")
    invalid = sources._native_runtime_journal_health(journal, "event")
    assert invalid["status"] == "ENVIRONMENT_BLOCKED" and invalid["invalid_record_count"] == 1
    assert invalid["record_count"] == 2


def test_native_incident_metadata_uses_wall_time_and_reports_scan_limits(tmp_path):
    import json
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import memory_context_sources as sources
    journal = tmp_path / "incidents.jsonl"
    journal.write_text(json.dumps({"timestamp_wall": 0, "timestamp_monotonic": 999999,
        "reason": "recovery", "status": "crashed"}) + "\n")
    health = sources._native_runtime_journal_health(journal, "incident")
    assert health["latest_event_at"] == "1970-01-01T00:00:00+00:00"
    assert health["status"] == "LIVE_READ_ONLY"
    original = b"x" * 2_000_001
    journal.write_bytes(original)
    blocked = sources._native_runtime_journal_health(journal, "incident")
    assert blocked["status"] == "ENVIRONMENT_BLOCKED"
    assert blocked["error"] == "journal_byte_bound_exceeded"
    assert blocked["record_count"] is None and blocked["invalid_record_count"] is None
    assert journal.read_bytes() == original


def test_native_journals_share_jarvis_ui_truth_without_new_executable_capabilities():
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.jarvis_live_read_models import build_jarvis_live_memory_federation_status
    from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.final_memory_map import build_final_memory_graph
    from MAKSIMAR_SERVER.SKILL_ADAPTER_REGISTRY.existing_capability_inventory import build_existing_capability_catalog
    federation = build_jarvis_live_memory_federation_status()
    graph = build_final_memory_graph()
    from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.final_memory_map import build_final_memory_summary
    summary = build_final_memory_summary()
    assert federation["inventory_coverage"] == graph.inventory_coverage == summary["inventory_coverage"]
    assert federation["whole_organism_inventory_complete"] is graph.whole_organism_inventory_complete is summary["whole_organism_inventory_complete"] is False
    catalog = build_existing_capability_catalog()
    memory_capabilities = {item["capability_id"] for item in catalog["memory_tools"]}
    for identity in ("native_event_journal", "native_incident_history"):
        surface = next(item for item in federation["surfaces"] if item["surface_id"] == identity)
        node = next(item for item in graph.nodes if item.node_id == identity)
        store = next(item for item in federation["physical_stores"] if identity in item["logical_surfaces"])
        assert node.classification == surface["classification"] == "CANONICAL_STORE"
        assert node.owner == surface["owner"] == store["owner"]
        assert node.storage_path == surface["path"] == store["path"]
        assert node.logical_roles == surface["logical_roles"]
        assert surface["native_memory_authority"] == {"conversation": False, "verified_experience": False}
        assert identity not in memory_capabilities


def test_actual_shared_native_inventory_fits_existing_final_brain_context(monkeypatch):
    import json
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.jarvis_live_read_models import build_jarvis_live_memory_federation_status
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    federation = build_jarvis_live_memory_federation_status()
    for stream in (False, True):
        payload = transport._grounded_final_brain_payload(original_text=(
            "Объясни текущее устройство твоей памяти по живым read models: какие слои канонические, "
            "какие являются индексами и проекциями, где физически хранятся данные, что доступно и что не настроено. "
            "Отдельно уточни роль Mempalace и не выдавай его документы за business, regulatory или conversation memory."),
            understanding={"goals": [{"description": "Explain actual existing memory organism"}]},
            execution_plan=_typed_memory_self_knowledge_plan(), evidence_bundle={"items": [{"kind": "memory_federation",
                "observation": json.dumps(federation)}]}, capability_state=(), session_context={},
            identity_facts={}, stream=stream)
        budget = _assert_measured_health_input(monkeypatch, transport, payload)
        assert budget["num_ctx"] == 4096 and budget["within_budget"] is True
        material = "\n".join(item["content"] for item in payload["messages"])
        for store in federation["physical_stores"]:
            assert store["path"] in material and store["owner"] in material
        for identity in ("native_event_journal", "native_incident_history"):
            surface = next(item for item in federation["surfaces"] if item["surface_id"] == identity)
            assert surface["logical_roles"][0] in material
        assert "snapshot_sha256" not in material
        assert "References bind exact paths, identities, counts, states and times for separate evidence presentation" in material
        assert "not a ban on the native writer or auxiliary reference retrieval" in material


def test_native_inventory_self_readback_with_real_plan_state_and_identity_fits_context(monkeypatch):
    import json
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.jarvis_live_read_models import build_jarvis_live_memory_federation_status
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    federation = build_jarvis_live_memory_federation_status()
    request = ("Объясни текущее устройство твоей памяти по живым read models: какие слои канонические, "
        "какие являются индексами и проекциями, где физически хранятся данные, что доступно и что не настроено. "
        "Отдельно уточни роль Mempalace и не выдавай его документы за business, regulatory или conversation memory.")
    operations = [("build_jarvis_live_memory_federation_status", "read_memory_federation_status"),
                  ("conversation.respond", "respond")]
    state = [{"capability_id": capability, "provider_id": "existing_project_readonly_tools",
        "provider_available": True, "policy_execution_allowed": True, "executed": True,
        "execution_receipt_present": True} for capability, operation in operations]
    for stream in (False, True):
        payload = transport._grounded_final_brain_payload(original_text=request,
            understanding={"goals": [{"description": "Explain live memory layers, canonical owners, physical paths, availability and auxiliary reference role"}],
                "operation_requirements": [{"capability_id": c, "operation_id": o} for c,o in operations], "confidence": 0.95},
            execution_plan={"steps": [{"step_id": f"step_{i}", "capability_id": c, "operation": o}
                for i,(c,o) in enumerate(operations,1)]}, capability_state=state,
            evidence_bundle={"items": [{"kind": "memory_federation", "observation": json.dumps(federation)}],
                "capability_ids": [c for c,o in operations], "status": "COMPLETE"},
            identity_facts={"identity_id": "aleksandr", "display_name": "aleksandr", "assistant_identity": "JARVIS", "verified": True},
            session_context={"session_id": "activation_current_native_inventory_self_readback_1791820487903918553",
                "bounded_chronological_turns": [], "recent_artifacts": [], "current_topic": ""}, stream=stream)
        assert _assert_measured_health_input(monkeypatch, transport, payload)["within_budget"] is True


def test_live_auxiliary_retrieval_availability_is_independent_of_native_domain_ownership():
    import json
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    child = {"status": "LIVE_READ_ONLY", "native_memory_authority": {"conversation": False,
        "business": False, "regulatory": False}, "logical_role": "AUXILIARY_PROJECT_DOCUMENT_REFERENCE_RETRIEVAL"}
    _, _, bounded, _, _ = transport._bounded_final_brain_inputs(understanding={}, execution_plan=_typed_memory_self_knowledge_plan(),
        evidence_bundle={"items": [{"kind": "memory_federation", "observation": json.dumps({"mempalace": child})}]},
        capability_state=(), session_context={})
    facts = bounded["mandatory_answer_facts"]["live_memory_health"]["mempalace"]
    assert facts["reference_retrieval_available"] is True
    assert facts["native_owned_domains"] == ()
    assert child["native_memory_authority"]["conversation"] is False
    projection = transport._bounded_observation("memory_federation", {"mempalace": child})
    assert projection["mempalace"]["native_memory_authority"] == child["native_memory_authority"]


def test_registered_memory_views_survive_final_brain_lifting_without_fake_completeness():
    import json
    from copy import deepcopy
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    federation = {"inventory_coverage": "REGISTERED_NATIVE_SURFACES_ONLY",
        "whole_organism_inventory_complete": False, "memory_surfaces_detected_count": 3,
        "physical_stores": [{"path": "/actual/store.jsonl", "owner": "actual_writer"}],
        "surfaces": [{"surface_id": "native_record", "classification": "CANONICAL_STORE", "runtime_status": "LIVE_READ_ONLY"},
                     {"surface_id": "history_reader", "classification": "READ_MODEL", "runtime_status": "LIVE_READ_ONLY"}]}
    evidence = {"status": "COMPLETE", "items": [{"kind": "memory_federation", "observation": federation}]}
    original = deepcopy(evidence)
    for stream in (False, True):
        payload = transport._grounded_final_brain_payload(original_text="Explain current memory", understanding={},
            execution_plan=_typed_memory_self_knowledge_plan(), capability_state=(), session_context={}, evidence_bundle=evidence, stream=stream)
        current = payload["messages"][-1]["content"]
        raw = current.split("MANDATORY GROUNDED FACTS FOR THIS ANSWER: ", 1)[1].split("\nMemory:", 1)[0]
        health = _restore_live_health_fact_groups(json.loads(raw)["mandatory_answer_facts"]["live_memory_health"])
        assert health["registered_view_columns"] == ["surface_id", "classification", "runtime_status"]
        # Preserve the original exact semantic row assertions after decoding
        # the reversible repeated-label representation.
        decoded = health["registered_view_sample"]
        assert decoded == [["native_record", "CANONICAL_STORE", "LIVE_READ_ONLY"],
                           ["history_reader", "READ_MODEL", "LIVE_READ_ONLY"]]
        assert health["omitted_registered_views"] == 1
        assert health["whole_organism_inventory_complete"] is False
        assert health["physical_stores"][0]["path"] == "/actual/store.jsonl"
        assert current.count("/actual/store.jsonl") == 1
        assert evidence == original


def test_live_health_prompt_owner_references_restore_all_actual_roles_and_writers():
    import json
    from copy import deepcopy
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.jarvis_live_read_models import build_jarvis_live_memory_federation_status
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    federation = build_jarvis_live_memory_federation_status()
    evidence = {"items": [{"kind": "memory_federation", "observation": federation}]}
    original = deepcopy(evidence)
    bounded = transport._bounded_observation("memory_federation", federation)
    for stream in (False, True):
        payload = transport._grounded_final_brain_payload(original_text="Explain current live memory", understanding={},
            execution_plan=_typed_memory_self_knowledge_plan(), capability_state=(), session_context={}, evidence_bundle=evidence, stream=stream)
        current = payload["messages"][-1]["content"]
        raw = current.split("MANDATORY GROUNDED FACTS FOR THIS ANSWER: ", 1)[1].split("\nMemory:", 1)[0]
        health = _restore_live_health_fact_groups(json.loads(raw)["mandatory_answer_facts"]["live_memory_health"])
        stores = health["physical_stores"]
        for key in ("logical_role_owners", "canonical_store_writers"):
            assert all(isinstance(row[1], str) for row in health[key])
            restored = [(row[0], stores[row[1]-1]["owner"] if isinstance(row[1], int) else row[1], *row[2:])
                        for row in health[key]]
            assert json.dumps(restored, sort_keys=True) == json.dumps(bounded[key], sort_keys=True)
        assert health["inventory_coverage"] == federation["inventory_coverage"]
        assert health["whole_organism_inventory_complete"] is False
        assert payload["options"]["num_ctx"] == 4096
        assert payload["options"]["num_predict"] == 1500
        assert evidence == original


def test_live_health_real_final_response_pending_state_has_admission_margin(monkeypatch):
    import json
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.jarvis_live_read_models import build_jarvis_live_memory_federation_status
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    request = ("Объясни текущее устройство твоей памяти по живым read models: какие слои канонические, "
        "какие являются индексами и проекциями, где физически хранятся данные, что доступно и что не настроено. "
        "Отдельно уточни роль Mempalace и не выдавай его документы за business, regulatory или conversation memory.")
    operations = [("build_jarvis_live_memory_federation_status", "read_memory_federation_status"),
                  ("conversation.respond", "respond")]
    state = [{"capability_id": capability, "provider_id": provider, "provider_available": True,
              "policy_execution_allowed": True, "executed": completed, "execution_receipt_present": completed}
             for capability,provider,completed in [
                 (operations[0][0], "existing_project_workspace_tools", True),
                 (operations[1][0], "existing_jarvis_final_brain", False)]]
    for stream in (False, True):
        payload = transport._grounded_final_brain_payload(original_text=request,
            understanding={"goals": [{"description": "устройство твоей памяти по живым read models"},
                {"description": "роль Mempalace и ограничение доступа к его документам"}], "confidence": 1.0},
            execution_plan={"steps": [{"step_id": f"step_{i}", "capability_id": c, "operation": o}
                for i,(c,o) in enumerate(operations, 1)]}, capability_state=state,
            evidence_bundle={"status": "COMPLETE", "items": [{"kind": "memory_federation",
                "observation": json.dumps(build_jarvis_live_memory_federation_status())}]},
            identity_facts={"identity_id": "aleksandr", "display_name": "aleksandr", "assistant_identity": "JARVIS",
                "profile_type": "owner", "verified": True, "grounding_rule": "use_only_supplied_identity_facts"},
            session_context={}, stream=stream)
        budget = _assert_measured_health_input(monkeypatch, transport, payload)
        assert budget["num_ctx"] == 4096
        assert budget["reserved_output_tokens"] == 1500
        assert budget["available_input_tokens"] - budget["estimated_prompt_tokens"] >= 80
        assert request in payload["messages"][-1]["content"]


def test_memory_health_sections_are_model_authored_and_missing_sections_fail_closed():
    import json
    import pytest
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    fields = ("coverage", "storage", "roles", "retrieval", "journals", "domains")
    model_values = {field: {"prose": f"Model paragraph for {field}.", "covered_fact_ids": []} for field in fields}
    assert transport._render_memory_health_answer_sections(json.dumps(model_values)) == "\n\n".join(value["prose"] for value in model_values.values())
    for missing in fields:
        with pytest.raises(ValueError, match="missing_sections"):
            transport._render_memory_health_answer_sections(json.dumps({k:v for k,v in model_values.items() if k != missing}))
    for bad in ("", None, [], {}):
        value = {**model_values, "storage": bad}
        with pytest.raises(ValueError, match="empty_section"):
            transport._render_memory_health_answer_sections(json.dumps(value))
    with pytest.raises(ValueError, match="invalid_json"):
        transport._render_memory_health_answer_sections("A short unstructured answer")
    with pytest.raises(ValueError, match="missing_sections"):
        transport._render_memory_health_answer_sections(json.dumps({**model_values, "invented": "extra"}))


def test_final_brain_json_health_output_contract_is_typed_evidence_only():
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    request = "Explain memory layers, physical paths and current health"
    for stream in (False, True):
        ordinary = transport._grounded_final_brain_payload(original_text=request, understanding={},
            execution_plan=_typed_memory_self_knowledge_plan(), capability_state=(), session_context={}, evidence_bundle={"items": []}, stream=stream)
        assert "format" not in ordinary
        health = transport._grounded_final_brain_payload(original_text=request, understanding={},
            execution_plan=_typed_memory_self_knowledge_plan(), capability_state=(), session_context={}, evidence_bundle={
                "items": [{"kind": "memory_federation", "observation": {"physical_stores": []}}]}, stream=stream)
        assert isinstance(health["format"], dict) and health["format"]["required"] == ["coverage", "storage", "roles", "retrieval", "journals", "domains"]
        assert health["options"]["num_ctx"] == 4096
        assert "covered_fact_ids" in health["messages"][1]["content"]


def test_memory_health_final_transport_uses_one_model_call_and_retains_raw_failure(monkeypatch):
    import json
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    monkeypatch.setattr(transport, "_validate_memory_self_knowledge_publication",
        lambda **kwargs: {"valid": True, "test_scope": "isolated_schema_transport"})
    fields = ("coverage", "storage", "roles", "retrieval", "journals", "domains")
    sections = {field: {"prose": f"Actual model paragraph {field}", "covered_fact_ids": []} for field in fields}
    evidence = {"items": [{"kind": "memory_federation", "observation": {"physical_stores": []}}]}
    for data, done_reason, valid in ((sections, "stop", True), ({"coverage": "partial"}, "stop", False),
                                     (sections, "length", False)):
        calls = []
        raw = json.dumps(data)
        def fake_post(url, payload, timeout_seconds):
            calls.append(payload)
            return {"model": payload["model"], "message": {"content": raw}, "done": True, "done_reason": done_reason}
        monkeypatch.setattr(transport, "ollama_post_json", fake_post)
        result = transport.grounded_final_brain_call(original_text="Explain memory", understanding={},
            execution_plan=_typed_memory_self_knowledge_plan(), capability_state=(), evidence_bundle=evidence)
        assert len(calls) == 1 and isinstance(calls[0]["format"], dict) and calls[0]["format"]["additionalProperties"] is False
        assert result["ok"] is valid and result["schema_valid"] is valid
        assert result["raw_model_result"]["content"] == raw
        if valid:
            assert result["response_text"] == "\n\n".join(value["prose"] for value in sections.values())
        else:
            assert result["response_text"] == "" and result["model_call_used"] is False
            assert result["error"] == ("model_output_truncated" if done_reason == "length"
                else "final_brain_memory_health_missing_sections")
            assert result["content"] == "" and result["evidence_used"] is False


def test_streamed_memory_health_is_buffered_until_validated_completion(monkeypatch):
    import json
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    monkeypatch.setattr(transport, "_validate_memory_self_knowledge_publication",
        lambda **kwargs: {"valid": True, "test_scope": "isolated_schema_transport"})
    fields = ("coverage", "storage", "roles", "retrieval", "journals", "domains")
    sections = {field: {"prose": f"Actual model paragraph {field}", "covered_fact_ids": []} for field in fields}
    evidence = {"items": [{"kind": "memory_federation", "observation": {"physical_stores": []}}]}
    for data, done_reason, valid in ((sections, "stop", True), ({"coverage": "partial"}, "stop", False),
                                     (sections, "length", False)):
        raw = json.dumps(data)
        calls = []
        class Response:
            def __enter__(self): return self
            def __exit__(self, *args): return False
            def raise_for_status(self): return None
            def iter_lines(self):
                for fragment in (raw[:10], raw[10:]):
                    yield json.dumps({"model": transport.DEFAULT_OLLAMA_MODEL_ID,
                        "message": {"content": fragment}, "done": False})
                yield json.dumps({"model": transport.DEFAULT_OLLAMA_MODEL_ID,
                    "message": {"content": ""}, "done": True, "done_reason": done_reason})
        def fake_stream(*args, **kwargs):
            calls.append(kwargs["json"])
            return Response()
        monkeypatch.setattr(transport.httpx, "stream", fake_stream)
        events = list(transport.grounded_final_brain_stream(original_text="Explain memory", understanding={},
            execution_plan=_typed_memory_self_knowledge_plan(), capability_state=(), evidence_bundle=evidence))
        assert len(calls) == 1 and isinstance(calls[0]["format"], dict) and calls[0]["format"]["additionalProperties"] is False
        chunks = [event["text"] for event in events if event["event"] == "chunk"]
        if valid:
            assert chunks == ["\n\n".join(value["prose"] for value in sections.values())]
            assert events[-1]["event"] == "done" and events[-1]["schema_valid"] is True
        else:
            assert chunks == [] and events[-1]["event"] == "error"
            assert events[-1]["response_text"] == "" and events[-1]["model_call_used"] is False
            assert events[-1]["raw_response_text"] == raw


def _restore_live_health_fact_groups(groups):
    """Restore the original fact fields for exact semantic-roundtrip assertions."""
    if "evidence" in groups:
        def strip(value):
            if isinstance(value, dict) and set(value) == {"$v"}:
                return groups["values"][value["$v"]]
            if isinstance(value, list) and len(value) == 2 and isinstance(value[0], list) and value[0] and all(type(i) is int for i in value[0]):
                return strip(value[1])
            if isinstance(value, dict):
                return {k: strip(v) for k,v in value.items()}
            if isinstance(value, list):
                return [strip(v) for v in value]
            return value
        return strip(groups["evidence"])
    fields = {}
    assert set(groups) == {"coverage", "storage", "roles", "retrieval", "journals", "domains"}
    for values in groups.values():
        assert isinstance(values, dict)
        for key, value in values.items():
            assert key not in fields
            fields[key] = value
    fields["registered_view_count_not_store_count"] = fields.pop("registered_view_count")
    if isinstance(fields.get("logical_role_owners"), dict):
        fields["logical_role_owners"] = [[surface, value["owner"], value["logical_roles"]]
            for surface, value in fields["logical_role_owners"].items()]
    if isinstance(fields.get("canonical_store_writers"), dict):
        fields["canonical_store_writers"] = list(map(list, fields["canonical_store_writers"].items()))
    if isinstance(fields.get("domain_data_states"), dict):
        fields["domain_data_states"] = [[surface, value["owner"], value["state"], value["persisted_dataset_available"]]
            for surface, value in fields["domain_data_states"].items()]
    for journal in fields.pop("native_store_health", []):
        stores = [store for store in fields["physical_stores"] if store["path"] == journal["physical_store_path"]]
        assert len(stores) == 1 and stores[0]["owner"] == journal["physical_store_owner"]
        stores[0]["native_journal_health"] = journal["health"]
    return fields


def _typed_memory_self_knowledge_plan():
    return {"steps": [{"capability_id": "build_jarvis_live_memory_federation_status",
        "operation": "read_memory_federation_status"}]}


def _factual_publication_fixture():
    import json
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    observation = {"inventory_coverage": "REGISTERED_NATIVE_SURFACES_ONLY",
        "whole_organism_inventory_complete": False, "memory_surfaces_detected_count": 13,
        "physical_store_count": 1, "live_physical_store_count": 1,
        "physical_stores": [{"path": "/isolated/native.jsonl", "owner": "RealNativeOwner",
            "native_journal_health": {"status": "LIVE_READ_ONLY", "record_count": 29,
                "invalid_record_count": 0, "latest_event_at": "2026-01-02T03:04:05Z"}}],
        "surfaces": [{"surface_id": "native_surface", "owner": "RealNativeOwner",
            "writer": "RealNativeWriter.append", "classification": "CANONICAL_STORE",
            "runtime_status": "LIVE_READ_ONLY", "logical_roles": ["conversation", "episodic history",
                "developer experience", "LearningBundle references", "execution receipt memory", "retrieval trace"]}]
            + [{"surface_id": "reader_"+str(i), "classification": "READ_MODEL", "runtime_status": "READ_MODEL_ONLY"}
               for i in range(12)],
        "canonical_session_health": {"status": "LIVE_READ_ONLY", "record_count": 71,
            "invalid_record_count": 0, "last_append_at": "2026-01-02T02:03:04Z"},
        "mempalace": {"status": "NOT_CONFIGURED", "freshness": "UNVERIFIED"}}
    inputs = dict(understanding={}, execution_plan=_typed_memory_self_knowledge_plan(),
        capability_state=(), session_context={}, evidence_bundle={"items": [
            {"kind": "memory_federation", "observation": observation}]})
    health = transport._bounded_final_brain_inputs(**inputs)[2]["mandatory_answer_facts"]["live_memory_health"]
    groups = transport._memory_self_knowledge_assertions(health)
    # Explicit model output fixture, not a production answer generator. Natural
    # acceptance must still use actual FinalBrain prose, never this fixture.
    paragraphs = {key: json.dumps(value, ensure_ascii=False) for key, value in groups.items()}
    return inputs, paragraphs


def _factual_coverage_content(inputs, paragraphs):
    """Isolated model-response fixture; never used for natural acceptance."""
    import json
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    health = transport._bounded_final_brain_inputs(**inputs)[2]["mandatory_answer_facts"]["live_memory_health"]
    projection, _ = transport._memory_fact_coverage_projection(health)
    return json.dumps({key: {"prose": prose, "covered_fact_ids": projection["required_fact_ids_by_section"][key]}
        for key, prose in paragraphs.items()}, ensure_ascii=False)


def test_factual_gate_checks_source_derived_assertions_and_keeps_answer_unmodified(monkeypatch):
    import json
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    inputs, paragraphs = _factual_publication_fixture()
    original = _factual_coverage_content(inputs, paragraphs)
    calls = []
    def verify(url, payload, timeout_seconds):
        calls.append(payload)
        facts = json.loads(payload["messages"][-1]["content"])
        assert facts["candidate"] == paragraphs
        assert payload["model"] == transport.DEFAULT_OLLAMA_MODEL_ID
        assert payload["think"] is False
        assert payload["options"]["num_ctx"] == transport.resident_context_tokens_for_jarvis_model(payload["model"])
        verdict = {"supported": [int(i) for i in facts["source_assertions"]],
            "contradictions": [], "unsupported_claims": []}
        return {"model": payload["model"], "message": {"content": json.dumps(verdict)},
            "done": True, "done_reason": "stop"}
    monkeypatch.setattr(transport, "ollama_get_json", lambda *args, **kwargs: {"models": [{"name": transport.DEFAULT_OLLAMA_MODEL_ID}]})
    monkeypatch.setattr(transport, "ollama_post_json", verify)
    result = transport._validate_memory_self_knowledge_publication(content=original, inputs=inputs, deadline_seconds=60)
    assert result["valid"] is True and len(calls) == 6
    assert result["correction_attempted"] is False and result["host_answer_synthesized"] is False
    assert _factual_coverage_content(inputs, paragraphs) == original


def test_missing_exact_owners_writers_roles_paths_dates_fail_before_verifier(monkeypatch):
    import json
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    inputs, paragraphs = _factual_publication_fixture()
    def forbidden(*args, **kwargs): raise AssertionError("No model correction or verification after missing facts")
    monkeypatch.setattr(transport, "ollama_post_json", forbidden)
    for literal in ("RealNativeOwner", "RealNativeWriter.append",
            "/isolated/native.jsonl", "2026-01-02T03:04:05Z", "UNVERIFIED", "REGISTERED_NATIVE_SURFACES_ONLY"):
        changed = {key: value.replace(literal, "native_surface") for key, value in paragraphs.items()}
        result = transport._validate_memory_self_knowledge_publication(
            content=_factual_coverage_content(inputs, changed), inputs=inputs, deadline_seconds=60)
        assert result["valid"] is False and result["reason"] == "required_exact_facts_missing"
        assert result["missing_exact_assertions"]


def test_semantic_gate_rejects_conflicting_count_identity_scope_even_when_all_literals_present(monkeypatch):
    import json
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    inputs, paragraphs = _factual_publication_fixture()
    for conflict in ("There are 10 registered views.", "The writer is native_surface.",
                     "The whole memory inventory is complete.", "All journals are fresh at a different date."):
        changed = {**paragraphs, "domains": paragraphs["domains"] + conflict}
        calls = []
        def verify(url, payload, timeout_seconds):
            calls.append(payload)
            facts = json.loads(payload["messages"][-1]["content"])
            assert conflict in facts["candidate"]["domains"]
            return {"model": payload["model"], "message": {"content": json.dumps({
                "supported": [int(i) for i in facts["source_assertions"]],
                "contradictions": [conflict], "unsupported_claims": []})}, "done": True, "done_reason": "stop"}
        monkeypatch.setattr(transport, "ollama_get_json", lambda *args, **kwargs: {"models": [{"name": transport.DEFAULT_OLLAMA_MODEL_ID}]})
        monkeypatch.setattr(transport, "ollama_post_json", verify)
        result = transport._validate_memory_self_knowledge_publication(
            content=_factual_coverage_content(inputs, changed), inputs=inputs, deadline_seconds=60)
        assert result["valid"] is False and result["reason"] == "semantic_assertions_not_proven"
        assert len(calls) == 1 and result["verification_results"][0]["model_call"]["raw_model_result"]


def test_six_section_contract_does_not_leak_to_dashboard_or_untyped_aggregate():
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    for kind, plan in (("dashboard_memory_models", _typed_memory_self_knowledge_plan()), ("memory_federation", {})):
        for stream in (False, True):
            payload = transport._grounded_final_brain_payload(original_text="Explain memory",
                understanding={}, execution_plan=plan, capability_state=(), session_context={},
                evidence_bundle={"items": [{"kind": kind, "observation": {"physical_stores": []}}]}, stream=stream)
            assert "format" not in payload
            assert "six string paragraphs" not in payload["messages"][1]["content"]


def test_factual_failure_blocks_ordinary_and_stream_publication_and_retains_raw(monkeypatch):
    import json
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    inputs, paragraphs = _factual_publication_fixture()
    paragraphs["roles"] = "native_surface is the writer"
    raw = _factual_coverage_content(inputs, paragraphs)
    monkeypatch.setattr(transport, "ollama_post_json", lambda url, payload, timeout_seconds:
        {"model": payload["model"], "message": {"content": raw}, "done": True, "done_reason": "stop"})
    ordinary = transport.grounded_final_brain_call(original_text="Current memory", **inputs)
    assert not ordinary["ok"] and ordinary["schema_valid"] and not ordinary["factual_valid"]
    assert ordinary["response_text"] == ordinary["content"] == ""
    assert ordinary["raw_model_result"]["content"] == raw and not ordinary["evidence_used"]
    class Response:
        def __enter__(self): return self
        def __exit__(self, *args): return False
        def raise_for_status(self): pass
        def iter_lines(self):
            yield json.dumps({"model": transport.DEFAULT_OLLAMA_MODEL_ID,
                "message": {"content": raw}, "done": False})
            yield json.dumps({"model": transport.DEFAULT_OLLAMA_MODEL_ID,
                "message": {"content": ""}, "done": True, "done_reason": "stop"})
    monkeypatch.setattr(transport.httpx, "stream", lambda *args, **kwargs: Response())
    events = list(transport.grounded_final_brain_stream(original_text="Current memory", **inputs))
    assert not any(event["event"] == "chunk" for event in events)
    assert events[-1]["event"] == "error" and events[-1]["response_text"] == ""
    assert events[-1]["raw_response_text"] == raw and events[-1]["factual_valid"] is False


def test_factual_publication_never_activates_installed_but_unloaded_exclusive_verifier(monkeypatch):
    import json
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    inputs, paragraphs = _factual_publication_fixture()
    monkeypatch.setattr(transport, "ollama_get_json", lambda *args, **kwargs: {"models": []})
    def forbidden(*args, **kwargs): raise AssertionError("Publication gate must not cold-activate an exclusive model")
    monkeypatch.setattr(transport, "ollama_post_json", forbidden)
    result = transport._validate_memory_self_knowledge_publication(
        content=_factual_coverage_content(inputs, paragraphs), inputs=inputs, deadline_seconds=60)
    assert not result["valid"] and result["reason"] == "semantic_verifier_not_live_loaded"
    assert result["provider_readiness"]["activation_attempted"] is False


def _assert_measured_health_input(monkeypatch, transport, payload):
    from copy import deepcopy
    original = deepcopy(payload)
    def prefill(url, probe, timeout_seconds):
        assert probe["messages"] == original["messages"]
        assert probe["format"] == original["format"]
        assert probe["options"]["num_ctx"] == 4096
        assert probe["options"]["num_predict"] == 1
        return {"model": probe["model"], "message": {"content": "{"},
            "done": True, "done_reason": "length", "eval_count": 1, "prompt_eval_count": 1500}
    monkeypatch.setattr(transport, "ollama_post_json", prefill)
    budget = transport._measured_final_brain_prompt_budget(payload, timeout_seconds=20)
    assert payload == original
    assert budget["within_budget"] is True
    if "tokenizer_probe" in budget:
        assert budget["tokenizer_probe"]["output_used_as_answer"] is False
        assert budget["tokenizer_probe"]["source_answer_payload_unchanged"] is True
    return budget


def test_exact_prefill_rejects_unproven_counts_and_does_not_activate_oversized_input(monkeypatch):
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    payload = {"model": transport.DEFAULT_OLLAMA_MODEL_ID, "format": "json", "stream": True,
        "messages": [{"role": "user", "content": "a" * 6000}],
        "options": {"num_ctx": 4096, "num_predict": 1500}}
    calls = []
    for count, evaluated, model, done in [(None,1,payload["model"],True),
            (0,1,payload["model"],True),(3936,1,payload["model"],True),
            (3100,1,payload["model"],True),(1500,2,payload["model"],True),(1500,True,payload["model"],True),
            (1500,1,"foreign",True),(1500,1,payload["model"],False)]:
        def prefill(url, probe, timeout_seconds):
            calls.append(probe)
            return {"model": model, "message": {"content": "{"}, "done": done,
                "done_reason": "length", "eval_count": evaluated, "prompt_eval_count": count}
        monkeypatch.setattr(transport, "ollama_post_json", prefill)
        result = transport._measured_final_brain_prompt_budget(payload, timeout_seconds=20)
        assert result["within_budget"] is False
        assert result["measurement_error"] == "complete_input_token_count_unproven"
        assert result["tokenizer_probe"]["output_used_as_answer"] is False
    prior = len(calls)
    oversized = {**payload, "messages": [{"role": "user", "content": "a" * 10000}]}
    result = transport._measured_final_brain_prompt_budget(oversized, timeout_seconds=20)
    assert result["measurement_error"] == "prefill_input_not_conservatively_bounded"
    assert len(calls) == prior
    assert transport._measured_final_brain_prompt_budget({**payload, "format": None}, timeout_seconds=20)["within_budget"] is False
    assert len(calls) == prior


def test_explanatory_roles_require_semantic_proof_without_literal_english_echo(monkeypatch):
    import json
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    inputs, paragraphs = _factual_publication_fixture()
    candidate = {k: v.replace("retrieval trace", "трасса извлечения") for k,v in paragraphs.items()}
    monkeypatch.setattr(transport, "ollama_get_json", lambda *a, **kw:
        {"models": [{"name": transport.DEFAULT_OLLAMA_MODEL_ID}]})
    rejected = False
    def verdict(url, payload, timeout_seconds):
        group = json.loads(payload["messages"][-1]["content"])["evidence_group"]
        return {"model": payload["model"], "message": {"content": json.dumps({
            "supported": [1], "contradictions": [],
            "unsupported_claims": ["role missing"] if rejected and group == "roles" else []})},
            "done": True, "done_reason": "stop"}
    monkeypatch.setattr(transport, "ollama_post_json", verdict)
    result = transport._validate_memory_self_knowledge_publication(content=_factual_coverage_content(inputs, candidate), inputs=inputs, deadline_seconds=60)
    assert result["valid"] is True and len(result["verification_results"]) == 6
    rejected = True
    result = transport._validate_memory_self_knowledge_publication(content=_factual_coverage_content(inputs, candidate), inputs=inputs, deadline_seconds=60)
    assert result["valid"] is False and result["reason"] == "semantic_assertions_not_proven"
    assert not result["missing_exact_assertions"]


def test_lossless_live_evidence_entities_restore_every_mandatory_fact():
    import json
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.jarvis_live_read_models import build_jarvis_live_memory_federation_status
    inputs = dict(understanding={}, execution_plan=_typed_memory_self_knowledge_plan(), capability_state=(),
        session_context={}, evidence_bundle={"items": [{"kind": "memory_federation",
        "observation": build_jarvis_live_memory_federation_status()}]})
    original = transport._bounded_final_brain_inputs(**inputs)[2]["mandatory_answer_facts"]["live_memory_health"]
    for stream in (False, True):
        payload = transport._grounded_final_brain_payload(original_text="Explain memory", **inputs, stream=stream)
        material = payload["messages"][-1]["content"]
        groups = json.loads(material.split("MANDATORY GROUNDED FACTS FOR THIS ANSWER: ",1)[1])["mandatory_answer_facts"]["live_memory_health"]
        restored = _restore_live_health_fact_groups(groups)
        child = restored["mempalace"]
        if "storage_path_literal_line" in child:
            child["storage_path"] = restored["physical_stores"][child.pop("storage_path_literal_line")-1]["path"]
        assert json.dumps(restored, sort_keys=True) == json.dumps(original, sort_keys=True)
        assert "registered_view_labels" not in material and "physical_store_index" not in material


def test_exact_integer_fact_at_sentence_end_is_not_mistaken_for_decimal(monkeypatch):
    import json
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    inputs, paragraphs = _factual_publication_fixture()
    paragraphs["coverage"] = "REGISTERED_NATIVE_SURFACES_ONLY; whole_organism_inventory_complete=false. Physical stores 1. Registered views 13."
    monkeypatch.setattr(transport, "ollama_get_json", lambda *a, **k: {"models": []})
    result = transport._validate_memory_self_knowledge_publication(content=_factual_coverage_content(inputs, paragraphs), inputs=inputs, deadline_seconds=30)
    assert not result["missing_exact_assertions"]
    assert result["reason"] == "semantic_verifier_not_live_loaded"
    paragraphs["coverage"] = paragraphs["coverage"].replace("13.", "13.5.")
    result = transport._validate_memory_self_knowledge_publication(content=_factual_coverage_content(inputs, paragraphs), inputs=inputs, deadline_seconds=30)
    assert not result["valid"] and result["reason"] == "semantic_verifier_not_live_loaded"


def test_writer_callable_names_are_exact_but_label_punctuation_is_semantic(monkeypatch):
    import json
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    inputs, paragraphs = _factual_publication_fixture()
    inputs["evidence_bundle"]["items"][0]["observation"]["surfaces"][0]["writer"] = "RealNativeWriter.append (ordinary/streaming) → CanonicalStore.append"
    paragraphs["roles"] += " Writer: RealNativeWriter.append через CanonicalStore.append; оба режима записи."
    monkeypatch.setattr(transport, "ollama_get_json", lambda *a, **k: {"models": []})
    result = transport._validate_memory_self_knowledge_publication(content=_factual_coverage_content(inputs, paragraphs), inputs=inputs, deadline_seconds=30)
    assert not result["missing_exact_assertions"]
    assert result["valid"] is False and result["reason"] == "semantic_verifier_not_live_loaded"
    paragraphs["roles"] = paragraphs["roles"].replace("CanonicalStore.append", "native_surface")
    result = transport._validate_memory_self_knowledge_publication(content=_factual_coverage_content(inputs, paragraphs), inputs=inputs, deadline_seconds=30)
    assert not result["valid"] and result["reason"] == "semantic_verifier_not_live_loaded"


def test_mandatory_evidence_requires_consistent_counts_and_physical_identities(monkeypatch):
    import json
    from copy import deepcopy
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    inputs, paragraphs = _factual_publication_fixture()
    def forbidden(*a, **kw):
        raise AssertionError("Invalid mandatory evidence must fail before provider call")
    monkeypatch.setattr(transport, "ollama_get_json", forbidden)
    monkeypatch.setattr(transport, "ollama_post_json", forbidden)
    changes = [lambda o: o.update(memory_surfaces_detected_count=14),
        lambda o: o.update(live_physical_store_count=2),
        lambda o: o.update(physical_store_count=-1),
        lambda o: o["physical_stores"][0].update(owner=None),
        lambda o: o["physical_stores"][0].update(path=""),
        lambda o: (o["physical_stores"].append(dict(o["physical_stores"][0])), o.update(physical_store_count=2))]
    for change in changes:
        altered = deepcopy(inputs)
        change(altered["evidence_bundle"]["items"][0]["observation"])
        result = transport._validate_memory_self_knowledge_publication(content=_factual_coverage_content(inputs, paragraphs), inputs=altered, deadline_seconds=30)
        assert result["valid"] is False and result["reason"] == "mandatory_live_evidence_incomplete"


def test_authorized_one_correction_publish_and_fail_closed_matrix(monkeypatch):
    import json
    from copy import deepcopy
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    inputs, paragraphs = _factual_publication_fixture()
    correct = _factual_coverage_content(inputs, paragraphs)
    wrong = _factual_coverage_content(inputs, {**paragraphs, "roles": "native_surface is the writer"})
    contradictory = _factual_coverage_content(inputs, {**paragraphs, "domains": paragraphs["domains"] + " whole memory is complete"})
    monkeypatch.setattr(transport, "ollama_get_json", lambda *a, **k:
        {"models": [{"name": transport.DEFAULT_OLLAMA_MODEL_ID}]})
    for first, second, success, corrections in [(wrong, correct, True, 1),
            (wrong, wrong, False, 1), (correct, wrong, True, 0),
            (wrong, "{}", False, 1), (wrong, contradictory, False, 1)]:
        author_calls = []
        original = deepcopy(inputs)
        def provider(url, payload, timeout_seconds):
            assert payload["model"] == transport.DEFAULT_OLLAMA_MODEL_ID
            assert payload["options"]["num_ctx"] == 4096
            if payload["options"]["num_predict"] == 1:
                return {"model": payload["model"], "message": {"content": "{"},
                    "done": True, "done_reason": "length", "eval_count": 1, "prompt_eval_count": 1500}
            if payload["options"]["num_predict"] == 256:
                facts = json.loads(payload["messages"][-1]["content"])
                conflict = ("whole memory is complete" in facts["candidate"]["domains"]
                    or (facts["evidence_group"] == "roles" and "native_surface is the writer" in facts["candidate"]["roles"]))
                raw = json.dumps({"supported": [1], "contradictions": ["false completeness"] if conflict else [],
                    "unsupported_claims": []})
            else:
                author_calls.append(deepcopy(payload))
                raw = first if len(author_calls) == 1 else second
                assert len(author_calls) <= 2
                if len(author_calls) == 2:
                    assert author_calls[0]["options"] == payload["options"]
                    assert "EVIDENCE_BUNDLE_JSON" not in payload["messages"][-1]["content"]
                    assert "Structured errors:" in payload["messages"][-1]["content"]
                    feedback = json.loads(payload["messages"][-1]["content"].split("Structured errors: ",1)[1])
                    assert feedback["original_failed_response"] == json.loads(first)
                    health = transport._bounded_final_brain_inputs(**inputs)[2]["mandatory_answer_facts"]["live_memory_health"]
                    _, catalog = transport._memory_fact_coverage_projection(health)
                    projected = feedback["correction_evidence_projection"]
                    assert projected
                    for fact_id, fact in projected.items():
                        assert (fact["assertion_path"], fact["value"]) == catalog[int(fact_id)]
                    assert any(fact["value"] == "RealNativeWriter.append" for fact in projected.values())
            return {"model": payload["model"], "message": {"content": raw}, "done": True, "done_reason": "stop"}
        monkeypatch.setattr(transport, "ollama_post_json", provider)
        outcome = transport.grounded_final_brain_call(original_text="Current memory", **inputs)
        assert outcome["ok"] is success
        assert len(author_calls) == 1 + corrections
        assert inputs == original
        proof = outcome["correction_proof"]
        assert proof["correction_attempts"] == corrections
        assert proof["BOUND_FINALBRAIN_CORRECTION_MAX_ATTEMPTS"] == 1
        if corrections:
            assert proof["FIRST_RAW_FAILED_RESPONSE"] == first
            assert proof["FIRST_VALIDATION_ERRORS"]["valid"] is False
            assert proof["CORRECTION_RESPONSE"] == second
        assert proof["FINAL_VALIDATION_RESULT"]["valid"] is success
        if success:
            assert outcome["response_text"] == transport._render_memory_health_answer_sections(correct)
        else:
            assert outcome["content"] == outcome["response_text"] == ""


def test_correction_never_resets_deadline_or_corrects_bad_source(monkeypatch):
    import json
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    inputs, paragraphs = _factual_publication_fixture()
    payload = transport._grounded_final_brain_payload(original_text="Current memory", **inputs, stream=False)
    def forbidden(*a, **k): raise AssertionError("No correction provider call")
    monkeypatch.setattr(transport, "ollama_post_json", forbidden)
    wrong = _factual_coverage_content(inputs, {**paragraphs, "roles": "missing writer"})
    result = transport._validated_memory_answer_once(content=wrong, inputs=inputs, payload=payload, deadline_at=0)
    assert not result["valid"] and result["proof"]["correction_attempts"] == 0
    inputs["evidence_bundle"]["items"][0]["observation"]["physical_store_count"] = -1
    result = transport._validated_memory_answer_once(content=wrong, inputs=inputs, payload=payload, deadline_at=10**20)
    assert not result["valid"] and result["proof"]["correction_attempts"] == 0
    assert result["factual"]["reason"] == "mandatory_live_evidence_incomplete"


def test_stream_correction_is_withheld_until_complete_factual_acceptance(monkeypatch):
    import json
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    inputs, paragraphs = _factual_publication_fixture()
    raw = _factual_coverage_content(inputs, {**paragraphs, "roles": "missing writer"})
    correct = _factual_coverage_content(inputs, paragraphs)
    class Response:
        def __enter__(self): return self
        def __exit__(self, *args): return False
        def raise_for_status(self): pass
        def iter_lines(self):
            yield json.dumps({"model": transport.DEFAULT_OLLAMA_MODEL_ID,
                "message": {"content": raw}, "done": True, "done_reason": "stop"})
    monkeypatch.setattr(transport.httpx, "stream", lambda *a, **k: Response())
    monkeypatch.setattr(transport, "ollama_get_json", lambda *a, **k:
        {"models": [{"name": transport.DEFAULT_OLLAMA_MODEL_ID}]})
    for corrected in (correct, raw, "{}"):
        calls = []
        def provider(url, payload, timeout_seconds):
            if payload["options"]["num_predict"] == 1:
                return {"model": payload["model"], "message": {"content": "{"},
                    "done": True, "done_reason": "length", "eval_count": 1, "prompt_eval_count": 1500}
            if payload["options"]["num_predict"] == 256:
                facts = json.loads(payload["messages"][-1]["content"])
                unsupported = ["writer claim is unsupported"] if facts["candidate"]["roles"] == "missing writer" else []
                content = json.dumps({"supported": [1], "contradictions": [], "unsupported_claims": unsupported})
            else:
                calls.append(payload)
                content = corrected
            return {"model": payload["model"], "message": {"content": content}, "done": True, "done_reason": "stop"}
        monkeypatch.setattr(transport, "ollama_post_json", provider)
        events = list(transport.grounded_final_brain_stream(original_text="Current memory", **inputs))
        assert len(calls) == 1
        assert events[-1]["correction_proof"]["FIRST_RAW_FAILED_RESPONSE"] == raw
        assert events[-1]["correction_proof"]["CORRECTION_RESPONSE"] == corrected
        if corrected == correct:
            assert events[-1]["event"] == "done" and events[-1]["factual_valid"]
            assert [e["chunk"] for e in events if e["event"] == "chunk"] == [transport._render_memory_health_answer_sections(correct)]
        else:
            assert events[-1]["event"] == "error" and not events[-1]["factual_valid"]
            assert not any(e["event"] == "chunk" for e in events)



def test_generic_fact_coverage_rejects_omitted_invented_duplicate_and_misplaced_ids(monkeypatch):
    import json
    from copy import deepcopy
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    inputs, paragraphs = _factual_publication_fixture()
    model = json.loads(_factual_coverage_content(inputs, paragraphs))
    def forbidden(*a, **kw):
        raise AssertionError("Coverage failure must precede semantic provider calls")
    monkeypatch.setattr(transport, "ollama_post_json", forbidden)
    monkeypatch.setattr(transport, "ollama_get_json", forbidden)
    omitted = deepcopy(model)
    omitted_id = omitted["coverage"]["covered_fact_ids"].pop()
    unknown = deepcopy(model)
    unknown["coverage"]["covered_fact_ids"].append(1000000)
    duplicate = deepcopy(omitted)
    duplicate["coverage"]["covered_fact_ids"].append(duplicate["coverage"]["covered_fact_ids"][0])
    misplaced = deepcopy(model)
    misplaced["storage"]["covered_fact_ids"].append(misplaced["coverage"]["covered_fact_ids"].pop())
    for value in (omitted, unknown, duplicate, misplaced, {}, []):
        result = transport._validate_memory_self_knowledge_publication(content=json.dumps(value), inputs=inputs, deadline_seconds=30)
        assert not result["valid"] and result["reason"] == "required_fact_coverage_invalid"
    result = transport._validate_memory_self_knowledge_publication(content=json.dumps(omitted), inputs=inputs, deadline_seconds=30)
    assert result["missing_fact_ids"] == [omitted_id]
    result = transport._validate_memory_self_knowledge_publication(content=json.dumps(unknown), inputs=inputs, deadline_seconds=30)
    assert result["unknown_fact_ids"] == [1000000]


def test_coverage_references_do_not_replace_exact_values_or_completeness_flag(monkeypatch):
    import json
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    inputs, paragraphs = _factual_publication_fixture()
    def forbidden(*a, **kw):
        raise AssertionError("Missing immutable facts must precede semantic calls")
    monkeypatch.setattr(transport, "ollama_post_json", forbidden)
    for original, replacement in (("RealNativeOwner", "native_surface"),
            ("RealNativeWriter.append", "native_surface"), ("false", "true"),
            ("2026-01-02T03:04:05Z", "2026-01-03T03:04:05Z")):
        changed = {key: value.replace(original, replacement) for key,value in paragraphs.items()}
        result = transport._validate_memory_self_knowledge_publication(content=_factual_coverage_content(inputs, changed), inputs=inputs, deadline_seconds=30)
        assert result["fact_coverage"]["missing_fact_ids"] == []
        assert not result["valid"] and result["reason"] == "required_exact_facts_missing"


def test_fact_catalog_is_derived_from_mandatory_assertions_and_projection_is_lossless():
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.jarvis_live_read_models import build_jarvis_live_memory_federation_status
    inputs = dict(understanding={}, execution_plan=_typed_memory_self_knowledge_plan(), capability_state=(),
        session_context={}, evidence_bundle={"items": [{"kind": "memory_federation", "observation": build_jarvis_live_memory_federation_status()}]})
    health = transport._bounded_final_brain_inputs(**inputs)[2]["mandatory_answer_facts"]["live_memory_health"]
    projection, catalog = transport._memory_fact_coverage_projection(health)
    assert catalog == dict(enumerate(transport._memory_assertion_leaves(transport._memory_self_knowledge_assertions(health))))
    import json
    assert json.dumps(_restore_live_health_fact_groups(projection), sort_keys=True) == json.dumps(health, sort_keys=True)
    bound = {}
    def walk(value):
        if isinstance(value, list) and len(value) == 2 and isinstance(value[0], list) and value[0] and all(type(i) is int for i in value[0]):
            for i in value[0]:
                assert i not in bound
                bound[i] = value[1]
        elif isinstance(value, dict):
            for child in value.values(): walk(child)
        elif isinstance(value, list):
            for child in value: walk(child)
    walk(projection["evidence"])
    for row in projection["derived_empty_assertions"]:
        for i in row["fact_ids"]:
            assert i not in bound
            bound[i] = row["value"]
    assert bound == {i:value for i,(path,value) in catalog.items()}
    assert sorted(i for ids in projection["required_fact_ids_by_section"].values() for i in ids) == list(catalog)





def test_removed_string_only_compatibility_does_not_bypass_coverage_schema():
    import json
    import pytest
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    legacy = {key: "Legacy paragraph with no fact identity" for key in ("coverage", "storage", "roles", "retrieval", "journals", "domains")}
    with pytest.raises(ValueError, match="grounded_response_invalid_section"):
        transport._render_memory_health_answer_sections(json.dumps(legacy))


def test_one_correction_receives_all_structured_coverage_failures(monkeypatch):
    import json
    import time
    from copy import deepcopy
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    inputs, paragraphs = _factual_publication_fixture()
    correct = _factual_coverage_content(inputs, paragraphs)
    base = json.loads(correct)
    mutations = []
    missing = deepcopy(base)
    missing["coverage"]["covered_fact_ids"].pop()
    mutations.append(missing)
    unknown = deepcopy(base)
    unknown["coverage"]["covered_fact_ids"].append(1000000)
    mutations.append(unknown)
    misplaced = deepcopy(base)
    misplaced["storage"]["covered_fact_ids"].append(misplaced["coverage"]["covered_fact_ids"].pop())
    mutations.append(misplaced)
    duplicate = deepcopy(base)
    duplicate["storage"]["covered_fact_ids"].append(duplicate["coverage"]["covered_fact_ids"][0])
    mutations.append(duplicate)
    monkeypatch.setattr(transport, "ollama_get_json", lambda *a, **k:
        {"models": [{"name": transport.DEFAULT_OLLAMA_MODEL_ID}]})
    for changed in mutations:
        failed = json.dumps(changed)
        first = transport._validate_memory_self_knowledge_publication(content=failed, inputs=inputs, deadline_seconds=30)
        assert first["reason"] == "required_fact_coverage_invalid"
        calls = []
        def provider(url, payload, timeout_seconds):
            assert payload["model"] == transport.DEFAULT_OLLAMA_MODEL_ID
            if payload["options"]["num_predict"] == 1:
                return {"model": payload["model"], "message": {"content": "{"},
                    "done": True, "done_reason": "length", "eval_count": 1, "prompt_eval_count": 1500}
            if payload["options"]["num_predict"] == 256:
                response = json.dumps({"supported": [1], "contradictions": [], "unsupported_claims": []})
            else:
                calls.append(deepcopy(payload))
                feedback = json.loads(payload["messages"][-1]["content"].split("Structured errors: ", 1)[1])
                assert feedback["original_failed_response"] == changed
                assert feedback["errors"]["fact_coverage"] == first["fact_coverage"]
                response = correct
            return {"model": payload["model"], "message": {"content": response}, "done": True, "done_reason": "stop"}
        monkeypatch.setattr(transport, "ollama_post_json", provider)
        payload = transport._grounded_final_brain_payload(original_text="Current memory", **inputs, stream=False)
        outcome = transport._validated_memory_answer_once(content=failed, inputs=inputs, payload=payload,
            deadline_at=time.monotonic()+30)
        assert outcome["valid"] is True
        assert len(calls) == 1
        assert outcome["proof"]["correction_attempts"] == 1
        assert outcome["proof"]["FIRST_VALIDATION_ERRORS"] == first
        assert outcome["response"] == transport._render_memory_health_answer_sections(correct)


def test_typed_memory_stream_requires_same_primary_author_on_every_chunk(monkeypatch):
    import json
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    inputs, paragraphs = _factual_publication_fixture()
    correct = _factual_coverage_content(inputs, paragraphs)
    for models in (("jarvis:helper3b",), (None,), (transport.DEFAULT_OLLAMA_MODEL_ID, "jarvis:coder14b")):
        class Response:
            def __enter__(self): return self
            def __exit__(self, *args): return False
            def raise_for_status(self): pass
            def iter_lines(self):
                for index, model in enumerate(models):
                    value = {"message": {"content": correct if index == 0 else " "},
                        "done": index == len(models)-1, "done_reason": "stop"}
                    if model is not None:
                        value["model"] = model
                    yield json.dumps(value)
        monkeypatch.setattr(transport.httpx, "stream", lambda *a, **k: Response())
        def forbidden(*a, **k):
            raise AssertionError("Wrong or unproven author cannot reach semantic validation or correction")
        monkeypatch.setattr(transport, "ollama_get_json", forbidden)
        monkeypatch.setattr(transport, "ollama_post_json", forbidden)
        events = list(transport.grounded_final_brain_stream(original_text="Current memory", **inputs))
        assert not any(event["event"] == "chunk" for event in events)
        assert events[-1]["event"] == "error"
        assert events[-1]["error_kind"] == "final_brain_unexpected_author_model"
        assert events[-1]["response_text"] == ""
        assert events[-1]["raw_response_text"].strip() == correct
        assert events[-1]["response_model_id"] == (models[-1] or "")
        assert events[-1]["model_call_used"] is False


def test_typed_coverage_generation_schema_is_evidence_bound_and_does_not_author_prose():
    import json
    from copy import deepcopy
    from jsonschema import Draft202012Validator
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    inputs, paragraphs = _factual_publication_fixture()
    payload = transport._grounded_final_brain_payload(original_text="unchanged natural memory question", **inputs, stream=False)
    schema = payload["format"]
    assert isinstance(schema, dict)
    valid = json.loads(_factual_coverage_content(inputs, paragraphs))
    validator = Draft202012Validator(schema)
    assert list(validator.iter_errors(valid)) == []
    common = schema["$defs"]["s"]["properties"]
    assert common["prose"] == {"type": "string", "minLength": 1}
    references = common["covered_fact_ids"]
    all_ids = [i for section in valid.values() for i in section["covered_fact_ids"]]
    assert references["items"] == {"type": "integer", "minimum": min(all_ids), "maximum": max(all_ids)}
    assert references["uniqueItems"] is True
    assert "enum" not in json.dumps(schema)
    assert len(json.dumps(schema, separators=(",", ":"))) < 650
    assert all(item == {"$ref": "#/$defs/s"} for item in schema["properties"].values())
    for mutation in ("omitted", "unknown", "duplicate", "misplaced"):
        failed = deepcopy(valid)
        if mutation == "omitted": failed["coverage"]["covered_fact_ids"].pop()
        elif mutation == "unknown": failed["coverage"]["covered_fact_ids"][0] = 1000000
        elif mutation == "duplicate": failed["coverage"]["covered_fact_ids"][1] = failed["coverage"]["covered_fact_ids"][0]
        else: failed["storage"]["covered_fact_ids"][0] = failed["coverage"]["covered_fact_ids"][0]
        if mutation in {"unknown", "duplicate"}:
            assert list(validator.iter_errors(failed))
        # Completeness and section ownership remain host factual-validation duties.
        check = transport._validate_memory_self_knowledge_publication(content=json.dumps(failed), inputs=inputs, deadline_seconds=0)
        assert not check["valid"] and check["reason"] == "required_fact_coverage_invalid"
    # Grammar is structural only: claiming every ID never proves prose truth.
    invented = deepcopy(valid)
    invented["storage"]["prose"] = "Полная память; все владельцы неизвестны."
    assert list(validator.iter_errors(invented)) == []
    check = transport._validate_memory_self_knowledge_publication(content=json.dumps(invented), inputs=inputs, deadline_seconds=0)
    assert not check["valid"]
    assert payload["model"] == transport.DEFAULT_OLLAMA_MODEL_ID
    assert payload["options"]["num_ctx"] == 4096
    assert payload["options"]["num_predict"] == 1500
    ordinary = transport._grounded_final_brain_payload(original_text="ordinary conversation", understanding={},
        execution_plan={}, evidence_bundle={"items": []}, capability_state=(), stream=False)
    assert "format" not in ordinary


def test_compact_memory_source_value_references_restore_exact_evidence_and_fact_ids():
    import json
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.jarvis_live_read_models import build_jarvis_live_memory_federation_status
    inputs = dict(understanding={}, execution_plan=_typed_memory_self_knowledge_plan(), capability_state=(),
        session_context={}, evidence_bundle={'items': [{'kind': 'memory_federation', 'observation': build_jarvis_live_memory_federation_status()}]})
    health = transport._bounded_final_brain_inputs(**inputs)[2]['mandatory_answer_facts']['live_memory_health']
    plain, catalog = transport._memory_fact_coverage_projection(health)
    compact, compact_catalog = transport._memory_fact_coverage_projection(health, compact_source_values=True)
    assert compact_catalog == catalog
    assert compact['required_fact_ids_by_section'] == plain['required_fact_ids_by_section']
    assert compact['values'] and len(compact['values']) == len(set(compact['values']))
    def expand(value):
        if isinstance(value, dict) and set(value) == {'$v'}:
            return compact['values'][value['$v']]
        if isinstance(value, dict): return {key: expand(child) for key,child in value.items()}
        if isinstance(value, list): return [expand(child) for child in value]
        return value
    assert expand(compact['evidence']) == plain['evidence']
    assert expand(compact['derived_empty_assertions']) == plain['derived_empty_assertions']
    assert len(json.dumps(compact, ensure_ascii=False)) < len(json.dumps(plain, ensure_ascii=False))
    assert json.dumps(_restore_live_health_fact_groups(compact), sort_keys=True) == json.dumps(health, sort_keys=True)


def test_grounded_reference_prose_passes_without_echo_and_presents_exact_source(monkeypatch):
    import json
    from copy import deepcopy
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    inputs, _ = _factual_publication_fixture()
    before = deepcopy(inputs)
    prose = {key: "Подтверждённые факты раздела объясняют соответствующий слой памяти; точные значения доступны по ссылкам."
        for key in ("coverage", "storage", "roles", "retrieval", "journals", "domains")}
    content = _factual_coverage_content(inputs, prose)
    calls = []
    monkeypatch.setattr(transport, "ollama_get_json", lambda *a, **kw: {"models": [{"name": transport.DEFAULT_OLLAMA_MODEL_ID}]})
    def verify(url, payload, timeout_seconds):
        material = json.loads(payload["messages"][-1]["content"])
        calls.append(material)
        assert material["candidate"] == prose
        assert material["covered_fact_ids_by_section"]
        assert material["group_fact_paths"]
        return {"model": payload["model"], "message": {"content": json.dumps({"supported": [1], "contradictions": [], "unsupported_claims": []})}, "done": True, "done_reason": "stop"}
    monkeypatch.setattr(transport, "ollama_post_json", verify)
    result = transport._validate_memory_self_knowledge_publication(content=content, inputs=inputs, deadline_seconds=60)
    assert result["valid"] and len(calls) == 6
    assert not result["missing_exact_assertions"]
    assert result["final_validation_uses_full_evidence"] is True
    health = transport._bounded_final_brain_inputs(**inputs)[2]["mandatory_answer_facts"]["live_memory_health"]
    _, catalog = transport._memory_fact_coverage_projection(health)
    facts = [fact for section in result["evidence_presentation"].values() for fact in section["facts"]]
    assert len(facts) == len(catalog)
    for fact in facts:
        assert (fact["assertion_path"], fact["value"]) == catalog[fact["fact_id"]]
        assert fact["assertion_source_sha256"] == result["assertion_source_sha256"]
    assert {k:v["prose"] for k,v in result["evidence_presentation"].items()} == prose
    assert inputs == before


def test_reference_only_prose_cannot_bypass_full_answer_contradiction_verifier(monkeypatch):
    import json
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import ollama_transport as transport
    inputs, _ = _factual_publication_fixture()
    base = {key: "Факты приведены по подтверждённым ссылкам." for key in ("coverage", "storage", "roles", "retrieval", "journals", "domains")}
    monkeypatch.setattr(transport, "ollama_get_json", lambda *a, **kw: {"models": [{"name": transport.DEFAULT_OLLAMA_MODEL_ID}]})
    for claim in ("Физических хранилищ четыре.", "Пишет native_surface.", "Путь /other/store.jsonl.", "Вся память полностью проинвентаризирована.", "Mempalace владеет conversation memory."):
        paragraphs = {**base, "domains": base["domains"] + claim}
        calls = []
        def verify(url, payload, timeout_seconds):
            material = json.loads(payload["messages"][-1]["content"])
            calls.append(material)
            assert claim in material["candidate"]["domains"]
            assert material["coverage_boundary"]["whole_organism_inventory_complete"] is False
            return {"model": payload["model"], "message": {"content": json.dumps({"supported": [1], "contradictions": [claim], "unsupported_claims": []})}, "done": True, "done_reason": "stop"}
        monkeypatch.setattr(transport, "ollama_post_json", verify)
        result = transport._validate_memory_self_knowledge_publication(content=_factual_coverage_content(inputs, paragraphs), inputs=inputs, deadline_seconds=60)
        assert not result["valid"] and result["reason"] == "semantic_assertions_not_proven"
        assert len(calls) == 1
        assert "evidence_presentation" not in result


def test_grounded_reference_presentation_rejects_unknown_ids_and_does_not_mutate_values():
    from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import GroundedResponseSection
    import pytest
    source = {0:("/storage/path", "/exact/path"), 1:("/coverage/complete", False), 2:("/roles/list", ["owner", "writer"])}
    section = GroundedResponseSection("Авторский текст", (0,1,2))
    result = section.evidence_presentation(source, source_digest="sha256-source")
    assert result["prose"] == section.prose
    assert result["facts"][0]["value"] == "/exact/path"
    assert result["facts"][1]["value"] is False
    result["facts"][2]["value"].append("not a source mutation")
    assert source[2][1] == ["owner", "writer"]
    with pytest.raises(ValueError, match="unknown_fact_id"):
        GroundedResponseSection("Авторский текст", (3,)).evidence_presentation(source, source_digest="source")


# Downstream stream units mock external resource facts, never admission itself.
import pytest as _resource_pytest

@_resource_pytest.fixture(autouse=True)
def _grounded_stream_resource_facts(request, monkeypatch, tmp_path):
    if request.node.originalname not in {'test_streamed_memory_health_is_buffered_until_validated_completion', 'test_factual_failure_blocks_ordinary_and_stream_publication_and_retains_raw', 'test_typed_memory_stream_requires_same_primary_author_on_every_chunk', 'test_stream_correction_is_withheld_until_complete_factual_acceptance'}:
        return
    from tests.ai_orchestration.test_model_admission_transport import acquisition
    acquisition.__wrapped__(monkeypatch, tmp_path)
