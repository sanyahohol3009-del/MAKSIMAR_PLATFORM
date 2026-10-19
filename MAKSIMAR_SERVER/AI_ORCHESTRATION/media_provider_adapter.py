from __future__ import annotations

"""Canonical read-only media provider over the installed ffprobe executable."""

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import (
    EvidenceBundle, EvidenceItem, ExecutionPlan, ExecutionReceipt, RequestDeadline,
    RequestUnderstanding, utc_observed_at,
)


PROVIDER_ID = "existing_ffmpeg_media_tools"
FFPROBE = Path("/usr/bin/ffprobe")

MEDIA_CAPABILITY_OPERATION_CONTRACTS: dict[str, tuple[dict[str, Any], ...]] = {
    "media.probe": ({
        "operation_id": "probe_media",
        "description": "Inspect an existing local media file and return typed stream and format metadata.",
        "required_parameters": ("path",), "evidence_kinds": ("media_probe",),
        "effect_type": "OBSERVE", "target_scope": "local_media_file",
        "semantic_owner_id": "media.probe", "reversibility": "REVERSIBLE",
        "external_side_effect": False, "risk_class": "READ_ONLY",
    },),
}


class ExistingFfprobeMediaAdapter:
    provider_id = PROVIDER_ID

    def health(self) -> dict[str, Any]:
        return {
            "provider_id": self.provider_id,
            "status": "AVAILABLE" if FFPROBE.is_file() else "UNAVAILABLE",
            "read_only": True,
        }

    def collect_evidence(
        self, understanding: RequestUnderstanding, plan: ExecutionPlan, trace_id: str,
        deadline: RequestDeadline | None = None,
    ) -> EvidenceBundle:
        items: list[EvidenceItem] = []
        receipts: list[ExecutionReceipt] = []
        errors: list[str] = []
        for step in plan.steps:
            if step.capability_id != "media.probe" or step.operation != "probe_media":
                errors.append(f"{step.operation}:unsupported_operation")
                continue
            path_value = str(dict(step.parameters).get("path") or "").strip()
            media_path = Path(path_value).expanduser()
            if not media_path.is_absolute() or not media_path.is_file():
                errors.append("probe_media:local_file_precondition_required")
                continue
            remaining = deadline.remaining() if deadline is not None else 30.0
            try:
                completed = subprocess.run(
                    [str(FFPROBE), "-v", "error", "-show_format", "-show_streams", "-of", "json", str(media_path)],
                    capture_output=True, text=True, encoding="utf-8", errors="replace",
                    timeout=min(30.0, max(0.1, remaining)), check=False,
                )
                payload = json.loads(completed.stdout) if completed.returncode == 0 else None
            except (OSError, subprocess.SubprocessError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
                errors.append(f"probe_media:{type(exc).__name__}")
                continue
            if not isinstance(payload, dict):
                errors.append("probe_media:ffprobe_failed")
                continue
            observation = json.dumps(payload, ensure_ascii=False, sort_keys=True)
            items.append(EvidenceItem(
                kind="media_probe", source=f"{self.provider_id}:probe_media",
                observation=observation, scope="local_media_file", confidence=1.0,
                trace_id=trace_id, observed_at=utc_observed_at(),
                content_hash="sha256:" + hashlib.sha256(observation.encode()).hexdigest(),
                source_reference=str(media_path), truncated=False, omitted_count=0,
                request_id=understanding.request_id, step_id=step.step_id,
                capability_id=step.capability_id, operation_id=step.operation, provider_id=self.provider_id,
            ))
            receipts.append(ExecutionReceipt(
                receipt_id=f"{trace_id}:{step.step_id}", request_id=understanding.request_id,
                trace_id=trace_id, step_id=step.step_id, capability_id=step.capability_id,
                operation_id=step.operation, provider_id=self.provider_id, status="COMPLETE",
                result="installed ffprobe inspected the existing local media file",
            ))
        status = "COMPLETE" if items and not errors else "PARTIAL" if items else "UNAVAILABLE"
        return EvidenceBundle(
            request_id=understanding.request_id, capability_id="media.probe", trace_id=trace_id,
            status=status, items=tuple(items), receipts=tuple(receipts), errors=tuple(errors),
            limitations=(() if status == "COMPLETE" else ("media probe incomplete",)),
            capability_ids=("media.probe",),
        )


__all__ = ["ExistingFfprobeMediaAdapter", "MEDIA_CAPABILITY_OPERATION_CONTRACTS", "PROVIDER_ID"]
