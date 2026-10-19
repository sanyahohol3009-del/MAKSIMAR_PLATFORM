from __future__ import annotations

import hashlib
import json
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from MAKSIMAR_SERVER.VOICE_ROUTING.voice_file_runtime import synthesize

_RUNTIME_ROOT = Path.home() / "MAKSIMAR_RUNTIME"
_ASSET_ROOT = _RUNTIME_ROOT / "content_factory" / "assets"
_FFMPEG = Path("/usr/bin/ffmpeg")
_FFPROBE = Path("/usr/bin/ffprobe")


def _req(value: str, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be non-empty")
    return value.strip()


@dataclass(frozen=True, slots=True)
class ContentJob:
    job_id: str
    request_id: str
    session_id: str
    content_goal: str
    format: str
    language: str
    platform_targets: tuple[str, ...] = ()
    brand_kit_ref: str = ""
    source_refs: tuple[str, ...] = ()
    constraints: tuple[str, ...] = ()
    approval_state: str = "NOT_REQUIRED"
    asset_refs: tuple[str, ...] = ()
    provenance: tuple[tuple[str, str], ...] = ()
    status: str = "PLANNED"

    def __post_init__(self) -> None:
        for n in ("job_id", "request_id", "session_id", "content_goal", "format", "language"):
            _req(getattr(self, n), n)
        if not re.fullmatch(r"content_job_[a-z0-9_]+", self.job_id):
            raise ValueError("invalid job_id")
        if self.approval_state not in {"NOT_REQUIRED", "PENDING", "APPROVED", "DENIED"}:
            raise ValueError("invalid approval_state")
        if self.status not in {"PLANNED", "RUNNING", "COMPLETE", "PARTIAL", "FAILED"}:
            raise ValueError("invalid status")

    def to_read_model(self) -> dict[str, Any]:
        return {k: getattr(self, k) for k in (
            "job_id", "request_id", "session_id", "content_goal", "format", "language",
            "platform_targets", "brand_kit_ref", "source_refs", "constraints",
            "approval_state", "asset_refs", "provenance", "status",
        )}


@dataclass(frozen=True, slots=True)
class ContentAsset:
    asset_id: str
    kind: str
    mime_type: str
    path: str
    content_hash: str
    generator_capability: str
    provider_receipt: str
    source_refs: tuple[str, ...]
    rights_provenance: str
    created_at: str

    def __post_init__(self) -> None:
        for n in ("asset_id", "kind", "mime_type", "path", "content_hash", "generator_capability", "provider_receipt", "rights_provenance", "created_at"):
            _req(getattr(self, n), n)
        if not Path(self.path).is_file():
            raise ValueError("asset path must exist")
        if not self.content_hash.startswith("sha256:"):
            raise ValueError("content_hash must be sha256")

    def to_read_model(self) -> dict[str, Any]:
        return self.__dict__ if hasattr(self, "__dict__") else {
            "asset_id": self.asset_id, "kind": self.kind, "mime_type": self.mime_type,
            "path": self.path, "content_hash": self.content_hash,
            "generator_capability": self.generator_capability,
            "provider_receipt": self.provider_receipt, "source_refs": self.source_refs,
            "rights_provenance": self.rights_provenance, "created_at": self.created_at,
        }


def build_content_job(*, request_id: str, session_id: str, goal: str, job_id: str | None = None) -> ContentJob:
    return ContentJob(job_id=job_id or "content_job_" + request_id.replace("-", "_"),
                      request_id=request_id, session_id=session_id, content_goal=goal,
                      format="shorts", language="ru", platform_targets=("local_preview",),
                      constraints=("no_publication", "local_assets_only"))


def _asset(path: Path, *, kind: str, capability: str, receipt: str, source_refs: tuple[str, ...]) -> ContentAsset:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return ContentAsset("media_asset_" + digest[:16], kind, "video/mp4" if kind == "video" else "audio/wav",
                        str(path), "sha256:" + digest, capability, receipt, source_refs,
                        "local_generated_from_user_request_no_external_sources",
                        datetime.now(timezone.utc).isoformat())


def generate_short_script(goal: str) -> dict[str, Any]:
    from MAKSIMAR_SERVER.AI_ORCHESTRATION.ollama_transport import ollama_chat_once, PRIMARY_CONVERSATION_MODEL_ID
    prompt = ("Create a compact Russian short-video script as JSON with exactly keys title, hook, body, "
              "outro, duration_seconds. Ground it in this goal; no publication claims. Goal: " + goal)
    result = ollama_chat_once(prompt, "Return only valid JSON.", model_id=PRIMARY_CONVERSATION_MODEL_ID,
                              options={"temperature": 0, "num_predict": 700, "num_ctx": 3072})
    if result.get("ok") is not True:
        raise RuntimeError("content_script_provider_unavailable")
    parsed = json.loads(str(result.get("content", "")))
    required = {"title", "hook", "body", "outro", "duration_seconds"}
    if set(parsed) != required or not all(isinstance(parsed[k], str) for k in required - {"duration_seconds"}):
        raise ValueError("invalid_content_script")
    if not isinstance(parsed["duration_seconds"], (int, float)) or not 1 <= float(parsed["duration_seconds"]) <= 60:
        raise ValueError("invalid_content_script_duration")
    return parsed


def compose_shorts_asset(job: ContentJob, script: dict[str, Any]) -> tuple[ContentAsset, ContentAsset]:
    _ASSET_ROOT.mkdir(parents=True, exist_ok=True)
    stem = job.job_id
    audio = synthesize(" ".join(str(script[k]) for k in ("hook", "body", "outro")),
                        output_path=_ASSET_ROOT / f"{stem}.wav")
    video = _ASSET_ROOT / f"{stem}.mp4"
    title = str(script["title"]).replace(":", " - ").replace("'", "")
    # Fixed local visual composition; no provider identity or public side effect.
    draw = title.replace("\\", "").replace("'", "")
    subprocess.run([str(_FFMPEG), "-y", "-f", "lavfi", "-i", "color=c=0x101827:s=540x960:r=25",
                    "-i", audio.audio_path, "-vf", f"drawtext=text='{draw}':fontcolor=white:fontsize=28:x=(w-text_w)/2:y=(h-text_h)/2",
                    "-t", str(audio.duration_seconds), "-pix_fmt", "yuv420p", "-c:v", "libx264", "-c:a", "aac",
                    "-shortest", str(video)], check=True, capture_output=True, timeout=120)
    probe = subprocess.run([str(_FFPROBE), "-v", "error", "-show_streams", "-show_format", "-of", "json", str(video)],
                           check=True, capture_output=True, text=True, timeout=30)
    metadata = json.loads(probe.stdout)
    streams = metadata.get("streams", [])
    if not any(s.get("codec_type") == "video" for s in streams) or not any(s.get("codec_type") == "audio" for s in streams):
        raise RuntimeError("shorts_mp4_missing_stream")
    return (_asset(video, kind="video", capability="content.shorts.generate",
                   receipt=f"{job.job_id}:ffmpeg", source_refs=(job.request_id,)),
            _asset(Path(audio.audio_path), kind="audio", capability="speech.synthesize",
                   receipt="silero_tts", source_refs=(job.request_id,)))


def run_shorts_factory(*, request_id: str, session_id: str, goal: str) -> dict[str, Any]:
    job = build_content_job(request_id=request_id, session_id=session_id, goal=goal)
    script = generate_short_script(goal)
    video, audio = compose_shorts_asset(job, script)
    completed = ContentJob(**{**job.to_read_model(), "asset_refs": (video.asset_id, audio.asset_id), "status": "COMPLETE"})
    return {"job": completed.to_read_model(), "script": script, "assets": (video.to_read_model(), audio.to_read_model()),
            "publication": {"status": "NOT_PUBLISHED", "approval_required": True},
            "evidence": {"kind": "content_factory_shorts", "status": "COMPLETE", "ffprobe": True,
                         "asset_ids": (video.asset_id, audio.asset_id)}}


def build_factory_gauntlet_spec() -> dict[str, Any]:
    """Provider-neutral complex acceptance graph for n8n's canonical compiler.

    The graph deliberately uses only deterministic installed orchestration
    primitives.  It fans out three language lanes, routes each lane through
    the four format transformations, fans them back in, and applies a bounded
    quality/rework gate.  It never names a model/provider or owns semantic
    authority.
    """
    formats = ("short", "long", "image", "audio")
    languages = ("ru", "de", "en")
    branches = []
    for language in languages:
        format_branches = []
        for fmt in formats:
            format_branches.append({
                "label": fmt,
                "steps": [
                    {"action": "transform", "code": "return items;"},
                ],
            })
        branches.append({
            "steps": [{
                "action": "transform",
                "code": "return [" + ",".join(
                    "{json:{language:%r,format:%r,variant:1,status:'received'}}" % (language, fmt)
                    for fmt in formats
                ) + "];",
            }, {
                "action": "route", "field": "format", "branches": [
                    {**branch, "value": branch["label"]} for branch in format_branches
                ],
                "default_steps": [{"action": "set_field", "field": "format_status", "value": "rejected"}],
            }],
        })
    return {
        "name": "JARVIS_FACTORY_GAUNTLET_v1",
        "trigger": "manual",
        "constraints": ["local_only", "no_publication"],
        "steps": [
            {"action": "set_field", "field": "job_status", "value": "received"},
            {"action": "parallel", "branches": branches, "merge": True},
            {"action": "condition", "field": "job_status", "operator": "equals", "value": "received",
             "true_steps": [
                 {"action": "set_field", "field": "quality", "value": "pass"},
                 {"action": "transform", "code": "return items;"},
             ],
             "false_steps": [
                 {"action": "set_field", "field": "quality", "value": "rework"},
                 {"action": "transform", "code": "return items;"},
             ]},
            {"action": "set_field", "field": "receipt_status", "value": "complete"},
        ],
    }
