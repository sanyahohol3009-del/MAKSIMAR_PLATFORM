from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.media_memory import build_generated_media_metadata


def test_generated_media_metadata_models_smoke() -> None:
    metadata = build_generated_media_metadata()

    assert metadata.template_binding_required is True
    assert metadata.render_artifact_logging_required is True
    assert metadata.provenance_visible is True
