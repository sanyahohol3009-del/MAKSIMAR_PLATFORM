#!/usr/bin/env bash
set -euo pipefail

BASE="$HOME/MAKSIMAR_PLATFORM/EVALUATION_LAYER/config"
mkdir -p "$BASE"
cd "$BASE"

cat > eval_registry.yaml <<'YAML'
schema_version: evaluation_registry.v1
description: Canonical registry configuration for evaluation domains and evaluators.

registry:
  benchmark_registry_enabled: true
  workflow_eval_enabled: true
  tool_use_eval_enabled: true
  knowledge_eval_enabled: true
  codegen_eval_enabled: true
  turing_style_eval_enabled: true

defaults:
  structured_results_required: true
  evaluator_trace_required: true
  audit_enabled: true

rules:
  - every evaluation must produce structured evidence
  - evaluation registry is source of truth for enabled eval families
  - disabled eval family must not silently run in production gates
YAML

cat > benchmark_registry.yaml <<'YAML'
schema_version: benchmark_registry.v1
description: Canonical benchmark registry policy for platform evaluation suites.

benchmark_families:
  dialogue:
    enabled: true

  workflow:
    enabled: true

  tool_use:
    enabled: true

  knowledge:
    enabled: true

  codegen:
    enabled: true

  simulation:
    enabled: true

policies:
  benchmark_case_versioning_required: true
  benchmark_result_history_required: true
  regression_comparison_enabled: true

rules:
  - benchmark families must remain explicit
  - benchmark history must be preserved for regression tracking
  - no benchmark may bypass governance gates by itself
YAML

cat > turing_style_eval_policy.yaml <<'YAML'
schema_version: turing_style_eval_policy.v1
description: Canonical policy for conversational human-likeness evaluation.

policy:
  enabled: true
  human_review_allowed: true
  rubric_eval_allowed: true
  model_eval_allowed: true
  sole_gate_for_deployment_forbidden: true

requirements:
  dialogue_ref_required: true
  score_required: true
  notes_recommended: true

rules:
  - turing-style eval is one signal only
  - human-likeness must not override safety, grounding, or correctness
  - turing-style score alone cannot promote deployment
YAML

cat > regression_policy.yaml <<'YAML'
schema_version: evaluation_regression_policy.v1
description: Canonical regression policy for preserving platform quality over time.

tracking:
  benchmark_regression_tracking_enabled: true
  workflow_regression_tracking_enabled: true
  codegen_regression_tracking_enabled: true
  knowledge_regression_tracking_enabled: true

thresholds:
  hard_fail_on_critical_regression: true
  warn_on_minor_regression: true
  preserve_baseline_required: true

rules:
  - regression checks must compare against explicit baseline
  - critical regressions must block promotion
  - regression history must remain auditable
YAML

echo "evaluation configs filled successfully"
