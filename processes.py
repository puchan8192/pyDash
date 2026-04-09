#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Process information retrieval utilities."""

import subprocess


def get_top_processes(limit=8):
    """Return the top processes sorted by CPU usage.

    Args:
        limit: Maximum number of processes to return. Defaults to 8.

    Returns:
        list[tuple[str, str, str, str]]: A list of
            (pid, cpu, mem, command) tuples.
    """
    output = subprocess.check_output(
        ["ps", "-Ao", "pid,pcpu,pmem,comm", "-r"],
        text=True,
    )
    lines = output.splitlines()[1:limit + 1]
    processes = []
    for line in lines:
        parts = line.split(None, 3)
        if len(parts) == 4:
            pid, cpu, mem, cmd = parts
            processes.append((pid, cpu, mem, cmd))
    return processes
