# Phase 10 Swarm Acceptance v1

Acceptance criteria covered by deterministic contracts and smoke tests:

- Swarm task routing uses the existing verified-owner autonomous model and tool router semantics.
- Agents select model and tool roles from task intent without slash commands.
- Swarm agents can propose, analyze, route, and explain, but cannot execute shell, PC, deploy, or canonical-memory actions directly.
- Heavy GPU concurrency is blocked when two heavy agents are requested at the same time.
- Voice-unverified direct PC action is denied.
- Verified terminal owner safe browser action is delegated to the Action Library path instead of executed by swarm.
- Swarm observability exposes active agents, selected model role, selected tools, conflict status, heavy GPU lock state, and direct-execution-disabled state.
