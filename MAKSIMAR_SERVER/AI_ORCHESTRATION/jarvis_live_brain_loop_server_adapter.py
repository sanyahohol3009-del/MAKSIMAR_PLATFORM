from __future__ import annotations

import json
from typing import Any, Iterator
from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import FinalBrainPort, RequestDeadline
from MAKSIMAR_SERVER.AI_ORCHESTRATION.project_workspace_tools import (
    read_file_outline, read_file_snippet, repo_files, repo_git_status,
    repo_import_graph, repo_search, repo_tree,
)
from MAKSIMAR_SERVER.AI_ORCHESTRATION.jarvis_live_read_models import (
    build_jarvis_live_project_status_read_model,
    build_jarvis_live_tool_catalog_read_model,
    build_project_workspace_read_model, model_runtime_status, status_tools,
)
from MAKSIMAR_SERVER.AI_ORCHESTRATION.ollama_transport import (
    DEFAULT_OLLAMA_MODEL_ID,
    build_model_call_timeout_truth,
    grounded_final_brain_call,
    grounded_final_brain_stream,
)


def build_jarvis_live_brain_health() -> dict[str, Any]:
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.jarvis_live_read_models import build_jarvis_live_brain_health as canonical
    return canonical()


def build_jarvis_live_session_status() -> dict[str, Any]:
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.jarvis_live_read_models import build_jarvis_live_session_status as canonical
    return canonical()


def run_jarvis_live_brain_once(user_text: str, session_id: str = "windows_voice_edge") -> dict[str, Any]:
    """Compatibility entrypoint migrated to the canonical semantic /hot turn."""
    from CONTROL_PLANE.api_server import jarvis_live_hot

    response = jarvis_live_hot({
        "text": user_text,
        "session_id": session_id,
        "input_channel": "windows_voice_edge",
        "identity": {
            "identity_id": "unknown",
            "source": "voice_unverified",
            "profile_type": "unknown",
            "verified": False,
            "trusted_session": False,
        },
    })
    result = response.get("result")
    return dict(result) if isinstance(result, dict) else dict(response)


def stream_jarvis_live_brain_response(
    user_text: str,
    session_id: str = "windows_voice_edge",
) -> Iterator[dict[str, Any]]:
    """Yield compatibility events from one canonical semantic result, without routing text."""
    result = run_jarvis_live_brain_once(user_text, session_id=session_id)
    response_text = str(result.get("response_text", result.get("llm_response", ""))).strip()
    yield {"event": "start", "status": "accepted", "orchestration_path": "canonical_semantic_turn_v2"}
    if response_text:
        yield {"event": "chunk", "text": response_text, "chunk": response_text}
    yield {
        "event": "done",
        "response_text": response_text,
        "llm_response": response_text,
        **result,
    }


def write_stream_event_safely(write_callable: Any, event: dict[str, Any]) -> bool:
    try:
        write_callable(json.dumps(event, ensure_ascii=False) + "\n")
    except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
        print("[WARNING] Client disconnected before receiving response")
        return False
    return True


























def run_grounded_final_brain(**payload: Any) -> dict[str, Any]:
    """Public server facade for the existing grounded Final Brain implementation."""
    return grounded_final_brain_call(**payload)




class ExistingFinalBrainAdapter(FinalBrainPort):
    def answer(self, *, deadline: RequestDeadline, **payload: Any) -> dict[str, Any]:
        timeout_truth = build_model_call_timeout_truth(
            DEFAULT_OLLAMA_MODEL_ID,
            deadline_remaining_seconds=deadline.remaining(),
        )
        timeout = float(timeout_truth["effective_transport_timeout_seconds"])
        if timeout <= 0 or deadline.cancelled:
            raise TimeoutError("final_brain_deadline_exceeded")
        result = grounded_final_brain_call(timeout_truth=timeout_truth, **payload)
        if deadline.cancelled:
            raise TimeoutError("final_brain_deadline_exceeded")
        return result

    def stream_answer(self, *, deadline: RequestDeadline, **payload: Any) -> Iterator[dict[str, Any]]:
        timeout_truth = build_model_call_timeout_truth(
            DEFAULT_OLLAMA_MODEL_ID,
            deadline_remaining_seconds=deadline.remaining(),
        )
        timeout = float(timeout_truth["effective_transport_timeout_seconds"])
        if timeout <= 0 or deadline.cancelled:
            yield {"event": "error", "error_kind": "final_brain_deadline_exceeded",
                   "error_message": "Final Brain deadline exceeded", "response_text": ""}
            return
        for event in grounded_final_brain_stream(timeout_truth=timeout_truth, **payload):
            if deadline.cancelled:
                yield {"event": "error", "error_kind": "final_brain_deadline_exceeded",
                       "error_message": "Final Brain deadline exceeded", "response_text": ""}
                return
            yield event
