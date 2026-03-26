from __future__ import annotations

from MAKSIMAR_CORE_LIB.platform_integration.bootstrap_models import (
    DomainBootstrapState,
    PlatformBootstrapContext,
)
from MAKSIMAR_CORE_LIB.platform_integration.health_models import (
    PlatformHealthDomain,
    PlatformHealthSnapshot,
)


def _to_health_domain(state: DomainBootstrapState) -> PlatformHealthDomain:
    """Convert bootstrap state to health domain state."""
    status = "ok" if state.is_loaded else "failed"
    return PlatformHealthDomain(
        domain_name=state.domain_name,
        total_items=state.total_items,
        is_loaded=state.is_loaded,
        status=status,
    )


def build_health_domains(
    context: PlatformBootstrapContext,
) -> list[PlatformHealthDomain]:
    """Build per-domain health states from bootstrap context."""
    states = [
        context.contract_validation,
        context.config_loaders,
        context.policy_engine,
        context.runtime_base,
        context.event_bus,
        context.workflow_engine,
        context.action_executor,
        context.memory_engine,
        context.knowledge_engine,
        context.simulation_layer,
        context.ai_services,
        context.voice_layer,
        context.products_layer,
    ]

    return [_to_health_domain(state) for state in states]


def build_platform_health_snapshot(
    context: PlatformBootstrapContext,
) -> PlatformHealthSnapshot:
    """Build unified platform health snapshot."""
    domains = build_health_domains(context)

    total_domains = len(domains)
    loaded_domains = sum(1 for domain in domains if domain.is_loaded)
    failed_domains = total_domains - loaded_domains
    total_items = sum(domain.total_items for domain in domains)

    overall_status = "ok" if failed_domains == 0 else "failed"

    return PlatformHealthSnapshot(
        overall_status=overall_status,
        total_domains=total_domains,
        loaded_domains=loaded_domains,
        failed_domains=failed_domains,
        total_items=total_items,
    )
