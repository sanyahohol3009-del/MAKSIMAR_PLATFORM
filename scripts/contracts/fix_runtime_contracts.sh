#!/usr/bin/env bash
set -e

cd "$HOME/MAKSIMAR_PLATFORM/MAKSIMAR_CORE/contracts/runtime"

cat > runtime_contract.v1.yaml <<'YAML'
contract_name: runtime_contract
schema_version: runtime_contract.v1
description: Canonical runtime state contract for foundation services.

required:
  - run_id
  - boot_id
  - runtime_state
  - started_at
  - schema_version

fields:
  run_id:
    type: string
    description: Unique runtime identifier for one active runtime lifecycle.

  boot_id:
    type: string
    description: Unique boot sequence identifier.

  runtime_state:
    type: string
    enum:
      - booting
      - healthy
      - degraded
      - shutdown_initiated
      - stopped
    description: Current runtime state.

  started_at:
    type: string
    format: date-time
    description: UTC timestamp when runtime started.

  last_transition_at:
    type: string
    format: date-time
    description: UTC timestamp of latest runtime state transition.

  active_components:
    type: array
    items:
      type: string
    description: Explicit list of active components currently expected to be running.

  runtime_paths_ref:
    type: string
    description: Reference to runtime paths contract or runtime path resolver source.

  source_of_truth:
    type: array
    items:
      type: string
    description: Ordered list of authoritative state sources used for runtime truth.

validation_rules:
  - run_id must be unique per boot cycle
  - runtime_state must match allowed enum
  - started_at must exist for every runtime instance
  - source_of_truth should list explicit evidence sources
  - active_components should not contain duplicates

security_rules:
  - no execution authority
  - no direct process control implied
  - runtime state is evidence and coordination metadata only
YAML

cat > pid_contract.v1.yaml <<'YAML'
contract_name: pid_contract
schema_version: pid_contract.v1
description: Canonical process identity contract.

required:
  - pid_id
  - component_name
  - pid
  - session_name
  - status

fields:
  pid_id:
    type: string
    description: Unique PID record identifier.

  component_name:
    type: string
    description: Logical component name bound to the PID.

  pid:
    type: integer
    description: Operating system process identifier.

  session_name:
    type: string
    description: Session or tmux session associated with the process.

  command_signature:
    type: string
    description: Stable normalized command signature for process identity checks.

  status:
    type: string
    enum:
      - running
      - stale
      - missing
      - stopped
    description: Current interpreted process state.

  created_at:
    type: string
    format: date-time
    description: UTC timestamp when PID record was created.

  updated_at:
    type: string
    format: date-time
    description: UTC timestamp of latest record update.

validation_rules:
  - pid must be positive integer
  - component_name must be unique within runtime role
  - status must match allowed enum
  - updated_at should not be earlier than created_at when both exist

security_rules:
  - no kill authority implied
  - pid record is evidence only
  - process identity does not grant control privileges
YAML

cat > heartbeat_contract.v1.yaml <<'YAML'
contract_name: heartbeat_contract
schema_version: heartbeat_contract.v1
description: Canonical heartbeat payload for monitored services.

required:
  - heartbeat_id
  - source
  - pid
  - wall_time
  - monotonic_time
  - status

fields:
  heartbeat_id:
    type: string
    description: Unique heartbeat record identifier.

  source:
    type: string
    description: Exact logical component emitting the heartbeat.

  pid:
    type: integer
    description: PID of the heartbeat-emitting process.

  wall_time:
    type: number
    description: Wall-clock time associated with heartbeat emission.

  monotonic_time:
    type: number
    description: Monotonic time associated with heartbeat emission.

  status:
    type: string
    enum:
      - warming_up
      - alive
      - stopped
      - degraded
    description: Health state reported by the source.

  sequence:
    type: integer
    description: Monotonic heartbeat sequence counter.

  metadata:
    type: object
    additional_properties: true
    description: Extra structured heartbeat metadata.

validation_rules:
  - monotonic_time must exist
  - source must identify exact component
  - pid must be positive integer
  - sequence should increase monotonically per source when present

security_rules:
  - heartbeat is evidence only
  - heartbeat does not authorize recovery or restart by itself
  - heartbeat metadata must not embed privileged commands
YAML

cat > incident_contract.v1.yaml <<'YAML'
contract_name: incident_contract
schema_version: incident_contract.v1
description: First-failure oriented runtime incident record.

required:
  - incident_id
  - timestamp
  - primary_failure
  - affected_layer
  - severity

fields:
  incident_id:
    type: string
    description: Unique incident identifier.

  timestamp:
    type: string
    format: date-time
    description: UTC timestamp of incident creation.

  primary_failure:
    type: string
    description: First identified failure cause.

  affected_layer:
    type: string
    description: Platform layer primarily affected by the incident.

  severity:
    type: string
    enum:
      - info
      - warning
      - critical
    description: Incident severity level.

  cascade_failures:
    type: array
    items:
      type: string
    description: Downstream failures caused by the primary failure.

  related_logs:
    type: array
    items:
      type: string
    description: References to relevant logs or log files.

  snapshot_ref:
    type: string
    description: Reference to supporting incident snapshot if present.

  resolution_status:
    type: string
    enum:
      - open
      - mitigated
      - resolved
      - archived
    description: Current incident lifecycle state.

validation_rules:
  - primary_failure must be populated
  - severity must match allowed enum
  - resolution_status must match allowed enum when present

security_rules:
  - incident records are append-oriented
  - incident record does not authorize remediation by itself
  - incident severity must not be silently downgraded without audit
YAML

cat > preflight_contract.v1.yaml <<'YAML'
contract_name: preflight_contract
schema_version: preflight_contract.v1
description: Canonical preflight validation snapshot before runtime startup.

required:
  - preflight_id
  - checked_at
  - stale_tmux_found
  - stale_pid_found
  - stale_heartbeat_found
  - port_conflict_found

fields:
  preflight_id:
    type: string
    description: Unique preflight snapshot identifier.

  checked_at:
    type: string
    format: date-time
    description: UTC timestamp of preflight execution.

  stale_tmux_found:
    type: boolean
    description: Whether stale tmux sessions were detected.

  stale_pid_found:
    type: boolean
    description: Whether stale PID files or mismatched PIDs were detected.

  stale_heartbeat_found:
    type: boolean
    description: Whether stale heartbeat state was detected.

  port_conflict_found:
    type: boolean
    description: Whether required ports were already occupied.

  previous_crash_found:
    type: boolean
    description: Whether evidence of previous abnormal termination was detected.

  details:
    type: object
    additional_properties: true
    description: Structured diagnostic details for preflight findings.

validation_rules:
  - checked_at is mandatory
  - all required findings must be explicit booleans
  - details should remain structured and serializable

security_rules:
  - no cleanup authority implied
  - preflight findings are diagnostic evidence only
  - destructive cleanup requires separate approved path
YAML

cat > event_journal_contract.v1.yaml <<'YAML'
contract_name: event_journal_contract
schema_version: event_journal_contract.v1
description: Append-only journal for runtime events.

required:
  - event_id
  - timestamp
  - component
  - event_type
  - severity

fields:
  event_id:
    type: string
    description: Unique journal event identifier.

  timestamp:
    type: string
    format: date-time
    description: UTC timestamp of event emission.

  component:
    type: string
    description: Component that emitted or owns the event.

  event_type:
    type: string
    description: Normalized event type label.

  severity:
    type: string
    enum:
      - info
      - warning
      - critical
    description: Event severity level.

  details:
    type: object
    additional_properties: true
    description: Structured event metadata payload.

validation_rules:
  - component must be present
  - event_type must be present
  - severity must match allowed enum

security_rules:
  - append only
  - journal entries are immutable audit evidence
  - event journal does not authorize action by itself
YAML

cat > boot_phase_contract.v1.yaml <<'YAML'
contract_name: boot_phase_contract
schema_version: boot_phase_contract.v1
description: Canonical boot phase state record.

required:
  - phase_id
  - phase_name
  - status
  - started_at

fields:
  phase_id:
    type: string
    description: Unique boot phase identifier.

  phase_name:
    type: string
    description: Human-readable boot phase name.

  status:
    type: string
    enum:
      - pending
      - running
      - done
      - failed
    description: Current boot phase status.

  started_at:
    type: string
    format: date-time
    description: UTC timestamp when the phase started.

  finished_at:
    type: string
    format: date-time
    description: UTC timestamp when the phase finished.

  duration_sec:
    type: number
    description: Computed phase duration in seconds.

  message:
    type: string
    description: Optional human-readable status message.

validation_rules:
  - phase_name must be unique inside one boot sequence
  - status must match allowed enum
  - finished_at should exist when status is done or failed

security_rules:
  - informational only
  - boot phase record does not imply transition authority
  - failed phases must remain visible for diagnostics
YAML

echo "runtime contracts restored successfully"
