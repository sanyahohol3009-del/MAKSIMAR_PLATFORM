#!/usr/bin/env bash
set -e

cd "$HOME/MAKSIMAR_PLATFORM"

create_domain() {
  local domain="$1"
  shift
  mkdir -p "MAKSIMAR_CORE/contracts/$domain"
  for file in "$@"; do
    touch "MAKSIMAR_CORE/contracts/$domain/$file"
  done
}

create_domain runtime \
  runtime_contract.v1.yaml \
  pid_contract.v1.yaml \
  heartbeat_contract.v1.yaml \
  incident_contract.v1.yaml \
  preflight_contract.v1.yaml \
  event_journal_contract.v1.yaml \
  boot_phase_contract.v1.yaml

create_domain governance \
  risk_matrix.v1.yaml \
  approval_policy.v1.yaml \
  permission_matrix.v1.yaml \
  capability_profile.v1.yaml \
  deployment_mode.v1.yaml \
  trust_policy.v1.yaml \
  node_role.v1.yaml

create_domain memory \
  memory_entity.v1.yaml \
  memory_relation.v1.yaml \
  memory_event.v1.yaml \
  memory_query.v1.yaml \
  memory_snapshot.v1.yaml \
  memory_retention.v1.yaml \
  memory_access.v1.yaml

create_domain knowledge \
  knowledge_object.v1.yaml \
  knowledge_source.v1.yaml \
  knowledge_index.v1.yaml \
  knowledge_pack.v1.yaml \
  retrieval_query.v1.yaml \
  retrieval_result.v1.yaml \
  provenance_record.v1.yaml

create_domain research \
  search_request.v1.yaml \
  search_result.v1.yaml \
  import_review.v1.yaml \
  citation_record.v1.yaml \
  source_rank.v1.yaml

create_domain workflow \
  workflow_definition.v1.yaml \
  action_step.v1.yaml \
  trigger_phrase.v1.yaml \
  workflow_execution.v1.yaml \
  optimization_suggestion.v1.yaml \
  action_result.v1.yaml \
  workflow_template.v1.yaml

create_domain action \
  action_manifest.v1.yaml \
  action_permission.v1.yaml \
  action_context.v1.yaml \
  action_execution.v1.yaml

create_domain module \
  module_manifest.v1.yaml \
  module_permission_matrix.v1.yaml \
  module_dependency.v1.yaml \
  module_lifecycle.v1.yaml \
  module_compatibility.v1.yaml

create_domain ui \
  dashboard_manifest.v1.yaml \
  settings_schema.v1.yaml \
  widget_schema.v1.yaml \
  notification_schema.v1.yaml \
  shell_surface_schema.v1.yaml

create_domain federation \
  node_identity.v1.yaml \
  node_registry.v1.yaml \
  sync_contract.v1.yaml \
  trust_link.v1.yaml \
  federation_snapshot.v1.yaml

create_domain product \
  product_profile.v1.yaml \
  product_bundle.v1.yaml \
  feature_set.v1.yaml \
  branding_profile.v1.yaml

create_domain packaging \
  packaging_profile.v1.yaml \
  bundle_selector.v1.yaml \
  capability_subset.v1.yaml

create_domain codegen \
  task_to_spec.v1.yaml \
  spec_to_module.v1.yaml \
  codegen_diff.v1.yaml \
  proposal_package.v1.yaml \
  test_report.v1.yaml \
  lint_report.v1.yaml \
  typecheck_report.v1.yaml

create_domain evaluation \
  benchmark_case.v1.yaml \
  benchmark_result.v1.yaml \
  turing_style_eval.v1.yaml \
  workflow_eval.v1.yaml \
  tool_use_eval.v1.yaml \
  knowledge_eval.v1.yaml \
  codegen_eval.v1.yaml

create_domain simulation \
  simulation_request.v1.yaml \
  simulation_result.v1.yaml \
  evaluator_result.v1.yaml \
  proposal_package.v1.yaml \
  environment_contract.v1.yaml \
  engine_registry.v1.yaml

create_domain robotics \
  robot_model.v1.yaml \
  controller_contract.v1.yaml \
  constraint_contract.v1.yaml \
  calibration_contract.v1.yaml \
  hardware_bridge_contract.v1.yaml

create_domain cad_3d_cam \
  geometry_object.v1.yaml \
  mesh_contract.v1.yaml \
  print_job.v1.yaml \
  cnc_job.v1.yaml \
  toolpath_contract.v1.yaml

create_domain visual_engineering \
  image_ingest.v1.yaml \
  image_transform.v1.yaml \
  machine_ready_asset.v1.yaml \
  image_to_3d.v1.yaml \
  visual_eval.v1.yaml \
  visual_approval.v1.yaml

create_domain energy \
  solar_node.v1.yaml \
  battery_state.v1.yaml \
  inverter_state.v1.yaml \
  load_balancing_rule.v1.yaml \
  energy_schedule.v1.yaml

create_domain compute_fleet \
  compute_node.v1.yaml \
  rig_inventory.v1.yaml \
  thermal_profile.v1.yaml \
  power_profile.v1.yaml \
  fleet_alert.v1.yaml

create_domain vpn \
  vpn_profile.v1.yaml \
  vpn_state.v1.yaml \
  vpn_policy.v1.yaml \
  vpn_route.v1.yaml

create_domain industrial \
  digital_twin.v1.yaml \
  plc_adapter.v1.yaml \
  scada_bridge.v1.yaml \
  industrial_constraint.v1.yaml

create_domain content_media \
  media_template.v1.yaml \
  publishing_job.v1.yaml \
  subtitle_animation.v1.yaml \
  beat_profile.v1.yaml

create_domain dialogue \
  dialogue_state.v1.yaml \
  dialogue_context.v1.yaml \
  clarification_request.v1.yaml \
  response_plan.v1.yaml

create_domain voice \
  stt_request.v1.yaml \
  stt_result.v1.yaml \
  tts_request.v1.yaml \
  tts_result.v1.yaml \
  wake_event.v1.yaml \
  voice_routing.v1.yaml

create_domain mobile \
  mobile_capability.v1.yaml \
  app_action.v1.yaml \
  app_intent.v1.yaml \
  mobile_permission_bridge.v1.yaml

create_domain shell \
  shell_contract.v1.yaml \
  shell_surface.v1.yaml \
  shell_action_bridge.v1.yaml

echo "All contract files created."
