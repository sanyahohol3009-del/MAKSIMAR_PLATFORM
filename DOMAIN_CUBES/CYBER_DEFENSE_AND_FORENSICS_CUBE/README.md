# CYBER_DEFENSE_AND_FORENSICS_CUBE

Status: accepted first-class domain cube  
Role: defensive cyber-security, observability, incident response and forensics capability surface  
Authority: policy-bound domain capability; not an alternate core or hidden execution authority

## Purpose

`CYBER_DEFENSE_AND_FORENSICS_CUBE` is a native MAKSIMAR/JARVIS domain cube.
It exists to protect the platform, servers, containers, networks, local services and connected devices, and to provide a governed learning/forensics surface for defensive cyber-security work.

Core capability families include:

- process, network, port and filesystem observation
- container and runtime observation
- authentication and security event collection
- anomaly and suspicious-behavior detection
- scan / brute-force / exploitation-attempt detection
- resource-abuse detection
- IDS/IPS-style defensive decisions within owned infrastructure
- rate-limit, temporary-block and quarantine proposals
- incident correlation and timeline construction
- evidence collection, provenance and chain-of-custody records
- process/network/filesystem/container forensics
- reproducible incident reports
- isolated cyber-security training scenarios

## Defensive-only invariant

This cube is defensive by design.
It may observe, detect, classify, preserve evidence, isolate owned resources and propose governed protective action.
It must not become a hackback or retaliation system.

Forbidden outside explicitly owned/authorized lab environments:

- attacking external systems
- exploiting third-party hosts
- destructive counter-attacks
- unauthorized scanning
- retaliation against an attacker

Canonical response path:

```text
Detection
  -> Finding
  -> Risk Classification
  -> Response Proposal
  -> Policy / Approval Gate
  -> Controlled Execution
  -> Verification
  -> Evidence / Audit
```

## Linux knowledge and platform integration

The Linux kernel is treated as a knowledge, architecture and operating-system mechanism donor, not as a code blob to copy into MAKSIMAR.

Relevant mechanisms include:

- eBPF and tracepoints
- cgroup v2
- seccomp
- Landlock / LSM concepts
- namespaces
- Linux capabilities
- netlink
- audit / journald
- procfs / sysfs
- inotify / fanotify
- tracing / perf interfaces

MAKSIMAR implementations should use documented public interfaces and independently implemented userspace adapters/controllers/sensors.
Kernel implementation code is not to be silently copied, renamed or treated as proprietary MAKSIMAR code.

Expected integration families may include:

- `ProcessObserver`
- `NetworkObserver`
- `FilesystemObserver`
- `CgroupResourceController`
- `SeccompPolicyCompiler`
- `LandlockPolicyAdapter`
- `EBPFEventCollector`
- `AuditEvidenceCollector`
- `ForensicsTimelineBuilder`

These names describe capability ownership, not permission to create duplicate platform truth or policy layers.
Existing canonical registries, policy, evidence and memory truth must be reused.

## Workbench relationship

`JARVIS_DEVELOPER_WORKBENCH` may expose this cube's read models, findings, incidents, evidence, timelines and governed response proposals.

The Workbench remains downstream and must not directly:

- mutate firewall rules
- kill processes
- close ports
- quarantine containers
- change kernel parameters
- override cube policy

All such actions remain behind canonical platform policy/approval/execution boundaries.

## Godot 4 relationship

Godot 4 is the engine for additional visual dashboards.
A cyber-defense dashboard built with Godot 4 may visualize read models from this cube, while `JARVIS_DEVELOPER_WORKBENCH` provides the developer/operator inspection surface.
Neither UI becomes the source of truth.

## Training lab boundary

Training and offensive-technique study must occur only in owned, isolated and authorized lab environments.
Lab results may become JARVIS knowledge only after validation and accepted ingestion; lab state must not silently become production truth.

## Final rule

This cube is part of MAKSIMAR/JARVIS and must reuse existing platform truth, policy, registry, memory, evidence and execution boundaries rather than creating parallel security brains or duplicate authority layers.
