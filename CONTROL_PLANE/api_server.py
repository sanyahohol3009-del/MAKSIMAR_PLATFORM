from fastapi import FastAPI
from pathlib import Path
import time

from CONTROL_PLANE.health.monitor import take_snapshot

app = FastAPI(title="MAKSIMAR Control Plane")


@app.get("/")
def root():
    return {"status": "MAKSIMAR control plane online"}


@app.get("/health")
def health():
    root = str(Path(__file__).resolve().parents[1])
    snap = take_snapshot(root)

    return {
        "ok": True,
        "health": snap.as_dict()
    }


@app.get("/health/latency")
def health_latency():
    t0 = time.perf_counter()
    dt_ms = (time.perf_counter() - t0) * 1000.0

    return {
        "ok": True,
        "latency_ms": dt_ms
    }

