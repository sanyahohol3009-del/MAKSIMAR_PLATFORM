from __future__ import annotations

from typing import Any, Iterator

from MAKSIMAR_CORE_LIB.runtime_activation import build_default_capability_activation_matrix
from MAKSIMAR_SERVER.AI_ORCHESTRATION.project_workspace_tools import (
    _project_tree_summary,
    read_file_outline,
    read_file_snippet,
    repo_files,
    repo_git_status,
    repo_import_graph,
    repo_search,
    repo_tree,
)
from MAKSIMAR_SERVER.AI_ORCHESTRATION.session_memory_store import (
    DANGEROUS_MEMORY_FLAGS,
    SESSION_STATE_PATH,
    _empty_session_state,
    _load_session_state,
    _memory_truth_contract,
    _save_session_state,
    _session_turn_log_path,
    _stable_style_profile_from_state,
)
from MAKSIMAR_SERVER.AI_ORCHESTRATION.jarvis_live_read_models import (
    build_jarvis_live_memory_federation_status,
)
from tools.jarvis_live_runtime.jarvis_live_read_models import (
    build_jarvis_live_project_status_read_model,
    build_jarvis_live_tool_catalog_read_model,
    build_project_workspace_read_model,
    model_runtime_status,
    status_tools,
)
from tools.jarvis_live_runtime.jarvis_live_stream_events import (
    _command_timeout_seconds,
    write_stream_event_safely,
)


def run_jarvis_live_brain_once(
    user_text: str,
    session_id: str = "default",
    command_timeout_seconds: float | None = None,
) -> dict[str, Any]:
    """Compatibility facade: all user text enters the canonical Semantic Spine."""
    del command_timeout_seconds
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.jarvis_live_brain_loop_server_adapter import (
        run_jarvis_live_brain_once as run_canonical_brain_once,
    )

    return run_canonical_brain_once(user_text, session_id=session_id)


def stream_jarvis_live_brain_response(
    user_text: str,
    session_id: str = "default",
    ollama_timeout_seconds: float | None = None,
) -> Iterator[dict[str, Any]]:
    """Compatibility facade: stream one canonical semantic result without rerouting text."""
    del ollama_timeout_seconds
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.jarvis_live_brain_loop_server_adapter import (
        stream_jarvis_live_brain_response as stream_canonical_brain_response,
    )

    yield from stream_canonical_brain_response(user_text, session_id=session_id)


def build_jarvis_live_brain_health() -> dict[str, Any]:
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.jarvis_live_read_models import build_jarvis_live_brain_health as canonical
    return canonical()


def build_jarvis_live_session_status() -> dict[str, Any]:
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.jarvis_live_read_models import build_jarvis_live_session_status as canonical
    return canonical()


def reset_jarvis_live_session() -> dict[str, Any]:
    _save_session_state(_empty_session_state())
    return build_jarvis_live_session_status()


def _format_activation_matrix_answer() -> str:
    matrix = build_default_capability_activation_matrix().to_read_model()
    lines = [
        "Activation Matrix: capability_scoped_policy=active; "
        "protected_execution_requires_approval=true.",
        "JARVIS остаётся senior/canonical authority.",
    ]
    for entry in matrix["entries"]:
        lines.append(
            f"- {entry['capability_id']}: {entry['activation_level']}; "
            f"runtime_started={str(entry['runtime_started']).lower()}"
        )
    return "\n".join(lines)


def _looks_like_incomplete_model_output(
    text: str,
    *,
    grounded_answer: bool = False,
) -> tuple[bool, str]:
    """Validate response completeness; this does not select a route or operation."""
    response = str(text or "").strip()
    if not response:
        return True, "model_response_looks_incomplete:empty_response"
    if response.endswith(("(", "[", "{", "`", " -", ":\n -")):
        return True, "model_response_looks_incomplete:broken_suffix"
    if grounded_answer and response[-1] not in ".!?)]}\"'":
        return True, "model_response_looks_incomplete:missing_terminal_punctuation"
    return False, ""
