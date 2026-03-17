#!/usr/bin/env bash
set -e

cd "$HOME/MAKSIMAR_PLATFORM/MAKSIMAR_CORE/contracts/robotics"

cat > robot_model.v1.yaml <<'YAML'
contract_name: robot_model
schema_version: robot_model.v1
description: Canonical robot model descriptor.

required:
  - robot_model_id
  - robot_type
  - kinematic_profile_ref

fields:
  robot_model_id:
    type: string
    description: Unique robot model identifier.

  robot_type:
    type: string
    description: Canonical robot class or mechanism type.

  kinematic_profile_ref:
    type: string
    description: Reference to kinematic profile definition.

  dynamic_profile_ref:
    type: string
    description: Reference to dynamic profile definition.

  constraint_refs:
    type: array
    items:
      type: string
    description: References to applicable robotics constraints.

validation_rules:
  - robot_model_id required
  - robot_type required
  - kinematic_profile_ref required
  - constraint_refs should be explicit even when empty

security_rules:
  - model metadata only
  - robot model does not imply hardware execution authority
  - model references must remain explicit and reviewable
YAML

cat > controller_contract.v1.yaml <<'YAML'
contract_name: controller_contract
schema_version: controller_contract.v1
description: Controller definition for robotics policies and control loops.

required:
  - controller_id
  - controller_type

fields:
  controller_id:
    type: string
    description: Unique controller identifier.

  controller_type:
    type: string
    description: Canonical controller type.

  target_robot_model:
    type: string
    description: Reference to target robot model.

  parameter_schema:
    type: object
    additional_properties: true
    description: Structured parameter schema for controller configuration.

  safety_limits_ref:
    type: string
    description: Reference to safety limits applied to this controller.

validation_rules:
  - controller_id required
  - controller_type required
  - target_robot_model should be explicit for concrete controllers

security_rules:
  - no direct deployment authority
  - controller definitions do not bypass approval policy
  - safety limits must remain externally reviewable
YAML

cat > constraint_contract.v1.yaml <<'YAML'
contract_name: constraint_contract
schema_version: constraint_contract.v1
description: Safety and physical constraints for robotics execution.

required:
  - constraint_id
  - constraint_type

fields:
  constraint_id:
    type: string
    description: Unique constraint identifier.

  constraint_type:
    type: string
    description: Canonical type of physical or safety constraint.

  values:
    type: object
    additional_properties: true
    description: Structured constraint values and bounds.

  severity:
    type: string
    description: Severity level associated with violating this constraint.

validation_rules:
  - constraint_id required
  - constraint_type required
  - values required
  - severity should be explicit

security_rules:
  - constraint violations must be blocking where policy demands
  - constraints do not authorize execution
  - unsafe bounds must remain visible in downstream review
YAML

cat > calibration_contract.v1.yaml <<'YAML'
contract_name: calibration_contract
schema_version: calibration_contract.v1
description: Calibration dataset or record for robot hardware.

required:
  - calibration_id
  - robot_model_id
  - calibration_type

fields:
  calibration_id:
    type: string
    description: Unique calibration record identifier.

  robot_model_id:
    type: string
    description: Reference to robot model being calibrated.

  calibration_type:
    type: string
    description: Type of calibration process or dataset.

  calibration_data_ref:
    type: string
    description: Reference to calibration data asset.

  verified:
    type: boolean
    description: Whether calibration has been verified by approved process.

validation_rules:
  - calibration_id required
  - robot_model_id required
  - calibration_type required
  - calibration_data_ref required for persistent calibration records

security_rules:
  - calibration updates require approval
  - unverified calibration must not be treated as production-safe
  - calibration records do not imply hardware activation rights
YAML

cat > hardware_bridge_contract.v1.yaml <<'YAML'
contract_name: hardware_bridge_contract
schema_version: hardware_bridge_contract.v1
description: Boundary contract between simulated or proposed control and real hardware.

required:
  - bridge_id
  - robot_model_id
  - bridge_mode

fields:
  bridge_id:
    type: string
    description: Unique hardware bridge identifier.

  robot_model_id:
    type: string
    description: Target robot model for this bridge boundary.

  bridge_mode:
    type: string
    enum:
      - sandbox
      - limited_hardware_test
      - blocked
    description: Allowed execution boundary mode for this bridge.

  approval_required:
    type: boolean
    description: Whether explicit approval is required before any bridge usage.

validation_rules:
  - bridge_id required
  - robot_model_id required
  - bridge_mode must match allowed enum
  - limited_hardware_test must imply approval_required=true

security_rules:
  - sandbox default
  - no direct production deploy
  - hardware bridge never bypasses approval or immutable safety rules
YAML

echo "robotics contracts restored successfully"
