"""Version-pinned LOCAL n8n capability catalog (offline, no internet).

Authoritative truth = installed canonical n8n 2.42.6 source/runtime,
NOT internet documentation. The 8B automation brain queries this catalog locally to
discover installed nodes/operations/credentials and synthesize workflows without any
cloud/network dependency.
"""
from __future__ import annotations

import json
import re
import sqlite3
from pathlib import Path
from typing import Any

_CATALOG_PATH = Path(__file__).resolve().parents[2] / "EXTERNAL_BACKENDS/vendor_quarantine/n8n-2.42.6-candidate/n8n_2.42.6_node_catalog.json"

_AI_KEYS = (
    "langchain", "openai", "anthropic", "ai", "lm", "llm", "gpt", "embedding",
    "vector", "tool", "agent", "mistral", "ollama", "hugging", "retrieval",
    "sentiment", "classif", "memory",
)
_LOCAL_GROUPS = {"transform", "core", "utility", "function", "flow", "editor"}

_cache: dict[str, Any] | None = None


def _load() -> dict[str, Any]:
    global _cache
    if _cache is None:
        _cache = json.loads(_CATALOG_PATH.read_text(encoding="utf-8"))
    return _cache


def _node_type(node: dict[str, Any]) -> str:
    """Canonical installed type across the compact and real export:nodes shapes."""
    value = str(node.get("type") or node.get("name") or "")
    return value if "." in value else f"n8n-nodes-base.{value}"


def _short_name(node: dict[str, Any]) -> str:
    return str(node.get("name") or node.get("type") or "").rsplit(".", 1)[-1]


def _credential_contracts(node: dict[str, Any]) -> tuple[dict[str, Any], ...]:
    return tuple(
        dict(value) if isinstance(value, dict) else {"name": str(value), "required": True}
        for value in node.get("credentials") or ()
    )


def _property_text(prop: dict[str, Any]) -> str:
    values = [prop.get("displayName"), prop.get("name"), prop.get("description")]
    for option in prop.get("options") or ():
        if isinstance(option, dict):
            values.extend((option.get("name"), option.get("value"), option.get("description"), option.get("action")))
    return " ".join(str(value) for value in values if value)


def _node_search_text(node: dict[str, Any]) -> str:
    return " ".join((
        _short_name(node), str(node.get("displayName") or ""), str(node.get("description") or ""),
        " ".join(_property_text(prop) for prop in node.get("properties") or () if isinstance(prop, dict)),
    )).lower()


def available_credential_instances(database_path: Path | None = None) -> tuple[dict[str, str], ...]:
    """Read credential identity/type truth without reading or decrypting secret data."""
    if database_path is None:
        # Canonical provider owns the data root; old user/migration DBs are not
        # current credential truth. Lazy import preserves the catalog/compiler graph.
        from MAKSIMAR_SERVER.AI_ORCHESTRATION.n8n_adapter import _CANONICAL_DATA_ROOT
        path = _CANONICAL_DATA_ROOT / "database.sqlite"
    else:
        path = database_path
    if not path.exists():
        return ()
    try:
        connection = sqlite3.connect(f"file:{path}?mode=ro", uri=True, timeout=2.0)
        try:
            rows = connection.execute("SELECT id, name, type FROM credentials_entity").fetchall()
        finally:
            connection.close()
    except (sqlite3.Error, OSError):
        return ()
    return tuple({"id": str(row[0]), "name": str(row[1]), "type": str(row[2])} for row in rows)


def credential_instance_ids(credential_type: str) -> tuple[str, ...]:
    return tuple(item["id"] for item in available_credential_instances() if item["type"] == credential_type)


def n8n_version() -> str:
    return str(_load()["n8n_version"])


# Known built-in intrinsic LOCAL n8n node names (no external network). Used as a
# small positive whitelist; everything else is resolved/classified, never assumed.
_LOCAL_INTRINSIC_NAMES = {
    "manualtrigger", "set", "code", "if", "noop", "merge", "split", "edit",
    "filter", "wait", "loop", "switch", "compare", "limit", "rename", "sort",
    "remove", "extract", "aggregate", "summarize", "html", "markdown", "cron",
    "interval", "scheduletrigger", "executecommand", "executeworkflow",
    "readwritefile", "readbinaryfile", "writebinaryfile", "movefile", "copyfile",
    "renamefile", "localfiletrigger", "sqlite",
}

# Known network-transport node names (strong positive signal).
_NETWORK_TRANSPORT_NAMES = {
    "ftp", "sftp", "httprequest", "webhook", "discord", "slack", "telegram",
    "whatsapp", "email", "smtp", "imap", "mqtt", "amqp", "kafka", "redis",
    "elasticsearch", "mongodb", "postgres", "mysql", "mariadb", "oracle",
    "mssql", "influxdb", "timescaledb", "dynamodb", "s3",
}

# Nodes whose network scope is an EXTERNAL internet/cloud service (vs localhost/LAN).
_EXTERNAL_SERVICE_NAMES = {
    "discord", "slack", "telegram", "whatsapp", "s3", "dynamodb", "github",
    "gitlab", "gmail", "googlesheets", "googledrive", "twitter", "x",
}


def transport_requirement(node: dict[str, Any]) -> str:
    """Typed transport classification; description text cannot grant policy facts."""
    node_type = _node_type(node)
    if not node_type.startswith("n8n-nodes-base."):
        return "UNKNOWN"
    name = node_type.removeprefix("n8n-nodes-base.").lower()
    if name in _LOCAL_INTRINSIC_NAMES:
        return "NONE"
    if name in _NETWORK_TRANSPORT_NAMES or name in _EXTERNAL_SERVICE_NAMES:
        return "NETWORK_TRANSPORT"
    return "UNKNOWN"


# Source-backed internal/UI nodes that are NOT user-facing executable capabilities.
# Proven from installed n8n 2.36.2 source: StickyNote has inputs:[] and outputs:[] and
# is a canvas annotation ("Make your workflow easier to understand"). OneSimpleApi is a
# genuine user-facing integration node (credentials + Utility category) -> USER_USABLE.
_INTERNAL_ONLY_NAMES = {"stickynote"}


def runtime_role(node: dict[str, Any]) -> str:
    """USER_USABLE / INTERNAL_ONLY — derived from installed node identity/role."""
    name = _short_name(node).lower()
    if name in _INTERNAL_ONLY_NAMES:
        return "INTERNAL_ONLY"
    return "USER_USABLE"


def network_scope(node: dict[str, Any]) -> str:
    """Typed LOCALHOST_OR_LAN_CAPABLE / EXTERNAL_SERVICE / UNKNOWN."""
    node_type = _node_type(node)
    if not node_type.startswith("n8n-nodes-base."):
        return "UNKNOWN"
    name = node_type.removeprefix("n8n-nodes-base.").lower()
    if name in _EXTERNAL_SERVICE_NAMES:
        return "EXTERNAL_SERVICE"
    if transport_requirement(node) in {"NONE", "NETWORK_TRANSPORT"}:
        return "LOCALHOST_OR_LAN_CAPABLE"
    return "UNKNOWN"


def network_truth(node: dict[str, Any]) -> str:
    """Project the same typed transport truth without a second text classifier."""
    return {"NONE": "LOCAL", "NETWORK_TRANSPORT": "NETWORK_REQUIRED"}.get(
        transport_requirement(node), "UNKNOWN",
    )


def _classify_network(node: dict[str, Any]) -> str:
    # Backward-compatible weak heuristic for search classification only (not policy).
    nt = network_truth(node)
    return "local" if nt == "LOCAL" else "cloud"


def _is_ai_tool(node: dict[str, Any]) -> bool:
    text = _node_search_text(node)
    return any(k in text for k in _AI_KEYS)


def search_n8n_catalog(query: str, top_k: int = 12) -> dict[str, Any]:
    """Search installed n8n nodes by a natural semantic goal.

    Returns the exact matching node/operation contracts (name, displayName, group,
    version, credentials, operations, isTrigger, network requirement, ai/tool flag).
    """
    catalog = _load()
    q = (query or "").lower()
    terms = [t for t in re.split(r"[^a-z0-9а-яё]+", q) if len(t) > 1]
    scored: list[tuple[float, dict[str, Any]]] = []
    for node in catalog["nodes"]:
        name = _short_name(node).lower()
        display = (node.get("displayName") or "").lower()
        desc = _node_search_text(node)
        score = 0.0
        # Exact identity match (name or display name) ranks deterministically first.
        if name == q or display == q:
            score += 10.0
        for t in terms:
            if t in name:
                score += 5.0
            if t in display:
                score += 2.5
            if t in desc:
                score += 1.0
        score += sum(1.5 for g in node.get("group") or [] if g in q)
        score += sum(2.0 for o in node.get("operations") or [] if str(o).lower() in q)
        if score > 0:
            scored.append((score, node))
    scored.sort(key=lambda x: (-x[0], x[1].get("name") or ""))
    results = []
    seen_types: set[str] = set()
    for score, node in scored:
        installed_type = _node_type(node)
        if installed_type in seen_types:
            continue
        seen_types.add(installed_type)
        item = dict(node)
        item["type"] = installed_type
        item["name"] = _short_name(node)
        item["credential_contracts"] = _credential_contracts(node)
        item["score"] = score
        item["network_requirement"] = _classify_network(node)
        item["ai_tool_capable"] = _is_ai_tool(node)
        results.append(item)
        if len(results) >= top_k:
            break
    return {
        "n8n_version": catalog["n8n_version"],
        "query": query,
        "source": "installed frozen n8n source (offline, authoritative)",
        "match_count": len(results),
        "matches": results,
    }


def node_contract(node_type: str) -> dict[str, Any]:
    """Return the exact installed node contract for a node type (or a truthful miss)."""
    catalog = _load()
    for node in catalog["nodes"]:
        if (_node_type(node) == node_type or _short_name(node) == node_type
                or str(node.get("displayName") or "").casefold() == str(node_type).casefold()):
            item = dict(node)
            item["type"] = _node_type(node)
            item["name"] = _short_name(node)
            item["credential_contracts"] = _credential_contracts(node)
            item["network_requirement"] = _classify_network(node)
            item["ai_tool_capable"] = _is_ai_tool(node)
            return {"found": True, "n8n_version": catalog["n8n_version"], "node": item}
    return {"found": False, "node_type": node_type, "n8n_version": catalog["n8n_version"]}


def _display_rule_matches(rule: dict[str, Any], values: dict[str, Any]) -> bool:
    for key, allowed in rule.items():
        if isinstance(allowed, list) and values.get(key) not in allowed:
            return False
    return True


def property_is_active(prop: dict[str, Any], values: dict[str, Any]) -> bool:
    display = prop.get("displayOptions") or {}
    show = display.get("show") or {}
    hide = display.get("hide") or {}
    return (not show or _display_rule_matches(show, values)) and not (hide and _display_rule_matches(hide, values))


def operation_candidates(node: dict[str, Any]) -> tuple[dict[str, str], ...]:
    """Return exact resource/operation values from installed node parameter truth."""
    resources: list[tuple[str, str]] = [("", "")]
    for prop in node.get("properties") or ():
        if isinstance(prop, dict) and prop.get("name") == "resource" and prop.get("type") == "options":
            resources = [(str(option.get("value")), str(option.get("name")))
                         for option in prop.get("options") or () if isinstance(option, dict)]
            break
    found: list[dict[str, str]] = []
    for prop in node.get("properties") or ():
        if not isinstance(prop, dict) or prop.get("name") != "operation" or prop.get("type") != "options":
            continue
        allowed_resources = (prop.get("displayOptions") or {}).get("show", {}).get("resource")
        for resource_value, resource_name in resources:
            if allowed_resources and resource_value not in allowed_resources:
                continue
            for option in prop.get("options") or ():
                if isinstance(option, dict):
                    found.append({
                        "resource": resource_value, "resource_name": resource_name,
                        "operation": str(option.get("value") or ""),
                        "operation_name": str(option.get("name") or ""),
                        "description": str(option.get("description") or option.get("action") or ""),
                    })
    return tuple(found)


def parameter_contract(node: dict[str, Any], resource: str, operation: str) -> tuple[dict[str, Any], ...]:
    """Exact active parameter schema for a chosen installed resource/operation."""
    values: dict[str, Any] = {"resource": resource, "operation": operation}
    for prop in node.get("properties") or ():
        if isinstance(prop, dict) and prop.get("name") not in values and "default" in prop:
            values[str(prop.get("name"))] = prop.get("default")
    result = []
    for prop in node.get("properties") or ():
        if not isinstance(prop, dict) or prop.get("name") in {"resource", "operation"}:
            continue
        if property_is_active(prop, values):
            result.append({key: prop[key] for key in (
                "displayName", "name", "type", "required", "default", "description", "options",
            ) if key in prop})
    return tuple(result)


def credential_requirements(node: dict[str, Any], bound_parameters: dict[str, Any]) -> tuple[dict[str, Any], ...]:
    result = []
    for credential in _credential_contracts(node):
        display = credential.get("displayOptions") or {}
        if display.get("show") and not _display_rule_matches(display["show"], bound_parameters):
            continue
        credential_type = str(credential.get("name") or "")
        instances = credential_instance_ids(credential_type)
        result.append({
            "credential_type": credential_type,
            "required": bool(credential.get("required", True)),
            "instance_available": bool(instances),
            "credential_instance_ids": instances,
        })
    return tuple(result)


__all__ = [
    "available_credential_instances", "credential_requirements", "network_scope", "node_contract",
    "n8n_version", "operation_candidates", "parameter_contract", "property_is_active", "runtime_role",
    "search_n8n_catalog", "transport_requirement",
]
