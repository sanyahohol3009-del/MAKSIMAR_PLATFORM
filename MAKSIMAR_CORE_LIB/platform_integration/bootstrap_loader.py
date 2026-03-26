from __future__ import annotations

from MAKSIMAR_CORE_LIB.action_executor import list_action_definitions
from MAKSIMAR_CORE_LIB.ai_services import list_service_definitions
from MAKSIMAR_CORE_LIB.contract_validation.file_loader import collect_contract_files
from MAKSIMAR_CORE_LIB.config_loaders.file_loader import collect_yaml_files
from MAKSIMAR_CORE_LIB.config_loaders.root_registry import get_config_roots
from MAKSIMAR_CORE_LIB.event_bus import read_event_journal
from MAKSIMAR_CORE_LIB.knowledge_engine import list_knowledge_definitions
from MAKSIMAR_CORE_LIB.memory_engine import list_memory_definitions
from MAKSIMAR_CORE_LIB.platform_integration.bootstrap_models import (
    DomainBootstrapState,
    PlatformBootstrapContext,
    PlatformBootstrapSnapshot,
)
from MAKSIMAR_CORE_LIB.policy_engine import list_policy_definitions
from MAKSIMAR_CORE_LIB.products_layer import list_product_definitions
from MAKSIMAR_CORE_LIB.runtime_base import list_runtime_documents
from MAKSIMAR_CORE_LIB.shared_services.path_resolver import PATHS
from MAKSIMAR_CORE_LIB.simulation_layer import list_simulation_definitions
from MAKSIMAR_CORE_LIB.voice_layer import list_voice_definitions
from MAKSIMAR_CORE_LIB.workflow_engine import list_workflow_definitions


def _build_state(domain_name: str, total_items: int) -> DomainBootstrapState:
    """Build one domain bootstrap state."""
    return DomainBootstrapState(
        domain_name=domain_name,
        total_items=total_items,
        is_loaded=True,
    )


def _count_all_configs() -> int:
    """Count all config files from registered config roots."""
    total = 0
    for root in get_config_roots():
        total += len(collect_yaml_files(root.path))
    return total


def build_platform_bootstrap_context() -> PlatformBootstrapContext:
    """Build unified platform bootstrap context."""
    contract_count = len(collect_contract_files(PATHS.contracts_root))
    config_count = _count_all_configs()
    policy_count = len(list_policy_definitions())
    runtime_count = len(list_runtime_documents("project_runtime"))
    event_count = len(read_event_journal())
    workflow_count = len(list_workflow_definitions())
    action_count = len(list_action_definitions())
    memory_count = len(list_memory_definitions())
    knowledge_count = len(list_knowledge_definitions())
    simulation_count = len(list_simulation_definitions())
    ai_service_count = len(list_service_definitions())
    voice_count = len(list_voice_definitions())
    product_count = len(list_product_definitions())

    snapshot = PlatformBootstrapSnapshot(
        contract_count=contract_count,
        config_count=config_count,
        policy_count=policy_count,
        runtime_count=runtime_count,
        event_count=event_count,
        workflow_count=workflow_count,
        action_count=action_count,
        memory_count=memory_count,
        knowledge_count=knowledge_count,
        simulation_count=simulation_count,
        ai_service_count=ai_service_count,
        voice_count=voice_count,
        product_count=product_count,
    )

    return PlatformBootstrapContext(
        contract_validation=_build_state("contract_validation", contract_count),
        config_loaders=_build_state("config_loaders", config_count),
        policy_engine=_build_state("policy_engine", policy_count),
        runtime_base=_build_state("runtime_base", runtime_count),
        event_bus=_build_state("event_bus", event_count),
        workflow_engine=_build_state("workflow_engine", workflow_count),
        action_executor=_build_state("action_executor", action_count),
        memory_engine=_build_state("memory_engine", memory_count),
        knowledge_engine=_build_state("knowledge_engine", knowledge_count),
        simulation_layer=_build_state("simulation_layer", simulation_count),
        ai_services=_build_state("ai_services", ai_service_count),
        voice_layer=_build_state("voice_layer", voice_count),
        products_layer=_build_state("products_layer", product_count),
        snapshot=snapshot,
    )
