from pathlib import Path


FILES = (
    Path("CONTAINER_DEPLOYMENT/cubes/chat_command/container_contract.yaml"),
    Path("CONTAINER_DEPLOYMENT/cubes/chat_command/network_policy.yaml"),
    Path("CONTAINER_DEPLOYMENT/cubes/chat_command/runtime_profile.yaml"),
)


def test_chat_command_dashboard_control_and_execution_are_false() -> None:
    combined = "\n".join(path.read_text(encoding="utf-8") for path in FILES)

    assert "dashboard_control_allowed: false" in combined
    assert "dashboard_control_allowed: true" not in combined
    assert "direct_execution_allowed: false" in combined
    assert "direct_execution_allowed: true" not in combined
    assert "external_network_access_allowed: false" in combined
    assert "external_network_access_allowed: true" not in combined
    assert "host_network_allowed: false" in combined
    assert "privileged_allowed: false" in combined
