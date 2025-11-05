"""
DataSync Pro v2.0 - Documentation Verification Test Suite

This script tests all examples from the corrected_readme.md to ensure
they work correctly with the current codebase.
"""

import asyncio
import json
import sys
import os
from pathlib import Path

# Add the workspace root to path for importing datasync_pro
sys.path.insert(0, str(Path(__file__).parent))

from datasync_pro.core import DataSyncPro, ConnectionError


class TestLogger:
    """Simple logger for test results"""
    
    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0
    
    def log(self, test_name, status, message=""):
        """Log test result"""
        result = f"[{status:8s}] {test_name}"
        if message:
            result += f" - {message}"
        print(result)
        self.results.append(result)
        
        if status == "PASS":
            self.passed += 1
        else:
            self.failed += 1
    
    def summary(self):
        """Print summary"""
        print("\n" + "="*80)
        print(f"TEST SUMMARY: {self.passed} PASSED, {self.failed} FAILED")
        print("="*80)
        return self.failed == 0


logger = TestLogger()


# TEST 1: Basic Quick Start Example
async def test_quick_start():
    """Test the Quick Start example from corrected_readme.md"""
    try:
        cache = ["user_1", "user_2"]
        remote = ["user_2", "user_3"]
        
        sync = DataSyncPro(cache, remote, retries=5)
        
        # Fetch remote data asynchronously
        remote_data = await sync.fetch_remote()
        assert isinstance(remote_data, list), "fetch_remote should return list"
        assert remote_data == ["user_2", "user_3"], "Remote data mismatch"
        
        # Sync all records
        report = await sync.sync_all()
        assert isinstance(report, dict), "sync_all should return dict"
        assert "synced_count" in report, "Report missing synced_count"
        assert "timestamp" in report, "Report missing timestamp"
        assert "validated" in report, "Report missing validated flag"
        assert report["synced_count"] == 3, f"Expected 3 synced records, got {report['synced_count']}"
        
        # Verify integrity
        verification = await sync.verify_integrity()
        assert isinstance(verification, dict), "verify_integrity should return dict"
        assert "ok" in verification, "Verification missing 'ok' field"
        assert "missing" in verification, "Verification missing 'missing' field"
        assert "checked" in verification, "Verification missing 'checked' field"
        assert verification["ok"] is True, "All records should be verified"
        assert verification["missing"] == [], "No missing records expected"
        
        logger.log("Quick Start Example", "PASS", "All async/await calls succeeded")
        return True
        
    except Exception as e:
        logger.log("Quick Start Example", "FAIL", f"Error: {e}")
        return False


# TEST 2: export_json() with proper sync
async def test_export_json():
    """Test export_json() after sync_all()"""
    try:
        cache = ["item_1"]
        remote = ["item_1", "item_2"]
        
        sync = DataSyncPro(cache, remote)
        
        # Must call sync_all() first
        await sync.sync_all()
        
        # Export to file
        filename = "test_report.json"
        result_filename = sync.export_json(filename)
        assert result_filename == filename, "Exported filename mismatch"
        
        # Verify file contents
        assert os.path.exists(filename), "Report file not created"
        with open(filename, 'r') as f:
            exported_data = json.load(f)
        
        assert "synced_count" in exported_data, "Exported report missing synced_count"
        
        # Cleanup
        os.remove(filename)
        
        logger.log("export_json() Usage", "PASS", "File export and content valid")
        return True
        
    except Exception as e:
        logger.log("export_json() Usage", "FAIL", f"Error: {e}")
        return False


# TEST 3: verify_integrity() with different data
async def test_verify_integrity_with_missing():
    """Test verify_integrity() when records are missing"""
    try:
        cache = ["user_1"]  # Only user_1 in cache
        remote = ["user_1", "user_2", "user_3"]  # Multiple users in remote
        
        sync = DataSyncPro(cache, remote)
        
        # Verify without sync - should show missing records
        result = await sync.verify_integrity()
        assert result["ok"] is False, "Should detect missing records"
        assert "user_2" in result["missing"], "user_2 should be missing"
        assert "user_3" in result["missing"], "user_3 should be missing"
        
        # Now sync and verify again
        await sync.sync_all()
        result = await sync.verify_integrity()
        assert result["ok"] is True, "All records should be present after sync"
        assert result["missing"] == [], "No records should be missing after sync"
        
        logger.log("verify_integrity() Missing Data", "PASS", "Correctly identifies missing records")
        return True
        
    except Exception as e:
        logger.log("verify_integrity() Missing Data", "FAIL", f"Error: {e}")
        return False


# TEST 4: Error Handling - ConnectionError
async def test_connection_error():
    """Test ConnectionError handling"""
    try:
        # remote_source must be a list
        invalid_remote = "not_a_list"
        sync = DataSyncPro(["item_1"], invalid_remote)
        
        try:
            await sync.fetch_remote()
            logger.log("ConnectionError Handling", "FAIL", "Should raise ConnectionError")
            return False
        except ConnectionError as e:
            logger.log("ConnectionError Handling", "PASS", f"Correctly raised ConnectionError: {e}")
            return True
            
    except Exception as e:
        logger.log("ConnectionError Handling", "FAIL", f"Unexpected error: {e}")
        return False


# TEST 5: Error Handling - ValueError for export before sync
async def test_export_before_sync_error():
    """Test ValueError when exporting before sync"""
    try:
        sync = DataSyncPro(["item_1"], ["item_2"])
        
        try:
            sync.export_json("report.json")  # Should fail - no sync report
            logger.log("ValueError Before Sync", "FAIL", "Should raise ValueError")
            return False
        except ValueError as e:
            logger.log("ValueError Before Sync", "PASS", f"Correctly raised ValueError: {e}")
            return True
            
    except Exception as e:
        logger.log("ValueError Before Sync", "FAIL", f"Unexpected error: {e}")
        return False


# TEST 6: Constructor Parameters - validate_schema
async def test_constructor_parameters():
    """Test constructor with different parameters"""
    try:
        cache = ["item_1"]
        remote = ["item_2"]
        
        # Test with custom retries
        sync1 = DataSyncPro(cache, remote, retries=10)
        assert sync1.retries == 10, "Custom retries not set"
        
        # Test with schema validation disabled
        sync2 = DataSyncPro(cache, remote, validate_schema=False)
        assert sync2.validate_schema is False, "validate_schema not disabled"
        report = await sync2.sync_all()
        assert report["validated"] is False, "Validated flag should be False"
        
        # Test with schema validation enabled
        sync3 = DataSyncPro(cache, remote, validate_schema=True)
        assert sync3.validate_schema is True, "validate_schema not enabled"
        
        logger.log("Constructor Parameters", "PASS", "All parameter configurations work")
        return True
        
    except Exception as e:
        logger.log("Constructor Parameters", "FAIL", f"Error: {e}")
        return False


# TEST 7: Batch Processing (async concurrency)
async def test_batch_processing():
    """Test concurrent batch sync operations"""
    try:
        # Create multiple sync operations
        syncs = []
        for i in range(3):
            cache = [f"user_{i}"]
            remote = [f"user_{i}", f"user_{i}_remote"]
            sync = DataSyncPro(cache, remote)
            syncs.append(sync.sync_all())
        
        # Run all concurrently
        reports = await asyncio.gather(*syncs)
        
        assert len(reports) == 3, "Should have 3 reports"
        for i, report in enumerate(reports):
            assert report["synced_count"] == 2, f"Batch {i} should have 2 records"
            assert "timestamp" in report, f"Batch {i} report missing timestamp"
        
        logger.log("Batch Processing (Concurrency)", "PASS", "All batch operations succeeded")
        return True
        
    except Exception as e:
        logger.log("Batch Processing (Concurrency)", "FAIL", f"Error: {e}")
        return False


# TEST 8: Timestamp Validity
async def test_timestamp_validity():
    """Test that timestamps are in valid ISO format"""
    try:
        import datetime
        
        sync = DataSyncPro(["item_1"], ["item_2"])
        report = await sync.sync_all()
        
        # Try parsing timestamp
        timestamp_str = report["timestamp"]
        # ISO format includes 'T' separator
        assert 'T' in timestamp_str, "Timestamp not in ISO format"
        
        # Verify it can be parsed
        try:
            datetime.datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        except:
            logger.log("Timestamp Validity", "FAIL", f"Invalid timestamp format: {timestamp_str}")
            return False
        
        logger.log("Timestamp Validity", "PASS", "Timestamps are valid ISO format")
        return True
        
    except Exception as e:
        logger.log("Timestamp Validity", "FAIL", f"Error: {e}")
        return False


# TEST 9: Cache Modification After Sync
async def test_cache_modification():
    """Test that cache is properly modified after sync"""
    try:
        cache = ["user_1"]
        remote = ["user_2", "user_3"]
        
        initial_cache = cache.copy()
        sync = DataSyncPro(cache, remote)
        
        await sync.sync_all()
        
        # Cache should be modified (using list concatenation)
        assert len(cache) > len(initial_cache), "Cache not expanded after sync"
        assert "user_1" in cache, "Original cache item missing"
        assert "user_2" in cache, "Remote item not added to cache"
        assert "user_3" in cache, "Remote item not added to cache"
        
        logger.log("Cache Modification", "PASS", "Cache properly updated after sync")
        return True
        
    except Exception as e:
        logger.log("Cache Modification", "FAIL", f"Error: {e}")
        return False


# TEST 10: Repeated Verification
async def test_repeated_verification():
    """Test that verify_integrity() can be called multiple times"""
    try:
        sync = DataSyncPro(["user_1"], ["user_1", "user_2"])
        
        # Call verify multiple times
        result1 = await sync.verify_integrity()
        result2 = await sync.verify_integrity()
        result3 = await sync.verify_integrity()
        
        # All should have same status but different timestamps
        assert result1["ok"] == result2["ok"] == result3["ok"], "Consistency check failed"
        assert result1["missing"] == result2["missing"] == result3["missing"], "Missing items changed"
        
        logger.log("Repeated Verification", "PASS", "Multiple verifications consistent")
        return True
        
    except Exception as e:
        logger.log("Repeated Verification", "FAIL", f"Error: {e}")
        return False


async def run_all_tests():
    """Run all test cases"""
    print("="*80)
    print("DataSync Pro v2.0 - Documentation Verification Test Suite")
    print("="*80)
    print()
    
    tests = [
        ("TEST 1: Basic Quick Start", test_quick_start),
        ("TEST 2: JSON Export", test_export_json),
        ("TEST 3: Integrity with Missing Data", test_verify_integrity_with_missing),
        ("TEST 4: Connection Error", test_connection_error),
        ("TEST 5: Value Error Before Sync", test_export_before_sync_error),
        ("TEST 6: Constructor Parameters", test_constructor_parameters),
        ("TEST 7: Batch Processing", test_batch_processing),
        ("TEST 8: Timestamp Validity", test_timestamp_validity),
        ("TEST 9: Cache Modification", test_cache_modification),
        ("TEST 10: Repeated Verification", test_repeated_verification),
    ]
    
    for test_name, test_func in tests:
        print(f"\nRunning {test_name}...")
        try:
            await test_func()
        except Exception as e:
            logger.log(test_name, "FAIL", f"Unhandled exception: {e}")
    
    print()
    success = logger.summary()
    return 0 if success else 1


if __name__ == "__main__":
    exit_code = asyncio.run(run_all_tests())
    sys.exit(exit_code)
