# DataSync Pro (v2.0)

An asynchronous library for synchronizing local and remote datasets.

---

## Installation

```bash
pip install datasync_pro
```

---

## Usage

```python
import asyncio
from datasync_pro.core import DataSyncPro

async def main():
    cache = ["user_1", "user_2"]
    remote = ["user_2", "user_3"]

    sync = DataSyncPro(cache, remote, retries=5, validate_schema=True)

    # v2.0: all methods are now async
    await sync.fetch_remote()
    report = await sync.sync_all()

    result = await sync.verify_integrity()
    if result["ok"]:
        print("All records verified!")
    else:
        print(f"Missing records: {result['missing']}")

    sync.export_json("report.json")
    print("Done!")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Expected Output

```
All records verified!
Done!
```
