#!/usr/bin/env bash
set -euo pipefail

BASE="$HOME/MAKSIMAR_PLATFORM/DIALOGUE_LAYER/config"
mkdir -p "$BASE"
cd "$BASE"

cat > dialogue_policy.yaml <<'YAML'
schema_version: dialogue_policy.v1
description: Canonical top-level policy for dialogue layer.

dialogue:
  multi_turn_enabled: true
  context_tracking_required: true
  intent_persistence_enabled: true
  project_awareness_enabled: true

safety:
  execution_authority_forbidden: true
  risk_critical_ambiguity_must_surface: true
  restricted_context_requires_filtering: true

rules:
  - dialogue layer manages context and response planning, not execution authority
  - dialogue must preserve access boundaries on referenced context
  - hidden action triggering from dialogue alone is forbidden
YAML

cat > clarification_policy.yaml <<'YAML'
schema_version: dialogue_clarification_policy.v1
description: Canonical policy for clarification requests in ambiguous or risky situations.

clarification:
  required_for_ambiguous_intent: true
  required_for_missing_critical_context: true
  required_for_risk_sensitive_requests: true
  options_should_be_explicit: true

safety:
  must_not_hide_risk: true
  must_not_fake_certainty: true
  must_preserve_operator_control: true

rules:
  - clarification is mandatory when ambiguity affects safety or correctness
  - dialogue must ask instead of guessing in risk-critical paths
  - clarification options must remain explicit and reviewable
YAML

cat > context_policy.yaml <<'YAML'
schema_version: dialogue_context_policy.v1
description: Canonical policy for dialogue context assembly and filtering.

context:
  source_refs_required: true
  active_project_ref_allowed: true
  active_workflow_ref_allowed: true
  memory_snapshot_ref_allowed: true

filtering:
  restricted_context_requires_policy: true
  context_scope_must_be_explicit: true
  cross-domain_context_allowed_when_authorized: true

rules:
  - context assembly must preserve provenance
  - restricted context must be filtered before response planning
  - dialogue context does not expand permissions by itself
YAML

echo "dialogue configs filled successfully"
