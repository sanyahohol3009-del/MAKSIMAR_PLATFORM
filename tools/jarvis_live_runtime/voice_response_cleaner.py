from __future__ import annotations

import json
import re

from tools.jarvis_live_runtime.voice_personality_policy_contract import (
    FORBIDDEN_GENERIC_TAILS,
)


THINK_MARKERS: tuple[tuple[str, str], ...] = (
    ("<think>", "</think>"),
    ("<thinking>", "</thinking>"),
    ("Thinking...", "...done thinking."),
    ("thinking...", "...done thinking."),
)

# Presentation metadata only. Permission, review and learning fields are facts.
PROTOCOL_MARKER_PREFIXES: tuple[str, ...] = (
    "selected_capability_id=",
    "trace_id=",
    "debug=",
)
_INLINE_PROTOCOL_MARKER_RE = re.compile(
    r"(?:^|[\s|])(?:selected_capability_id|trace_id|debug)=[^\s|]+",
    flags=re.IGNORECASE,
)
_JSONISH_RE = re.compile(r"\{[^{}]*:[^{}]*\}|\[[^\[\]]*:[^\[\]]*\]")


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


def clean_spoken_output(text: str, mode: str = "command") -> str:
    cleaned = strip_reasoning_blocks(text)
    if str(mode).casefold() in {"dictation", "code"}:
        return " ".join(cleaned.split())
    cleaned = _strip_protocol_markers(cleaned)
    # Never erase unknown JSON or arbitrary key=value evidence. Only an object
    # consisting entirely of known presentation metadata may be omitted.
    for match in tuple(_JSONISH_RE.finditer(cleaned)):
        try:
            metadata = json.loads(match.group())
        except (ValueError, TypeError):
            continue
        if isinstance(metadata, dict) and metadata and set(metadata) <= {"route", "selected_capability_id"}:
            cleaned = cleaned.replace(match.group(), " ")
    cleaned = _normalize_spoken_formatting(cleaned)
    cleaned = " ".join(cleaned.split())
    for marker in FORBIDDEN_GENERIC_TAILS:
        # Remove only a complete boilerplate tail, never a phrase inside a
        # factual statement such as "Мне не нужна помощь".
        if cleaned.endswith(marker):
            prefix = cleaned[:-len(marker)].rstrip()
            if not prefix or prefix.endswith((".", "!", "?")):
                cleaned = prefix

    cleaned = " ".join(cleaned.split())
    return " ".join(cleaned.split())


def clean_voice_response(text: str, mode: str = "command") -> str:
    return clean_spoken_output(text, mode=mode)


def build_output_channels(text: str, mode: str = "command") -> dict[str, str]:
    visible_text = str(text or "").strip()
    return {
        "visible_text": visible_text,
        "spoken_text": clean_spoken_output(visible_text, mode=mode),
    }


def guarded_voice_response(text: str, fallback: str = "Принял, брат. Держу курс.") -> str:
    cleaned = clean_voice_response(text)
    if not cleaned:
        return fallback
    return cleaned


def _strip_protocol_markers(text: str) -> str:
    kept_lines: list[str] = []
    for raw_line in str(text or "").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        lowered = line.casefold()
        if any(prefix in lowered for prefix in PROTOCOL_MARKER_PREFIXES):
            line = _remove_inline_protocol_markers(line)
        if line.strip():
            kept_lines.append(line.strip())
    return "\n".join(kept_lines)


def _remove_inline_protocol_markers(text: str) -> str:
    cleaned = _INLINE_PROTOCOL_MARKER_RE.sub(" ", str(text))
    kept_parts: list[str] = []
    for segment in cleaned.split(" | "):
        lowered = segment.strip().casefold()
        if not lowered:
            continue
        if any(lowered.startswith(prefix) for prefix in PROTOCOL_MARKER_PREFIXES):
            continue
        kept_parts.append(segment.strip())
    return " ".join(kept_parts).strip()


def _normalize_spoken_formatting(text: str) -> str:
    # Unknown punctuation/symbols may carry a factual sign or identifier.
    # The presentation layer has no authority to reinterpret them.
    return " ".join(str(text or "").split())
