from pathlib import Path


SUPERVISOR = Path("SUPERVISOR/process_supervisor.py")


def _source() -> str:
    return SUPERVISOR.read_text(encoding="utf-8")


def test_process_supervisor_starts_control_plane_with_helper_classifier_env() -> None:
    source = _source()

    assert "def build_environment()" in source
    assert '"JARVIS_HELPER_CLASSIFIER_ENABLED", "true"' in source
    assert '"JARVIS_HELPER_MODEL", "jarvis:helper3b"' in source
    assert '"OLLAMA_KEEP_ALIVE", "30m"' in source
    assert '"OLLAMA_NUM_PARALLEL", "1"' in source
    assert '"OLLAMA_MAX_LOADED_MODELS", "1"' in source
    assert "env=build_environment()" in source


def test_process_supervisor_preserves_control_plane_command_and_no_shell() -> None:
    source = _source()

    assert "CONTROL_PLANE.api_server:app" in source
    assert '"uvicorn"' in source
    assert "shell=True" not in source
    assert "subprocess.Popen(" in source
