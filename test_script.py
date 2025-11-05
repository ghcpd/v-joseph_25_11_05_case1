import asyncio
import json
import traceback
from datasync_pro.core import DataSyncPro

print("=== Running corrected README examples for DataSync Pro v2.0 ===")

cache = ["user_1", "user_2"]
remote = ["user_2", "user_3"]

sync = DataSyncPro(cache, remote, retries=5)

def log_exc(e):
    print("ERROR:", e)
    print(traceback.format_exc())

try:
    remote_data = asyncio.run(sync.fetch_remote())
    print("Remote data:", remote_data)

    report = asyncio.run(sync.sync_all())
    print("Sync report:", report)

    status = asyncio.run(sync.verify_integrity())
    print("Verify status:", status)

    if status.get('ok'):
        print("All records verified!")
    else:
        print("Some records are missing! Missing:", status.get('missing'))

    filename = sync.export_json("report.json")
    print("Exported report:", filename)

    # Quick verification of exported JSON
    with open(filename, "r", encoding="utf-8") as f:
        exported = json.load(f)
    print("Exported JSON:", exported)

except Exception as e:
    log_exc(e)
    raise
