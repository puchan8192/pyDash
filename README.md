# macOS Resource Monitor

A lightweight, terminal-based system resource monitoring tool for macOS, built with Python and `curses`.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Platform](https://img.shields.io/badge/Platform-macOS-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)
![Code style](https://img.shields.io/badge/code%20style-PEP8-brightgreen)

## Features

- **CPU usage** — real-time user + system percentage with sparkline history
- **Memory usage** — physical memory pressure via `vm_stat`
- **Disk usage** — root filesystem usage (`/`)
- **Network speed** — live download / upload throughput in B/s, KB/s, or MB/s with sparkline history
- **Top processes** — top 8 processes by CPU usage (PID, CPU%, MEM%, command)
- **Color-coded bars** — green / yellow / red thresholds at 50% and 80%
- **Safe rendering** — terminal-size-aware; content that does not fit is clipped or skipped

## Screenshot

```
CPU    [████████████████░░░░░░░░░░░░░░]  53.2%
CPU History
▃▄▄▅▅▆▅▄▃▄▅▆▇▆▅▄▄▃▄▅

MEM    [████████████████████████░░░░░░]  80.1%
DISK   [████████████░░░░░░░░░░░░░░░░░░]  41.7%
NET ↓ 128.4 KB/s ↑ 12.0 KB/s
NET History
▁▁▂▂▁▁▂▃▂▁▁▂

Top Processes
PID     CPU%   MEM%   COMMAND
1234   25.3   4.1    python3
5678   10.2   2.8    node
...

Press q to quit
```

## Requirements

- macOS (uses `top`, `vm_stat`, `netstat`, `ps`)
- Python 3.10 or later
- No third-party packages required

## Installation

```bash
git clone https://github.com/soma2108/macos-resource-monitor.git
cd macos-resource-monitor
```

No virtual environment or `pip install` is needed — the tool relies only on the Python standard library.

## Usage

```bash
python main.py
```

Press `q` to quit.

## Project Structure

```
.
├── main.py          # Entry point; initialises curses and launches the dashboard
├── monitor.py       # Main loop; collects stats and orchestrates rendering
├── system_status.py # macOS system stat collectors (CPU, memory, disk, network)
├── processes.py     # Top-process retrieval via ps
└── ui.py            # Curses drawing primitives (bars, sparklines, tables)
```

## Code Quality

The codebase is fully compliant with the following tools at their default settings:

| Tool | Status |
|---|---|
| `pylint` | 10.00 / 10 |
| `pycodestyle` | No warnings |
| `pydocstyle` | No warnings |

To verify locally:

```bash
pip install pylint pycodestyle pydocstyle
pylint main.py monitor.py system_status.py processes.py ui.py
pycodestyle main.py monitor.py system_status.py processes.py ui.py
pydocstyle main.py monitor.py system_status.py processes.py ui.py
```

## Limitations

- **macOS only.** The stat collection in `system_status.py` relies on macOS-specific CLI tools (`top -l`, `vm_stat`, `netstat -ib`). Linux and Windows are not supported.
- **Network speed on first run** will show `0 B/s` for one second while the baseline byte count is established.
- **Terminal size** — a minimum height of roughly 25 rows is recommended for all sections to be visible simultaneously.

## License

MIT License. See [LICENSE](LICENSE) for details.