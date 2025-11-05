# DataSync Pro — Corrected Usage (v2.0)

This document replaces the original README usage examples with code compatible with DataSync Pro v2.0.

## Installation

This repository is provided as local source code. To set up a development environment, run the included `setup.sh` or use the venv of your choice.

```bash
# create a virtual environment and install test dependencies
./setup.sh
```

## Usage (async-safe)

DataSync Pro v2.0 exposes async methods; call them using `asyncio.run()` or within an async runtime.

```python
import asyncio
from datasync_pro.core import DataSyncPro

cache = ["user_1", "user_2"]
remote = ["user_2", "user_3"]

sync = DataSyncPro(cache, remote, retries=5)

# fetch remote data (optional)
remote_data = asyncio.run(sync.fetch_remote())
print("Remote data:", remote_data)

# run sync and collect a report
report = asyncio.run(sync.sync_all())
print("Sync report:", report)

# verify integrity — the method now returns a dict with an `ok` boolean
status = asyncio.run(sync.verify_integrity())
if status.get("ok"):
    print("All records verified!")
else:
    print("Some records are missing! Missing:", status.get("missing"))

# export the report to a JSON file (requires that sync_all() has been executed previously)
sync.export_json("report.json")
print("Done!")
```

## Expected Output

```
Remote data: ['user_2', 'user_3']
Sync report: {'synced_count': 3, 'timestamp': '2025-11-05T...', 'validated': True}
All records verified!
Done!
```

Notes:
- `fetch_remote`, `sync_all`, and `verify_integrity` are now async — use `asyncio.run()` or an async runner
- `verify_integrity` returns a dictionary with `ok` (boolean) and `missing` (list) entries
- `export_json` requires a previously generated internal report (call `sync_all()` first)
