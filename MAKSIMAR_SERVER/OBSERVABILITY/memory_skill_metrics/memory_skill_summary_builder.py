from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.memory_adapter_selection_metrics_models import (
    build_memory_adapter_selection_metrics_contract,
)
from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.memory_conflict_metrics_models import (
    build_memory_conflict_metrics_contract,
)
from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.memory_promotion_metrics_models import (
    build_memory_promotion_metrics_contract,
)
from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.memory_retrieval_metrics_models import (
    build_memory_retrieval_metrics_contract,
)
from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.memory_skill_metrics_contract import (
    build_memory_skill_metrics_contract,
)


def build_memory_skill_summary() -> Dict[str, object]:
    base = build_memory_skill_metrics_contract()
    retrieval = build_memory_retrieval_metrics_contract()
    conflict = build_memory_conflict_metrics_contract()
    promotion = build_memory_promotion_metrics_contract()
    adapter = build_memory_adapter_selection_metrics_contract()

    total_metric_entries = (
        base.total_entries
        + retrieval.total_entries
        + conflict.total_entries
        + promotion.total_entries
        + adapter.total_entries
    )
    ready_metric_entries = (
        base.active_entries
        + retrieval.ready_entries
        + conflict.ready_entries
        + promotion.ready_entries
        + adapter.ready_entries
    )

    summary_ready = (
        base.active_entries == base.total_entries
        and retrieval.ready_entries == retrieval.total_entries
        and conflict.ready_entries == conflict.total_entries
        and promotion.ready_entries == promotion.total_entries
        and adapter.ready_entries == adapter.total_entries
        and retrieval.backend_execution_allowed_entries == 0
        and promotion.auto_promotion_allowed_entries == 0
        and adapter.backend_execution_allowed_entries == 0
        and conflict.conflict_entries == 0
    )

    return {
        "base_metric_entries": base.total_entries,
        "retrieval_metric_entries": retrieval.total_entries,
        "conflict_metric_entries": conflict.total_entries,
        "promotion_metric_entries": promotion.total_entries,
        "adapter_selection_metric_entries": adapter.total_entries,
        "total_metric_entries": total_metric_entries,
        "ready_metric_entries": ready_metric_entries,
        "conflict_entries": conflict.conflict_entries,
        "promotion_auto_allowed_entries": promotion.auto_promotion_allowed_entries,
        "backend_execution_allowed_entries": (
            retrieval.backend_execution_allowed_entries
            + adapter.backend_execution_allowed_entries
        ),
        "mgrep_blocked": retrieval.mgrep_blocked_entries == retrieval.total_entries
        and adapter.mgrep_blocked_entries == adapter.total_entries,
        "sqlite_vec_blocked": (
            retrieval.sqlite_vec_blocked_entries == retrieval.total_entries
            and adapter.sqlite_vec_blocked_entries == adapter.total_entries
        ),
        "read_only_ready": (
            retrieval.read_only_entries == retrieval.total_entries
            and conflict.read_only_entries == conflict.total_entries
            and promotion.read_only_entries == promotion.total_entries
            and adapter.read_only_entries == adapter.total_entries
        ),
        "summary_ready": summary_ready,
    }
