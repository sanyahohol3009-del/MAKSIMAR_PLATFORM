from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Any, Dict

import psutil


@dataclass(frozen=True)
class HealthSnapshot:
    ts: float
    uptime_s: float
    loadavg: tuple[float, float, float]
    cpu_count: int
    mem_total: int
    mem_available: int
    mem_used: int
    disk_total: int
    disk_free: int
    disk_used: int

    def as_dict(self) -> Dict[str, Any]:
        return {
            "ts": self.ts,
            "uptime_s": self.uptime_s,
            "loadavg": self.loadavg,
            "cpu_count": self.cpu_count,
            "mem": {
                "total": self.mem_total,
                "available": self.mem_available,
                "used": self.mem_used,
            },
            "disk": {
                "total": self.disk_total,
                "free": self.disk_free,
                "used": self.disk_used,
            },
        }


def take_snapshot(root_path: str) -> HealthSnapshot:
    ts = time.time()
    boot_ts = psutil.boot_time()
    uptime_s = ts - boot_ts

    try:
        loadavg = os.getloadavg()
    except OSError:
        loadavg = (0.0, 0.0, 0.0)

    vm = psutil.virtual_memory()
    du = psutil.disk_usage(root_path)

    return HealthSnapshot(
        ts=ts,
        uptime_s=uptime_s,
        loadavg=loadavg,
        cpu_count=psutil.cpu_count() or 0,
        mem_total=int(vm.total),
        mem_available=int(vm.available),
        mem_used=int(vm.used),
        disk_total=int(du.total),
        disk_free=int(du.free),
        disk_used=int(du.used),
    )
