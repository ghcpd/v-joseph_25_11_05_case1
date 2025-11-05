# DataSync Pro — Updated Usage (v2.0)

A lightweight tool to sync your local cache with remote data sources (async-first API).

---

## Installation (local development)

If you're working from this repository (development), install the package in editable mode:

```bash
pip install -e .
```

For published installs (PyPI):

```bash
pip install datasync_pro
```

---

## Quick Example (async)

DataSync Pro v2.0 exposes async methods. Use asyncio.run to execute them from synchronous code:

```python
import asyncio
from datasync_pro.core import DataSyncPro

cache = ["user_1", "user_2"]
remote = ["user_2", "user_3"]

sync = DataSyncPro(cache, remote, retries=5)

async def main():
    # fetch_remote is async and can be awaited if you need the data separately
    remote_data = await sync.fetch_remote()

    # perform the sync
    report = await sync.sync_all()

    # verify_integrity returns a dict {"ok": bool, "missing": list, "checked": str}
    status = await sync.verify_integrity()

    if status.get("ok"):
        print("All records verified!")
    else:
        print("Some records are missing:", status.get("missing"))

    # export the latest report
    sync.export_json("report.json")
    print("Done!")

asyncio.run(main())
```

---

## Notes on API changes from v1.x

- Methods that were synchronous in v1 (fetch_remote, sync_all, verify_integrity) are now async. Await them using asyncio.
- verify_integrity returns a dictionary, not a bool. Check the `ok` key for a boolean result.
- export_json remains synchronous and writes the last report created by `sync_all()`.

---

## Testing manually

A provided `test_script.py` contains a single example demonstrating the updated API. Run it with:

```bash
python test_script.py
```

---

## Expected Output

```
All records verified!
Done!
```
