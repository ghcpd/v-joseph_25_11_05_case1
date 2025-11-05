DataSync Pro - v2.0

Overview
--------
DataSync Pro synchronizes a local list-like cache with a remote list-like data source. Version 2.0 uses an asynchronous API for remote calls and verification.

Installation (local development)
--------------------------------
This repository includes a local package `datasync_pro`. You can prepare a virtual environment and install the developer dependencies using:

On Unix or Git Bash:

    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

On Windows PowerShell:

    python -m venv venv
    .\venv\Scripts\Activate.ps1; pip install -r requirements.txt

Usage (async, modern API)
-------------------------
Example demonstrating correct usage of the async API and the new return types.

```python
import asyncio
from datasync_pro.core import DataSyncPro, ConnectionError

async def main():
    cache = ["user_1", "user_2"]
    remote = ["user_2", "user_3"]

    sync = DataSyncPro(cache, remote, retries=5, validate_schema=True)

    # fetch_remote is async - await it
    try:
        remote_data = await sync.fetch_remote()
        print("Remote data fetched:", remote_data)
    except ConnectionError as exc:
        print("Remote error:", exc)
        return

    # sync_all is async - it returns a `report` dict and also sets `last_report`
    report = await sync.sync_all()
    print("Sync report:", report)

    # verify_integrity is async - it returns a dict (not a bool)
    integrity = await sync.verify_integrity()
    print("Integrity check:", integrity)
    if integrity.get("ok"):
        print("All records verified!")
    else:
        print("Missing records:", integrity.get("missing"))

    # export_json requires a last_report
    try:
        exported = sync.export_json("report.json")
        print("Report exported to:", exported)
    except ValueError as exc:
        print("Export failed:", exc)

if __name__ == "__main__":
    asyncio.run(main())
```

Expected behavior
-----------------
- `fetch_remote()` must be awaited, and will raise `ConnectionError` if the remote source is not a list.
- `sync_all()` returns a report dict and updates the `last_report` attribute.
- `verify_integrity()` returns a dict with the keys `ok` (bool) and `missing` (list), so check the `ok` value rather than the dict itself.
- `export_json()` will throw a `ValueError` if called before `sync_all()` has run and produced a report.

Notes
-----
- The README in this repository previously contained synchronous examples compatible with v1.x. Those examples are outdated for v2.0, which uses asyncio. This documentation corrects example usage and shows the new return types.
