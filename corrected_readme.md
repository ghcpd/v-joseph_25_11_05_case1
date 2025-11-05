# DataSync Pro

A lightweight asynchronous tool to sync your local cache with remote data sources.

---

## Installation

```bash
pip install datasync_pro
```

---

## Quick Start

```python
import asyncio
from datasync_pro.core import DataSyncPro

async def main():
    cache = ["user_1", "user_2"]
    remote = ["user_2", "user_3"]
    
    sync = DataSyncPro(cache, remote, retries=5)
    
    # Fetch remote data asynchronously
    remote_data = await sync.fetch_remote()
    print(f"Remote data: {remote_data}")
    
    # Sync all records
    report = await sync.sync_all()
    print(f"Sync report: {report}")
    
    # Verify integrity
    verification = await sync.verify_integrity()
    
    if verification["ok"]:
        print("All records verified!")
    else:
        print(f"Some records are missing: {verification['missing']}")
    
    # Export report to JSON
    sync.export_json("report.json")
    print("Done!")

# Run the async main function
asyncio.run(main())
```

---

## Expected Output

```
Remote data: ['user_1', 'user_2', 'user_3']
Sync report: {'synced_count': 3, 'timestamp': '2025-11-05T12:34:56.789012', 'validated': True}
All records verified!
Done!
```

---

## API Reference

### DataSyncPro Class

#### Constructor

```python
DataSyncPro(cache, remote_source, *, retries=3, validate_schema=True)
```

**Parameters:**
- `cache` (list): Local cache of records
- `remote_source` (list): Remote data source (must be a list)
- `retries` (int, optional): Number of retry attempts. Default: 3
- `validate_schema` (bool, optional): Enable schema validation. Default: True

**Raises:**
- `ConnectionError`: If `remote_source` is not a list

#### Methods

##### `async fetch_remote()`

Fetches data from the remote source asynchronously.

**Returns:** list of remote records

**Raises:** `ConnectionError` if remote source is invalid

**Example:**
```python
remote_data = await sync.fetch_remote()
```

---

##### `async sync_all()`

Synchronizes all records between cache and remote source.

**Returns:** Dictionary with sync report containing:
- `synced_count` (int): Number of records after merge
- `timestamp` (str): UTC ISO format timestamp
- `validated` (bool): Whether schema validation was enabled

**Example:**
```python
report = await sync.sync_all()
print(f"Synced {report['synced_count']} records at {report['timestamp']}")
```

---

##### `async verify_integrity()`

Verifies that all remote records exist in the cache.

**Returns:** Dictionary containing:
- `ok` (bool): True if all remote records are in cache, False otherwise
- `missing` (list): Records in remote source but not in cache
- `checked` (str): UTC ISO format timestamp of check

**Example:**
```python
result = await sync.verify_integrity()
if result["ok"]:
    print("All records verified!")
else:
    print(f"Missing records: {result['missing']}")
```

---

##### `export_json(filename, *, indent=2)`

Exports the last sync report to a JSON file.

**Parameters:**
- `filename` (str): Path to output JSON file
- `indent` (int, optional): JSON indentation. Default: 2

**Returns:** filename of exported report

**Raises:** `ValueError` if no sync report is available (must call `sync_all()` first)

**Example:**
```python
await sync.sync_all()  # Must call before export
sync.export_json("report.json")
```

---

## Advanced Examples

### Error Handling

```python
import asyncio
from datasync_pro.core import DataSyncPro, ConnectionError

async def safe_sync():
    try:
        sync = DataSyncPro(["user_1"], ["user_2"], retries=3)
        
        # Validate connection
        try:
            remote_data = await sync.fetch_remote()
        except ConnectionError as e:
            print(f"Connection failed: {e}")
            return
        
        # Sync records
        report = await sync.sync_all()
        
        # Verify integrity
        result = await sync.verify_integrity()
        if not result["ok"]:
            print(f"Integrity check failed. Missing: {result['missing']}")
            
    except Exception as e:
        print(f"Unexpected error: {e}")

asyncio.run(safe_sync())
```

### Batch Processing

```python
import asyncio
from datasync_pro.core import DataSyncPro

async def batch_sync(cache_list, remote_sources):
    """Sync multiple cache/remote pairs concurrently"""
    tasks = []
    
    for cache, remote in zip(cache_list, remote_sources):
        sync = DataSyncPro(cache, remote)
        tasks.append(sync.sync_all())
    
    # Run all syncs concurrently
    reports = await asyncio.gather(*tasks)
    return reports

async def main():
    caches = [["user_1"], ["user_2"]]
    remotes = [["user_1", "user_2"], ["user_3"]]
    
    results = await batch_sync(caches, remotes)
    for i, report in enumerate(results):
        print(f"Batch {i}: {report['synced_count']} records synced")

asyncio.run(main())
```

---

## Version History

### v2.0 (Current)
- **Major Change**: All methods are now asynchronous (`async/await`)
- `verify_integrity()` now returns dictionary instead of boolean
- Added timestamp tracking for all operations
- Schema validation support
- Retry mechanism with configurable attempts

### v1.x (Deprecated)
- Synchronous blocking API
- `verify_integrity()` returned boolean
- Limited error information

---

## Migration from v1.x to v2.0

If upgrading from DataSync Pro v1.x, follow these steps:

1. **Wrap code in async function**
   ```python
   # v1.x
   sync = DataSyncPro(cache, remote)
   result = sync.verify_integrity()
   
   # v2.0
   async def main():
       sync = DataSyncPro(cache, remote)
       result = await sync.verify_integrity()
   asyncio.run(main())
   ```

2. **Add `await` keyword to all method calls**
   - `sync.fetch_remote()` → `await sync.fetch_remote()`
   - `sync.sync_all()` → `await sync.sync_all()`
   - `sync.verify_integrity()` → `await sync.verify_integrity()`

3. **Update boolean checks to dictionary checks**
   - `if sync.verify_integrity():` → `if (await sync.verify_integrity())["ok"]:`

4. **Handle new exception types**
   - `ConnectionError` for invalid remote sources
   - `ValueError` for operations without sync report

---

## Requirements

- Python 3.7+
- No external dependencies (asyncio is part of Python stdlib)

---

## License

MIT
