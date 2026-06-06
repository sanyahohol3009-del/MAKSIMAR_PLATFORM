# JARVIS-LIVE CI Guard Usage v0.1

Use the JARVIS-LIVE CI status wrapper after each JARVIS batch, before commit,
before push, and before opening the JL-10 download gate.

Commands:

```bash
python tools/project_readiness_control/jarvis_live_ci_status.py
TMPDIR="$HOME/.tmp" PYTHONDONTWRITEBYTECODE=1 python -m pytest tests/jarvis_live -q
TMPDIR="$HOME/.tmp" PYTHONDONTWRITEBYTECODE=1 python -m pytest tests/architecture_map/test_architecture_blueprint_drift_guard.py -q
python tools/architecture_xray_radar.py
python tools/roadmap_post_step_drift_check.py
TMPDIR="$HOME/.tmp" PYTHONDONTWRITEBYTECODE=1 python -m pytest -n auto -q
```

The status wrapper is read-only. It does not start runtime, does not download
models, does not open microphone, STT, TTS, or wake-word runtime, and does not enable
PC or app control.

Interpretation examples:

```text
JARVIS_DRIFT_GUARD_OK=true
NEXT_BATCH=JL-2
MODEL_DOWNLOAD_ALLOWED=false
```

Expected meaning:

- `JARVIS_DRIFT_GUARD_OK=true` means no forbidden parallel JARVIS-LIVE roots were
  detected by the roadmap status builder.
- `NEXT_BATCH=JL-2` means JL-0 and JL-1 are ready and model profile/resource
  registry binding is the next allowed architecture step.
- `MODEL_DOWNLOAD_ALLOWED=false` means model weights are still blocked as runtime
  assets until the JL-10 download gate is reached and its storage/vendor boundaries
  are present.

Before JL-10, downloads must remain blocked. Before JL-11, voice smoke must remain
blocked. Before JL-14, PC control must remain blocked. The same no-drift rules still
apply: no new AI registry, no new worker registry, no new runtime queue, no new
memory engine, no new voice root, no raw shell, and no direct control without
allowlist and approval.

