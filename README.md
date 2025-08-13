# IP Request Handler

A tiny Python script that simulates network requests from random IPv4 addresses and flags suspicious activity based on a simple rate limit.

## Quick start

Prerequisites: Python 3.8+ (standard library only).

Run:

```powershell
pwsh> python .\main.py
# or
pwsh> py -3 .\main.py
```

Config knobs (edit in `main.py`):
- `Network.request_monitoring_time_window` (seconds, default 60)
- `Network.request_monitoring_threshold` (requests within window, default 10)
- `Network(size=5)` (number of distinct IPs to simulate)
- `runs = 100` and the random sleep control the total activity

What you’ll see:
- Normal progress is silent. When a single IP exceeds the threshold within the time window, a summary is printed and an interactive prompt appears.

## Notes and limitations
- The script is interactive when a suspicious burst is detected (waits for Enter). For headless/CI usage, remove or guard the `input()` call.
- Request timestamps are retained in memory; only recent ones are counted when checking the threshold.

## Ideas for small improvements
- Use a deque per IP and evict old timestamps on insert for O(1) window maintenance.
- Make thresholds and time window configurable via CLI flags (e.g., `argparse`) or environment variables.
- Replace prints with `logging` and add a non-interactive mode to avoid blocking on `input()`.
- Add minimal unit tests for `IPv4.generate()` and `Network.is_suspicious()`.
- Optionally track a temporary blocklist with an expiry to simulate blocking action.

