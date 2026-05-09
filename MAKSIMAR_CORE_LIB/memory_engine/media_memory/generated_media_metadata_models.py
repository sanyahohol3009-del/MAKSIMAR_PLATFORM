from __future__ import annotations

import re
from dataclasses import dataclass


_GENERATED_ID_PATTERN = re.compile(r"^generated_media_[a-z][a-z0-9_]*$")


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _ensure_bool(value: bool, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field_name} must be bool")
    return value


@dataclass(frozen=True, slots=True)
class GeneratedMediaMetadata:
    """Metadata for generated image/video/audio/render outputs."""

    generated_media_id: str
    prompt_ref: str
    template_ref: str
    render_trace_ref: str
    output_artifact_ref: str
    template_binding_required: bool
    render_artifact_logging_required: bool
    provenance_visible: bool

    def __post_init__(self) -> None:
        generated_media_id = _ensure_non_empty_str(
            self.generated_media_id,
            "generated_media_id",
        )
        prompt_ref = _ensure_non_empty_str(self.prompt_ref, "prompt_ref")
        template_ref = _ensure_non_empty_str(self.template_ref, "template_ref")
        render_trace_ref = _ensure_non_empty_str(
            self.render_trace_ref,
            "render_trace_ref",
        )
        output_artifact_ref = _ensure_non_empty_str(
            self.output_artifact_ref,
            "output_artifact_ref",
        )

        if not _GENERATED_ID_PATTERN.fullmatch(generated_media_id):
            raise ValueError(f"Invalid generated_media_id: {generated_media_id}")

        for field_name in (
            "template_binding_required",
            "render_artifact_logging_required",
            "provenance_visible",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.template_binding_required:
            raise ValueError("template_binding_required must be True")
        if not self.render_artifact_logging_required:
            raise ValueError("render_artifact_logging_required must be True")
        if not self.provenance_visible:
            raise ValueError("provenance_visible must be True")

        object.__setattr__(self, "generated_media_id", generated_media_id)
        object.__setattr__(self, "prompt_ref", prompt_ref)
        object.__setattr__(self, "template_ref", template_ref)
        object.__setattr__(self, "render_trace_ref", render_trace_ref)
        object.__setattr__(self, "output_artifact_ref", output_artifact_ref)
