#!/usr/bin/env bash
set -e

cd "$HOME/MAKSIMAR_PLATFORM/MAKSIMAR_CORE/contracts/cad_3d_cam"

cat > geometry_object.v1.yaml <<'YAML'
contract_name: geometry_object
schema_version: geometry_object.v1
description: Canonical geometry object descriptor.

required:
  - geometry_id
  - geometry_type

fields:
  geometry_id:
    type: string
    description: Unique geometry object identifier.

  geometry_type:
    type: string
    enum:
      - sketch
      - mesh
      - solid
      - toolpath
    description: Canonical type of geometry asset.

  source_ref:
    type: string
    description: Reference to source object, image, or upstream artifact.

  format:
    type: string
    description: Native or exchange format of the geometry object.

validation_rules:
  - geometry_id required
  - geometry_type must match allowed enum
  - format should be explicit for persisted objects

security_rules:
  - object metadata only
  - geometry object does not imply manufacturing authority
  - source references must remain traceable
YAML

cat > mesh_contract.v1.yaml <<'YAML'
contract_name: mesh_contract
schema_version: mesh_contract.v1
description: Mesh descriptor for STL, OBJ, or similar manufacturing-ready assets.

required:
  - mesh_id
  - source_geometry_ref
  - format

fields:
  mesh_id:
    type: string
    description: Unique mesh asset identifier.

  source_geometry_ref:
    type: string
    description: Reference to source geometry object.

  format:
    type: string
    description: Mesh file format or canonical representation.

  watertight:
    type: boolean
    description: Whether the mesh is watertight.

  validated:
    type: boolean
    description: Whether mesh validation has been completed.

validation_rules:
  - mesh_id required
  - source_geometry_ref required
  - format required
  - validated must be explicit for production-facing meshes

security_rules:
  - validation state must be explicit
  - mesh assets do not authorize print or machine start
  - non-validated meshes must not be treated as production-safe by default
YAML

cat > print_job.v1.yaml <<'YAML'
contract_name: print_job
schema_version: print_job.v1
description: Canonical print job contract for additive manufacturing workflows.

required:
  - print_job_id
  - mesh_ref
  - material_profile

fields:
  print_job_id:
    type: string
    description: Unique print job identifier.

  mesh_ref:
    type: string
    description: Reference to mesh asset used for printing.

  material_profile:
    type: string
    description: Material profile selected for the print.

  slicer_profile_ref:
    type: string
    description: Reference to slicer profile or slicing preset.

  approval_required:
    type: boolean
    description: Whether explicit approval is required before any real print execution.

validation_rules:
  - print_job_id required
  - mesh_ref required
  - material_profile required
  - approval_required must be explicit for real-world print paths

security_rules:
  - no direct hardware start without approval policy
  - print job contract is planning metadata, not machine authority
  - unsafe or unvalidated mesh use must remain reviewable
YAML

cat > cnc_job.v1.yaml <<'YAML'
contract_name: cnc_job
schema_version: cnc_job.v1
description: Canonical CNC job contract.

required:
  - cnc_job_id
  - geometry_ref
  - toolpath_ref

fields:
  cnc_job_id:
    type: string
    description: Unique CNC job identifier.

  geometry_ref:
    type: string
    description: Reference to source geometry used for machining.

  toolpath_ref:
    type: string
    description: Reference to generated toolpath artifact.

  machine_profile_ref:
    type: string
    description: Reference to machine profile or machine capability definition.

  material_profile:
    type: string
    description: Material profile selected for machining.

validation_rules:
  - cnc_job_id required
  - geometry_ref required
  - toolpath_ref required
  - machine_profile_ref should be explicit for machine-bound jobs

security_rules:
  - machine execution requires separate approval
  - cnc job contract does not authorize machine motion
  - unsafe toolpaths must remain blocked by downstream validation and approval
YAML

cat > toolpath_contract.v1.yaml <<'YAML'
contract_name: toolpath_contract
schema_version: toolpath_contract.v1
description: Canonical toolpath descriptor for CNC or related machine execution planning.

required:
  - toolpath_id
  - source_geometry_ref
  - machine_type

fields:
  toolpath_id:
    type: string
    description: Unique toolpath identifier.

  source_geometry_ref:
    type: string
    description: Reference to source geometry object used to generate the toolpath.

  machine_type:
    type: string
    description: Canonical machine type targeted by the toolpath.

  format:
    type: string
    description: Toolpath format or postprocessor output format.

  bounds_verified:
    type: boolean
    description: Whether machine bounds and movement envelope were verified.

validation_rules:
  - toolpath_id required
  - source_geometry_ref required
  - machine_type required
  - bounds_verified must be explicit for machine-bound toolpaths

security_rules:
  - unsafe toolpaths must be flagged
  - toolpath artifacts do not imply execution permission
  - machine-specific outputs remain subject to approval and validation
YAML

echo "cad_3d_cam contracts restored successfully"
