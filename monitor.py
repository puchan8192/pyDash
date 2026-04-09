#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Main loop for the resource monitoring dashboard."""

import time

from system_status import (
    get_cpu_usage,
    get_memory_usage,
    get_disk_usage,
    get_network_speed,
    format_speed,
)
from processes import get_top_processes
from ui import draw_bar, draw_history, draw_process_table, safe_addstr

MAX_HISTORY = 40
_QUIT_KEY = ord("q")


def _update_history(history, value):
    """Append a value to the history list and enforce the maximum length.

    Args:
        history: The list storing historical values.
        value: The new value to append.
    """
    history.append(value)
    if len(history) > MAX_HISTORY:
        history.pop(0)


def dashboard(stdscr):
    """Run the main monitoring loop, rendering stats to the terminal.

    Args:
        stdscr: The curses window object used for rendering.
    """
    cpu_history = []
    net_history = []
    stdscr.nodelay(True)

    while True:
        stdscr.clear()
        height, _ = stdscr.getmaxyx()

        cpu = get_cpu_usage()
        mem = get_memory_usage()
        disk = get_disk_usage()
        down, up = get_network_speed()
        processes = get_top_processes()

        _update_history(cpu_history, cpu)

        net_value = min((down + up) / 1024 / 100, 100)
        _update_history(net_history, net_value)

        y = 1
        draw_bar(stdscr, y, "CPU", cpu)
        y += 2
        draw_history(stdscr, y, cpu_history, "CPU History")
        y += 3
        draw_bar(stdscr, y, "MEM", mem)
        y += 2
        draw_bar(stdscr, y, "DISK", disk)
        y += 2
        net_line = f"NET \u2193 {format_speed(down)} \u2191 {format_speed(up)}"
        safe_addstr(stdscr, y, 0, net_line)
        y += 1
        draw_history(stdscr, y, net_history, "NET History")
        y += 3

        if y + 10 < height:
            draw_process_table(stdscr, y, processes)
            y += len(processes) + 3

        safe_addstr(stdscr, height - 1, 0, "Press q to quit")
        stdscr.refresh()

        key = stdscr.getch()
        if key == _QUIT_KEY:
            break

        time.sleep(1)
