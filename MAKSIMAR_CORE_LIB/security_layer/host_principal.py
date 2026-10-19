"""Small HOST principal verifier for control-plane protected actions.

The signing secret is deployment configuration (never a request field).  With
no configured secret every HTTP principal is rejected fail-closed.
"""
from __future__ import annotations

import base64
import getpass
import hashlib
import hmac
import json
import os
from pathlib import Path
import secrets
import time
from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.ai_orchestration.semantic_intent_contract import IdentityContext


HOST_SECRET_PATH = Path.home() / "MAKSIMAR_RUNTIME" / "security" / "jarvis_host_auth_secret"


def load_host_secret() -> str:
    """Load/generate the HOST-owned secret with restrictive permissions."""
    configured = os.environ.get("JARVIS_HOST_AUTH_SECRET", "")
    if configured:
        return configured
    HOST_SECRET_PATH.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.chmod(HOST_SECRET_PATH, 0o600)
        value = HOST_SECRET_PATH.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        value = ""
    if not value:
        value = secrets.token_urlsafe(48)
        fd = os.open(HOST_SECRET_PATH, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        try:
            os.write(fd, value.encode())
        finally:
            os.close(fd)
    os.chmod(HOST_SECRET_PATH, 0o600)
    return value


@dataclass(frozen=True, slots=True)
class HostPrincipal:
    identity_id: str
    session_id: str
    profile_type: str = "owner"


def issue_host_token(principal: HostPrincipal, *, secret: str | None = None, ttl_seconds: int = 300) -> str:
    key = (secret or load_host_secret()).encode()
    if not key:
        raise ValueError("JARVIS_HOST_AUTH_SECRET is not configured")
    now = int(time.time())
    raw = json.dumps({"identity_id": principal.identity_id, "session_id": principal.session_id,
                      "profile_type": principal.profile_type, "issued_at": now,
                      "expires_at": now + ttl_seconds, "purpose": "host_approval",
                      "schema_version": "host_principal.v1"}, sort_keys=True, separators=(",", ":")).encode()
    body = base64.urlsafe_b64encode(raw).decode().rstrip("=")
    sig = hmac.new(key, body.encode(), hashlib.sha256).hexdigest()
    return f"{body}.{sig}"


def verify_host_token(token: str, *, secret: str | None = None) -> HostPrincipal | None:
    key = (secret or load_host_secret()).encode()
    if not key or not isinstance(token, str) or "." not in token:
        return None
    body, signature = token.split(".", 1)
    expected = hmac.new(key, body.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(signature, expected):
        return None
    try:
        raw = base64.urlsafe_b64decode(body + "=" * (-len(body) % 4))
        payload = json.loads(raw)
        principal = HostPrincipal(str(payload["identity_id"]), str(payload["session_id"]), str(payload["profile_type"]))
        now = int(time.time())
        if (not principal.identity_id or not principal.session_id or principal.profile_type != "owner"
                or payload.get("purpose") != "host_approval"
                or payload.get("schema_version") != "host_principal.v1"
                or not isinstance(payload.get("issued_at"), int)
                or not isinstance(payload.get("expires_at"), int)
                or payload["expires_at"] <= now or payload["issued_at"] > now + 5):
            return None
        return principal
    except (ValueError, TypeError, KeyError, json.JSONDecodeError):
        return None


def identity_from_host_token(token: str) -> tuple[HostPrincipal, IdentityContext] | None:
    principal = verify_host_token(token)
    if principal is None:
        return None
    return principal, IdentityContext(
        principal.identity_id, "authenticated_http_session", "owner", True, True,
        principal.identity_id, "JARVIS",
    )


def bootstrap_local_owner_token(*, session_id: str) -> str:
    """Issue a short-lived owner token only to the local OS user process."""
    if not session_id.strip() or os.getuid() < 0:
        raise ValueError("local owner session is required")
    return issue_host_token(HostPrincipal(getpass.getuser(), session_id))


__all__ = ["HOST_SECRET_PATH", "HostPrincipal", "load_host_secret", "issue_host_token", "verify_host_token", "identity_from_host_token", "bootstrap_local_owner_token"]
