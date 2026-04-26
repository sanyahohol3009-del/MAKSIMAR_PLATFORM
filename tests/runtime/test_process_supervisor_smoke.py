from __future__ import annotations

from SUPERVISOR.process_supervisor import build_command


def test_build_command_uses_uvicorn_module() -> None:
    command = build_command()

    assert "-m" in command
    assert "uvicorn" in command
    assert "CONTROL_PLANE.api_server:app" in command


def test_build_command_uses_project_python() -> None:
    command = build_command()

    assert command[0].endswith("/python")
    assert ".venv/bin/python" in command[0] or "/venv/bin/python" in command[0]
