from __future__ import annotations

from pathlib import Path

from MAKSIMAR_CORE_LIB.voice_layer.voice_loader import load_voice_definition


def test_voice_loader_rejects_missing_schema_version(tmp_path: Path) -> None:
    """Voice loader should reject missing schema_version."""
    file_path = tmp_path / "voice_policy.yaml"
    file_path.write_text(
        "\n".join(
            [
                "policy_id: voice_policy",
                "description: test",
            ]
        ),
        encoding="utf-8",
    )

    result = load_voice_definition(file_path)

    assert result.is_valid is False
    assert result.definition is None
    assert result.error is not None


def test_voice_loader_accepts_valid_definition(tmp_path: Path) -> None:
    """Voice loader should accept valid voice definition."""
    file_path = tmp_path / "voice_policy.yaml"
    file_path.write_text(
        "\n".join(
            [
                "schema_version: voice_policy.v1",
                "policy_id: voice_policy",
                "description: test",
            ]
        ),
        encoding="utf-8",
    )

    result = load_voice_definition(file_path)

    assert result.is_valid is True
    assert result.definition is not None
    assert result.definition.policy_id == "voice_policy"
    assert result.definition.version == "voice_policy.v1"
