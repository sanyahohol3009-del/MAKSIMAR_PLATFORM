from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.platform_integration.bootstrap_models import (
    PlatformBootstrapContext,
)


@dataclass(frozen=True, slots=True)
class PlatformSummaryLine:
    """One human-readable bootstrap summary line."""

    domain_name: str
    total_items: int
    is_loaded: bool


def build_platform_summary(
    context: PlatformBootstrapContext,
) -> list[PlatformSummaryLine]:
    """Convert platform bootstrap context into summary lines."""
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

    return [
        PlatformSummaryLine(
            domain_name=state.domain_name,
            total_items=state.total_items,
            is_loaded=state.is_loaded,
        )
        for state in states
    ]
