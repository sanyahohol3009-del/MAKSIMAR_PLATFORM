# FULL PROJECT SURFACE CENSUS v1

## STATUS LEGEND
- exists_in_core: yes/no
- has_contract: yes/no
- has_test: yes/no
- has_preview: yes/no
- integrated_into_unified_shell: yes/partial/no
- current_ui_world: graph_workspace/chart_workspace/foundation_dashboard/operator_shell/preview_only/backend_only/unknown
- priority: critical/high/medium/low
- drift_status: canonical/preview_only/partially_integrated/duplicate/legacy_or_removed/unknown

---

## 1. GRAPH SURFACES

| surface_id | domain | subdomain | exists_in_core | has_contract | has_test | has_preview | integrated_into_unified_shell | current_ui_world | canonical_owner | priority | drift_status | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| topology_graph | graph | topology | yes | yes | yes | yes | yes | graph_workspace | frontend_graph_registry | critical | canonical | Already integrated into unified graph workspace |
| dependency_graph | graph | dependency | yes | yes | yes | yes | yes | graph_workspace | frontend_graph_registry | high | canonical | Already integrated into unified graph workspace |
| dataflow_graph | graph | dataflow | yes | yes | yes | yes | yes | graph_workspace | frontend_graph_registry | high | canonical | Already integrated into unified graph workspace |
| modules_graph | graph | modules | yes | yes | yes | yes | yes | graph_workspace | frontend_graph_registry | high | canonical | Already integrated into unified graph workspace |
| guard_chain_graph | graph | foundation_guard_chain | yes | yes | yes | yes | yes | graph_workspace | frontend_graph_registry | critical | canonical | Backed by foundation guard-chain truth layers |
| truth_consistency_graph | graph | foundation_truth_consistency | yes | yes | yes | yes | yes | graph_workspace | frontend_graph_registry | critical | canonical | Backed by foundation truth consistency layers |
| workspace_graph | graph | workspace | yes | yes | yes | yes | yes | graph_workspace | frontend_graph_registry | high | canonical | Backed by workspace/display placement relations |
| displays_graph | graph | display_assignment | yes | yes | yes | yes | yes | graph_workspace | frontend_graph_registry | high | canonical | Backed by display assignment registry |

---

## 2. CHART / TELEMETRY SURFACES

| surface_id | domain | subdomain | exists_in_core | has_contract | has_test | has_preview | integrated_into_unified_shell | current_ui_world | canonical_owner | priority | drift_status | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| node_resources_chart | chart | node_resources | yes | yes | yes | yes | yes | operator_shell | chart_registry | critical | canonical | Chart family is now available through the unified visual shell and no longer depends on a separate chart-only world |
| export_validation_assets_chart | chart | export_validation_assets | yes | yes | yes | yes | yes | operator_shell | chart_registry | high | canonical | Chart family is now available through the unified visual shell and no longer depends on a separate chart-only world |
| security_telemetry_chart | chart | security_telemetry | yes | yes | yes | yes | yes | operator_shell | chart_registry | high | canonical | Chart family is now available through the unified visual shell and no longer depends on a separate chart-only world |
| multi_series_summary_chart | chart | summary | yes | yes | yes | yes | yes | operator_shell | chart_registry | medium | canonical | Chart family is now available through the unified visual shell and no longer depends on a separate chart-only world |

---

## 3. PANEL / DASHBOARD SURFACES

| surface_id | domain | subdomain | exists_in_core | has_contract | has_test | has_preview | integrated_into_unified_shell | current_ui_world | canonical_owner | priority | drift_status | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| foundation_unified_dashboard | dashboard | foundation | yes | yes | yes | yes | partial | foundation_dashboard | oob_dashboard_foundation | critical | partially_integrated | Canonical read-only dashboard world exists |
| foundation_incident_dashboard | dashboard | incidents | yes | yes | yes | yes | partial | foundation_dashboard | oob_dashboard_foundation | high | canonical | Present in foundation stack |
| foundation_diagnostics_correlation | dashboard | diagnostics | yes | yes | yes | yes | partial | foundation_dashboard | oob_dashboard_foundation | high | canonical | Present in foundation stack |
| main_operator_dashboard | dashboard | operator | yes | yes | yes | partial | no | operator_shell | main_operator_dashboard_layer | critical | partially_integrated | Contracts exist, but full single-shell assembly not confirmed |
| visual_shell | dashboard | visual_shell | yes | yes | yes | partial | partial | operator_shell | visual_shell_layer | critical | partially_integrated | Visual shell contracts exist, but final consolidated assembly not yet proven |
| panel_registry_surface | dashboard | panel_registry | yes | yes | yes | partial | partial | operator_shell | panel_registry_layer | critical | partially_integrated | Panel registry contracts and models exist in oob_dashboard |
| panel_binding_surface | dashboard | panel_binding | yes | yes | yes | partial | partial | operator_shell | panel_binding_layer | high | partially_integrated | Panel binding contracts/models exist but final shell exposure is not yet fully proven |
| panel_orchestration_surface | dashboard | panel_orchestration | yes | yes | yes | partial | partial | backend_only | panel_orchestration_layer | high | partially_integrated | Canonical orchestration layer exists but is not yet fully surfaced in unified shell |
| panel_content_surface | dashboard | panel_content | yes | yes | yes | partial | partial | foundation_dashboard | panel_content_layer | high | partially_integrated | Content contracts and payload/content builders exist across dashboard surfaces |
| panel_view_display_chain_surface | dashboard | panel_display_chain | yes | yes | yes | partial | partial | backend_only | panel_display_chain_layer | high | partially_integrated | Panel/view/display chain exists but needs explicit single-shell exposure mapping |
| main_operator_interaction_surface | dashboard | main_operator_interaction | yes | yes | yes | partial | partial | operator_shell | main_operator_surface_layer | critical | partially_integrated | Main operator interaction contracts/models exist but final assembly must be verified |
| main_operator_read_model_surface | dashboard | main_operator_read_model | yes | yes | yes | partial | partial | operator_shell | main_operator_read_model_layer | critical | partially_integrated | Read-model layer exists and must remain canonical during consolidation |
| dashboard_execution_shell_surface | dashboard | execution_shell | yes | yes | yes | partial | partial | operator_shell | dashboard_execution_shell_layer | high | partially_integrated | Execution shell contract exists, but final shell integration still needs confirmation |
| workspace_registry_dashboard_surface | dashboard | workspace_registry | yes | yes | yes | partial | partial | operator_shell | workspace_layer | critical | partially_integrated | Workspace registry contracts/models exist and should participate in single-shell navigation |
| foundation_status_menu_surface | dashboard | status_menu_registry | yes | yes | yes | partial | partial | foundation_dashboard | oob_dashboard_foundation | high | canonical | Foundation status menu registry exists and should map into left-nav semantics |
| dashboard_visible_state_surface | dashboard | visible_state | yes | yes | yes | partial | partial | operator_shell | visual_shell_layer | high | partially_integrated | Visible state contract exists but final ownership in single-shell must be confirmed |
| panel_exposure_policy_surface | dashboard | panel_exposure_policy | yes | yes | yes | partial | partial | backend_only | panel_exposure_layer | high | partially_integrated | Exposure policy exists and should gate what becomes visible in final shell |
| panel_family_surface | dashboard | panel_family | yes | yes | yes | partial | partial | operator_shell | panel_family_layer | medium | partially_integrated | Panel family contracts exist and should become part of shell taxonomy/navigation |
| panel_taxonomy_surface | dashboard | panel_taxonomy | yes | yes | yes | partial | partial | operator_shell | panel_taxonomy_layer | medium | partially_integrated | Taxonomy exists and should unify panel grouping in shell navigation |

---

## 4. OPERATOR / INTERACTION SURFACES

| surface_id | domain | subdomain | exists_in_core | has_contract | has_test | has_preview | integrated_into_unified_shell | current_ui_world | canonical_owner | priority | drift_status | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| operator_intent_surface | interaction | operator_intent | yes | yes | yes | partial | partial | operator_shell | operator_interaction_layer | critical | partially_integrated | Intent contracts confirmed |
| operator_guard_surface | interaction | guarded_actions | yes | yes | yes | partial | partial | operator_shell | operator_interaction_layer | critical | partially_integrated | Guard contracts confirmed |
| command_strip_surface | interaction | commands | yes | yes | yes | partial | partial | operator_shell | operator_interaction_layer | critical | partially_integrated | Exists, but not yet confirmed as embedded final shell path |
| control_plane_handoff_surface | interaction | handoff | yes | yes | yes | partial | partial | backend_only | operator_interaction_layer | high | canonical | Exists as canonical handoff layer |
| interaction_exposure_surface | interaction | exposure | yes | yes | yes | partial | partial | operator_shell | interaction_exposure_layer | high | partially_integrated | Interaction exposure contract exists in oob_dashboard |
| interaction_observability_surface | interaction | observability | yes | yes | yes | partial | partial | backend_only | interaction_observability_layer | high | partially_integrated | Interaction observability exists but is not yet unified into final shell |
| interaction_incident_surface | interaction | incidents | yes | yes | yes | partial | partial | foundation_dashboard | interaction_incident_layer | medium | partially_integrated | Incident-facing interaction surface exists but shell placement remains to be finalized |
| operator_workspace_binding_surface | interaction | workspace_binding | yes | yes | yes | partial | partial | operator_shell | operator_workspace_layer | high | partially_integrated | Operator-to-workspace binding exists and must be mapped into single-shell target |
| operator_audit_visibility_surface | interaction | audit_visibility | yes | yes | yes | partial | partial | operator_shell | operator_audit_layer | high | partially_integrated | Audit visibility layer exists and should be preserved during shell consolidation |

---

## 5. CHAT / JARVIS / MESSAGING SURFACES

| surface_id | domain | subdomain | exists_in_core | has_contract | has_test | has_preview | integrated_into_unified_shell | current_ui_world | canonical_owner | priority | drift_status | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| embedded_jarvis_chat_surface | chat | messaging | yes | yes | yes | yes | partial | operator_shell | main_operator_dashboard_layer | critical | partially_integrated | Canonical host is main_operator_dashboard in workspace_operator_interaction; frontend chat panel/command surfaces exist, but full history/input/output path is not yet fully confirmed |
| chat_history_surface | chat | history | yes | yes | yes | yes | partial | operator_shell | frontend_chat_panel_layer | critical | partially_integrated | History capability is confirmed in frontend chat panel via supportsHistory and visibleMessages, but backend canonical history source is not yet confirmed |
| command_message_surface | chat | commands | yes | yes | yes | yes | partial | operator_shell | operator_interaction_layer | critical | partially_integrated | Frontend command queue/command strip surfaces exist and align with operator shell, but final message/history binding is still incomplete |
| operator_intent_contract_surface | chat | operator_intent_routing | yes | yes | yes | yes | partial | operator_shell | operator_intent_layer | critical | partially_integrated | Builder confirmed with total_entries=3 and operator intent entry schema |
| operator_interaction_guard_chat_boundary | chat | guarded_interaction_boundary | yes | yes | yes | yes | partial | operator_shell | operator_interaction_layer | critical | partially_integrated | Guard contract builder confirmed; interaction is policy-bound and not direct execution |
| operator_control_plane_chat_handoff | chat | control_plane_handoff | yes | yes | yes | yes | partial | backend_only | operator_interaction_layer | critical | canonical | Handoff contract builder confirmed as canonical bridge to control-plane |
| interaction_exposure_chat_surface | chat | exposure_channels | yes | yes | yes | no | partial | operator_shell | interaction_exposure_layer | high | partially_integrated | Interaction exposure contract confirmed with contract_id and total_entries=2 |
| main_operator_dashboard_chat_host | chat | dashboard_host_surface | yes | yes | yes | yes | partial | operator_shell | main_operator_dashboard_layer | critical | partially_integrated | Main operator dashboard contract exists and operator previews are present |
| chat_contract_surface | chat | chat_contract | partial | partial | yes | no | no | unknown | to_be_assigned | critical | unknown | Compiled chat_contract/chat_input_contract traces exist, but canonical active source file not confirmed in this pass |
| chat_input_surface | chat | input_contract | yes | yes | yes | yes | partial | operator_shell | frontend_chat_panel_layer | critical | partially_integrated | Input capability is confirmed in frontend chat panel via supportsInput, but backend canonical input source is not yet confirmed |
| frontend_chat_panel_surface | chat | panel_contract | yes | yes | yes | yes | partial | operator_shell | frontend_chat_panel_layer | critical | partially_integrated | frontend/contracts/chat_panel_contract.ts, tests, and preview exist and align with main operator shell host |
| frontend_command_queue_surface | chat | command_queue | yes | yes | yes | yes | partial | operator_shell | frontend_command_layer | high | partially_integrated | frontend command queue contract/test exist and should bind into embedded chat/operator surface |
| frontend_command_strip_surface | chat | command_strip | yes | yes | yes | yes | partial | operator_shell | frontend_command_layer | high | partially_integrated | frontend command strip contract/test exist and should bind into embedded chat/operator surface |
| main_operator_dashboard_read_model_chat_surface | chat | read_model_host | yes | yes | yes | yes | partial | operator_shell | main_operator_dashboard_layer | high | partially_integrated | Main operator dashboard read-model contracts/tests exist and likely host chat visibility path inside the shell |
| chat_output_render_surface | chat | explain_output_render | yes | yes | yes | yes | partial | operator_shell | explainability_layer | high | partially_integrated | Output rendering is currently best mapped through the chat/explain/command split preview and visual explainability sidebar path |

---

## 6. MEMORY / HISTORY / PROJECT-AWARENESS SURFACES

| surface_id | domain | subdomain | exists_in_core | has_contract | has_test | has_preview | integrated_into_unified_shell | current_ui_world | canonical_owner | priority | drift_status | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| project_history_surface | memory | history | yes | partial | partial | no | no | backend_only | memory_layer | critical | partially_integrated | Important for JARVIS context, not yet confirmed in unified UI |
| project_context_surface | memory | project_awareness | yes | partial | partial | no | no | backend_only | memory_layer | critical | partially_integrated | Exists conceptually, unified shell exposure not confirmed |
| memory_retrieval_surface | memory | retrieval | yes | partial | partial | no | no | backend_only | memory_layer | high | partially_integrated | Must later connect to chat/operator surfaces |
| memory_engine_registry_surface | memory | registry_loader_accessor | yes | yes | yes | no | no | backend_only | memory_engine_layer | critical | canonical | memory_accessor/memory_loader/memory_registry/query_models/retrieval_summary are present |
| memory_classification_policy_surface | memory | classification_policy | yes | yes | yes | no | no | backend_only | memory_policy_layer | critical | canonical | memory_classification_policy enforces approval, deduplication, conflict, language, script, provenance rules |
| knowledge_engine_registry_surface | memory | knowledge_registry | yes | yes | yes | no | no | backend_only | knowledge_engine_layer | high | canonical | knowledge_accessor/loader/models/registry/query_models/retrieval_summary are present |
| memory_registry_surface | memory | registry_contracts | yes | partial | yes | no | no | backend_only | memory_registry_layer | high | partially_integrated | Dedicated test folder exists for memory_registry, but unified UI exposure is not confirmed |
| memory_promotion_pipeline_surface | memory | promotion_pipeline | yes | partial | yes | no | no | backend_only | memory_promotion_layer | high | partially_integrated | Dedicated test folder exists for promotion pipeline, but shell exposure is not confirmed |
| memory_conflict_resolution_surface | memory | conflict_resolution | yes | partial | yes | no | no | backend_only | memory_conflict_layer | high | partially_integrated | Dedicated test folder exists for conflict resolution, but shell exposure is not confirmed |
| memory_skill_metrics_surface | memory | metrics | yes | partial | yes | no | no | backend_only | memory_metrics_layer | medium | partially_integrated | Dedicated tests exist; later should connect to chat/operator awareness |
| real_dashboard_clients_mobile_memory_surface | memory | mobile_client_exposure | yes | partial | yes | no | no | backend_only | real_dashboard_clients_mobile_layer | high | partially_integrated | Dedicated test directory exists, but integrated shell path is not yet confirmed |
| surface_intelligence_context_surface | memory | project_context_enrichment | yes | yes | yes | no | no | backend_only | surface_intelligence_layer | medium | canonical | surface_intelligence contract exists with explainable/production-usable constraints |
| memory_registry_summary_shell_exposure | memory | inspect_exposure | yes | yes | yes | yes | yes | operator_shell | memory_engine_layer | high | canonical | Read-only memory registry summary is now exposed inside the unified shell inspect lane |
| knowledge_registry_summary_shell_exposure | memory | inspect_exposure | yes | yes | yes | yes | yes | operator_shell | knowledge_engine_layer | high | canonical | Read-only knowledge registry summary is now exposed inside the unified shell inspect lane |
| project_context_summary_shell_exposure | memory | chat_context_exposure | yes | yes | yes | yes | yes | operator_shell | surface_intelligence_layer | high | canonical | Bounded project context summary is now exposed inside unified shell as chat-context-facing read-only lane |
| memory_policy_summary_shell_exposure | memory | explain_exposure | yes | yes | yes | yes | yes | operator_shell | memory_policy_layer | high | canonical | Memory policy summary is now exposed through explain-oriented shell lane without opening write access |

---

## 7. DISPLAY / WORKSPACE / PLACEMENT SURFACES

| surface_id | domain | subdomain | exists_in_core | has_contract | has_test | has_preview | integrated_into_unified_shell | current_ui_world | canonical_owner | priority | drift_status | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| display_assignment_spine | display | assignment_registry | yes | yes | yes | yes | partial | graph_workspace | display_layer | critical | canonical | Canonical display assignment stack exists |
| display_restore_spine | display | restore_continuity | yes | yes | yes | yes | partial | preview_only | display_layer | high | canonical | Exists but not fully merged into one shell |
| workspace_placement_surface | display | workspace | yes | yes | yes | yes | yes | graph_workspace | workspace_layer | high | canonical | Reflected in workspace graph |
| display_conflict_resolution_surface | display | conflict_resolution | yes | yes | yes | partial | no | backend_only | display_layer | high | partially_integrated | Exists, but not surfaced in unified shell |
| display_target_vocabulary_surface | display | target_vocabulary | yes | yes | yes | partial | partial | backend_only | display_layer | critical | canonical | Display target vocabulary exists and should remain the canonical naming layer |
| display_role_surface | display | display_roles | yes | yes | yes | partial | partial | backend_only | display_layer | high | canonical | Display role contract exists and defines role semantics for placement and routing |
| display_resolver_surface | display | resolver_decision | yes | yes | yes | partial | partial | backend_only | display_layer | critical | partially_integrated | Resolver decision/routing contracts exist, but final shell wiring is not yet confirmed |
| display_assignment_restore_surface | display | assignment_restore | yes | yes | yes | yes | partial | preview_only | display_layer | high | partially_integrated | Restore contracts exist and are previewed, but not yet collapsed into one shell path |
| display_occupancy_surface | display | occupancy | yes | yes | yes | partial | no | backend_only | display_layer | high | partially_integrated | Occupancy layer exists but is not yet visibly surfaced in unified shell |
| display_replacement_policy_surface | display | replacement_policy | yes | yes | yes | partial | no | backend_only | display_layer | high | partially_integrated | Replacement policy exists and must later bind to operator/display shell decisions |
| free_display_selection_surface | display | free_selection | yes | yes | yes | partial | no | backend_only | display_layer | medium | partially_integrated | Free display selection exists as derived selection layer, not final shell UI |
| display_runtime_resolver_surface | display | runtime_resolver_integration | yes | yes | yes | partial | no | backend_only | display_layer | critical | partially_integrated | Runtime resolver integration exists but single-shell integration remains unconfirmed |
| workspace_registry_surface | display | workspace_registry | yes | yes | yes | partial | partial | operator_shell | workspace_layer | critical | partially_integrated | Workspace registry contracts/models exist and should anchor final shell workspace navigation |
| workspace_binding_surface | display | workspace_binding | yes | yes | yes | yes | partial | operator_shell | workspace_layer | high | partially_integrated | Operator workspace binding previews exist, but final integrated shell still needs confirmation |

---

## 8. PREVIEW-ONLY / ORPHANED / LEGACY SURFACES

| surface_id | domain | subdomain | exists_in_core | has_contract | has_test | has_preview | integrated_into_unified_shell | current_ui_world | canonical_owner | priority | drift_status | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| node_resources_family_preview | preview | node_resources | yes | yes | yes | yes | no | preview_only | node_resources_family | medium | preview_only | Exists as terminal/web preview, should not remain final UI |
| chart_preview_world | preview | chart_workspace | yes | yes | yes | yes | no | preview_only | chart_layer | medium | preview_only | Separate chart preview world is now harness-only because canonical chart access lives in the unified visual shell |
| old_visual_reset_artifacts | legacy | removed_or_reset | yes | unknown | unknown | no | no | unknown | unknown | medium | legacy_or_removed | Must be audited against canonical rebuild targets |
| foundation_preview_scatter | preview | foundation_views | yes | yes | yes | yes | partial | foundation_dashboard | oob_dashboard_foundation | medium | preview_only | Multiple foundation previews exist and must collapse into single-shell navigation |
| operator_preview_scatter | preview | operator_views | yes | yes | yes | partial | no | preview_only | operator_shell | medium | preview_only | Operator-oriented preview surfaces exist but are not yet one final assembled shell |
| display_preview_scatter | preview | display_restore_views | yes | yes | yes | yes | no | preview_only | display_layer | medium | preview_only | Display/restore/assignment previews exist separately and risk drift if left detached |
| workspace_preview_scatter | preview | workspace_views | yes | yes | yes | yes | no | preview_only | workspace_layer | medium | preview_only | Workspace-related previews exist separately and should collapse into one shell navigation path |
| panel_preview_scatter | preview | panel_views | yes | yes | yes | partial | no | preview_only | panel_layer | medium | preview_only | Panel-related previews/contracts exist beyond final integrated shell and may drift if left detached |

---

## 9. GAP LIST

| gap_id | missing_surface | severity | why_it_matters | where_it_should_land |
|---|---|---|---|---|
| GAP-001 | embedded_jarvis_chat_surface | critical | User specifically requires chat/messages/commands inside dashboard, not separate worlds | single-shell right/center integrated chat surface |
| GAP-002 | chart_preview_world_collapse | high | Canonical chart access is now solved in unified shell, but separate chart preview world still exists as a secondary path and must be demoted to harness-only | consolidation execution plan |
| GAP-003 | memory_history_project_awareness_exposure | critical | Project context and chat history must be visible to JARVIS/operator path | embedded chat + inspect + memory side surfaces |
| GAP-004 | preview_only_surface_cleanup | high | Too many separate previews create drift and forgotten functionality | consolidation pass / single-shell map |
| GAP-005 | explicit_canonical_owner_mapping | high | Without owner mapping, future integration will drift again | census registry + target map |
| GAP-006 | unified_panel_registry_to_single_shell_mapping | critical | Panel registry/binding/orchestration exist, but final shell ownership and placement are still fragmented | left nav + center workspace + right inspect map |
| GAP-007 | main_operator_surface_assembly_confirmation | critical | Main operator contracts/models exist, but final integrated operator shell is not yet explicitly confirmed | center workspace/operator shell |
| GAP-008 | preview_scatter_collapse | high | Foundation/operator/display previews still risk becoming parallel worlds | consolidation pass / single-shell execution plan |
| GAP-009 | canonical_chat_contract_confirmation | critical | Messaging is strategically required, but active canonical chat source files are not yet explicitly confirmed in the current pass | embedded JARVIS chat surface |
| GAP-010 | memory_and_knowledge_ui_exposure | resolved | Memory/knowledge exposure now exists in unified shell through inspect / explain / chat_context read-only lanes | resolved in unified visual shell |
| GAP-011 | operator_to_chat_surface_binding | critical | Operator intent/guard/handoff layers exist, but binding them into one visible JARVIS interaction surface is not yet confirmed | operator shell + embedded chat |
| GAP-012 | project_history_visibility_path | high | Project/memory/history awareness exists conceptually and structurally, but visible shell path is not yet defined | chat history + inspect/memory surfaces |
| GAP-013 | display_resolver_to_single_shell_mapping | critical | Display resolver, restore, occupancy and replacement layers exist, but their final shell exposure path is not yet explicitly mapped | display/workspace/operator shell |
| GAP-014 | workspace_registry_navigation_binding | critical | Workspace registry exists, but left-nav/center workspace binding is not yet finalized | left nav + center workspace |
| GAP-015 | panel_taxonomy_and_family_shell_binding | high | Panel family/taxonomy/exposure layers exist, but final shell grouping is still fragmented | left nav + shell taxonomy |
| GAP-016 | preview_workspace_panel_collapse | high | Workspace/panel previews still risk remaining parallel worlds instead of one shell | consolidation execution plan |
| GAP-017 | backend_chat_history_source_confirmation | high | Frontend history path is confirmed, but backend canonical history source is still not explicitly confirmed | embedded JARVIS chat history backend path |
| GAP-018 | backend_chat_input_source_confirmation | high | Frontend input path is confirmed, but backend canonical input source is still not explicitly confirmed | embedded JARVIS chat input backend path |
| GAP-019 | final_output_render_binding | medium | Output path is likely explain/explainability-bound, but final shell binding still needs explicit confirmation | embedded JARVIS chat + explain/output surface |
| GAP-020 | unified_graph_chart_registry | resolved | Graph and chart families are now navigable through one shell taxonomy | resolved in unified visual shell |
| GAP-021 | unified_center_workspace_mode_switch | resolved | Graph canvas and chart stage now switch inside one shell center workspace | resolved in unified visual shell |
| GAP-022 | separate_preview_runtime_collapse_for_graph_and_chart | high | Unified shell exists, but separate preview runtimes still remain and should be clearly demoted to non-canonical harness paths | consolidation execution plan |
| GAP-023 | embedded_chat_memory_context_binding | high | Read-only project context is now visible in shell, but it is not yet bound into the embedded JARVIS chat host as active chat context | embedded chat + chat_context surface |
| GAP-024 | panel_family_taxonomy_exposure_shell_lane | resolved | Family / taxonomy / exposure semantics are now visible in unified shell through a dedicated read-only inspect lane | resolved in unified visual shell |

---

## 10. SINGLE-SHELL TARGET MAP

### LEFT NAV
- graph families
- chart families
- panel families
- workspace / display families

### CENTER WORKSPACE
- unified graph workspace
- unified chart workspace
- main operator dashboard surfaces

### RIGHT INSPECT / EXPLAIN
- inspect panel
- explanation panel
- diagnostics / payload / semantic details

### EMBEDDED JARVIS CHAT / COMMAND SURFACE
- jarvis chat window
- command history
- message history
- code block / answer output
- future memory-aware interaction surface

### BACKEND-ONLY / NOT DIRECTLY SURFACED
- control-plane handoff internals
- policy enforcement internals
- routing internals
- some restore / conflict resolution internals

---

## 11. DRIFT / DUPLICATION AUDIT

### CANONICAL SURFACES
- topology_graph
- dependency_graph
- dataflow_graph
- modules_graph
- guard_chain_graph
- truth_consistency_graph
- workspace_graph
- displays_graph
- foundation_unified_dashboard
- foundation_incident_dashboard
- foundation_diagnostics_correlation
- operator_control_plane_chat_handoff
- memory_engine_registry_surface
- memory_classification_policy_surface
- knowledge_engine_registry_surface
- display_assignment_spine
- display_target_vocabulary_surface
- display_role_surface
- node_resources_chart
- export_validation_assets_chart
- security_telemetry_chart
- multi_series_summary_chart
- chart_registry
- chart_inspect_surface
- unified_visual_shell_app
- unified_visual_workspace_registry
- unified_visual_workspace_snapshot
- memory_registry_summary_shell_exposure
- knowledge_registry_summary_shell_exposure
- project_context_summary_shell_exposure
- memory_policy_summary_shell_exposure
- memory_knowledge_exposure_registry
- memory_knowledge_shell_read_model
- panel_navigation_lane_shell_exposure
- panel_family_taxonomy_exposure_shell_lane
- panel_family_taxonomy_exposure_registry
- panel_family_taxonomy_exposure_read_model

### PARTIALLY INTEGRATED SURFACES
- main_operator_dashboard
- visual_shell
- panel_registry_surface
- panel_binding_surface
- panel_orchestration_surface
- panel_content_surface
- panel_view_display_chain_surface
- main_operator_interaction_surface
- main_operator_read_model_surface
- dashboard_execution_shell_surface
- workspace_registry_dashboard_surface
- dashboard_visible_state_surface
- panel_exposure_policy_surface
- panel_family_surface
- panel_taxonomy_surface
- operator_intent_surface
- operator_guard_surface
- command_strip_surface
- interaction_exposure_surface
- interaction_observability_surface
- interaction_incident_surface
- operator_workspace_binding_surface
- operator_audit_visibility_surface
- operator_intent_contract_surface
- operator_interaction_guard_chat_boundary
- interaction_exposure_chat_surface
- main_operator_dashboard_chat_host
- project_history_surface
- project_context_surface
- memory_retrieval_surface
- memory_registry_surface
- memory_promotion_pipeline_surface
- memory_conflict_resolution_surface
- memory_skill_metrics_surface
- real_dashboard_clients_mobile_memory_surface
- display_conflict_resolution_surface
- display_resolver_surface
- display_assignment_restore_surface
- display_occupancy_surface
- display_replacement_policy_surface
- free_display_selection_surface
- display_runtime_resolver_surface
- workspace_registry_surface
- workspace_binding_surface

### PREVIEW-ONLY SURFACES
- node_resources_family_preview
- chart_preview_world
- foundation_preview_scatter
- operator_preview_scatter
- display_preview_scatter
- workspace_preview_scatter
- panel_preview_scatter

### UNKNOWN / REQUIRES CONFIRMATION
- embedded_jarvis_chat_surface
- chat_history_surface
- command_message_surface
- chat_contract_surface
- chat_input_surface

### LEGACY OR REMOVED
- old_visual_reset_artifacts

---

## 12. CONSOLIDATION PRIORITY ORDER

1. embedded_jarvis_chat_surface
2. unified_shell_integration_for_chart_workspace
3. memory_and_knowledge_ui_exposure
4. unified_panel_registry_to_single_shell_mapping
5. main_operator_surface_assembly_confirmation
6. display_resolver_to_single_shell_mapping
7. workspace_registry_navigation_binding
8. preview_scatter_collapse

---

## 13. SINGLE-SHELL CONSOLIDATION DECISIONS (WORKING)

### MUST LAND IN FINAL SHELL
- graph workspace
- chart workspace
- main operator dashboard
- visual shell
- panel registry / taxonomy / family grouping
- operator intent / guard / command strip
- embedded JARVIS chat surface
- inspect / explain surface
- memory-aware project context exposure
- workspace navigation
- display resolver outcomes (as visible state, not as raw internals)

### MUST REMAIN BACKEND-ONLY
- control-plane handoff internals
- policy enforcement internals
- raw conflict resolution internals
- raw replacement-policy internals
- low-level routing internals

### MUST BE COLLAPSED / REMOVED AS STANDALONE WORLDS
- chart_preview_world
- node_resources_family_preview
- foundation_preview_scatter
- operator_preview_scatter
- display_preview_scatter
- workspace_preview_scatter
- panel_preview_scatter

---

## 14. SINGLE-SHELL EXECUTION PLAN

### STEP C2.1 — EMBEDDED JARVIS CHAT SURFACE CONFIRMATION
**Goal**
- Confirm canonical host surface for embedded JARVIS chat inside the final shell.

**Must use**
- main_operator_dashboard
- visual_shell
- operator_intent_surface
- operator_guard_surface
- command_strip_surface
- interaction_exposure_chat_surface

**Must resolve**
- whether active canonical chat source files exist now
- where message history lives
- where command history lives
- where code/output blocks render

**Acceptance**
- one canonical shell location for chat is defined
- no separate browser world for chat
- chat is marked as final-shell target, not preview-only

---

### STEP C2.2 — CHART WORKSPACE MERGE INTO SINGLE SHELL
**Goal**
- Merge chart workspace into the same shell world as graph workspace.

**Must use**
- node_resources_chart
- export_validation_assets_chart
- security_telemetry_chart
- multi_series_summary_chart

**Must resolve**
- chart family location in left nav
- chart mount area in center workspace
- inspect/explain reuse on the right side

**Acceptance**
- chart workspace no longer treated as a separate world
- chart family is part of one shell navigation model

---

### STEP C2.3 — MEMORY / KNOWLEDGE UI EXPOSURE
**Goal**
- Expose memory/knowledge/project-awareness through shell-visible surfaces.

**Must use**
- memory_engine_registry_surface
- memory_classification_policy_surface
- knowledge_engine_registry_surface
- project_history_surface
- project_context_surface
- memory_retrieval_surface

**Must resolve**
- what is visible in embedded chat
- what is visible in inspect/explain
- what remains backend-only

**Acceptance**
- memory-aware project context has visible shell path
- knowledge/memory do not remain completely backend-only

---

### STEP C2.4 — PANEL REGISTRY / TAXONOMY / FAMILY CONSOLIDATION
**Goal**
- Turn panel registry/taxonomy/family layers into one shell navigation model.

**Must use**
- panel_registry_surface
- panel_binding_surface
- panel_orchestration_surface
- panel_exposure_policy_surface
- panel_family_surface
- panel_taxonomy_surface
- workspace_registry_dashboard_surface

**Must resolve**
- left-nav grouping
- panel family ownership
- visibility gating
- canonical registry path

**Acceptance**
- one canonical panel navigation model exists
- panel grouping is not fragmented across previews

---

### STEP C2.5 — EMBEDDED CHAT CONTEXT BINDING
**Goal**
- Confirm one final operator shell assembly path.

**Must use**
- main_operator_dashboard
- main_operator_interaction_surface
- main_operator_read_model_surface
- dashboard_execution_shell_surface
- dashboard_visible_state_surface
- visual_shell

**Must resolve**
- shell root
- shell visible state
- shell read model
- shell interaction path

**Acceptance**
- one final operator shell path is confirmed
- no ambiguity about shell root remains

---

### STEP C2.6 — DISPLAY / WORKSPACE / RESOLVER INTEGRATION
**Goal**
- Bind display/workspace/resolver layers into visible shell behavior.

**Must use**
- display_assignment_spine
- display_resolver_surface
- display_assignment_restore_surface
- display_occupancy_surface
- display_replacement_policy_surface
- display_runtime_resolver_surface
- workspace_registry_surface
- workspace_binding_surface

**Must resolve**
- what becomes visible state
- what remains backend-only
- how display outcomes affect workspace navigation

**Acceptance**
- display resolver outcomes are represented in shell-visible state
- raw resolver internals remain backend-only

---

### STEP C2.7 — PREVIEW COLLAPSE PLAN
**Goal**
- Eliminate standalone preview worlds as final UX destinations.

**Must collapse**
- chart_preview_world
- node_resources_family_preview
- foundation_preview_scatter
- operator_preview_scatter
- display_preview_scatter
- workspace_preview_scatter
- panel_preview_scatter

**Acceptance**
- preview surfaces remain only as harness/test tooling
- final UX is defined through one shell model

---

## 15. IMMEDIATE NEXT ACTION

**Next execution target**
- STEP C2.5 — EMBEDDED CHAT CONTEXT BINDING

**Reason**
- Unified visual shell is now working for graph, chart, memory/knowledge, panel navigation, and panel family/taxonomy/exposure read-only lanes.
- The next highest unresolved shell gap is binding project context into the embedded chat host as active chat context.
