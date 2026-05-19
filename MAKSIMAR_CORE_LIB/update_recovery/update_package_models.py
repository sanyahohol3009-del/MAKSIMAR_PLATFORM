from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from enum import Enum
from typing import Any


class UpdatePackageArtifactKind(str, Enum):
    CODE_BUNDLE = "code_bundle"
    CONFIG_BUNDLE = "config_bundle"
    POLICY_BUNDLE = "policy_bundle"
    MODEL_BUNDLE = "model_bundle"


class UpdatePackageSignatureAlgorithm(str, Enum):
    ED25519 = "ed25519"
    ECDSA_P256_SHA256 = "ecdsa_p256_sha256"
    RSA_PSS_SHA256 = "rsa_pss_sha256"


@dataclass(frozen=True, slots=True)
class UpdatePackageArtifactRef:
    artifact_id: str
    artifact_kind: UpdatePackageArtifactKind
    artifact_uri: str
    artifact_sha256: str
    size_bytes: int
    content_type: str

    def __post_init__(self) -> None:
        _validate_non_empty("artifact_id", self.artifact_id)
        if not isinstance(self.artifact_kind, UpdatePackageArtifactKind):
            raise TypeError("artifact_kind must be UpdatePackageArtifactKind")
        _validate_non_empty("artifact_uri", self.artifact_uri)
        _validate_sha256("artifact_sha256", self.artifact_sha256)
        if self.size_bytes <= 0:
            raise ValueError("size_bytes must be greater than zero")
        _validate_non_empty("content_type", self.content_type)

    def to_dict(self) -> dict[str, Any]:
        return {
            "artifact_id": self.artifact_id,
            "artifact_kind": self.artifact_kind.value,
            "artifact_uri": self.artifact_uri,
            "artifact_sha256": self.artifact_sha256,
            "size_bytes": self.size_bytes,
            "content_type": self.content_type,
        }


@dataclass(frozen=True, slots=True)
class UpdatePackageSignatureEnvelope:
    signature_id: str
    signer_id: str
    algorithm: UpdatePackageSignatureAlgorithm
    public_key_ref: str
    signature_ref: str
    signature_sha256: str
    signed_payload_sha256: str

    def __post_init__(self) -> None:
        _validate_non_empty("signature_id", self.signature_id)
        _validate_non_empty("signer_id", self.signer_id)
        if not isinstance(self.algorithm, UpdatePackageSignatureAlgorithm):
            raise TypeError("algorithm must be UpdatePackageSignatureAlgorithm")
        _validate_non_empty("public_key_ref", self.public_key_ref)
        _validate_non_empty("signature_ref", self.signature_ref)
        _validate_sha256("signature_sha256", self.signature_sha256)
        _validate_sha256("signed_payload_sha256", self.signed_payload_sha256)

    def to_dict(self) -> dict[str, Any]:
        return {
            "signature_id": self.signature_id,
            "signer_id": self.signer_id,
            "algorithm": self.algorithm.value,
            "public_key_ref": self.public_key_ref,
            "signature_ref": self.signature_ref,
            "signature_sha256": self.signature_sha256,
            "signed_payload_sha256": self.signed_payload_sha256,
        }


@dataclass(frozen=True, slots=True)
class UpdatePackageManifest:
    package_id: str
    package_version: str
    target_layer_id: str
    created_at_utc: str
    artifacts: tuple[UpdatePackageArtifactRef, ...]
    package_sha256: str
    signature: UpdatePackageSignatureEnvelope | None
    requires_snapshot: bool
    rollback_ref: str
    signed_update_required: bool = True
    direct_apply_allowed: bool = False
    dashboard_execution_allowed: bool = False
    canonical_write_allowed: bool = False

    def __post_init__(self) -> None:
        _validate_non_empty("package_id", self.package_id)
        _validate_non_empty("package_version", self.package_version)
        _validate_non_empty("target_layer_id", self.target_layer_id)
        _validate_utc_timestamp("created_at_utc", self.created_at_utc)
        _validate_artifacts(self.artifacts)
        _validate_sha256("package_sha256", self.package_sha256)
        _validate_non_empty("rollback_ref", self.rollback_ref)

        expected_hash = compute_update_package_payload_sha256(
            package_id=self.package_id,
            package_version=self.package_version,
            target_layer_id=self.target_layer_id,
            created_at_utc=self.created_at_utc,
            artifacts=self.artifacts,
            requires_snapshot=self.requires_snapshot,
            rollback_ref=self.rollback_ref,
        )
        if self.package_sha256 != expected_hash:
            raise ValueError("package_sha256 must match canonical update package payload hash")

        if self.signature is not None:
            if not isinstance(self.signature, UpdatePackageSignatureEnvelope):
                raise TypeError("signature must be UpdatePackageSignatureEnvelope or None")
            if self.signature.signed_payload_sha256 != self.package_sha256:
                raise ValueError("signature.signed_payload_sha256 must match package_sha256")

        if not self.signed_update_required:
            raise ValueError("signed_update_required must remain true")
        if self.direct_apply_allowed:
            raise ValueError("direct_apply_allowed must remain false")
        if self.dashboard_execution_allowed:
            raise ValueError("dashboard_execution_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")

    @property
    def is_signed(self) -> bool:
        return self.signature is not None

    def to_dict(self) -> dict[str, Any]:
        return {
            "package_id": self.package_id,
            "package_version": self.package_version,
            "target_layer_id": self.target_layer_id,
            "created_at_utc": self.created_at_utc,
            "artifacts": tuple(artifact.to_dict() for artifact in self.artifacts),
            "package_sha256": self.package_sha256,
            "signature": None if self.signature is None else self.signature.to_dict(),
            "requires_snapshot": self.requires_snapshot,
            "rollback_ref": self.rollback_ref,
            "signed_update_required": self.signed_update_required,
            "direct_apply_allowed": self.direct_apply_allowed,
            "dashboard_execution_allowed": self.dashboard_execution_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
        }


def compute_update_package_payload_sha256(
    *,
    package_id: str,
    package_version: str,
    target_layer_id: str,
    created_at_utc: str,
    artifacts: tuple[UpdatePackageArtifactRef, ...],
    requires_snapshot: bool,
    rollback_ref: str,
) -> str:
    _validate_non_empty("package_id", package_id)
    _validate_non_empty("package_version", package_version)
    _validate_non_empty("target_layer_id", target_layer_id)
    _validate_utc_timestamp("created_at_utc", created_at_utc)
    _validate_artifacts(artifacts)
    _validate_non_empty("rollback_ref", rollback_ref)

    payload = {
        "package_id": package_id,
        "package_version": package_version,
        "target_layer_id": target_layer_id,
        "created_at_utc": created_at_utc,
        "artifacts": tuple(artifact.to_dict() for artifact in artifacts),
        "requires_snapshot": requires_snapshot,
        "rollback_ref": rollback_ref,
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def build_update_package_manifest(
    *,
    package_id: str,
    package_version: str,
    target_layer_id: str,
    created_at_utc: str,
    artifacts: tuple[UpdatePackageArtifactRef, ...],
    signature: UpdatePackageSignatureEnvelope | None,
    requires_snapshot: bool,
    rollback_ref: str,
) -> UpdatePackageManifest:
    package_sha256 = compute_update_package_payload_sha256(
        package_id=package_id,
        package_version=package_version,
        target_layer_id=target_layer_id,
        created_at_utc=created_at_utc,
        artifacts=artifacts,
        requires_snapshot=requires_snapshot,
        rollback_ref=rollback_ref,
    )

    if signature is not None and signature.signed_payload_sha256 != package_sha256:
        raise ValueError("signature.signed_payload_sha256 must match computed package payload hash")

    return UpdatePackageManifest(
        package_id=package_id,
        package_version=package_version,
        target_layer_id=target_layer_id,
        created_at_utc=created_at_utc,
        artifacts=artifacts,
        package_sha256=package_sha256,
        signature=signature,
        requires_snapshot=requires_snapshot,
        rollback_ref=rollback_ref,
    )


def _validate_artifacts(artifacts: tuple[UpdatePackageArtifactRef, ...]) -> None:
    if not isinstance(artifacts, tuple):
        raise TypeError("artifacts must be a tuple")
    if not artifacts:
        raise ValueError("artifacts must not be empty")
    artifact_ids: set[str] = set()
    for artifact in artifacts:
        if not isinstance(artifact, UpdatePackageArtifactRef):
            raise TypeError("artifacts must contain UpdatePackageArtifactRef")
        if artifact.artifact_id in artifact_ids:
            raise ValueError("artifact_id values must be unique")
        artifact_ids.add(artifact.artifact_id)


def _validate_non_empty(field_name: str, value: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    if not value:
        raise ValueError(f"{field_name} must not be empty")


def _validate_sha256(field_name: str, value: str) -> None:
    _validate_non_empty(field_name, value)
    if len(value) != 64:
        raise ValueError(f"{field_name} must be a 64-character sha256 hex string")
    int(value, 16)


def _validate_utc_timestamp(field_name: str, value: str) -> None:
    _validate_non_empty(field_name, value)
    if "T" not in value or not value.endswith("Z"):
        raise ValueError(f"{field_name} must be an ISO-like UTC timestamp ending with Z")
