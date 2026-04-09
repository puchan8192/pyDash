#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""System resource statistics collection for macOS."""

import re
import shutil
import subprocess
import time

CPU_REGEX = re.compile(r"CPU usage: (\d+\.\d+)% user, (\d+\.\d+)% sys")

_PREV_RX = None
_PREV_TX = None
_PREV_TIME = None


def get_cpu_usage():
    """Return the current CPU usage as a percentage (user + sys).

    Returns:
        float: CPU usage percentage, or 0.0 if it cannot be determined.
    """
    output = subprocess.check_output(["top", "-l", "1", "-n", "0"], text=True)
    for line in output.splitlines():
        if "CPU usage" in line:
            match = CPU_REGEX.search(line)
            if match:
                user = float(match.group(1))
                sys_cpu = float(match.group(2))
                return user + sys_cpu
    return 0.0


def get_memory_usage():
    """Return the current memory usage as a percentage.

    Parses vm_stat output to compute used vs total memory based on page counts.

    Returns:
        float: Memory usage percentage.
    """
    vm_output = subprocess.check_output(["vm_stat"], text=True)
    pages = {}
    page_size = 4096

    for line in vm_output.splitlines():
        if "page size of" in line:
            page_size = int(line.split("page size of")[1].split()[0])
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        val = val.strip().replace(".", "")
        if val.isdigit():
            pages[key] = int(val)

    free = pages.get("Pages free", 0)
    inactive = pages.get("Pages inactive", 0)
    speculative = pages.get("Pages speculative", 0)
    wired = pages.get("Pages wired down", 0)
    active = pages.get("Pages active", 0)

    used = (active + wired) * page_size
    free_mem = (free + inactive + speculative) * page_size
    total = used + free_mem
    return used / total * 100


def get_disk_usage():
    """Return the disk usage of the root filesystem as a percentage.

    Returns:
        float: Disk usage percentage.
    """
    total, used, _ = shutil.disk_usage("/")
    return used / total * 100


def get_network_bytes():
    """Return the cumulative network RX and TX byte counts.

    Parses netstat output, excluding loopback interfaces.

    Returns:
        tuple[int, int]: Total received bytes and total transmitted bytes.
    """
    output = subprocess.check_output(["netstat", "-ib"], text=True)
    rx_total = 0
    tx_total = 0

    for line in output.splitlines()[1:]:
        parts = line.split()
        if len(parts) < 10:
            continue
        interface = parts[0]
        if interface.startswith("lo"):
            continue
        try:
            rx_total += int(parts[6])
            tx_total += int(parts[9])
        except ValueError:
            pass

    return rx_total, tx_total


def get_network_speed():
    """Return the current network download and upload speeds in bytes/sec.

    Uses module-level state to compute the delta between successive calls.
    Returns (0, 0) on the first call.

    Returns:
        tuple[float, float]: Download and upload speeds in bytes per second.
    """
    global _PREV_RX, _PREV_TX, _PREV_TIME  # pylint: disable=global-statement

    rx, tx = get_network_bytes()
    now = time.time()

    if _PREV_RX is None:
        _PREV_RX = rx
        _PREV_TX = tx
        _PREV_TIME = now
        return 0, 0

    elapsed = now - _PREV_TIME
    down = (rx - _PREV_RX) / elapsed
    up = (tx - _PREV_TX) / elapsed

    _PREV_RX = rx
    _PREV_TX = tx
    _PREV_TIME = now

    return down, up


def format_speed(bytes_per_sec):
    """Format a byte-per-second value as a human-readable string.

    Args:
        bytes_per_sec: Network speed in bytes per second.

    Returns:
        str: Human-readable speed string (e.g. "1.2 MB/s").
    """
    if bytes_per_sec < 1024:
        return f"{bytes_per_sec:.0f} B/s"
    if bytes_per_sec < 1024 ** 2:
        return f"{bytes_per_sec / 1024:.1f} KB/s"
    return f"{bytes_per_sec / 1024 ** 2:.1f} MB/s"
