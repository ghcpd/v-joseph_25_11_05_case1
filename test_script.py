import os
import json
import asyncio
import tempfile
import pytest
from datasync_pro.core import DataSyncPro, ConnectionError


def run_example():
    async def main():
        cache = ["user_1", "user_2"]
        remote = ["user_2", "user_3"]
        sync = DataSyncPro(cache, remote, retries=2)

        remote_data = await sync.fetch_remote()
        print("Fetched:", remote_data)

        report = await sync.sync_all()
        print("Sync report:", report)

        integrity = await sync.verify_integrity()
        print("Integrity:", integrity)

        tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        try:
            fname = sync.export_json(tmpfile.name)
            print("Exported to:", fname)
        finally:
            tmpfile.close()
            if os.path.exists(tmpfile.name):
                os.remove(tmpfile.name)

    asyncio.run(main())


# pytest tests

def test_fetch_remote_success():
    cache = ["a"]
    remote = ["b"]
    ds = DataSyncPro(cache, remote)
    out = asyncio.run(ds.fetch_remote())
    assert out == ["b"]


def test_fetch_remote_failure():
    cache = []
    remote = "not-a-list"
    ds = DataSyncPro(cache, remote)
    with pytest.raises(ConnectionError):
        asyncio.run(ds.fetch_remote())


def test_sync_and_verify():
    cache = ["one"]
    remote = ["one", "two"]
    ds = DataSyncPro(cache, remote)
    report = asyncio.run(ds.sync_all())
    assert isinstance(report, dict)
    assert report["synced_count"] == 2
    integrity = asyncio.run(ds.verify_integrity())
    assert isinstance(integrity, dict)
    assert integrity["ok"] is True


def test_sync_missing_verify_false():
    cache = ["x"]
    remote = ["x", "y"]
    ds = DataSyncPro(cache, remote)
    integrity = asyncio.run(ds.verify_integrity())
    assert integrity["ok"] is False
    assert integrity["missing"] == ["y"]


def test_export_json_requires_sync(tmp_path):
    import pytest
    cache = ["1"]
    remote = ["1"]
    ds = DataSyncPro(cache, remote)
    with pytest.raises(ValueError):
        ds.export_json(str(tmp_path / "r.json"))


if __name__ == "__main__":
    print("Running usage example")
    run_example()
