#!/usr/bin/env bash
set -euo pipefail

BASE="$HOME/MAKSIMAR_PLATFORM/ROBOTICS_LAYER/config"
mkdir -p "$BASE"
cd "$BASE"

cat > robotics_layer.yaml <<'YAML'
schema_version: robotics_layer_config.v1
description: Canonical top-level configuration for robotics and hardware control layer.

registry:
  robot_registry_enabled: true
  controller_registry_enabled: true
  kinematics_registry_enabled: true
  hardware_adapter_registry_enabled: true

execution:
  simulation_required_for_validation: true
  direct_hardware_execution_forbidden: true
  approval_required_for_real_hardware: true

defaults:
  safety_constraints_enabled: true
  telemetry_required: true
  command_logging_required: true

rules:
  - robotics layer must not execute hardware commands without approval
  - robotics modules must pass simulation validation before proposal
  - robotics layer must not mutate CORE_ROOT
YAML


cat > robot_registry.yaml <<'YAML'
schema_version: robotics_robot_registry.v1
description: Canonical registry for robot model definitions.

robots:

  quadruped:
    enabled: true
    class: locomotion

  manipulator:
    enabled: true
    class: industrial_arm

  mobile_base:
    enabled: true
    class: wheeled_robot

  cnc_machine:
    enabled: true
    class: industrial_motion

  printer_3d:
    enabled: true
    class: additive_manufacturing

rules:
  - robot models must remain explicit
  - robot registry must not contain hidden devices
  - registry must remain auditable
YAML


cat > controller_policy.yaml <<'YAML'
schema_version: robotics_controller_policy.v1
description: Canonical policy for robot controllers and control algorithms.

controllers:

  pid_controller:
    enabled: true

  model_predictive_controller:
    enabled: true

  rl_policy_controller:
    enabled: true

requirements:
  safety_check_required: true
  constraint_validation_required: true

rules:
  - controllers must respect safety constraints
  - controller outputs must remain bounded
  - controller policy must remain simulation-verifiable
YAML


cat > safety_constraints.yaml <<'YAML'
schema_version: robotics_safety_constraints.v1
description: Canonical safety constraints for robotics and machine motion.

constraints:

  max_velocity_check: true
  max_torque_check: true
  workspace_limit_check: true
  collision_detection_required: true
  emergency_stop_supported: true

rules:
  - constraint violation must block execution
  - safety constraints must remain active even in testing
  - constraints must be evaluated before hardware command dispatch
YAML


cat > hardware_adapters.yaml <<'YAML'
schema_version: robotics_hardware_adapter_registry.v1
description: Canonical registry for robotics hardware adapters.

adapters:

  ros2_adapter:
    enabled: true

  serial_motion_adapter:
    enabled: true

  ethernet_robot_adapter:
    enabled: true

  plc_bridge_adapter:
    enabled: true

rules:
  - adapters must not bypass safety constraints
  - hardware adapters must remain policy bounded
  - adapter configuration must remain auditable
YAML


echo "robotics configs filled successfully"
