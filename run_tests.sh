#!/usr/bin/env bash
set -e
echo 'Running tests (python test_script.py)...'
# Run the test harness; capture stdout/stderr
python test_script.py > test_run.log 2>&1 || true

echo '--- TEST LOG ---' > defects.txt
cat test_run.log >> defects.txt

if [ -f test_results.json ]; then
	echo '\n--- JSON RESULTS ---' >> defects.txt
	cat test_results.json >> defects.txt
fi

echo 'Done. See defects.txt and test_results.json.'
