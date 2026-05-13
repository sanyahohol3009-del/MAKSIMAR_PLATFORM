from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Tuple


ClientMetricKind = Literal[
    "usage_signal",
    "operator_feedback",
    "quality_signal",
    "error_signal",
    "latency_signal",
    "feature_request_signal",
]

ClientMetricTrustLevel = Literal[
    "low",
    "medium",
    "high",
]


@dataclass(frozen=True, slots=True)
class ClientMetricSignal:
    signal_id: str
    metric_kind: ClientMetricKind
    trust_level: ClientMetricTrustLevel
    source_bound: bool
    tenant_bound: bool
    personal_data_present: bool
    raw_payload_allowed: bool
    pii_redacted: bool
    consent_required: bool
    consent_present: bool
    learning_input_allowed: bool
    automatic_training_allowed: bool
    runtime_mutation_allowed: bool
    signal_ready: bool

    def __post_init__(self) -> None:
        if not self.signal_id:
            raise ValueError("signal_id must be non-empty")
        if self.source_bound is not True:
            raise ValueError("source_bound must be True")
        if self.tenant_bound is not True:
            raise ValueError("tenant_bound must be True")
        if self.raw_payload_allowed:
            raise ValueError("raw_payload_allowed must be False")
        if self.personal_data_present and self.pii_redacted is not True:
            raise ValueError("personal_data_present requires pii_redacted=True")
        if self.consent_required is not True:
            raise ValueError("consent_required must be True")
        if self.consent_present is not True:
            raise ValueError("consent_present must be True")
        if self.automatic_training_allowed:
            raise ValueError("automatic_training_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.signal_ready is not True:
            raise ValueError("signal_ready must be True")


@dataclass(frozen=True, slots=True)
class ClientMetricsFilterPolicy:
    policy_id: str
    signals: Tuple[ClientMetricSignal, ...]
    source_bound_required: bool
    tenant_boundary_required: bool
    personal_data_redaction_required: bool
    consent_required_for_all: bool
    raw_payload_allowed: bool
    automatic_training_allowed: bool
    runtime_mutation_allowed: bool
    productization_allowed_now: bool
    filter_policy_ready: bool

    def __post_init__(self) -> None:
        if not self.policy_id:
            raise ValueError("policy_id must be non-empty")
        if not self.signals:
            raise ValueError("signals must be non-empty")
        signal_ids = {signal.signal_id for signal in self.signals}
        if len(signal_ids) != len(self.signals):
            raise ValueError("signal_id values must be unique")
        if self.source_bound_required is not True:
            raise ValueError("source_bound_required must be True")
        if self.tenant_boundary_required is not True:
            raise ValueError("tenant_boundary_required must be True")
        if self.personal_data_redaction_required is not True:
            raise ValueError("personal_data_redaction_required must be True")
        if self.consent_required_for_all is not True:
            raise ValueError("consent_required_for_all must be True")
        if self.raw_payload_allowed:
            raise ValueError("raw_payload_allowed must be False")
        if self.automatic_training_allowed:
            raise ValueError("automatic_training_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.productization_allowed_now:
            raise ValueError("productization_allowed_now must be False")
        if not all(signal.signal_ready for signal in self.signals):
            raise ValueError("all signals must be ready")
        if self.filter_policy_ready is not True:
            raise ValueError("filter_policy_ready must be True")


def build_client_metrics_filter_policy() -> ClientMetricsFilterPolicy:
    signals = (
        ClientMetricSignal(
            signal_id="client_metric_usage_signal_001",
            metric_kind="usage_signal",
            trust_level="medium",
            source_bound=True,
            tenant_bound=True,
            personal_data_present=False,
            raw_payload_allowed=False,
            pii_redacted=True,
            consent_required=True,
            consent_present=True,
            learning_input_allowed=True,
            automatic_training_allowed=False,
            runtime_mutation_allowed=False,
            signal_ready=True,
        ),
        ClientMetricSignal(
            signal_id="client_metric_operator_feedback_001",
            metric_kind="operator_feedback",
            trust_level="high",
            source_bound=True,
            tenant_bound=True,
            personal_data_present=True,
            raw_payload_allowed=False,
            pii_redacted=True,
            consent_required=True,
            consent_present=True,
            learning_input_allowed=True,
            automatic_training_allowed=False,
            runtime_mutation_allowed=False,
            signal_ready=True,
        ),
        ClientMetricSignal(
            signal_id="client_metric_quality_signal_001",
            metric_kind="quality_signal",
            trust_level="medium",
            source_bound=True,
            tenant_bound=True,
            personal_data_present=False,
            raw_payload_allowed=False,
            pii_redacted=True,
            consent_required=True,
            consent_present=True,
            learning_input_allowed=True,
            automatic_training_allowed=False,
            runtime_mutation_allowed=False,
            signal_ready=True,
        ),
        ClientMetricSignal(
            signal_id="client_metric_error_signal_001",
            metric_kind="error_signal",
            trust_level="medium",
            source_bound=True,
            tenant_bound=True,
            personal_data_present=False,
            raw_payload_allowed=False,
            pii_redacted=True,
            consent_required=True,
            consent_present=True,
            learning_input_allowed=True,
            automatic_training_allowed=False,
            runtime_mutation_allowed=False,
            signal_ready=True,
        ),
        ClientMetricSignal(
            signal_id="client_metric_feature_request_signal_001",
            metric_kind="feature_request_signal",
            trust_level="low",
            source_bound=True,
            tenant_bound=True,
            personal_data_present=True,
            raw_payload_allowed=False,
            pii_redacted=True,
            consent_required=True,
            consent_present=True,
            learning_input_allowed=True,
            automatic_training_allowed=False,
            runtime_mutation_allowed=False,
            signal_ready=True,
        ),
    )

    return ClientMetricsFilterPolicy(
        policy_id="client_metrics_filter_policy_phase_6_6_001",
        signals=signals,
        source_bound_required=True,
        tenant_boundary_required=True,
        personal_data_redaction_required=True,
        consent_required_for_all=all(signal.consent_required for signal in signals),
        raw_payload_allowed=False,
        automatic_training_allowed=False,
        runtime_mutation_allowed=False,
        productization_allowed_now=False,
        filter_policy_ready=True,
    )
