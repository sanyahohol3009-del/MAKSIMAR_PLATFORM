from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal


JurisdictionLevel = Literal["country", "region", "supranational"]

_JURISDICTION_ID_PATTERN = re.compile(r"^jurisdiction_[a-z][a-z0-9_]*$")
_COUNTRY_CODE_PATTERN = re.compile(r"^[A-Z]{2}$")
_DATE_PATTERN = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _ensure_bool(value: bool, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field_name} must be bool")
    return value


@dataclass(frozen=True, slots=True)
class LegalJurisdictionEntry:
    jurisdiction_id: str
    country_code: str
    jurisdiction_name: str
    jurisdiction_level: JurisdictionLevel
    legal_domains: tuple[str, ...]
    effective_date: str
    source_ref: str
    source_bound: bool
    versioned: bool
    read_only: bool
    approval_required: bool
    jurisdiction_ready: bool
    description: str

    def __post_init__(self) -> None:
        jurisdiction_id = _ensure_non_empty_str(self.jurisdiction_id, "jurisdiction_id")
        country_code = _ensure_non_empty_str(self.country_code, "country_code")
        _ensure_non_empty_str(self.jurisdiction_name, "jurisdiction_name")
        _ensure_non_empty_str(self.effective_date, "effective_date")
        _ensure_non_empty_str(self.source_ref, "source_ref")
        _ensure_non_empty_str(self.description, "description")

        if not _JURISDICTION_ID_PATTERN.fullmatch(jurisdiction_id):
            raise ValueError(f"Invalid jurisdiction_id: {jurisdiction_id}")
        if not _COUNTRY_CODE_PATTERN.fullmatch(country_code):
            raise ValueError(f"Invalid country_code: {country_code}")
        if not _DATE_PATTERN.fullmatch(self.effective_date):
            raise ValueError(f"Invalid effective_date: {self.effective_date}")

        if not isinstance(self.legal_domains, tuple) or not self.legal_domains:
            raise ValueError("legal_domains must be a non-empty tuple")
        if len(set(self.legal_domains)) != len(self.legal_domains):
            raise ValueError("legal_domains must contain unique values")
        for legal_domain in self.legal_domains:
            _ensure_non_empty_str(legal_domain, "legal_domain")

        for field_name in (
            "source_bound",
            "versioned",
            "read_only",
            "approval_required",
            "jurisdiction_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.source_bound:
            raise ValueError("source_bound must be True")
        if not self.versioned:
            raise ValueError("versioned must be True")
        if not self.read_only:
            raise ValueError("read_only must be True")
        if not self.approval_required:
            raise ValueError("approval_required must be True")
        if not self.jurisdiction_ready:
            raise ValueError("jurisdiction_ready must be True")


@dataclass(frozen=True, slots=True)
class LegalJurisdictionContract:
    total_jurisdictions: int
    ready_jurisdictions: int
    source_bound_jurisdictions: int
    versioned_jurisdictions: int
    read_only_jurisdictions: int
    approval_required_jurisdictions: int
    entries: tuple[LegalJurisdictionEntry, ...]

    def __post_init__(self) -> None:
        if self.total_jurisdictions != len(self.entries):
            raise ValueError("total_jurisdictions must match entries length")
        if self.total_jurisdictions <= 0:
            raise ValueError("total_jurisdictions must be >= 1")

        expected = {
            "ready_jurisdictions": sum(1 for entry in self.entries if entry.jurisdiction_ready),
            "source_bound_jurisdictions": sum(1 for entry in self.entries if entry.source_bound),
            "versioned_jurisdictions": sum(1 for entry in self.entries if entry.versioned),
            "read_only_jurisdictions": sum(1 for entry in self.entries if entry.read_only),
            "approval_required_jurisdictions": sum(1 for entry in self.entries if entry.approval_required),
        }

        for field_name, expected_value in expected.items():
            if getattr(self, field_name) != expected_value:
                raise ValueError(f"{field_name} must match computed count")

        if self.ready_jurisdictions != self.total_jurisdictions:
            raise ValueError("all jurisdictions must be ready")
        if self.source_bound_jurisdictions != self.total_jurisdictions:
            raise ValueError("all jurisdictions must be source-bound")
        if self.versioned_jurisdictions != self.total_jurisdictions:
            raise ValueError("all jurisdictions must be versioned")
        if self.read_only_jurisdictions != self.total_jurisdictions:
            raise ValueError("all jurisdictions must be read-only")
        if self.approval_required_jurisdictions != self.total_jurisdictions:
            raise ValueError("all jurisdictions must require approval")


def build_legal_jurisdiction_contract() -> LegalJurisdictionContract:
    entries = (
        LegalJurisdictionEntry(
            jurisdiction_id="jurisdiction_de_federal",
            country_code="DE",
            jurisdiction_name="Germany Federal Jurisdiction",
            jurisdiction_level="country",
            legal_domains=("business_compliance", "data_protection"),
            effective_date="2026-01-01",
            source_ref="source_ref_de_federal_placeholder_v1",
            source_bound=True,
            versioned=True,
            read_only=True,
            approval_required=True,
            jurisdiction_ready=True,
            description="Source-bound jurisdiction placeholder for Germany.",
        ),
        LegalJurisdictionEntry(
            jurisdiction_id="jurisdiction_ua_national",
            country_code="UA",
            jurisdiction_name="Ukraine National Jurisdiction",
            jurisdiction_level="country",
            legal_domains=("business_compliance", "data_protection"),
            effective_date="2026-01-01",
            source_ref="source_ref_ua_national_placeholder_v1",
            source_bound=True,
            versioned=True,
            read_only=True,
            approval_required=True,
            jurisdiction_ready=True,
            description="Source-bound jurisdiction placeholder for Ukraine.",
        ),
        LegalJurisdictionEntry(
            jurisdiction_id="jurisdiction_eu_union",
            country_code="EU",
            jurisdiction_name="European Union Jurisdiction",
            jurisdiction_level="supranational",
            legal_domains=("data_protection", "digital_services"),
            effective_date="2026-01-01",
            source_ref="source_ref_eu_union_placeholder_v1",
            source_bound=True,
            versioned=True,
            read_only=True,
            approval_required=True,
            jurisdiction_ready=True,
            description="Source-bound jurisdiction placeholder for EU-level compliance.",
        ),
    )

    return LegalJurisdictionContract(
        total_jurisdictions=len(entries),
        ready_jurisdictions=sum(1 for entry in entries if entry.jurisdiction_ready),
        source_bound_jurisdictions=sum(1 for entry in entries if entry.source_bound),
        versioned_jurisdictions=sum(1 for entry in entries if entry.versioned),
        read_only_jurisdictions=sum(1 for entry in entries if entry.read_only),
        approval_required_jurisdictions=sum(1 for entry in entries if entry.approval_required),
        entries=entries,
    )
