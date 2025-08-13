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

Config knobs (current defaults in `main.py`):
- `Network.request_monitoring_time_window` (seconds, default 10.0)
- `Network.request_rate_limit` (req/sec, default 2.0)
- `Network.request_monitoring_threshold` (derived = window * rate)
- `max_size` (number of devices, default 1)
- `runs` (iterations, default 100)
- Random inter-request delay: normalvariate scaled (approx mean ~0.1–0.2s)

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

## TODOs (high-level)
- Introduce a protocol-based approach (event handlers)
- Create a handler registry and example runners
- Add automated tests for processing & rate limit logic
- Improve docs with usage examples and contribution guide
- Prepare packaging (pyproject.toml) and CI workflow

