from __future__ import annotations

import ast
from pathlib import Path

import pytest

from tools.jarvis_live_runtime.voice_response_cleaner import (
    build_output_channels, clean_voice_response, guarded_voice_response,
    strip_reasoning_blocks,
)

ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("text", [
    "review_status=PARTIAL_PENDING_INDEPENDENT_REVIEW training_eligible=false",
    "training_eligible=true training_export_allowed=false candidate_created=false",
    "review_status=unknown training_eligible=unknown",
    "review_status=pending reviewer=unknown",
    "review_status=rejected reviewer=reviewer_17",
    "review_status=approved reviewer=reviewer_17",
    'execution_allowed=false approval_required=true risk_class=HIGH',
    '{"review_status":"pending","training_eligible":false}',
    '{"review_status":"approved","training_eligible":true}',
    '{"route":"SOURCE_DOCUMENT","training_eligible":false}',
    '{"review_status":"pending", "training_eligible":false',
    "-5.25 degrees; 13 views; 4 stores; ratio=0.125",
    "2026-10-18T11:09:10+02:00 /home/aleksandr/data.db",
    "Обучение не разрешено. Мне не нужна помощь.",
    "Training is not allowed; 0 receipts exist.",
    "Training ist nicht erlaubt; keine Freigabe.",
    "Принял, проверка ещё не завершена.",
    "Hello, the review is pending.",
    "Review: ❌; approval: unknown; language=C#; delta=±0.5",
])
def test_fact_values_survive_both_channels(text: str) -> None:
    channels = build_output_channels(text)
    assert channels["visible_text"] == text
    assert channels["spoken_text"] == text
    assert clean_voice_response(text) == text
    assert guarded_voice_response(text) == text


def test_terminal_uses_existing_sanitizer_without_spoken_projection() -> None:
    source = (ROOT / "tools/jarvis_live_runtime/jarvis_live_stream_events.py").read_text()
    node = next(n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == "_sanitize_model_output")
    namespace = {"strip_reasoning_blocks": strip_reasoning_blocks}
    exec(compile(ast.Module(body=[node], type_ignores=[]), source, "exec"), namespace)
    text = 'review_status=pending training_eligible=false **13** {"count":4}'
    assert namespace["_sanitize_model_output"](text) == text
    assert namespace["_sanitize_model_output"]("<think>private</think>" + text) == text




def test_reasoning_removal_does_not_invent_publication() -> None:
    assert clean_voice_response("<think>private</think>") == ""
    assert build_output_channels("<think>private</think>")["spoken_text"] == ""


def test_trace_prefix_does_not_erase_facts_on_same_line() -> None:
    spoken = build_output_channels("[trace] review_status=pending training_eligible=false")["spoken_text"]
    assert "review_status=pending" in spoken
    assert "training_eligible=false" in spoken


def test_formatting_preserves_negative_values_and_pending_status() -> None:
    spoken = build_output_channels("# Status\n- review_status=pending\n- training_eligible=false\n- temperature=-5.25")["spoken_text"]
    for fact in ("review_status=pending", "training_eligible=false", "temperature=-5.25"):
        assert fact in spoken
