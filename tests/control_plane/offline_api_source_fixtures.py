"""Explicit offline provider substitutions for source-delivery acceptance only.

Not production availability/evidence. Real import probes remain unchanged.
"""
import pytest


@pytest.fixture(autouse=True)
def no_external_package_import_probe(monkeypatch):
    from MAKSIMAR_CORE_LIB.action_library_adapters import agent_tooling_runtime_probe as owner
    def unavailable(runtime_python,package_name,import_name):
        return owner.AgentToolingRuntimeProbeResult(
            installed=False,import_probe_passed=False,package_name=package_name,
            import_name=import_name,version_if_available="",runtime_python=str(runtime_python),
            errors=("SYNTHETIC_OFFLINE_IMPORT_PROBE_NOT_EXECUTED",),import_attempted=False,
            runtime_capability_verified=False)
    monkeypatch.setattr(owner,"_probe_import_with_runtime_python",unavailable)
