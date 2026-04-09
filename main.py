#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Entry point for the terminal resource monitoring tool."""

import curses

from monitor import dashboard


def main(stdscr):
    """Initialize curses settings and launch the dashboard.

    Args:
        stdscr: The curses window object provided by curses.wrapper.
    """
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    dashboard(stdscr)


if __name__ == "__main__":
    curses.wrapper(main)
