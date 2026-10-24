# Phase 1 Dependency Map

```text
MAKSIMAR_CORE_LIB contracts and ProjectUnderstandingPort
                         ^
                         |
tools/jarvis_live_runtime existing project adapter implementation
                         ^
                         |
CONTROL_PLANE composition root and canonical project-read orchestrator
                         |
       existing model transport and public Final Brain facade
```

Core has no import of `tools`, `MAKSIMAR_SERVER`, concrete project adapters or
Ollama. Capability requirements are produced before provider/tool discovery.
The single injected project adapter owns no writable state and performs no network
requests. The API remains the sole HTTP server.

