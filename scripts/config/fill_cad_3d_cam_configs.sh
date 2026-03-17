#!/usr/bin/env bash
set -euo pipefail

BASE="$HOME/MAKSIMAR_PLATFORM/CAD_3D_CAM_LAYER/config"
mkdir -p "$BASE"
cd "$BASE"

cat > cad_pipeline.yaml <<'YAML'
schema_version: cad_pipeline_config.v1
description: Canonical top-level configuration for CAD, 3D, and CAM pipeline layer.

registry:
  geometry_registry_enabled: true
  mesh_registry_enabled: true
  print_job_registry_enabled: true
  cnc_job_registry_enabled: true
  toolpath_registry_enabled: true

execution:
  validation_required_before_export: true
  direct_machine_execution_forbidden: true
  approval_required_for_machine_bound_jobs: true

defaults:
  geometry_validation_enabled: true
  mesh_validation_enabled: true
  artifact_logging_required: true

rules:
  - CAD/3D/CAM layer produces validated manufacturing artifacts, not machine authority
  - machine-bound outputs require approval before downstream execution
  - layer must not mutate CORE_ROOT
YAML

cat > mesh_pipeline.yaml <<'YAML'
schema_version: mesh_pipeline_config.v1
description: Canonical mesh processing policy for manufacturing-ready geometry assets.

processing:
  watertight_check_required: true
  manifold_check_required: true
  normals_check_required: true
  format_validation_required: true

export:
  supported_formats:
    - stl
    - obj
    - ply
    - step
  default_format: stl

rules:
  - mesh exports must remain explicit
  - invalid meshes must not be promoted as production-ready
  - mesh processing must preserve provenance
YAML

cat > print_pipeline.yaml <<'YAML'
schema_version: print_pipeline_config.v1
description: Canonical additive manufacturing pipeline policy.

validation:
  mesh_required: true
  slicer_profile_required: true
  material_profile_required: true
  approval_required_before_machine_use: true

defaults:
  dry_run_preview_enabled: true
  machine_start_forbidden: true

rules:
  - print jobs are preparation artifacts only until approved
  - slicer and material profile must remain explicit
  - print pipeline does not imply printer control authority
YAML

cat > cnc_pipeline.yaml <<'YAML'
schema_version: cnc_pipeline_config.v1
description: Canonical CNC preparation and toolpath policy.

validation:
  geometry_required: true
  toolpath_required: true
  machine_profile_required: true
  bounds_verification_required: true
  approval_required_before_machine_use: true

defaults:
  preview_required: true
  machine_start_forbidden: true

rules:
  - unsafe or out-of-bounds toolpaths must be blocked
  - CNC pipeline prepares jobs but does not start machines
  - machine-specific output remains approval-gated
YAML

echo "cad_3d_cam configs filled successfully"
