# DataSync Pro (Corrected Documentation for v2.0)

This document shows the correct usage for `DataSyncPro` v2.0 which exposes async APIs.

Example (async usage):

```python
import asyncio
from datasync_pro.core import DataSyncPro

async def main():
    cache = ["user_1", "user_2"]
    remote = ["user_2", "user_3"]

    # Note: constructor signature changed (remote_source positional), and methods are async
    sync = DataSyncPro(cache, remote, retries=5)

    # Await async methods
    remote_data = await sync.fetch_remote()
    report = await sync.sync_all()
    status = await sync.verify_integrity()

    if status.get('ok'):
        print("All records verified!")
    else:
        print("Some records are missing!", status.get('missing'))

    # Export the last report (sync.export_json is synchronous)
    sync.export_json('report.json')
    print('Done!')

asyncio.run(main())
```

Notes:
- `fetch_remote`, `sync_all`, and `verify_integrity` are async and must be awaited.
- `verify_integrity` returns a dictionary: use `status.get('ok')` to check.
- `export_json` is synchronous and writes the last report to disk.
