from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.memory_skill_summary_builder import (
    build_memory_skill_summary,
)


_MEMORY_SKILL_OBSERVABILITY_FLOW = (
    "memory_skill_base_metrics",
    "memory_retrieval_metrics",
    "memory_conflict_metrics",
    "memory_promotion_metrics",
    "memory_adapter_selection_metrics",
    "memory_skill_summary",
    "memory_skill_preview",
)


def build_memory_skill_preview() -> Dict[str, object]:
    summary = build_memory_skill_summary()

    return {
        "flow": _MEMORY_SKILL_OBSERVABILITY_FLOW,
        "base_metric_entries": summary["base_metric_entries"],
        "retrieval_metric_entries": summary["retrieval_metric_entries"],
        "conflict_metric_entries": summary["conflict_metric_entries"],
        "promotion_metric_entries": summary["promotion_metric_entries"],
        "adapter_selection_metric_entries": summary["adapter_selection_metric_entries"],
        "total_metric_entries": summary["total_metric_entries"],
        "ready_metric_entries": summary["ready_metric_entries"],
        "conflict_entries": summary["conflict_entries"],
        "promotion_auto_allowed_entries": summary["promotion_auto_allowed_entries"],
        "backend_execution_allowed_entries": summary["backend_execution_allowed_entries"],
        "mgrep_blocked": summary["mgrep_blocked"],
        "sqlite_vec_blocked": summary["sqlite_vec_blocked"],
        "read_only_ready": summary["read_only_ready"],
        "summary_ready": summary["summary_ready"],
        "preview_ready": True,
        "phase_batch_ready": bool(summary["summary_ready"]),
    }
