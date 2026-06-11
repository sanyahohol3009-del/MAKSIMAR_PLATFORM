from tools.jarvis_live_runtime.jarvis_live_brain_loop import (
    build_jarvis_live_brain_context,
    build_jarvis_live_memory_federation_status,
    run_jarvis_live_brain_once,
    stream_jarvis_live_brain_response,
)


def test_memory_federation_inventory_reports_existing_surfaces() -> None:
    status = build_jarvis_live_memory_federation_status()
    surfaces = {surface["surface_id"]: surface for surface in status["surfaces"]}

    assert status["memory_federation_available"] is True
    assert status["memory_surfaces_detected_count"] >= 6
    assert "runtime_history_store" in surfaces
    assert "memory_engine_registry" in surfaces
    assert "enterprise_business_memory" in surfaces
    assert "regulatory_memory_foundation" in surfaces
    assert "mempalace_read_only_sandbox" in surfaces
    assert surfaces["mempalace_read_only_sandbox"]["status"] == "sandbox_only"
    assert status["mempalace_status"] in {
        "sandbox_only_read_only",
        "sandbox_only_manual_review_required",
        "not_connected",
    }
    assert status["canonical_memory_write_allowed"] is False
    assert status["pc_control_allowed"] is False


def test_context_assembly_includes_mocked_multiple_memory_surfaces(monkeypatch) -> None:
    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop

    monkeypatch.setattr(
        brain_loop,
        "_retrieve_history_snippets",
        lambda text, deep: ["runtime_history_store: MAKSIMAR project history"],
    )
    monkeypatch.setattr(
        brain_loop,
        "_retrieve_enterprise_memory_snippets",
        lambda text: ["enterprise_business_memory: sovereign AI sales memory"],
    )
    monkeypatch.setattr(
        brain_loop,
        "_retrieve_regulatory_memory_snippets",
        lambda text: ["regulatory_memory_foundation: laws memory"],
    )
    monkeypatch.setattr(
        brain_loop,
        "_retrieve_mempalace_status_snippets",
        lambda text: ["mempalace_read_only_sandbox: sandbox only"],
    )

    context = build_jarvis_live_brain_context(
        "Что у нас есть по продаже суверенного ИИ и regulatory memory MemPalace?",
        {"recent_turns": [], "rolling_summary": "", "active_topics": []},
    )
    read_model = context.to_read_model()

    assert read_model["retrieved_snippet_count"] >= 4
    assert "runtime_history_store" in read_model["retrieval_surfaces_used"]
    assert "enterprise_business_memory" in read_model["retrieval_surfaces_used"]
    assert "regulatory_memory_foundation" in read_model["retrieval_surfaces_used"]
    assert "mempalace_read_only_sandbox" in read_model["retrieval_surfaces_used"]
    assert read_model["canonical_memory_write_allowed"] is False
    assert read_model["pc_control_allowed"] is False


def test_permanent_memory_write_request_is_rejected_without_canonical_write(monkeypatch) -> None:
    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop

    monkeypatch.setattr(brain_loop, "SESSION_MEMORY_ROOT", brain_loop.PROJECT_ROOT)
    monkeypatch.setattr(brain_loop, "_load_session_state", lambda: brain_loop._empty_session_state())
    monkeypatch.setattr(brain_loop, "_save_session_state", lambda state: None)

    payload = run_jarvis_live_brain_once("Джарвис, запиши это в постоянную память.", session_id="test")

    assert "canonical_memory_write_allowed=false" in payload["llm_response"]
    assert payload["canonical_memory_write_allowed"] is False
    assert payload["pc_control_allowed"] is False


def test_stream_start_and_done_include_memory_federation_fields(monkeypatch) -> None:
    import tools.jarvis_live_runtime.jarvis_live_brain_loop as brain_loop

    monkeypatch.setattr(brain_loop, "SESSION_MEMORY_ROOT", brain_loop.PROJECT_ROOT)
    monkeypatch.setattr(brain_loop, "_load_session_state", lambda: brain_loop._empty_session_state())
    monkeypatch.setattr(brain_loop, "_save_session_state", lambda state: None)

    events = list(stream_jarvis_live_brain_response("Джарвис, видишь ли ты runtime_history_store?", session_id="test"))
    start = events[0]
    done = events[-1]

    assert start["memory_federation_available"] is True
    assert "retrieval_surfaces_used" in start
    assert "mempalace_status" in start
    assert done["memory_federation_available"] is True
    assert "retrieval_surfaces_used" in done
    assert "mempalace_status" in done
    assert done["canonical_memory_write_allowed"] is False
    assert done["pc_control_allowed"] is False
