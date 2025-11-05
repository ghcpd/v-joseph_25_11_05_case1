import asyncio
import json
from datetime import datetime

class ConnectionError(Exception):
    pass


class DataSyncPro:
    """
    DataSyncPro v2.0
    Provides asynchronous synchronization between local cache and remote data source.
    """

    def __init__(self, cache, remote_source, *, retries=3, validate_schema=True):
        self.cache = cache
        self.remote_source = remote_source
        self.retries = retries
        self.validate_schema = validate_schema
        self.last_report = None

    async def fetch_remote(self):
        """
        Async method that simulates fetching remote data.
        """
        await asyncio.sleep(0.1)
        if not isinstance(self.remote_source, list):
            raise ConnectionError("Remote source must be a list")
        return self.remote_source

    async def sync_all(self):
        """
        Syncs all records between cache and remote source.
        Returns a report dictionary.
        """
        remote_data = await self.fetch_remote()
        merged = list(set(self.cache + remote_data))
        self.cache[:] = merged
        self.last_report = {
            "synced_count": len(merged),
            "timestamp": datetime.utcnow().isoformat(),
            "validated": self.validate_schema
        }
        return self.last_report

    async def verify_integrity(self):
        """
        Now async (used to be sync). Returns dict, not bool.
        """
        await asyncio.sleep(0.05)
        missing = [item for item in self.remote_source if item not in self.cache]
        return {
            "ok": len(missing) == 0,
            "missing": missing,
            "checked": datetime.utcnow().isoformat()
        }

    def export_json(self, filename, *, indent=2):
        """
        Exports the last report.
        """
        if not self.last_report:
            raise ValueError("No sync report available. Run sync_all() first.")
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.last_report, f, indent=indent)
        return filename
