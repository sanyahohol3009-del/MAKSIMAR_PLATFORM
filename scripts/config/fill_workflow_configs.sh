#!/usr/bin/env bash
set -euo pipefail

BASE="$HOME/MAKSIMAR_PLATFORM/WORKFLOW_ENGINE/config"
mkdir -p "$BASE"
cd "$BASE"

cat > workflow_engine.yaml <<'YAML'
schema_version: workflow_engine_config.v1
description: Canonical top-level configuration for workflow orchestration layer.

registry_policy:
  workflow_registry_enabled: true
  trigger_registry_enabled: true
  suggestion_registry_enabled: true
  execution_log_enabled: true
  template_registry_enabled: true

execution_policy:
  max_steps_per_workflow: 50
  default_step_timeout_sec: 15
  fail_fast: true
  allow_partial_success: false
  require_ordered_step_execution: true

optimization_policy:
  suggestion_engine_enabled: true
  min_repetition_count: 5
  min_confidence: 0.70
  auto_apply_suggestions: false

logging:
  level: INFO
  structured_logging: true
  execution_audit_enabled: true

rules:
  - workflow engine provides orchestration, not ultimate authority
  - workflow engine must not mutate CORE_ROOT
  - workflow execution remains bounded by action library and approval bridge
  - suggestions must remain human-confirmed
YAML

cat > risk_matrix.yaml <<'YAML'
schema_version: workflow_risk_matrix.v1
description: Canonical workflow risk matrix aligned with governance risk levels.

risk_levels:
  safe:
    approval_required: false
    voice_confirmation_required: false
    hardware_key_required: false
    execution_forbidden: false

  sensitive:
    approval_required: true
    voice_confirmation_required: true
    hardware_key_required: false
    execution_forbidden: false

  dangerous:
    approval_required: true
    voice_confirmation_required: true
    hardware_key_required: true
    execution_forbidden: false

  blocked:
    approval_required: false
    voice_confirmation_required: false
    hardware_key_required: false
    execution_forbidden: true

rules:
  - blocked workflows and steps must never execute
  - action-level blocking overrides workflow-level aggregation
  - dangerous workflows must remain human-gated
YAML

cat > trigger_policy.yaml <<'YAML'
schema_version: trigger_policy.v1
description: Canonical policy for workflow trigger phrases and aliases.

trigger_rules:
  allow_multiple_aliases: true
  max_alias_count: 10
  language_required: true
  disabled_triggers_must_not_execute: true
  case_normalization_enabled: true
  whitespace_normalization_enabled: true

validation:
  min_phrase_length: 2
  max_phrase_length: 120
  unique_trigger_phrase_per_scope: true

rules:
  - disabled triggers must never activate workflows
  - trigger aliases must remain explicit and auditable
  - normalized trigger matching must not change intended meaning silently
YAML

cat > action_policy.yaml <<'YAML'
schema_version: action_policy.v1
description: Canonical workflow-to-action policy binding.

ruleset:
  action_library_required: true
  freeform_shell_forbidden: true
  direct_core_write_forbidden: true
  privileged_actions_require_policy: true
  hidden_action_resolution_forbidden: true

contexts:
  allowed:
    - desktop
    - android
    - ios
    - server
    - family_mode
    - engineering_mode

forbidden:
  - write_to_CORE_ROOT
  - bypass_approval
  - disable_security
  - unrestricted_shell_execution

rules:
  - every workflow step must resolve to approved action manifest
  - workflow layer cannot synthesize privileged actions outside action library
  - context filtering must remain explicit
YAML

cat > optimization_policy.yaml <<'YAML'
schema_version: workflow_optimization_policy.v1
description: Canonical policy for workflow suggestion and optimization generation.

suggestion_rules:
  suggestion_engine_enabled: true
  min_pattern_repetition: 5
  min_confidence: 0.70
  require_human_confirmation: true
  auto_register_new_workflows: false

pattern_sources:
  execution_history_enabled: true
  trigger_usage_enabled: true
  accepted_suggestions_feedback_enabled: true

rules:
  - optimization suggestions are advisory only
  - no suggestion may auto-promote itself into executable workflow
  - low-confidence patterns must remain non-binding
YAML

cat > execution_policy.yaml <<'YAML'
schema_version: workflow_execution_policy.v1
description: Canonical execution behavior policy for workflow runs.

defaults:
  fail_fast: true
  allow_partial_success: false
  require_execution_log: true
  require_action_result_tracking: true
  max_concurrent_workflows: 5

timeouts:
  default_step_timeout_sec: 15
  max_step_timeout_sec: 300
  default_workflow_timeout_sec: 900

recovery:
  rollback_when_supported: best_effort
  preserve_failed_step_context: true
  preserve_execution_trace: true

rules:
  - every workflow run must produce execution evidence
  - failed and blocked steps must remain visible in logs
  - execution timeout must remain bounded and explicit
YAML

echo "workflow configs filled successfully"
