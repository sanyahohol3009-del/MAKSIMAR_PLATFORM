from __future__ import annotations

import math
import os
import platform
import re
import shutil
import subprocess
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
            "--query-gpu=index,name,memory.total,memory.free",
            "--format=csv,noheader,nounits",
        ]
    )
    if not output:
        return (), ()

    gpus: list[DetectedGpuSnapshot] = []
    for line in output.splitlines():
        parts = [part.strip() for part in line.split(",")]
        if len(parts) != 4:
            continue

        try:
            gpu_index = int(parts[0])
            vram_total = max(int(parts[2]) // 1024, 0)
            vram_free = max(int(parts[3]) // 1024, 0)
        except ValueError:
            continue

        gpus.append(
            DetectedGpuSnapshot(
                gpu_index=gpu_index,
                gpu_vendor="NVIDIA",
                gpu_model=parts[1],
                accelerator_class="discrete_gpu",
                vram_total_gb=vram_total,
                vram_free_gb=vram_free,
                shared_memory_mode=False,
                gpu_capabilities=("graphics", "compute", "cuda"),
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
            )
        )

    return tuple(detected), ("lspci",)


def _merge_gpu_snapshots(
    primary: Iterable[DetectedGpuSnapshot],
    secondary: Iterable[DetectedGpuSnapshot],
) -> tuple[DetectedGpuSnapshot, ...]:
    """Merge GPU snapshots while avoiding obvious duplicates."""
    merged: list[DetectedGpuSnapshot] = []
    seen: set[tuple[str, str]] = set()

    for gpu in list(primary) + list(secondary):
        key = (gpu.gpu_vendor, gpu.gpu_model)
        if key in seen:
            continue
        seen.add(key)
        merged.append(gpu)

    for index, gpu in enumerate(merged):
        merged[index] = DetectedGpuSnapshot(
            gpu_index=index,
            gpu_vendor=gpu.gpu_vendor,
            gpu_model=gpu.gpu_model,
            accelerator_class=gpu.accelerator_class,
            vram_total_gb=gpu.vram_total_gb,
            vram_free_gb=gpu.vram_free_gb,
            shared_memory_mode=gpu.shared_memory_mode,
            gpu_capabilities=gpu.gpu_capabilities,
        )

    return tuple(merged)


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
