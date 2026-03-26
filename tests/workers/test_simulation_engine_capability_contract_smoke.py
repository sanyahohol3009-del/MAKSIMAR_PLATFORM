from __future__ import annotations

from MAKSIMAR_SERVER.WORKERS.simulation_worker import (
    build_simulation_engine_capability_contract,
)


def test_simulation_engine_capability_contract_builds() -> None:
    """Simulation engine capability contract should build successfully."""
    contract = build_simulation_engine_capability_contract()

    assert contract.engine_id == "sim_engine_python_001"
    assert contract.engine_kind == "simulation_engine"
    assert contract.engine_version == "1.0.0"
    assert contract.contract_version == "1.0"
    assert contract.language_runtime == "python"
    assert contract.latency_profile == "balanced"
    assert contract.expected_latency_budget_ms == 150


def test_simulation_engine_capability_contract_contains_runtime_and_security_fields() -> None:
    """Simulation engine capability contract should expose scheduling and security metadata."""
    contract = build_simulation_engine_capability_contract()

    assert contract.expected_cpu_load == "medium"
    assert contract.expected_ram_profile == "moderate"
    assert contract.requires_gpu is False
    assert contract.required_gpu_class == "cpu_only"
    assert contract.requires_native_runtime is False
    assert contract.sandbox_required is True
    assert contract.network_access_required is False
    assert contract.write_to_core_allowed is False


def test_simulation_engine_capability_contract_contains_backend_and_language_data() -> None:
    """Simulation engine capability contract should expose backend and multilingual metadata."""
    contract = build_simulation_engine_capability_contract()

    assert "control_validation" in contract.supported_workloads
    assert "safety_regression" in contract.supported_workloads
    assert "runtime_pressure_probe" in contract.supported_workloads

    assert "python" in contract.compatible_backends
    assert "fallback" in contract.fallback_backends
    assert contract.fallback_available is True

    assert "ru" in contract.supported_languages
    assert "de" in contract.supported_languages
    assert "Latin" in contract.supported_scripts
    assert "Cyrillic" in contract.supported_scripts
