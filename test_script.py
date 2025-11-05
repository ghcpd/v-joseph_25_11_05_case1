import asyncio
import traceback
import json
from datasync_pro.core import DataSyncPro


async def run_examples():
    results = {
        'example_runs': [],
        'errors': []
    }

    # Example derived from README (v1) - we'll attempt the old way first
    cache = ["user_1", "user_2"]
    remote = ["user_2", "user_3"]

    try:
        sync = DataSyncPro(cache, remote, retries=5)

        # Attempt old usage (sync.fetch_remote() synchronous call)
        try:
            remote_data = sync.fetch_remote()
            # If it's a coroutine, note that it must be awaited
            if asyncio.iscoroutine(remote_data):
                results['example_runs'].append(('fetch_remote_sync', 'returned_coroutine', None))
            else:
                results['example_runs'].append(('fetch_remote_sync', 'unexpected_success', remote_data))
        except Exception as e:
            results['example_runs'].append(('fetch_remote_sync', 'failed_as_expected', str(type(e)) + ': ' + str(e)))

        # Correct modern usage: await async methods
        try:
            remote_data = await sync.fetch_remote()
            report = await sync.sync_all()
            status = await sync.verify_integrity()
            export_file = sync.export_json('report.json')
            results['example_runs'].append(('modern_flow', 'success', {
                'remote_data': remote_data,
                'report': report,
                'status': status,
                'export_file': export_file
            }))
        except Exception as e:
            tb = traceback.format_exc()
            results['errors'].append({'step': 'modern_flow', 'error': str(e), 'traceback': tb})

    except Exception as e:
        tb = traceback.format_exc()
        results['errors'].append({'step': 'init', 'error': str(e), 'traceback': tb})

    # Save results
    with open('test_results.json', 'w', encoding='utf-8') as fh:
        json.dump(results, fh, indent=2)

    # Also print summary
    print('Test summary:')
    for run in results['example_runs']:
        print(run)
    if results['errors']:
        print('\nErrors:')
        for err in results['errors']:
            print(err['step'], err['error'])


if __name__ == '__main__':
    asyncio.run(run_examples())

