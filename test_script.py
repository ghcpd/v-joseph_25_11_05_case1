import asyncio
import json
from datasync_pro.core import DataSyncPro

print("=== Running corrected README examples (v2.0) ===")

cache = ["user_1", "user_2"]
remote = ["user_2", "user_3"]

sync = DataSyncPro(cache, remote, retries=5)

async def main():
    remote_data = await sync.fetch_remote()
    print("fetched remote:", remote_data)

    report = await sync.sync_all()
    print("sync report:", json.dumps(report))

    status = await sync.verify_integrity()
    print("verify status:", json.dumps(status))

    sync.export_json("report.json")
    print("report exported to report.json")

if __name__ == '__main__':
    asyncio.run(main())
