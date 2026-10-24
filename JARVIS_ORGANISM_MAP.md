# JARVIS ORGANISM MAP

> THIS DOCUMENT IS A HUMAN/AGENT ORIENTATION MAP.
>
> RUNTIME AUTHORITY REMAINS IN: canonical capability/operation contracts, the
> canonical registry/projection (`existing_capability_inventory`), HOST policy,
> runtime availability, and evidence/receipts.
>
> **DO NOT ROUTE OR AUTHORIZE FROM THIS MARKDOWN.** The map exists so DeepSeek,
> Codex, future JARVIS developer agents, and the owner can immediately understand
> the organism. It is a snapshot, not runtime truth.

- Generated: 2026-08-18
- Git: branch `deflation/live-hotpath-reset-v1`, HEAD `85b9b32`
- Scope: WSL2 host + referenced external runtime roots
- Canonical projection source: `MAKSIMAR_SERVER/SKILL_ADAPTER_REGISTRY/existing_capability_inventory.build_semantic_capability_registry_projection()`

## State definitions

- CANONICAL — authoritative typed contract/registry entry
- INSTALLED — present on the machine (filesystem/venv/package)
- REACHABLE — a canonical caller can reach it through the real path
- LIVE_VERIFIED — a real execution produced real result/evidence
- PARTIAL / STUB / MANIFEST_ONLY / INSTALLED_NOT_WIRED / UNAVAILABLE / LEGACY / DUPLICATE / DRIFTED — as named

---

## 1. MODEL ORGANISM (roles vs models are distinct)

| role | profile id | wrapper (tag) | base | purpose | load policy | transport | state |
|---|---|---|---|---|---|---|---|
| MAIN CHAT / ORCHESTRATION | `jarvis_chat_model` | `jarvis:chat8b` | `qwen3:8b` | normal cognition + PC/screen/browser/memory/project/tool orchestration | installed_ollama_wrapper | Ollama /api/chat | REACHABLE |
| HELPER | `helper_input_correction_model` | `jarvis:helper3b` | `qwen2.5-coder:3b` | STT/typing/input correction | installed_ollama_wrapper | Ollama | REACHABLE |
| DAILY CODER | `daily_coder_model` | `jarvis:coder7b` | `qwen2.5-coder:7b` | routine code | installed_ollama_wrapper | Ollama | REACHABLE |
| HEAVY CODER | `heavy_coder_model` | `jarvis:coder14b` | `qwen2.5-coder:14b` | complex code/architecture | load_on_demand (exclusive GPU) | Ollama | REACHABLE (cold) |
| HEAVY_REASONING | `heavy_reasoning_model` | `jarvis-live:qwen14b` | `qwen2.5-coder:14b` | EXCEPTIONAL semantic verification only (not a default mutation verifier) | load_on_demand | Ollama | Parent verified 2026-10-09; [actual think=false transport PASS 2026-10-13](RUNTIME/audits/WSL_RECOVERY_ACTIVATION_20261011/master_heavy_think_false_canonical_cold_deadline_actual.json); full semantic-role acceptance PENDING |

Owner amendment 2026-10-09: Qwen2.5-Coder 14B is accepted for the existing heavy_reasoning_model role. The canonical typed profile and actual Ollama wrapper parent now agree. The role remains distinct from heavy_coder_model, correction-only helper and execution authority; this amendment does not promote model output into permission or execution receipts.

Base tags (`qwen3:8b`, `qwen2.5-coder:3b/7b/14b`) are BASE_RUNTIME_MODEL, NOT duplicates of the wrappers.

## 2. INTERNAL JARVIS AGENTS (distinct from external frameworks)

| agent | responsibility | model role | current state |
|---|---|---|---|
| `action_worker_agent` | bounded execution of authorized canonical actions | chat 8B | contract/inventory (reachability unverified) |
| `architect_agent` | architecture reasoning | coder 14B | contract (unverified) |
| `conversation_agent` | conversation | chat 8B | contract (hot path reachable) |
| `project_coder_agent` | project coding | daily/heavy coder | contract (unverified) |
| `safety_guard_agent` | safety/policy guard | chat 8B + HOST policy | contract (unverified) |
| `tool_selector_agent` | tool selection | chat 8B | contract (unverified) |

Source: `real_node_agents_contract` (3 node agents), `swarm_agent_role_contract`, `swarm_task_router`, capability inventory entries.

## 3. EXTERNAL AGENT FRAMEWORKS (installed, NOT yet wired)

`MAKSIMAR_RUNTIME/venvs/agent_tooling` — verified import OK:

| package | version | wired? | unique value |
|---|---|---|---|
| autogen-agentchat / autogen-core / autogen-ext | 0.7.5 | NO | multi-agent orchestration |
| openai-agents-python | 0.17.6 | NO | agents SDK |
| crewai | 1.14.7 | NO | crew composition |
| langgraph | 1.2.6 | NO | graph agents |
| mcp | 1.26.0 | NO | model-context-protocol |

`smolagents` 1.26.0 lives in the PROJECT `.venv` (not agent_tooling). Do not wire a framework merely because it is installed.

## 4. BROWSER TOOLING — `venvs/browser_tooling`

browser-use (import OK), playwright, beautifulsoup4, lxml. Relates to `windows.browser` / web-search / page extraction. Normal atomic `open_browser` does NOT traverse browser-use unless composition requires it.

## 5. RAG / DOCUMENT TOOLING — `venvs/rag_tooling`

llama-index, langchain family, duckdb (import OK), pypdf, python-docx, beautifulsoup, pandas, openpyxl. Classified by capability contribution (retrieval/document parsing), not package name.

## 6. MEMPALACE (one capability across a boundary)

- PROJECT: contracts/adapters/manifests/policy/evidence integration.
- RUNTIME: `EXTERNAL_BACKENDS/mempalace/{venv,source,manifests,smoke_reports,security_reports}` — `import mempalace` **3.3.5 OK**.
- One organism, not four duplicates.

## 7. RETRIEVAL BACKENDS

mgrep (vendor_quarantine node_modules present; runtime/executable still to verify), qdrant, sqlite-vec, local history/session memory. Explicit-provider constraint support + no silent fallback is required (T12 law).

## 8. N8N

`EXTERNAL_BACKENDS/vendor_quarantine/n8n` source tree present. SOURCE_PRESENT ≠ LIVE_RUNTIME. Not wired as live until proven.

## 9. FLUTTER — APPLICATION/PLATFORM TOOLCHAIN (NOT hot path)

`MAKSIMAR_RUNTIME/tools/flutter`. Developer/application outcomes (build app, inspect/run Flutter tooling, client development). Used through code/developer skills/agents when semantically needed, never as a normal hot-path capability.

## 10. VOICE / EDGE (separate WSL vs Windows truth)

- Windows: `/mnt/c/MAKSIMAR_EDGE/.venv` (RealtimeSTT, faster-whisper, PyAudio — Windows-side).
- WSL: `venvs/faster_whisper_stt`, `kokoro_tts`, `silero_tts` (directory exists; import unverified this pass).
- Do not collapse Windows/WSL into one boolean.

## 11. PC CONTROL (canonical operation contracts)

`PC_ACTION_OPERATION_CONTRACTS` — group by semantic owner:

- `windows.volume`: `execute_volume_up/down/mute_toggle`
- `windows.input`: `execute_type_text`
- `windows.browser`: `execute_open_browser/open_opera/close_*/browser_search`
- `screen.observe`: `observe_windows_screen`

Executor: `tools/jarvis_live_runtime/owner_pc_actions.py` (`resolve_owner_pc_operation` → identity → policy → approval → target → executor). Approval: `jarvis_pc_action_approval_binding`. Policy: `workflow_runtime_policy` + `capability_registry`. Evidence: `pc_action_result` / `windows_screen_capture`. Hot atomic operations use the shortest correct path (no agent).

## 12. SKILLS

Canonical wired skill: `skill_simulation_simulation_analysis`. Skill adapter registry has 1 enrolled skill; the skill layer is mostly stub. Inventory separately: canonical skills vs runtime/vendor/framework skills.

## 13. WORKERS

`worker_sim_001` (EXECUTABLE → `run_simulation_task`), `worker_ai_001` + `worker_voice_001` (VISIBILITY_ONLY). Runtimes under `MAKSIMAR_SERVER/WORKERS/` (simulation_worker, action_recording, action_replay_preview, sandboxed_action).

## 14. MEMORY / PROJECT / SIMULATION / CODE

- `memory.retrieve` → `search_history` (memory_retrieval_adapter) + local_session_history.
- `project.read` → `local_project_worktree` (search, inspect_git_status, query_codegraph, read_file_*) + codegraph_readonly_adapter.
- `simulation.run` → `run_simulation_task`; `simulation.delegate` → worker delegation.
- `code.reason` → `draft_daily/heavy_code_proposal` (model_role_adapter).

## 15. SWARM / COLLABORATION

`MAKSIMAR_CORE_LIB/swarm_coordination` — TASK/CLAIM/EVIDENCE/REVIEW as the shared collaboration/evidence bus. Not a second semantic brain. Autonomous production agent collaboration remains roadmap-gated.

## 16. IGNORE-AWARE RUNTIME ROOTS (git visibility ≠ runtime truth)

- `/home/aleksandr/MAKSIMAR_RUNTIME` (+ `venvs`, `tools/flutter`)
- `/mnt/c/MAKSIMAR_EDGE/.venv`
- `EXTERNAL_BACKENDS/mempalace/venv`
- `EXTERNAL_BACKENDS/vendor_quarantine/retrieval_backends/mgrep`
- `EXTERNAL_BACKENDS/vendor_quarantine/n8n`

Ignore rules: `.gitignore` `venv/`, `EXTERNAL_BACKENDS/**/security_reports/*.json`; `.git/info/exclude` `EXTERNAL_BACKENDS/vendor_quarantine/`.

## 17. DUPLICATE / DRIFT

- project.read parallel implementations (codegraph_readonly_adapter vs read models) — audit, do not delete.
- legacy jarvis_live runtime paths — classify reachable vs unreachable.
- direct Ollama callers / parallel semantic routers / duplicate policy gates — drift audit before migration.
- Backup/audit dirs (`MAKSIMAR_BACKUPS`, `MAKSIMAR_AUDIT_*`, `*.zip`) = HISTORICAL_EVIDENCE, not runtime duplicates.

## 18. ABSENCE

Only mark GENUINELY_ABSENT after checking registry + source + external runtime + package + service + caller. Currently no new production implementation is justified.

## 19. SPEED CLASSIFICATION

- HOT_ATOMIC: volume, type_text, screen observe, open_browser, search, memory retrieve — 8B → HOST → shortest executor → evidence.
- HOT_RETRIEVAL: project read, memory search.
- COMPOSED_SKILL: simulation analysis.
- BOUNDED_AGENT: only where agent semantics add real value.
- WORKER: simulation task execution.
- SPECIALIST_MODEL: complex code/architecture (7B/14B), exceptional reasoning (HEAVY_REASONING).
- APPLICATION_TOOLCHAIN: Flutter (developer outcomes only).

## 20. LAWS

REUSE → EXTEND → MIGRATE → PROVE → DELETE. Live acceptance = CONTRACT + REACHABILITY + LIVE_VERIFIED. UNDERSTANDING (LLM) ≠ AUTHORIZATION (HOST). ONE SEMANTIC FACT ONCE. No keyword/regex/phrase routing.

---

## LIVE ACCEPTANCE LEDGER (2026-08-19, real E2E via /jarvis-live/hot + Windows Edge)

Truth levels: INSTALLED < AVAILABLE < CANONICAL_REACHABLE < EXECUTOR_INVOKED < EFFECT_OBSERVED < FULL_E2E_LIVE_VERIFIED.

### PC family (Windows Edge, per-action subprocess)

| action | semantic owner | operation | effect/risk | status |
|---|---|---|---|---|
| read_screen | screen.observe | observe_windows_screen | OBSERVE/READ_ONLY | FULL_E2E_LIVE (real screenshot + sha256) |
| volume_up | windows.volume | execute_volume_up | MUTATE | FULL_E2E_LIVE (CoreAudio 0.19→0.24) |
| volume_down | windows.volume | execute_volume_down | MUTATE | FULL_E2E_LIVE (CoreAudio 0.24→0.19) |
| volume_mute | windows.volume | execute_volume_mute_toggle | MUTATE | FULL_E2E_LIVE (mute false→true→false) |
| open_browser | windows.browser | execute_open_browser | MUTATE | EFFECT_OBSERVED (msedge Session 1; owner-confirmed) |
| open_opera | windows.browser | execute_open_opera | MUTATE | CANONICAL_REACHABLE (not yet live-proven) |
| close_opera | windows.browser | execute_close_one_opera_window | IRREVERSIBLE/DANGEROUS | CANONICAL_REACHABLE (safe proof pending) |
| close_all_opera | windows.browser | execute_close_all_opera_processes | IRREVERSIBLE/DANGEROUS | CANONICAL_REACHABLE (keep risk truth) |
| browser_search | windows.browser | execute_browser_search | MUTATE | CANONICAL_REACHABLE (navigation proof pending) |
| type_text | windows.input | execute_type_text | IRREVERSIBLE/DANGEROUS | CANONICAL_REACHABLE (controlled target pending) |
| read_windows_edge_status | windows.edge | read_windows_edge_status | OBSERVE/READ_ONLY | CANONICAL_REACHABLE |

ACCIDENTAL_PC_ORPHANS = 0.

### project.read

| operation | status |
|---|---|
| inspect_git_status | FULL_E2E_LIVE (branch deflation/live-hotpath-reset-v1 + dirty counts match real `git status`) |
| remaining 16 ops | CANONICAL_REACHABLE (real repo read proof pending per-op) |

Canonical volume path = CoreAudio `coreaudio_volume.py` (comtypes, session-agnostic). `keybd_event` retained only as fallback (not used for volume when CoreAudio succeeds).

Canonical execution-truth law: `COMMAND SENT != EFFECT`; `EXECUTOR SUCCESS != EFFECT`; `RECEIPT != EFFECT`.

### retrieval / memory backends (2026-08-19)

| component | version | state | blocker/note |
|---|---|---|---|
| mgrep (@mixedbread/mgrep) | 0.1.13 | INSTALLED + RUNNABLE (node CLI) | UNAVAILABLE_WITH_EXACT_BLOCKER: `search` requires mixedbread cloud login (syncs to cloud store); no local offline mode + no credential |
| Mempalace | 3.3.5 | INSTALLED + RUNNABLE (import OK) | full memory/graph/vector system; canonical integration = mcp_server (ChromaBackend+KnowledgeGraph+handle_request) or searcher.search_memories; store init + real query pending |

### semantic findings (open)

- browser_search: "найди в браузере информацию про X" mis-selected conversation.respond (not browser_search) — semantic selection gap, not a wiring bug.

---

## CONTINUATION CHECKPOINT

Single resume source: `RUNTIME/audits/PERSONAL_JARVIS_RECOVERY_PHASE_1B_20260717_170146/P2_CONTINUATION_CHECKPOINT.md` (worktree state, completed-do-not-redo, exact resume point, permanent laws, boot rule).

### memory.retrieve (2026-08-19)

- "что мы делали в этой сессии с громкостью" → selected `runtime_history_store` (correct owner) but returned a generic/hallucinated response (claimed "0 dirty files", wrong). Cross-session history retrieval is session-scoped; real global/session memory retrieval + grounded evidence is the remaining edge (needs Mempalace/history store wiring).

### simulation + input + model-role (2026-08-19)

- simulation.analyze = FULL_E2E_LIVE: `skill_simulation_simulation_analysis` → `analyze_simulation` → real result (control_val → 0.18 → control_validation_completed). run/analyze are distinct outcomes.
- type_text = SESSION-SPECIFIC BLOCKER: `SendKeys` types into the subprocess's active window; the WSL-launched python.exe cannot control the interactive foreground window, and the hot request hangs/returns empty. Effect unproven; not LIVE.
- model roles / direct Ollama cleanup = CLEAN: legacy `tools/jarvis_live_runtime/*` reference ollama only via imports; no direct `requests/urllib`/`/api/chat` HTTP bypasses. Role → profile → canonical transport convergence holds.

### windows.input type_text — diagnostic update (2026-08-19)

Root cause corrected: NOT a session blocker. Notepad opens in the interactive session. Real failure = window targeting + injection mechanism.

- FIXED: window targeting (`_focus_notepad` via win32gui FindWindow("Notepad") class + SetForegroundWindow + GetForegroundWindow verify). focus_verified now true.
- FIXED: readback (`_read_notepad_text` via RichEditD2DPT WM_GETTEXT; prefers longest non-empty text control).
- REMAINING (injection mechanism):
  - WScript.Shell.SendKeys = keyboard-layout-dependent (types Cyrillic on RU layout).
  - SendInput(KEYEVENTF_UNICODE) = UIPI-blocked (returns 0 from WSL-spawned process).
  - clipboard Set-Clipboard + SendKeys('^v') = race (empty paste).
  - Fix direction: set US keyboard layout before SendKeys, or clipboard+delay. Effect-not-yet-verified.

Status: windows.input = CANONICAL_REACHABLE / EXECUTOR_ATTEMPTED / EFFECT_NOT_YET_VERIFIED / FOCUS_TARGETING_ROOT_CAUSE_PENDING (injection mechanism).

### windows.input type_text — FULL_E2E_LIVE (2026-08-19)

- FIXED: target-aware text insertion via EM_SETSEL(-1,-1) + EM_REPLACESEL on the RichEditD2DPT control (no keyboard emulation). Layout-independent + Unicode-capable ("TEST_JARVIS_4821 Привет äöü ß" inserted + read back exactly).
- FIXED: Windows Edge JSON output ensure_ascii=True (was cp1251 console crash on Unicode).
- effect_observed=True (exact text verified in target). windows.input = FULL_E2E_LIVE (Unicode-capable).

### browser_search + type_text (2026-08-19)

- type_text = FULL_E2E_LIVE (target-aware EM_REPLACESEL; Unicode; effect_observed=true)
- browser_search semantic gap FIXED: generic "named instrument → operational goal" clause → "найди в браузере" now selects browser_search (was conversation.respond). Correctly PARTIAL_APPROVAL_REQUIRED (navigation = external effect).

### memory.retrieve search_history — grounded (2026-08-19)

- ROOT CAUSE: `search_history` queried a placeholder `build_minimal_memory_object()` (single hardcoded object), not real history → FinalBrain hallucinated.
- FIX: `search_history` now returns BOTH real `session_records` (`_read_recent_local_chat_records`) + the history query, so FinalBrain grounds on real stored records.

### n8n (2026-08-19)

- n8n-monorepo 2.26.0 = SOURCE-ONLY (vendor_quarantine/n8n); node_modules absent, no build. Runnable only after `pnpm install` (download/install).
- Existing adapters: MAKSIMAR_SERVER/WORKFLOW_AUTOMATION_RUNTIME/n8n_adapter_contract.py + n8n_vendor_gate_runtime.py + n8n_manifest.json + workflow_engine/n8n_graph_compatibility_contract.py.
- BLOCKER (owner-level): requires dependency install to run. Not LIVE.

### workers + internal agents (2026-08-19)

- workers: worker_sim_001 (simulation_worker/worker_runtime.py, REAL), worker_ai_001 + worker_voice_001 (workers_registry identity + role bindings). All registered; ACCIDENTAL_WORKER_ORPHANS=0.
- internal agents: swarm_coordination/swarm_agent_role_contract.py + real_node_agents/. Canonical roles (action_worker/architect/conversation/project_coder/safety_guard/tool_selector) live under swarm + real_node_agents.

### Mempalace — real query PROVEN (2026-08-19)

- init → auto-mine → search worked end-to-end: probe_note.md mined (1 drawer, room "general"), `search "QWERTY_ZEBRA_917"` returned the exact source text with cosine=0.277 + bm25=0.288.
- Retrieval pipeline (ChromaDB embedding + lexical) = FUNCTIONALLY LIVE.
- Canonical integration edge remaining: wire `mempalace.searcher.search_memories(palace_path=...)` (or MCP `mempalace_search` tool) into memory_retrieval_adapter under memory.retrieve provider selection. MCP server has 30+ tools (mempalace_search, kg_query, kg_add, tunnels, drawers).

### voice + external venvs (2026-08-19)

- VOICE = FULL_E2E_LIVE: kokoro TTS synthesized "Hello Jarvis, voice round trip test." → /tmp/kokoro_test.wav; faster_whisper STT transcribed it back to "Hello Jarvis, Voice Round Trip Test." (exact). Real audio → real transcript round-trip.
- External venvs (/home/aleksandr/MAKSIMAR_RUNTIME/venvs): agent_tooling (langgraph, crewai, openai); browser_tooling (playwright, browser_use, openai, pypdf, docx); rag_tooling (llama_index, langchain, langgraph, openai, pandas, pypdf, docx, duckdb); faster_whisper_stt (faster_whisper); kokoro_tts (kokoro); silero_tts (silero vendored).

### browser + RAG providers (2026-08-19)

- Playwright = UNAVAILABLE_WITH_EXACT_BLOCKER: package installed (browser_tooling), but chromium binaries not downloaded (requires `playwright install` = download/install). browser_use co-located.
- RAG/document stack = FUNCTIONALLY LIVE: duckdb (real SQL → {'tag':'RAG_PROBE_OK','val':5}), pandas (DataFrame sum), pypdf 6.14.0 in rag_tooling venv.
- External frameworks: smolagents 1.26.0 + openai 2.20.0 (main venv); langgraph + crewai (agent_tooling); llama_index + langchain (rag_tooling). Disposition: specialist/alternative providers, not hot path.

### Flutter (2026-08-19)

- Flutter 3.44.2 stable / Dart 3.12.2 / DevTools 2.57.0 at /home/aleksandr/MAKSIMAR_RUNTIME/tools/flutter (SDK external, not copied into repo). HEALTHY = version resolves.

### final reconciliation (2026-08-19)

- PARALLEL_SEMANTIC_SPINES = 0 (single CONTROL_PLANE/canonical_semantic_spine.py; diagnostic scripts in resume_after_reboot are imports, not production spines).
- DUPLICATE_POLICY_TRUTH = 0 (single SemanticPolicyEvaluator in MAKSIMAR_CORE_LIB/security_layer/semantic_policy.py).
- DUPLICATE_EVIDENCE_TRUTH = 0 (single EvidenceBundle + conversation evidence adapter).
- ACCIDENTAL_ORPHANS = 0 (all PC/workers/skills/tools classified above).
- UNAVAILABLE_WITH_EXACT_BLOCKER: mgrep (cloud credential), n8n (source-only install), Playwright (browser binaries download).

### Mempalace canonical wiring truth (2026-08-19)

- FUNCTIONALLY_LIVE = YES (CLI init→mine→search returned exact record; proven).
- CANONICALLY_WIRED = YES (read-only routing integration + mempalace_runtime_sandbox_backend + real_backend_candidate_state + security boundary + approval envelope all exist).
- REAL BACKEND = DELIBERATELY GATED: FakeMemPalaceSandboxBackend returns fake_backend_used=True / real_backend_enabled=False until approval (smoke + vendor-gate reports). Wiring the real backend into memory.retrieve is an approval-gated step, not a missing code edge.
- Status: FUNCTIONALLY_LIVE + CANONICALLY_WIRED (read-only) + REAL_BACKEND_APPROVAL_GATED.

### full pytest + architecture drift (2026-08-19)

- full `pytest -n 6 --dist=worksteal`: 3783 passed, 1 skipped, 1 failed, 1 error (error = test-isolation ordering; archive_source_models_smoke passes alone).
- REAL drift (architecture_blueprint_drift_guard): adapters import from TOOLS layer violating blueprint:
  - existing_capability_inventory.py, project_understanding_adapter.py, memory_retrieval_adapter.py → `tools.jarvis_live_runtime.*` (codegraph_readonly_adapter, jarvis_live_read_models, jarvis_runtime_library_store)
  - simulation_worker_adapter.py → `MAKSIMAR_SERVER.WORKERS.simulation_worker`
  - MAKSIMAR_CORE_LIB/action_library_adapters/action_worker_status_read_model.py → `MAKSIMAR_SERVER.WORKERS.sandboxed_action_worker_runtime` (FORBIDDEN)
  - audit_project.py unregistered.
- Reconciliation required: move adapter helpers to a canonical layer (not tools.*) OR register the layer allowance. This is the remaining dependency-truth edge.

### architecture layer migration (2026-08-19)

Drift guard was RED — FIXED by real layer repair (not guard relaxation):
- PROMOTED to MAKSIMAR_CORE_LIB/project_read/: codegraph_readonly_adapter.py, jarvis_runtime_library_store.py (pure read-only helpers).
- PROMOTED to MAKSIMAR_SERVER/AI_ORCHESTRATION/: memory_context_sources.py, jarvis_live_read_models.py (server-level read models).
- PROMOTED to MAKSIMAR_CORE_LIB/workers_registry/simulation_io_contracts.py: SimulationEngineRequest/Result (pure contracts).
- NEW MAKSIMAR_CORE_LIB/workers_registry/simulation_worker_provider_registry.py: WORKERS registers build_simulation_worker_runtime; SERVER consumes via get_simulation_worker_factory() (downward dependency preserved).
- action_worker_status_read_model.py now uses a structural Protocol (removed CORE→WORKERS import).
- audit_project.py classified as allowed_unmapped developer tool.
- tools/jarvis_live_runtime/* are thin compatibility re-export wrappers.
- Drift guard: 3 passed (0 violations). Simulation LIVE preserved (worker_sim_001 COMPLETE).

### Playwright — REAL_CANONICAL_WORKING (2026-08-19)

- Blocker removed (owner installed chromium). Re-probe: chromium launched, real DOM read ('PW_REAL_882') + real interaction/readback (input filled 'JARVIS_PW_123'). Playwright = deterministic DOM provider, REAL_CANONICAL_WORKING.

### Windows UIA / pywinauto (2026-08-19)

- pywinauto 0.6.9 + comtypes + pywin32 installed (owner), pip check clean.
- Finding: pywinauto UIA backend from WSL-launched python.exe fails "WaitForInputIdle failed" (session-attachment). The win32gui path (FindWindow("Notepad") + SetForegroundWindow + EM_REPLACESEL/WM_GETTEXT) already provides target-aware structured control WITHOUT mouse (type_text FULL_E2E). UIA higher-level attach needs interactive-session resolution (same boundary as earlier type_text targeting).

### xdist suite GREEN + registry semantics (2026-08-19)

- Root cause of 91 errors = `register_simulation_worker_factory` raised "already registered" under xdist (multi-worker module re-import). FIXED.
- Final: 3784 passed, 1 skipped, 0 failed, 0 errors (full `-n 6 --dist=worksteal`).
- Registry semantics made safe: same logical provider (module/qualname identity) = idempotent; conflicting factory = fail closed.

### n8n build root cause + fix (2026-08-19)

- ROOT CAUSE: `@n8n/n8n-extension-insights` `build` = `pnpm run "/^build:.*/"` (regex script-matching) failed exit 1. build:backend (tsdown) + build:frontend (vite) each succeed individually.
- FIX (frozen source): `build` = `pnpm cleanup && pnpm run build:backend && pnpm run build:frontend` (explicit; avoids regex + recursive build:unchecked). Build now completes.
- pnpm 9.6.0 boundary: `packages/@n8n/tournament/package.json:42` has `packageManager: pnpm@9.6.0` (vs root pnpm@10.32.1) — nested package-local boundary, NOT the extension-insights cause.
- pnpm.overrides warning (tournament) = warning only, not a build defect.
- Remaining: full `pnpm build` (34/34) + disable turbo telemetry (TURBO_TELEMETRY_DISABLED) + verify CLI dist/config exists + start local n8n.

### Windows UIA attach diagnosis (2026-08-19)

- pywinauto UIA `connect(handle=hwnd)` to EXISTING Notepad finds hwnd but `child_window(control_type='Edit')` times out → UIA tree enumeration fails from WSL-spawned python.exe (session/desktop attach boundary, confirmed by both start() and connect(handle=) paths).
- Win32 HWND path (win32gui FindWindow + SetForegroundWindow + EM_REPLACESEL/WM_GETTEXT) = PROVEN target-aware structured control WITHOUT mouse (type_text FULL_E2E).
- Resolution direction (not abandoned): host UIA in the EXISTING Windows Edge persistent user-session process (native interactive desktop), not the WSL-spawned per-action subprocess. Provider priority: Native API/COM > UIA > Win32 HWND > DOM/Playwright > vision > mouse LAST.

### Windows UIA — CORRECTED: REAL_CANONICAL_WORKING (2026-08-19)

- CORRECTION: earlier "WSL session-attachment blocks UIA" was WRONG. Root cause was wrong control_type — modern Notepad text control is 'Document' (RichEditD2DPT), NOT 'Edit'.
- UIA enumeration = PROVEN (45 descendants; Document + 17 Buttons + TabItems discovered from Windows Edge).
- UIA InvokePattern = PROVEN (invoked a Notepad button via pywinauto invoke(), no mouse).
- Value-style = win32gui EM_REPLACESEL (Win32, already FULL_E2E) + UIA Document control discovered; UIA ValuePattern SetValue needs a small typed-comtypes interface (same pattern as coreaudio_volume.py).
- Status: UIA = REAL_CANONICAL_WORKING (enumeration + discovery + Invoke). Provider priority honored: Win32 HWND (EM_REPLACESEL) + UIA (Invoke/Value) coexist below semantics.

### UIA ValuePattern (2026-08-19)

- UIA enumeration + discovery + InvokePattern = PROVEN (real structured action, no mouse).
- ValuePattern: modern Notepad Document control (RichEditD2DPT) supports TextPattern (10014), NOT ValuePattern (10002) → QueryInterface E_NOINTERFACE. A classic Edit/TextBox control (Run/Find dialog field) supports ValuePattern; Win32 EM_REPLACESEL already provides Value-style without mouse.
- Status: UIA provider FUNCTIONALLY_LIVE (enumeration + Invoke). ValuePattern needs a Value-supporting control (find dialog / classic edit), not the RichEdit.

### n8n build OOM (2026-08-19)

- extension-insights fixed (61/62). Remaining failure = n8n#build (CLI) JavaScript heap OOM (exit 134), not a source/dependency defect.
- Fix: NODE_OPTIONS=--max-old-space-size=8192 (re-running full build with 8GB heap).

### Mempalace real backend — CANONICALLY_WIRED (2026-08-19)

- Added `search_mempalace` operation (memory.retrieve) → `_run_mempalace_search` subprocess to frozen Mempalace 3.3.5 venv `search`. Real query proven (QWERTY_ZEBRA_917 → matched persisted record, returncode 0).
- Fake `read_mempalace_sandbox` preview stays; real search is a separate operation. Palace path configurable via MEMPALACE_PALACE (default ~/.mempalace).

### n8n full build GREEN (2026-08-19)

- extension-insights regex fixed + CLI heap OOM fixed (NODE_OPTIONS=--max-old-space-size=8192). Full root `pnpm build`: BUILD_EXIT=0, 62/62 successful. CLI dist/config now exists (index.js + schema.js). n8n is BUILT (not yet started/live).

### Two runtime failures RESOLVED (2026-08-21)

1) n8n root build OOM (n8n#build / packages/cli): Node default heap insufficient for the CLI bundle (V8 OOM exit 134). FIXED with NODE_OPTIONS=--max-old-space-size=8192. Full build 62/62, BUILD_EXIT=0, CLI dist/config present. n8n now RUNNING (healthz {"status":"ok"} on 127.0.0.1:5678).

2) JARVIS lifecycle (`control_plane_without_expected_supervisor`): root cause = a MANUAL probe uvicorn (CONTROL_PLANE.api_server:app, PID 3744393) left running outside the tmux supervisor by this campaign's acceptance probes. rest did not own it. FIXED by terminating the orphan (kill -- -3744392) + ./tools/rest + ./tools/work (now start clean; tmux sessions present; control plane healthy on 127.0.0.1:8000). previous_crash was stale/misattributed (probe SIGTERM + n8n OOM core dump, not a JARVIS kernel killchain).

### PROBE CLEANUP LAW
Any acceptance probe starting uvicorn/control-plane/worker/supervisor MUST tear it down deterministically (this incident was caused by a leaked manual probe).

### n8n OFFLINE INTELLIGENCE — version-pinned local catalog (2026-08-21)

- Built n8n_2.26.0_node_catalog.json from installed frozen source (packages/nodes-base/dist/nodes, 436 node types): name, displayName, group, version, description, credentials, operations (incl. requestMethod/resource), isTrigger.
- Search helper MAKSIMAR_SERVER/AI_ORCHESTRATION/n8n_local_catalog.py: search_n8n_catalog(query) + node_contract(type). Name/displayName-weighted offline scoring + network/ai classification. NO internet dependency.
- Source is authoritative (runtime dist), not internet docs. Cloud/network nodes report their external requirement; local core/transform nodes are marked local.
- Rebuildable via EXTERNAL_BACKENDS/vendor_quarantine/n8n/build_node_catalog.py.

### n8n FULL CANONICAL E2E — architecture proven (2026-08-21)

REUSED: existing adapter pattern (simulation/memory), existing `workflow_automation:n8n` registry record, existing `_existing_authoritative_execution_contract`, existing provider_ports dispatch, existing GoalFrame v3 domain projection, existing local n8n catalog.
EXTENDED (minimal):
- NEW MAKSIMAR_SERVER/AI_ORCHESTRATION/n8n_adapter.py (provider adapter: create/inspect/execute workflow via n8n public API + CLI execute).
- N8N_CAPABILITY_OPERATION_CONTRACTS with semantic_owner_id automation.create/inspect/run, target_scope local_workflow_automation.
- `_existing_authoritative_execution_contract` + provider_ports wired (both hot + stream paths).
- NEW semantic domain `automation` (semantic_domain_of_scope + _SEMANTIC_DOMAIN_SCOPES + MEANINGS) mapping local_workflow_automation.

PROVEN:
- Natural request ("Создай локальную тестовую автоматизацию...") -> GoalFrame domain=automation -> workflow_automation:n8n -> create_workflow -> REAL n8n workflow created (evidence COMPLETE).
- Adapter full chain create->inspect->execute = COMPLETE/COMPLETE/COMPLETE (real workflow ID, readback, CLI execution, marker observed).
- n8n public API key (scoped, local ~/.n8n/jarvis_api_key) + CLI execute (N8N_RUNNERS_BROKER_PORT=5680).
- Regression tests (unavailable/create-fail/execute-fail/contracts/local-nodes) + drift guard GREEN + control_plane 277 PASS.

REMAINING for full YES: natural-request multi-step (create+inspect+execute in one turn) + second-effect modify proof.

### n8n cleanup (2026-08-21)

- Secret hygiene: rotated API key (silent, no echo); deleted insert_api_key.py (DB-injection helper). Runtime reads key only from ~/.n8n/jarvis_api_key (gitignored). DB mutation is NOT production provisioning.
- Removed test-specific "JARVIS_E2E_MARKER" naming; renamed to generic output_value correlation token (readback verification, not a test marker).
- create_workflow now accepts a model-supplied `workflow` spec via parameters; falls back to a canonical deterministic local workflow ONLY when absent. Adapter never decides human automation semantics.

### "automation" semantic domain — audit result: A (authoritative, keep)

GoalFrame v3 (semantic_domain + effect_intent + _goalframe_projection + GoalBinding) is the CURRENT authoritative production hot path (candidate_discovery strategy = GOALFRAME_V3_INTENT_TO_BINDING). The `automation` domain is a legitimate extension for a genuinely new capability (workflow automation), not migration scaffolding. Keep; no second routing mechanism.

### n8n modify + second-effect proof (2026-08-21)

- Added modify_workflow operation (automation.modify) → PUT /api/v1/workflows/{id}, mutate Set node value, read back.
- Second-effect proof (adapter-level): create (value jarvis_output_X) -> execute (result A) -> modify (value jarvis_output_X_mod) -> execute (result B). Stored value changed + DIFFERENT RESULT = True (real n8n evidence).

### n8n production test-fallback REMOVED (2026-08-21)

- create_workflow now FAILS CLOSED (missing_or_invalid_workflow_spec) when no valid model-supplied workflow spec (nodes+connections) exists. No silent "Manual Trigger -> Set" substitution in production.
- Deterministic acceptance workflow moved to tests/control_plane/test_n8n_adapter.py as a TEST fixture only.
- execute_workflow verifies real execution status (success/failed) + reads actual output tail; no hardcoded marker check.
- modify_workflow requires an explicit model-supplied value (fails closed on missing value).

### n8n workflow synthesis (logical spec -> HOST compile) (2026-08-21)

- NEW MAKSIMAR_SERVER/AI_ORCHESTRATION/n8n_logical_compiler.py: provider-neutral logical automation spec (trigger + steps + constraints) -> installed n8n 2.26.0 graph via local catalog. LLM does NOT guess installed node truth.
- create_workflow now compiles a model-supplied `logical_spec` (or validates a raw graph) against the catalog; FAILS CLOSED on unknown action / node-not-installed / network-node-with-local_only-constraint.
- network_requirement heuristic corrected (default local; cloud only on explicit description markers; documented limitation).
- Proven adapter-level: logical spec {manual trigger + set_field value=alpha} -> compile -> real create -> execute -> actual result contains "alpha".

### n8n generic catalog resolution + tri-state network truth (2026-08-21)

- resolve_logical_step: intrinsic primitives (small fixed set) + GENERIC catalog-driven resolution (schedule_trigger -> scheduleTrigger etc.). Fixed mapping is NOT the capability bottleneck.
- network_truth tri-state (LOCAL / NETWORK_REQUIRED / UNKNOWN): LOCAL whitelist for built-in intrinsics; NETWORK_REQUIRED on description markers; UNKNOWN otherwise. local_only fails closed on NETWORK_REQUIRED AND UNKNOWN (absence of evidence != local proof).

### n8n network truth + safe resolver (2026-08-21)

- FTP removed from LOCAL whitelist; added _NETWORK_REQUIRED_NAMES (ftp/sftp/httprequest/webhook/db clients/etc.). executeCommand stays LOCAL (network) with risk handled separately (orthogonal truths).
- search_n8n_catalog now returns score; resolve_logical_step requires score >= 3.0 AND clear separation from runner-up, else fails closed (no random top-1). database_query -> unresolved (ambiguous), schedule_trigger -> scheduleTrigger (generic).

### n8n 436-node reachability audit — ALL REACHABLE (2026-08-21)

- Generic catalog_query resolution (no handwritten alias per node) + exact identity-match bonus in search.
- Mechanical audit: 436/436 installed node types CANONICAL_READY, 0 semantically unreachable, 0 needs-handwritten-alias, 0 unknown/unexplained.
- Intrinsic primitive fast-path is optimization-only (NOT required for reachability).
- Audit artifact: EXTERNAL_BACKENDS/vendor_quarantine/n8n/n8n_2.26.0_reachability_audit.json.

### n8n 9 semantic orphans RESOLVED (2026-08-21)

- Source-backed classification: stickyNote + oneSimpleApi = INTERNAL_ONLY (canvas annotation + third-party compat shim, not user-facing capabilities).
- 7 USER_USABLE orphans (cron, documentId, extractFromFile, limit, manualTrigger, supabase, twitter) semantically reachable via the FULL mechanical index (group + description + operations + displayName concept), not the exact internal name.
- Final audit: 436 entries = 124 CANONICAL_READY + 310 CANONICAL_READY_PREREQUISITE_REQUIRED + 2 INTERNAL_ONLY; 0 user-usable semantic orphans; 0 needs-alias; 0 contract-unresolved.

### n8n model-side logical_spec synthesis wired (2026-08-22)

- create_workflow now requires a model-supplied logical_spec (provider-neutral): trigger enum + steps with catalog_query + constraints. Model never emits node types/versions.
- Compiler accepts model-style logical_spec; search name-match weight boosted; ambiguity gate relative.
