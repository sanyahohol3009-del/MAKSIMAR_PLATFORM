from __future__ import annotations

import math
import json
import os
import platform
import re
import shutil
import subprocess
from pathlib import Path
from dataclasses import replace
from typing import Iterable

from MAKSIMAR_CORE_LIB.node_roles.node_identity_models import CanonicalNodeId
from MAKSIMAR_SERVER.EXECUTION_CONTROL.node_runtime.hardware_detection_adapter_models import (
    DetectedCpuSnapshot,
    DetectedGpuSnapshot,
    DetectedMemorySnapshot,
    NodeHardwareDetectionContract,
)


def _run_command(command: list[str]) -> str:
    """Run a command safely and return stripped stdout."""
    if not command:
        return ""

    executable = command[0]
    if shutil.which(executable) is None:
        return ""

    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return ""

    if completed.returncode != 0:
        return ""

    return completed.stdout.strip()


def _read_text_file(path: str) -> str:
    """Read a UTF-8 text file safely."""
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as handle:
            return handle.read()
    except OSError:
        return ""


def _parse_key_value_output(raw: str) -> dict[str, str]:
    """Parse 'Key: Value' command output into a dictionary."""
    parsed: dict[str, str] = {}

    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        parsed[key.strip()] = value.strip()

    return parsed


def _parse_proc_cpuinfo() -> dict[str, str]:
    """Parse /proc/cpuinfo first processor block."""
    cpuinfo = _read_text_file("/proc/cpuinfo")
    if not cpuinfo:
        return {}

    first_block = cpuinfo.split("\n\n", 1)[0]
    return _parse_key_value_output(first_block)


def _detect_cpu_snapshot() -> tuple[DetectedCpuSnapshot, tuple[str, ...]]:
    """Detect CPU snapshot using lscpu and /proc/cpuinfo."""
    sources: list[str] = []
    lscpu_output = _run_command(["lscpu"])
    lscpu_map = _parse_key_value_output(lscpu_output)

    if lscpu_output:
        sources.append("lscpu")

    cpuinfo_map = _parse_proc_cpuinfo()
    if cpuinfo_map:
        sources.append("/proc/cpuinfo")

    cpu_vendor = (
        lscpu_map.get("Vendor ID")
        or cpuinfo_map.get("vendor_id")
        or platform.processor()
        or "unknown"
    )
    cpu_model = (
        lscpu_map.get("Model name")
        or cpuinfo_map.get("model name")
        or platform.processor()
        or "unknown"
    )
    cpu_arch = lscpu_map.get("Architecture") or platform.machine() or "unknown"

    cpu_cores_text = lscpu_map.get("Core(s) per socket", "")
    sockets_text = lscpu_map.get("Socket(s)", "")
    cpu_threads_text = lscpu_map.get("CPU(s)", "")

    try:
        cores_per_socket = int(cpu_cores_text) if cpu_cores_text else 0
    except ValueError:
        cores_per_socket = 0

    try:
        sockets = int(sockets_text) if sockets_text else 0
    except ValueError:
        sockets = 0

    cpu_cores = cores_per_socket * sockets if cores_per_socket and sockets else 0
    if cpu_cores <= 0:
        cpu_cores = os.cpu_count() or 1

    try:
        cpu_threads = int(cpu_threads_text) if cpu_threads_text else 0
    except ValueError:
        cpu_threads = 0

    if cpu_threads <= 0:
        cpu_threads = os.cpu_count() or cpu_cores

    flags_text = (
        lscpu_map.get("Flags")
        or lscpu_map.get("Features")
        or cpuinfo_map.get("flags")
        or cpuinfo_map.get("Features")
        or ""
    )
    cpu_features = tuple(flag for flag in flags_text.split() if flag)

    snapshot = DetectedCpuSnapshot(
        cpu_vendor=cpu_vendor,
        cpu_model=cpu_model,
        cpu_arch=cpu_arch,
        cpu_cores=cpu_cores,
        cpu_threads=cpu_threads,
        cpu_features=cpu_features,
    )

    return snapshot, tuple(dict.fromkeys(sources))


def _parse_meminfo_value_kb(meminfo: str, key: str) -> int:
    """Extract a numeric kB value from /proc/meminfo."""
    match = re.search(rf"^{re.escape(key)}:\s+(\d+)\s+kB$", meminfo, re.MULTILINE)
    if not match:
        return 0
    return int(match.group(1))


def _extract_first_int(raw: str) -> int:
    """Extract the first integer from a string."""
    match = re.search(r"(\d+)", raw)
    if not match:
        return 0
    return int(match.group(1))


def _detect_memory_details_from_dmidecode() -> dict[str, object]:
    """Best-effort memory detail detection from dmidecode."""
    output = _run_command(["dmidecode", "--type", "memory"])
    if not output:
        return {}

    details: dict[str, object] = {
        "ram_generation": "unknown",
        "ram_frequency_mhz": 0,
        "ram_module_count": 0,
        "ram_channels": 0,
        "ram_layout": "unknown",
        "ecc_present": False,
        "registered_or_buffered": "unknown",
        "slot_population": "unknown",
    }

    generation_match = re.search(r"Type:\s+(DDR\d|LPDDR\dX?|LPDDR\d)", output)
    if generation_match:
        details["ram_generation"] = generation_match.group(1)

    speed_matches = re.findall(r"(?:Speed|Configured Memory Speed):\s+(\d+)", output)
    if speed_matches:
        details["ram_frequency_mhz"] = max(int(value) for value in speed_matches)

    size_matches = re.findall(r"^\s*Size:\s+(\d+)\s+(MB|GB)$", output, re.MULTILINE)
    populated_slots = 0
    for size_value, _ in size_matches:
        if int(size_value) > 0:
            populated_slots += 1
    details["ram_module_count"] = populated_slots

    locator_matches = re.findall(r"^\s*Locator:\s+(.+)$", output, re.MULTILINE)
    if locator_matches:
        details["slot_population"] = f"{populated_slots}/{len(locator_matches)}"

    if "Multi-bit ECC" in output or "Single-bit ECC" in output:
        details["ecc_present"] = True

    if "Registered" in output:
        details["registered_or_buffered"] = "registered"
    elif "Buffered" in output:
        details["registered_or_buffered"] = "buffered"
    else:
        details["registered_or_buffered"] = "unbuffered"

    channels_output = _run_command(["lscpu"])
    channels_map = _parse_key_value_output(channels_output)
    channels = _extract_first_int(channels_map.get("Channel(s)", ""))
    if channels > 0:
        details["ram_channels"] = channels

    if populated_slots > 0 and channels > 0:
        details["ram_layout"] = f"{populated_slots}modules{channels}_channels"

    return details


def _detect_memory_snapshot() -> tuple[DetectedMemorySnapshot, tuple[str, ...]]:
    """Detect memory snapshot using /proc/meminfo and dmidecode when available."""
    sources: list[str] = []

    meminfo = _read_text_file("/proc/meminfo")
    if meminfo:
        sources.append("/proc/meminfo")

    total_kb = _parse_meminfo_value_kb(meminfo, "MemTotal")
    free_kb = _parse_meminfo_value_kb(meminfo, "MemAvailable")
    if free_kb <= 0:
        free_kb = _parse_meminfo_value_kb(meminfo, "MemFree")

    ram_total_gb = math.ceil(total_kb / (1024 * 1024)) if total_kb else 0
    ram_free_gb = math.floor(free_kb / (1024 * 1024)) if free_kb else 0

    used_kb = max(total_kb - free_kb, 0)
    ram_pressure_percent = int((used_kb / total_kb) * 100) if total_kb else 0

    details = _detect_memory_details_from_dmidecode()
    if details:
        sources.append("dmidecode")

    domains, scope_complete = _memory_constraint_domains(free_kb * 1024 if free_kb else None)
    snapshot = DetectedMemorySnapshot(
        ram_total_gb=ram_total_gb,
        ram_free_gb=ram_free_gb,
        ram_pressure_percent=ram_pressure_percent,
        ram_generation=str(details.get("ram_generation", "unknown")),
        ram_frequency_mhz=int(details.get("ram_frequency_mhz", 0)),
        ram_module_count=int(details.get("ram_module_count", 0)),
        ram_channels=int(details.get("ram_channels", 0)),
        ram_layout=str(details.get("ram_layout", "unknown")),
        ecc_present=bool(details.get("ecc_present", False)),
        registered_or_buffered=str(details.get("registered_or_buffered", "unknown")),
        slot_population=str(details.get("slot_population", "unknown")),
        available_bytes=free_kb * 1024 if free_kb else None,
        constraint_domains=domains,
        scope_complete=scope_complete,
    )

    return snapshot, tuple(dict.fromkeys(sources))


def _classify_gpu(vendor: str, model: str) -> tuple[str, bool, tuple[str, ...]]:
    """Classify GPU/accelerator type and capabilities."""
    vendor_lower = vendor.lower()
    model_lower = model.lower()

    if not vendor and not model:
        return "cpu_only", False, ()

    if vendor_lower in {"intel", "qualcomm", "apple"}:
        return "integrated_gpu", True, ("graphics",)

    if "integrated" in model_lower or "apu" in model_lower:
        return "integrated_gpu", True, ("graphics",)

    if "tesla" in model_lower or "instinct" in model_lower:
        return "accelerator", False, ("compute",)

    if vendor_lower == "nvidia":
        return "discrete_gpu", False, ("graphics", "compute")
    if vendor_lower == "amd":
        return "discrete_gpu", False, ("graphics", "compute")

    return "discrete_gpu", False, ("graphics",)


def _detect_nvidia_gpus() -> tuple[tuple[DetectedGpuSnapshot, ...], tuple[str, ...]]:
    """Detect NVIDIA GPUs via nvidia-smi when available."""
    output = _run_command(
        [
            "nvidia-smi",
            "--query-gpu=index,uuid,pci.bus_id,name,memory.total,memory.free",
            "--format=csv,noheader,nounits",
        ]
    )
    if not output:
        return (), ()

    gpus: list[DetectedGpuSnapshot] = []
    for line in output.splitlines():
        parts = [part.strip() for part in line.split(",")]
        if len(parts) != 6:
            continue

        try:
            gpu_index = int(parts[0])
            vram_total = max(int(parts[4]) // 1024, 0)
            vram_free = max(int(parts[5]) // 1024, 0)
        except ValueError:
            continue

        gpus.append(
            DetectedGpuSnapshot(
                gpu_index=gpu_index,
                gpu_vendor="NVIDIA",
                gpu_model=parts[3],
                accelerator_class="discrete_gpu",
                vram_total_gb=vram_total,
                vram_free_gb=vram_free,
                shared_memory_mode=False,
                gpu_capabilities=("graphics", "compute", "cuda"),
                gpu_uuid=parts[1].lower() if re.fullmatch(r"GPU-[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}", parts[1], re.IGNORECASE) else "",
                pci_bus_id=_normalize_pci_identity(parts[2]),
            )
        )

    return tuple(gpus), ("nvidia-smi",)


def _vendor_from_lspci_line(line: str) -> str:
    """Infer GPU vendor from lspci line."""
    lowered = line.lower()
    if "nvidia" in lowered:
        return "NVIDIA"
    if "advanced micro devices" in lowered or "amd/" in lowered or " amd " in lowered:
        return "AMD"
    if "intel corporation" in lowered or " intel " in lowered:
        return "Intel"
    if "qualcomm" in lowered:
        return "Qualcomm"
    return "unknown"


def _model_from_lspci_line(line: str, vendor: str) -> str:
    """Infer GPU model from lspci line."""
    model = line
    if vendor != "unknown":
        vendor_index = model.lower().find(vendor.lower())
        if vendor_index >= 0:
            model = model[vendor_index + len(vendor) :].strip(" :-")
    return model.strip()


def _detect_generic_gpus() -> tuple[tuple[DetectedGpuSnapshot, ...], tuple[str, ...]]:
    """Detect generic GPU devices via lspci."""
    output = _run_command(["lspci"])
    if not output:
        return (), ()

    gpu_lines = [
        line
        for line in output.splitlines()
        if any(token in line.lower() for token in ("vga compatible controller", "3d controller", "display controller"))
    ]
    if not gpu_lines:
        return (), ("lspci",)

    detected: list[DetectedGpuSnapshot] = []
    for index, line in enumerate(gpu_lines):
        vendor = _vendor_from_lspci_line(line)
        model = _model_from_lspci_line(line, vendor)
        accelerator_class, shared_memory_mode, capabilities = _classify_gpu(vendor, model)

        detected.append(
            DetectedGpuSnapshot(
                gpu_index=index,
                gpu_vendor=vendor,
                gpu_model=model,
                accelerator_class=accelerator_class,
                vram_total_gb=0,
                vram_free_gb=0,
                shared_memory_mode=shared_memory_mode,
                gpu_capabilities=capabilities,
                pci_bus_id=_normalize_pci_identity(line.split()[0]),
            )
        )

    return tuple(detected), ("lspci",)


def _merge_gpu_snapshots(
    primary: Iterable[DetectedGpuSnapshot],
    secondary: Iterable[DetectedGpuSnapshot],
) -> tuple[DetectedGpuSnapshot, ...]:
    """Merge verified aliases, preserving distinct identical accelerators.

    Vendor/model/index are descriptions, not global physical identities. Unknown
    identities remain explicit observations and are never admission capacity.
    """
    merged: list[DetectedGpuSnapshot] = []
    for gpu in tuple(primary) + tuple(secondary):
        uuid = gpu.gpu_uuid.lower()
        pci = _normalize_pci_identity(gpu.pci_bus_id)
        normalized = replace(gpu, gpu_uuid=uuid, pci_bus_id=pci)
        matches = [i for i, prior in enumerate(merged) if
                   (uuid and prior.gpu_uuid == uuid) or (pci and prior.pci_bus_id == pci)]
        if len(matches) > 1:
            raise ValueError("ambiguous_physical_accelerator_identity")
        if matches:
            i = matches[0]; prior = merged[i]
            if ((uuid and prior.gpu_uuid and uuid != prior.gpu_uuid)
                    or (pci and prior.pci_bus_id and pci != prior.pci_bus_id)):
                raise ValueError("conflicting_physical_accelerator_identity")
            # Prefer the authoritative memory observation; enrich only identities.
            merged[i] = replace(prior, gpu_uuid=prior.gpu_uuid or uuid,
                                pci_bus_id=prior.pci_bus_id or pci)
        else:
            merged.append(normalized)
    return tuple(replace(gpu, gpu_index=index) for index, gpu in enumerate(merged))


def _normalize_pci_identity(value: str) -> str:
    """Normalize a PCI address from a host adapter, never a model-name heuristic."""
    value = value.strip().lower()
    if re.fullmatch(r"[0-9a-f]{2}:[0-9a-f]{2}\.[0-7]", value):
        return "00000000:" + value
    if re.fullmatch(r"[0-9a-f]{4,8}:[0-9a-f]{2}:[0-9a-f]{2}\.[0-7]", value):
        domain, bus, function = value.split(":")
        return domain.zfill(8) + ":" + bus + ":" + function
    return ""


# The existing hardware adapter owns this bounded, read-only local host query.
# No remote ComputerName, credentials, state writes, model/provider calls or cache.
_WINDOWS_PARENT_MEMORY_COMMAND = (
    "$ErrorActionPreference='Stop';"
    "$os=Get-CimInstance Win32_OperatingSystem;"
    "$memory=Get-CimInstance Win32_PerfFormattedData_PerfOS_Memory;"
    "[PSCustomObject]@{schema_version=1;source='windows_parent_cim_v1';"
    "platform=[Environment]::OSVersion.Platform.ToString();"
    "total_physical_bytes=([uint64]$os.TotalVisibleMemorySize*1024);"
    "available_physical_bytes=[uint64]$memory.AvailableBytes;"
    "commit_limit_bytes=[uint64]$memory.CommitLimit;"
    "committed_bytes=[uint64]$memory.CommittedBytes} | ConvertTo-Json -Compress"
)


def _parse_windows_parent_memory(raw, *, started, finished):
    # Validate a local acquisition; never accept partial/guessed capacities.
    try:
        payload = json.loads(raw)
    except (ValueError, TypeError):
        return None
    if (not isinstance(payload, dict)
            or type(payload.get("schema_version")) is not int
            or payload["schema_version"] != 1
            or payload.get("source") != "windows_parent_cim_v1"
            or payload.get("platform") != "Win32NT"):
        return None
    fields = ("total_physical_bytes", "available_physical_bytes",
              "commit_limit_bytes", "committed_bytes")
    if any(type(payload.get(name)) is not int or payload[name] < 0 for name in fields):
        return None
    total, free, limit, committed = (payload[name] for name in fields)
    if total <= 0 or limit <= 0 or free > total or committed > limit:
        return None
    if (type(started) not in (int, float) or type(finished) not in (int, float)
            or not math.isfinite(started) or not math.isfinite(finished)
            or not 0 <= finished - started <= 5):
        return None
    return {"source": "windows_parent_cim_v1", "association": "local_windows_interop",
            "observed_monotonic": started, "completed_monotonic": finished,
            "total_physical_bytes": total, "available_physical_bytes": free,
            "commit_limit_bytes": limit, "committed_bytes": committed,
            "constraint_domains": (("windows_parent_physical", free),
                                   ("windows_parent_commit", limit - committed))}


def _detect_windows_parent_memory():
    # Use the existing five-second command owner; unavailable interop is unknown.
    import time
    if "microsoft" not in _read_text_file("/proc/sys/kernel/osrelease").lower():
        return None
    started = time.monotonic()
    raw = _run_command(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command",
                        _WINDOWS_PARENT_MEMORY_COMMAND])
    return _parse_windows_parent_memory(raw, started=started, finished=time.monotonic())


def _cgroup_interface_state(path):
    # Unlike _read_text_file, ENOENT is distinct from unreadable/unsafe metadata.
    import stat
    try:
        mode = os.lstat(path).st_mode
        return "PRESENT" if stat.S_ISREG(mode) else "UNKNOWN"
    except FileNotFoundError:
        return "ABSENT"
    except OSError:
        return "UNKNOWN"


def _cgroup_v2_topology(*, process_pid=None):
    """Prove a full hierarchy view, not merely a namespace-visible '/' path."""
    if process_pid is not None and (type(process_pid) is not int or process_pid <= 0):
        return {"status": "UNKNOWN", "mountinfo": ""}
    proc = "/proc/self" if process_pid is None else f"/proc/{process_pid}"
    access_prefix = "" if process_pid is None else proc + "/root"
    raw = _read_text_file(proc + "/mountinfo")
    proof = {"status": "UNKNOWN", "mountinfo": raw}
    if process_pid is not None:
        proof["process_pid"] = process_pid
    try:
        proof["cgroup_namespace"] = os.readlink(proc + "/ns/cgroup")
        proof["mount_namespace"] = os.readlink(proc + "/ns/mnt")
        # Membership paths are relative to the reader's cgroup namespace.
        # A different coordinate namespace cannot be silently treated as self.
        if process_pid is not None and proof["cgroup_namespace"] != os.readlink("/proc/self/ns/cgroup"):
            return proof
    except OSError:
        return proof
    if (not re.fullmatch(r"cgroup:\[[0-9]+\]", proof["cgroup_namespace"])
            or not re.fullmatch(r"mnt:\[[0-9]+\]", proof["mount_namespace"])):
        return proof
    mounts = []
    for line in raw.splitlines():
        fields = line.split()
        try:
            sep = fields.index("-")
            if sep < 6 or len(fields) != sep + 4:
                return proof
            decode = lambda value: re.sub(r"\\(040|011|012|134)",
                                          lambda match: chr(int(match[1], 8)), value)
            mount_root, point = decode(fields[3]), decode(fields[4])
            if "\\" in mount_root or "\\" in point:
                return proof
            mounts.append((mount_root, point, fields[sep + 1], fields[0]))
        except (ValueError, IndexError):
            return proof
    candidates = [m for m in mounts if m[1] == "/sys/fs/cgroup"]
    if len(candidates) != 1:
        return proof
    root, point, filesystem, mount_id = candidates[0]
    proof.update(mount_root=root, mount_point=point, filesystem=filesystem, mount_id=mount_id)
    if (filesystem != "cgroup2" or root != "/"
            or any(m[1].startswith(point + "/") for m in mounts)):
        return proof
    # Kernel CFTYPE_NOT_ON_ROOT tests cgroup_parent(), not namespace root.
    # cgroup.type cannot be removed from a live non-root cgroup.
    inspection_root = access_prefix + point
    if process_pid is not None:
        proof["inspection_root"] = inspection_root
    proof["root_type_state"] = _cgroup_interface_state(inspection_root + "/cgroup.type")
    proof["root_events_state"] = _cgroup_interface_state(inspection_root + "/cgroup.events")
    proof["root_memory_states"] = tuple(_cgroup_interface_state(inspection_root + "/" + name)
                                         for name in ("memory.max", "memory.current"))
    if (proof["root_type_state"] == "ABSENT"
            and proof["root_events_state"] == "ABSENT"
            and proof["root_memory_states"] == ("ABSENT", "ABSENT")
            and "memory" in _read_text_file(inspection_root + "/cgroup.controllers").split()):
        proof["status"] = "TRUE_HIERARCHY_ROOT"
    return proof


def _memory_constraint_domains(available_bytes, *, host_observation=None, provenance=None, process_pid=None):
    """Intersect environment/cgroup budgets; unsupported host scope stays unknown."""
    if type(available_bytes) is not int or available_bytes <= 0:
        return (), False
    if process_pid is not None and (type(process_pid) is not int or process_pid <= 0):
        return (), False
    domains = [("execution_environment", available_bytes)]
    complete = True
    proc = "/proc/self" if process_pid is None else f"/proc/{process_pid}"
    access_prefix = "" if process_pid is None else proc + "/root"
    cgroups = _read_text_file(proc + "/cgroup")
    topology = None
    memory_memberships = 0
    for line in cgroups.splitlines():
        parts = line.split(":", 2)
        if len(parts) != 3 or not parts[0].isascii() or not parts[0].isdigit():
            complete = False; continue
        controllers, relative = parts[1], parts[2]
        if controllers and "memory" not in controllers.split(","):
            continue
        memory_memberships += 1
        if (not relative.startswith("/") or "\x00" in relative
                or any(part in {".", ".."} for part in relative.split("/"))
                or "//" in relative or (relative != "/" and relative.endswith("/"))
                or (not controllers and parts[0] != "0")):
            complete = False; continue
        root = Path(access_prefix + ("/sys/fs/cgroup" if not controllers else "/sys/fs/cgroup/memory"))
        target = root / relative.lstrip("/")
        if not controllers:
            topology = _cgroup_v2_topology(process_pid=process_pid)
            complete = complete and topology["status"] == "TRUE_HIERARCHY_ROOT"
        elif process_pid is not None:
            # Legacy client v1 behavior stays unchanged; provider mount proof
            # is not established by the legacy hard-coded v1 mount assumption.
            complete = False
        limit_name, current_name = (("memory.max", "memory.current") if not controllers
                                    else ("memory.limit_in_bytes", "memory.usage_in_bytes"))
        cursor = target
        while cursor == root or root in cursor.parents:
            if cursor == root and not controllers and topology["status"] == "TRUE_HIERARCHY_ROOT":
                # Only the proven hierarchy root has no resource interfaces.
                break
            limit = _read_text_file(str(cursor / limit_name)).strip()
            current = _read_text_file(str(cursor / current_name)).strip()
            if limit == "max" and (controllers or (current.isascii() and current.isdigit())):
                pass
            elif limit.isascii() and limit.isdigit() and current.isascii() and current.isdigit():
                domains.append((("cgroup:" if process_pid is None else "provider_cgroup:")
                                + str(cursor).removeprefix(access_prefix), max(0, int(limit) - int(current))))
            else:
                complete = False
            if cursor == root:
                break
            cursor = cursor.parent
    if not cgroups or memory_memberships != 1:
        complete = False
    if topology is not None:
        after = _cgroup_v2_topology(process_pid=process_pid)
        stable = after == topology and _read_text_file(proc + "/cgroup") == cgroups
        complete = complete and stable
        if provenance is not None:
            import hashlib
            provenance.update({k: v for k, v in topology.items() if k != "mountinfo"})
            provenance.update(membership=cgroups.strip(), stable=stable,
                              mountinfo_sha256=hashlib.sha256(topology["mountinfo"].encode()).hexdigest(),
                              root_controls=("NOT_APPLICABLE" if stable and topology["status"] == "TRUE_HIERARCHY_ROOT"
                                             else "UNKNOWN"))
    # Simultaneous guest/host/commit constraints are never added.
    kernel = _read_text_file("/proc/sys/kernel/osrelease").lower()
    if not kernel:
        complete = False
    elif "microsoft" in kernel:
        if host_observation is None:
            complete = False
        else:
            domains.extend(host_observation["constraint_domains"])
    return tuple(domains), complete


def detect_model_resource_observation(*, provider_pid=None) -> dict:
    """Targeted fresh physical observations; no logical-node duplication or store."""
    import time
    started = time.monotonic()
    # Avoid dmidecode/capacity projection work on the load path.
    raw = _read_text_file("/proc/meminfo")
    available = _parse_meminfo_value_kb(raw, "MemAvailable") * 1024
    host = _detect_windows_parent_memory()
    cgroup_provenance = {}
    domains, complete = _memory_constraint_domains(available or None, host_observation=host,
                                                    provenance=cgroup_provenance, process_pid=provider_pid)
    primary, _ = _detect_nvidia_gpus()
    secondary, _ = _detect_generic_gpus()
    gpus = _merge_gpu_snapshots(primary, secondary)
    accelerator_values = []
    identities_verified = True
    for gpu in gpus:
        identity = gpu.gpu_uuid or gpu.pci_bus_id
        if not identity:
            identities_verified = False
            continue
        accelerator_values.append((identity, gpu.vram_free_gb * 1024 ** 3))
    try:
        threads = len(os.sched_getaffinity(0 if provider_pid is None else provider_pid))
    except (AttributeError, OSError, ValueError):
        threads = (os.cpu_count() or 0) if provider_pid is None else 0
        if provider_pid is not None:
            complete = False
    return {"observed_monotonic": started, "memory_available_bytes": domains,
            "accelerator_available_bytes": tuple(accelerator_values),
            "physical_identity_verified": identities_verified,
            "cpu_threads": threads, "scope_complete": complete,
            "scope_id": "local_execution_environment" if provider_pid is None else f"provider_process:{provider_pid}",
            "source": ((__name__ + ";windows_parent_cim_v1;local_windows_interop" if host else __name__)
                       + (";cgroup_v2=" + json.dumps(cgroup_provenance, sort_keys=True, separators=(",", ":"))
                          if cgroup_provenance else "")),
            "host_memory_observation": host}


def detect_node_hardware(node_id: CanonicalNodeId) -> NodeHardwareDetectionContract:
    """Detect vendor-neutral hardware profile for a node."""
    cpu_snapshot, cpu_sources = _detect_cpu_snapshot()
    memory_snapshot, memory_sources = _detect_memory_snapshot()
    nvidia_gpus, nvidia_sources = _detect_nvidia_gpus()
    generic_gpus, generic_sources = _detect_generic_gpus()

    merged_gpus = _merge_gpu_snapshots(nvidia_gpus, generic_gpus)
    detection_sources = tuple(
        dict.fromkeys(cpu_sources + memory_sources + nvidia_sources + generic_sources)
    )

    return NodeHardwareDetectionContract(
        node_id=node_id,
        cpu=cpu_snapshot,
        memory=memory_snapshot,
        gpu_count=len(merged_gpus),
        gpus=merged_gpus,
        detection_sources=detection_sources,
    )


def observe_provider_process_identity(endpoint: str, *, check_request, proc_root=None):
    """Read-only endpoint/socket/process association; never management authority."""
    from pathlib import Path
    from shutil import which
    from urllib.parse import urlsplit
    from ipaddress import ip_address
    from uuid import UUID
    from CORE_ROOT.heartbeat_io import _process_start_ticks
    import hashlib
    unknown = {"status": "UNKNOWN", "reason": "provider_process_identity_unproven"}
    try:
        check_request()
        url = urlsplit(endpoint)
        address = ip_address(url.hostname or "")
        port = url.port if url.port is not None else (80 if url.scheme == "http" else 443)
        if (url.scheme != "http" or not address.is_loopback or url.username or url.password
                or url.query or url.fragment or url.path not in ("", "/") or not 1 <= port <= 65535):
            return {**unknown, "reason": "unsupported_direct_local_endpoint"}
        # A proxy path cannot be associated with a local listener by assumption.
        if any(os.environ.get(name) for name in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY",
                                                 "http_proxy", "https_proxy", "all_proxy")):
            return {**unknown, "reason": "environment_proxy_binding_unproven"}
        executable = which("ollama")  # Same installed executable discovery as existing transport.
        if not executable:
            return {**unknown, "reason": "provider_executable_unavailable"}
        expected = Path(executable).resolve(strict=True).stat()
        raw = _run_command(["ss", "-H", "-ltnpe", f"sport = :{port}"])
        check_request()
        candidates = []
        for line in raw.splitlines():
            fields = line.split()
            if len(fields) < 5 or fields[0] != "LISTEN":
                return {**unknown, "reason": "listener_metadata_malformed"}
            host, observed_port = fields[3].rsplit(":", 1)
            host = host.strip("[]")
            if host == "*":
                return {**unknown, "reason": "listener_address_ambiguous"}
            observed_address = ip_address(host)
            if int(observed_port) != port:
                return {**unknown, "reason": "listener_port_mismatch"}
            if observed_address != address and not (observed_address.version == address.version and observed_address.is_unspecified):
                continue
            owners = re.findall(r"pid=([0-9]+),fd=([0-9]+)", line)
            inodes = re.findall(r"\bino:([0-9]+)\b", line)
            if len(owners) != 1 or len(inodes) != 1:
                return {**unknown, "reason": "listener_owner_ambiguous_or_inaccessible"}
            candidates.append((int(owners[0][0]), int(owners[0][1]), inodes[0]))
        if len(candidates) != 1:
            return {**unknown, "reason": "listener_not_uniquely_proven"}
        pid, fd, inode = candidates[0]
        if pid <= 0 or int(inode) <= 0:
            return unknown
        root = Path("/proc") if proc_root is None else Path(proc_root)
        process = root / str(pid)
        boot_path = root / "sys/kernel/random/boot_id"
        boot = _read_text_file(str(boot_path)).strip()
        if str(UUID(boot)) != boot:
            return {**unknown, "reason": "kernel_boot_identity_invalid"}
        ticks = _process_start_ticks(process)
        if not isinstance(ticks, str) or not ticks.isascii() or not ticks.isdigit() or int(ticks) <= 0:
            return {**unknown, "reason": "process_start_identity_unavailable"}
        actual = process.joinpath("exe").stat()
        if (actual.st_dev, actual.st_ino) != (expected.st_dev, expected.st_ino):
            return {**unknown, "reason": "listener_executable_identity_mismatch"}
        socket_identity = f"socket:[{inode}]"
        if os.readlink(process / "fd" / str(fd)) != socket_identity:
            return {**unknown, "reason": "listener_socket_identity_mismatch"}
        namespaces = {name: os.readlink(process / "ns" / name) for name in ("net", "mnt", "cgroup")}
        client_namespaces = {name: os.readlink(root / "self/ns" / name) for name in ("net", "cgroup")}
        if (any(not re.fullmatch(name + r":\[[0-9]+\]", value) for name, value in namespaces.items())
                or any(namespaces[name] != value for name, value in client_namespaces.items())):
            return {**unknown, "reason": "provider_namespace_coordinates_unproven"}
        cgroup = _read_text_file(str(process / "cgroup"))
        mountinfo = _read_text_file(str(process / "mountinfo"))
        if not cgroup or not mountinfo:
            return {**unknown, "reason": "provider_scope_metadata_unavailable"}
        if (_process_start_ticks(process) != ticks
                or _read_text_file(str(boot_path)).strip() != boot
                or os.readlink(process / "fd" / str(fd)) != socket_identity):
            return {**unknown, "reason": "provider_identity_changed_during_read"}
        identity = {"endpoint": endpoint, "boot_id": boot, "pid": pid,
                    "process_start_ticks": ticks, "socket_inode": inode, "socket_fd": fd,
                    "executable_identity": (actual.st_dev, actual.st_ino),
                    "namespaces": namespaces, "client_coordinate_namespaces": client_namespaces,
                    "cgroup_membership": cgroup.strip(), "mountinfo_sha256": hashlib.sha256(mountinfo.encode()).hexdigest()}
        instance = hashlib.sha256(json.dumps(identity, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        check_request()
        return {"status": "PROVEN", "provider_instance_id": "linux_listener:" + instance,
                "identity": identity, "management_authority": "NONE"}
    except (OSError, ValueError, IndexError, TypeError):
        return unknown
