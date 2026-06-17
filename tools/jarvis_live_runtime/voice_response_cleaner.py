from __future__ import annotations

from tools.jarvis_live_runtime.voice_personality_policy_contract import (
    FORBIDDEN_GENERIC_TAILS,
)


THINK_MARKERS: tuple[tuple[str, str], ...] = (
    ("<think>", "</think>"),
    ("<thinking>", "</thinking>"),
    ("Thinking...", "...done thinking."),
    ("thinking...", "...done thinking."),
)


def strip_reasoning_blocks(text: str) -> str:
    cleaned = text or ""
    lowered = cleaned.casefold()

    for start_marker, end_marker in THINK_MARKERS:
        start_key = start_marker.casefold()
        end_key = end_marker.casefold()

        while start_key in lowered:
            start = lowered.find(start_key)
            end = lowered.find(end_key, start + len(start_key))
            if end == -1:
                cleaned = cleaned[:start]
            else:
                cleaned = cleaned[:start] + cleaned[end + len(end_marker):]
            lowered = cleaned.casefold()

    return cleaned.strip()


def contains_forbidden_generic_tail(text: str) -> bool:
    lowered = (text or "").casefold()
    return any(marker.casefold() in lowered for marker in FORBIDDEN_GENERIC_TAILS)


def clean_voice_response(text: str) -> str:
    cleaned = strip_reasoning_blocks(text)
    cleaned = " ".join(cleaned.split())

    for marker in FORBIDDEN_GENERIC_TAILS:
        cleaned = cleaned.replace(marker, "").strip()

    cleaned = " ".join(cleaned.split())
    return cleaned


def guarded_voice_response(text: str, fallback: str = "Принял, брат. Держу курс.") -> str:
    cleaned = clean_voice_response(text)
    if not cleaned:
        return fallback
    if contains_forbidden_generic_tail(cleaned):
        return fallback
    return cleaned
