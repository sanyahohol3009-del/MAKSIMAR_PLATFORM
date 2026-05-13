# PHASE 6.6 — Client Metrics / Learning Input Acceptance v1

## Roadmap track

roadmap_family: memory_roadmap_v5_1  
phase_id: PHASE 6.6  
track_scope: client_metrics_learning_input  
applies_to_current_track: true  

## Purpose

This phase creates the governed learning input layer after Bootstrapped Self-Expansion Gate.

It allows client/operator metrics to become learning input only when:

- source-bound
- tenant-bound
- personal data is redacted
- consent is present
- proposal route is required
- human review is required

It does not allow:

- raw payload storage
- cross-tenant merge
- automatic training mutation
- direct model mutation
- runtime mutation
- productization

## Reused existing surfaces

- MAKSIMAR_CORE_LIB/enterprise_memory_domains/customer_metrics_memory_models.py
- MAKSIMAR_CORE_LIB/enterprise_memory_domains/tenant_memory_models.py
- MAKSIMAR_CORE_LIB/memory_policy/
- MAKSIMAR_SERVER/MEMORY_SYNC/
- MAKSIMAR_SERVER/CONTROL_PLANE/memory_routing/
- MAKSIMAR_SERVER/SELF_EXPANSION_GATE/
- MAKSIMAR_SERVER/OBSERVABILITY/memory_skill_metrics/

## Implemented layer

- MAKSIMAR_SERVER/CLIENT_LEARNING_INPUT/
- MAKSIMAR_SERVER/OBSERVABILITY/memory_skill_metrics/client_learning_input_summary_builder.py

## Accepted state

- filter_policy_ready: True
- privacy_boundary_ready: True
- tenant_boundary_ready: True
- learning_input_pack_ready: True
- preview_ready: True
- source_bound: True
- proposal_route_required: True
- human_review_required: True
- raw_payload_allowed: False
- cross_tenant_merge_allowed: False
- automatic_training_allowed: False
- direct_model_mutation_allowed: False
- runtime_mutation_allowed: False
- productization_allowed_now: False
- polyglot_model_worker_allowed_next: True

## Next step after acceptance

Polyglot / Model / Worker Bridge.

No Productization before Polyglot / Model / Worker Bridge is accepted.
