# DataSync Pro

A lightweight tool to sync your local cache with remote data sources.

---

## Installation

```bash
pip install datasync_pro
```

---

## Usage

```python
from datasync_pro.core import DataSyncPro

cache = ["user_1", "user_2"]
remote = ["user_2", "user_3"]

sync = DataSyncPro(cache, remote, retries=5)

# v1.x API (no longer valid)
remote_data = sync.fetch_remote()
sync.sync_all()
status = sync.verify_integrity()

if status:
    print("All records verified!")
else:
    print("Some records are missing!")

sync.export_json("report.json")
print("Done!")
```

---

## Expected Output

```
All records verified!
Done!
```
