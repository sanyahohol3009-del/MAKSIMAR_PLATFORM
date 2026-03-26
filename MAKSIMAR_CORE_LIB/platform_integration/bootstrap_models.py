from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DomainBootstrapState:
    """Bootstrap state for one domain registry."""

    domain_name: str
    total_items: int
    is_loaded: bool


@dataclass(frozen=True, slots=True)
class PlatformBootstrapSnapshot:
    """Unified snapshot of platform bootstrap state."""

    contract_count: int
    config_count: int
    policy_count: int
    runtime_count: int
    event_count: int
    workflow_count: int
    action_count: int
    memory_count: int
    knowledge_count: int
    simulation_count: int
    ai_service_count: int
    voice_count: int
    product_count: int


@dataclass(frozen=True, slots=True)
class PlatformBootstrapContext:
    """Unified platform bootstrap context."""

    contract_validation: DomainBootstrapState
    config_loaders: DomainBootstrapState
    policy_engine: DomainBootstrapState
    runtime_base: DomainBootstrapState
    event_bus: DomainBootstrapState
    workflow_engine: DomainBootstrapState
    action_executor: DomainBootstrapState
    memory_engine: DomainBootstrapState
    knowledge_engine: DomainBootstrapState
    simulation_layer: DomainBootstrapState
    ai_services: DomainBootstrapState
    voice_layer: DomainBootstrapState
    products_layer: DomainBootstrapState
    snapshot: PlatformBootstrapSnapshot
