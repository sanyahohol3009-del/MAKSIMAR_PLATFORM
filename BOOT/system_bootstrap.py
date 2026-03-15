#!/usr/bin/env python3

import os
import sys
import subprocess
from pathlib import Path


def _fail(msg: str, code: int = 2) -> None:
    print(msg)
    sys.exit(code)


def _resolve_under(base: Path, target: Path) -> Path:
    """Resolve target and ensure it stays under base (basic path-traversal guard)."""
    base_r = base.resolve()
    target_r = target.resolve()
    if base_r not in target_r.parents and target_r != base_r:
        _fail(f"[BOOT] Path escape blocked: {target_r}", 3)
    return target_r


def verify_genesis_signature(trust_dir: Path) -> None:
    """
    Verifies genesis_hash.bin.sig against genesis_hash.bin using ssh-keygen -Y verify.
    Requires:
      - allowed_signers
      - genesis_hash.bin
      - genesis_hash.bin.sig
    """
    allowed = _resolve_under(trust_dir, trust_dir / "allowed_signers")
    genesis = _resolve_under(trust_dir, trust_dir / "genesis_hash.bin")
    sig = _resolve_under(trust_dir, trust_dir / "genesis_hash.bin.sig")

    for p in (allowed, genesis, sig):
        if not p.exists():
            _fail(f"[BOOT] Missing trust file: {p}", 1)

    # We pass the message file via stdin: "< genesis_hash.bin"
    cmd = [
        "ssh-keygen",
        "-Y",
        "verify",
        "-f",
        str(allowed),
        "-I",
        "maksimar",
        "-n",
        "maksimar-genesis",
        "-s",
        str(sig),
    ]

    res = subprocess.run(
        cmd,
        input=genesis.read_bytes(),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )

    out = res.stdout.decode(errors="replace").strip()
    if res.returncode != 0:
        _fail("[BOOT] GENESIS SIGNATURE INVALID\n" + out, 10)

    print("[BOOT] Genesis signature OK")


def run_core_integrity(repo_root: Path) -> None:
    verifier = _resolve_under(repo_root, repo_root / "CORE_ROOT" / "core_integrity_verifier.py")
    if not verifier.exists():
        _fail(f"[BOOT] Missing verifier: {verifier}", 1)

    # Run verifier. It already prints SYSTEM INTEGRITY FAILURE / verified.
    res = subprocess.run(
        ["python3", str(verifier)],
        cwd=str(repo_root),
        check=False,
    )
    if res.returncode != 0:
        _fail("[BOOT] CORE INTEGRITY CHECK FAILED (blocking boot)", 20)

    print("[BOOT] Core integrity OK")


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]  # .../MAKSIMAR_PLATFORM
    trust_dir = Path.home() / ".local" / "share" / "maksimar" / "trust"

    print("[BOOT] Starting secure bootstrap")
    verify_genesis_signature(trust_dir)
    run_core_integrity(repo_root)

    print("[BOOT] Secure bootstrap completed. System may start now.")
    # Следующий шаг позже: здесь будет запуск CONTROL_PLANE / api_gateway.


if __name__ == "__main__":
    main()
