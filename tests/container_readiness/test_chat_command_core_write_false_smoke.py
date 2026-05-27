from pathlib import Path


FILES = (
    Path("CONTAINER_DEPLOYMENT/cubes/chat_command/container_contract.yaml"),
    Path("CONTAINER_DEPLOYMENT/cubes/chat_command/runtime_profile.yaml"),
)


def test_chat_command_core_write_is_false() -> None:
    for path in FILES:
        text = path.read_text(encoding="utf-8")
        assert "canonical_write_allowed: false" in text
        assert "canonical_write_allowed: true" not in text
        assert "runtime_mutation_allowed: false" in text
        assert "runtime_mutation_allowed: true" not in text
