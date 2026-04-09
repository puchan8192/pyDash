#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Curses-based UI rendering functions for the monitoring dashboard."""

import curses

BLOCKS = "\u2581\u2582\u2583\u2584\u2585\u2586\u2587\u2588"

_COLOR_GREEN = 1
_COLOR_YELLOW = 2
_COLOR_RED = 3
_BAR_WIDTH = 30
_MEM_THRESHOLD_LOW = 50
_MEM_THRESHOLD_HIGH = 80


def draw_bar(stdscr, y, label, percent):
    """Draw a colored usage bar at the specified row.

    Args:
        stdscr: The curses window object.
        y: The row at which to draw the bar.
        label: A short label displayed to the left of the bar.
        percent: The usage value as a percentage (0.0 to 100.0).
    """
    filled = int(_BAR_WIDTH * percent / 100)
    fill_bar = "\u2588" * filled + "\u2591" * (_BAR_WIDTH - filled)

    if percent < _MEM_THRESHOLD_LOW:
        color = _COLOR_GREEN
    elif percent < _MEM_THRESHOLD_HIGH:
        color = _COLOR_YELLOW
    else:
        color = _COLOR_RED

    stdscr.addstr(y, 0, f"{label:<6}")
    stdscr.addstr(y, 8, "[")
    stdscr.addstr(fill_bar, curses.color_pair(color))
    stdscr.addstr("]")
    stdscr.addstr(f" {percent:5.1f}%")


def draw_history(stdscr, y, history, label):
    """Draw a sparkline graph of historical values.

    Args:
        stdscr: The curses window object.
        y: The row at which to draw the label; the graph appears on y+1.
        history: A list of float values (0.0 to 100.0) representing history.
        label: A short label displayed above the graph.
    """
    stdscr.addstr(y, 0, label)
    graph = ""
    num_blocks = len(BLOCKS) - 1
    for value in history:
        index = int(value / 100 * num_blocks)
        index = max(0, min(index, num_blocks))
        graph += BLOCKS[index]
    stdscr.addstr(y + 1, 0, graph)


def draw_process_table(stdscr, y, processes):
    """Draw a table of top processes.

    Args:
        stdscr: The curses window object.
        y: The row at which to start drawing the table.
        processes: A list of (pid, cpu, mem, command) tuples.
    """
    stdscr.addstr(y, 0, "Top Processes")
    stdscr.addstr(y + 1, 0, "PID     CPU%   MEM%   COMMAND")
    row = y + 2
    for pid, cpu, mem, cmd in processes:
        safe_addstr(stdscr, row, 0, f"{pid:<7}{cpu:<7}{mem:<7}{cmd}")
        row += 1


def safe_addstr(stdscr, y, x, text):
    """Write a string to the curses window, clipping to fit within bounds.

    Silently skips rendering if the row is out of bounds.

    Args:
        stdscr: The curses window object.
        y: The row at which to write.
        x: The column at which to start writing.
        text: The string to write.
    """
    height, width = stdscr.getmaxyx()
    if y >= height:
        return
    text = text[: width - x - 1]
    stdscr.addstr(y, x, text)
