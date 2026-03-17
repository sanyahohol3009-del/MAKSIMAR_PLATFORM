#!/usr/bin/env bash
set -euo pipefail

BASE="$HOME/MAKSIMAR_PLATFORM/SIMULATION_LAYER/config"
mkdir -p "$BASE"
cd "$BASE"

cat > simulation_layer.yaml <<'YAML'
schema_version: simulation_layer_config.v1
description: Canonical top-level configuration for backend-agnostic simulation layer.

registry:
  engine_registry_enabled: true
  environment_registry_enabled: true
  evaluator_registry_enabled: true
  artifact_registry_enabled: true

execution:
  sandbox_required: true
  queue_enabled: true
  evidence_retention_required: true
  direct_hardware_execution_forbidden: true

defaults:
  default_engine: pybullet
  default_timeout_sec: 300
  default_save_logs: true
  default_save_metrics: true
  default_save_failure_snapshot: true

rules:
  - simulation layer is evidence-producing, not deployment authority
  - simulation must not write to CORE_ROOT
  - real hardware execution is outside simulation authority
YAML

cat > engine_registry.yaml <<'YAML'
schema_version: simulation_engine_registry.v1
description: Canonical engine registry for supported simulation backends.

engines:
  pybullet:
    enabled: true
    class: physics_general
    gpu_required: false

  mujoco:
    enabled: true
    class: physics_control
    gpu_required: false

  genesis:
    enabled: true
    class: advanced_physics
    gpu_required: true

  isaac:
    enabled: true
    class: industrial_robotics
    gpu_required: true

rules:
  - enabled engines must remain explicit
  - engine selection must be routed through registry and policy
  - backend-specific settings must not leak into portable contracts
YAML

cat > routing_rules.yaml <<'YAML'
schema_version: simulation_routing_rules.v1
description: Canonical routing rules for selecting simulation engine by scenario and constraints.

routes:
  cartpole:
    preferred_engines:
      - pybullet
      - mujoco

  quadruped_locomotion:
    preferred_engines:
      - mujoco
      - genesis
      - isaac

  manipulator_pick_place:
    preferred_engines:
      - mujoco
      - isaac

  cnc_motion:
    preferred_engines:
      - pybullet
      - genesis

  printer_motion:
    preferred_engines:
      - pybullet
      - genesis

  digital_twin_validation:
    preferred_engines:
      - isaac
      - genesis

rules:
  - route must choose from registered engines only
  - unavailable engine must fall back to next allowed engine
  - routing remains bounded by sandbox and runtime policy
YAML

cat > evaluator_defaults.yaml <<'YAML'
schema_version: simulation_evaluator_defaults.v1
description: Canonical default evaluator policy for simulation result interpretation.

evaluators:
  safety_score_enabled: true
  stability_score_enabled: true
  task_success_enabled: true
  constraint_violation_check_enabled: true
  artifact_quality_check_enabled: true

thresholds:
  minimum_safety_score_for_promotion: 0.80
  minimum_stability_score_for_promotion: 0.75
  hard_block_on_constraint_violation: true

rules:
  - evaluator results are mandatory for proposal generation
  - constraint violations must remain visible and blocking when configured
  - evaluator defaults may be tightened per scenario, not weakened silently
YAML

cat > backend_pybullet.yaml <<'YAML'
schema_version: simulation_backend_pybullet.v1
description: Backend-specific operational defaults for PyBullet adapter.

backend:
  enabled: true
  sandbox_profile: sim_cpu_small
  gpu_allowed: false
  headless_default: true

limits:
  default_timeout_sec: 300
  cpu_limit: 2
  memory_limit_mb: 2048

artifacts:
  save_logs: true
  save_metrics: true
  save_video: false
  save_failure_snapshot: true

rules:
  - backend settings remain adapter-local
  - backend config must not override portable simulation contracts
YAML

cat > backend_mujoco.yaml <<'YAML'
schema_version: simulation_backend_mujoco.v1
description: Backend-specific operational defaults for MuJoCo adapter.

backend:
  enabled: true
  sandbox_profile: sim_cpu_large
  gpu_allowed: false
  headless_default: true

limits:
  default_timeout_sec: 300
  cpu_limit: 4
  memory_limit_mb: 4096

artifacts:
  save_logs: true
  save_metrics: true
  save_video: false
  save_failure_snapshot: true

rules:
  - backend settings remain adapter-local
  - mujoco backend is preferred for control-oriented evaluation where routed
YAML

cat > backend_genesis.yaml <<'YAML'
schema_version: simulation_backend_genesis.v1
description: Backend-specific operational defaults for Genesis adapter.

backend:
  enabled: true
  sandbox_profile: sim_gpu_small
  gpu_allowed: true
  headless_default: true

limits:
  default_timeout_sec: 600
  cpu_limit: 4
  memory_limit_mb: 8192

artifacts:
  save_logs: true
  save_metrics: true
  save_video: true
  save_failure_snapshot: true

rules:
  - backend settings remain adapter-local
  - genesis runs must remain sandbox-bounded
YAML

cat > backend_isaac.yaml <<'YAML'
schema_version: simulation_backend_isaac.v1
description: Backend-specific operational defaults for Isaac adapter.

backend:
  enabled: true
  sandbox_profile: sim_gpu_large
  gpu_allowed: true
  headless_default: true

limits:
  default_timeout_sec: 900
  cpu_limit: 8
  memory_limit_mb: 16384

artifacts:
  save_logs: true
  save_metrics: true
  save_video: true
  save_failure_snapshot: true

rules:
  - backend settings remain adapter-local
  - isaac backend is intended for industrial and robotics-heavy scenarios
  - adapter config must not bypass sandbox policy
YAML

echo "simulation configs filled successfully"
