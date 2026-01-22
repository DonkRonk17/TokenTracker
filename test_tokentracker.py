#!/usr/bin/env python3
"""
Comprehensive Test Suite for TokenTracker v1.0

Tests cover:
- Core functionality (logging, summaries, budget)
- Edge cases (empty input, boundaries)
- Error handling (validation, SQL injection)
- Integration scenarios

Run: python test_tokentracker.py

Author: Atlas (Team Brain)
For: Logan Smith / Metaphy LLC
Date: January 22, 2026
"""

import unittest
import sys
import os
import sqlite3
import tempfile
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import patch

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from tokentracker import TokenTracker


class TestTokenTrackerCore(unittest.TestCase):
    """Test core TokenTracker functionality."""
    
    def setUp(self):
        """Set up test fixtures with isolated database."""
        # Create temp directory for test database
        self.test_dir = tempfile.mkdtemp()
        self.test_db = Path(self.test_dir) / "test_tokens.db"
        self.tracker = TokenTracker(db_path=self.test_db)
    
    def tearDown(self):
        """Clean up test directory."""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_initialization(self):
        """Test TokenTracker initializes correctly with database."""
        self.assertIsNotNone(self.tracker)
        self.assertTrue(self.test_db.exists())
    
    def test_initialization_creates_tables(self):
        """Test database tables are created on initialization."""
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        
        # Check tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        self.assertIn("usage_log", tables)
        self.assertIn("budget", tables)
        self.assertIn("agents", tables)
        
        conn.close()
    
    def test_log_usage_basic(self):
        """Test basic token logging."""
        log_id = self.tracker.log_usage(
            agent="ATLAS",
            model="sonnet-4.5",
            input_tokens=50000,
            output_tokens=15000,
            notes="Test session"
        )
        
        self.assertIsNotNone(log_id)
        self.assertIsInstance(log_id, int)
        self.assertGreater(log_id, 0)
    
    def test_log_usage_cost_calculation(self):
        """Test that cost is calculated correctly."""
        # Log usage and verify cost in database
        self.tracker.log_usage(
            agent="ATLAS",
            model="sonnet-4.5",
            input_tokens=1000000,  # 1M input
            output_tokens=1000000  # 1M output
        )
        
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute("SELECT cost_usd FROM usage_log ORDER BY id DESC LIMIT 1")
        cost = cursor.fetchone()[0]
        conn.close()
        
        # Expected: (1M/1M * $3) + (1M/1M * $15) = $3 + $15 = $18
        self.assertAlmostEqual(cost, 18.0, places=2)
    
    def test_log_usage_with_session_id(self):
        """Test logging with session ID for tracking related entries."""
        session_id = "test_session_123"
        
        self.tracker.log_usage(
            agent="ATLAS",
            model="sonnet-4.5",
            input_tokens=10000,
            output_tokens=5000,
            session_id=session_id,
            notes="First part"
        )
        
        self.tracker.log_usage(
            agent="ATLAS",
            model="sonnet-4.5",
            input_tokens=15000,
            output_tokens=8000,
            session_id=session_id,
            notes="Second part"
        )
        
        # Query by session_id
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM usage_log WHERE session_id = ?", (session_id,))
        count = cursor.fetchone()[0]
        conn.close()
        
        self.assertEqual(count, 2)
    
    def test_get_usage_summary_empty(self):
        """Test usage summary with no data."""
        summary = self.tracker.get_usage_summary("today")
        
        self.assertEqual(summary['sessions'], 0)
        self.assertEqual(summary['total_tokens'], 0)
        self.assertEqual(summary['total_cost'], 0.0)
        self.assertEqual(summary['agents'], [])
        self.assertEqual(summary['models'], [])
    
    def test_get_usage_summary_with_data(self):
        """Test usage summary returns correct aggregated data."""
        # Log some test data
        self.tracker.log_usage("ATLAS", "sonnet-4.5", 10000, 5000)
        self.tracker.log_usage("FORGE", "opus-4.5", 20000, 10000)
        self.tracker.log_usage("ATLAS", "sonnet-4.5", 15000, 8000)
        
        summary = self.tracker.get_usage_summary("today")
        
        self.assertEqual(summary['sessions'], 3)
        self.assertEqual(summary['total_tokens'], 68000)  # 10k+5k + 20k+10k + 15k+8k
        self.assertEqual(len(summary['agents']), 2)  # ATLAS and FORGE
        self.assertEqual(len(summary['models']), 2)  # sonnet-4.5 and opus-4.5
    
    def test_get_budget_status_new_month(self):
        """Test budget status for month with no data."""
        budget = self.tracker.get_budget_status()
        
        self.assertEqual(budget['budget'], 60.0)  # DEFAULT_BUDGET
        self.assertEqual(budget['spent'], 0.0)
        self.assertEqual(budget['remaining'], 60.0)
        self.assertEqual(budget['percent_used'], 0.0)
        self.assertTrue(budget['on_track'])
    
    def test_get_budget_status_after_usage(self):
        """Test budget status updates after logging usage."""
        # Log $5 worth of usage
        # sonnet-4.5: (500k/1M * $3) + (500k/1M * $15) = $1.5 + $7.5 = $9
        self.tracker.log_usage("ATLAS", "sonnet-4.5", 500000, 500000)
        
        budget = self.tracker.get_budget_status()
        
        self.assertEqual(budget['budget'], 60.0)
        self.assertAlmostEqual(budget['spent'], 9.0, places=2)
        self.assertAlmostEqual(budget['remaining'], 51.0, places=2)
        self.assertAlmostEqual(budget['percent_used'], 15.0, places=1)
        self.assertTrue(budget['on_track'])  # Under 80%
    
    def test_set_budget(self):
        """Test setting budget for a month."""
        self.tracker.set_budget("2026-01", 75.0)
        
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute("SELECT budget_usd FROM budget WHERE month = '2026-01'")
        budget = cursor.fetchone()[0]
        conn.close()
        
        self.assertEqual(budget, 75.0)
    
    def test_export_report_json(self):
        """Test JSON report export."""
        self.tracker.log_usage("ATLAS", "sonnet-4.5", 10000, 5000, notes="Test")
        
        report = self.tracker.export_report("today", "json")
        
        self.assertIn('"usage":', report)
        self.assertIn('"budget":', report)
        self.assertIn('"generated_at":', report)
        
        # Should be valid JSON
        import json
        data = json.loads(report)
        self.assertIn('usage', data)
        self.assertIn('budget', data)
    
    def test_export_report_text(self):
        """Test text report export."""
        self.tracker.log_usage("ATLAS", "sonnet-4.5", 10000, 5000, notes="Test")
        
        report = self.tracker.export_report("today", "text")
        
        self.assertIn("TOKEN TRACKER REPORT", report)
        self.assertIn("BUDGET STATUS:", report)
        self.assertIn("USAGE SUMMARY:", report)


class TestTokenTrackerValidation(unittest.TestCase):
    """Test input validation and error handling."""
    
    def setUp(self):
        """Set up test fixtures with isolated database."""
        self.test_dir = tempfile.mkdtemp()
        self.test_db = Path(self.test_dir) / "test_tokens.db"
        self.tracker = TokenTracker(db_path=self.test_db)
    
    def tearDown(self):
        """Clean up test directory."""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_validate_agent_empty(self):
        """Test validation rejects empty agent name."""
        with self.assertRaises(ValueError) as context:
            self.tracker.log_usage("", "sonnet-4.5", 1000, 500)
        
        self.assertIn("empty", str(context.exception).lower())
    
    def test_validate_agent_whitespace(self):
        """Test validation rejects whitespace-only agent name."""
        with self.assertRaises(ValueError) as context:
            self.tracker.log_usage("   ", "sonnet-4.5", 1000, 500)
        
        self.assertIn("empty", str(context.exception).lower())
    
    def test_validate_agent_sql_injection(self):
        """Test validation blocks SQL injection attempts."""
        malicious_names = [
            "ATLAS; DROP TABLE usage_log;--",
            "FORGE /* evil */",
            "DELETE FROM budget",
            "INSERT INTO agents"
        ]
        
        for name in malicious_names:
            with self.assertRaises(ValueError) as context:
                self.tracker.log_usage(name, "sonnet-4.5", 1000, 500)
            self.assertIn("invalid", str(context.exception).lower())
    
    def test_validate_model_empty(self):
        """Test validation rejects empty model name."""
        with self.assertRaises(ValueError) as context:
            self.tracker.log_usage("ATLAS", "", 1000, 500)
        
        self.assertIn("empty", str(context.exception).lower())
    
    def test_validate_tokens_negative_input(self):
        """Test validation rejects negative input tokens."""
        with self.assertRaises(ValueError) as context:
            self.tracker.log_usage("ATLAS", "sonnet-4.5", -1000, 500)
        
        self.assertIn("negative", str(context.exception).lower())
    
    def test_validate_tokens_negative_output(self):
        """Test validation rejects negative output tokens."""
        with self.assertRaises(ValueError) as context:
            self.tracker.log_usage("ATLAS", "sonnet-4.5", 1000, -500)
        
        self.assertIn("negative", str(context.exception).lower())
    
    def test_validate_tokens_excessive(self):
        """Test validation rejects excessive token counts."""
        with self.assertRaises(ValueError) as context:
            self.tracker.log_usage("ATLAS", "sonnet-4.5", 100000000, 500)  # 100M
        
        self.assertIn("maximum", str(context.exception).lower())
    
    def test_validate_month_format_invalid(self):
        """Test validation rejects invalid month format."""
        invalid_months = [
            "January-2026",
            "2026/01",
            "01-2026",
            "26-01",
            "2026-1",  # Single digit month
            "2026-13"  # Invalid month
        ]
        
        for month in invalid_months:
            with self.assertRaises(ValueError):
                self.tracker.set_budget(month, 60.0)
    
    def test_validate_budget_negative(self):
        """Test validation rejects negative budget."""
        with self.assertRaises(ValueError) as context:
            self.tracker.set_budget("2026-01", -50.0)
        
        self.assertIn("negative", str(context.exception).lower())
    
    def test_validate_budget_excessive(self):
        """Test validation rejects excessive budget."""
        with self.assertRaises(ValueError) as context:
            self.tracker.set_budget("2026-01", 500000.0)  # $500k
        
        self.assertIn("limit", str(context.exception).lower())


class TestTokenTrackerEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def setUp(self):
        """Set up test fixtures with isolated database."""
        self.test_dir = tempfile.mkdtemp()
        self.test_db = Path(self.test_dir) / "test_tokens.db"
        self.tracker = TokenTracker(db_path=self.test_db)
    
    def tearDown(self):
        """Clean up test directory."""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_zero_tokens(self):
        """Test logging zero tokens works."""
        log_id = self.tracker.log_usage("ATLAS", "sonnet-4.5", 0, 0)
        self.assertIsNotNone(log_id)
    
    def test_unknown_agent_warning(self):
        """Test unknown agent generates warning but still logs."""
        # Should log but print warning
        log_id = self.tracker.log_usage("UNKNOWN_AGENT", "sonnet-4.5", 1000, 500)
        self.assertIsNotNone(log_id)
    
    def test_unknown_model_warning(self):
        """Test unknown model generates warning but still logs."""
        # Should log but print warning and use default pricing
        log_id = self.tracker.log_usage("ATLAS", "unknown-model", 1000, 500)
        self.assertIsNotNone(log_id)
    
    def test_long_notes_truncation(self):
        """Test very long notes are truncated."""
        long_notes = "x" * 2000  # 2000 characters
        log_id = self.tracker.log_usage("ATLAS", "sonnet-4.5", 1000, 500, notes=long_notes)
        
        # Verify notes were truncated in database
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute("SELECT notes FROM usage_log WHERE id = ?", (log_id,))
        stored_notes = cursor.fetchone()[0]
        conn.close()
        
        self.assertLessEqual(len(stored_notes), 1000)
        self.assertTrue(stored_notes.endswith("..."))
    
    def test_agent_name_normalization(self):
        """Test agent names are normalized to uppercase."""
        self.tracker.log_usage("atlas", "sonnet-4.5", 1000, 500)
        self.tracker.log_usage("Atlas", "sonnet-4.5", 1000, 500)
        self.tracker.log_usage("ATLAS", "sonnet-4.5", 1000, 500)
        
        summary = self.tracker.get_usage_summary("today")
        
        # All should be logged as same agent (ATLAS)
        self.assertEqual(len(summary['agents']), 1)
        self.assertEqual(summary['agents'][0]['agent'], "ATLAS")
        self.assertEqual(summary['agents'][0]['sessions'], 3)
    
    def test_model_name_normalization(self):
        """Test model names are normalized to lowercase."""
        self.tracker.log_usage("ATLAS", "SONNET-4.5", 1000, 500)
        self.tracker.log_usage("ATLAS", "Sonnet-4.5", 1000, 500)
        self.tracker.log_usage("ATLAS", "sonnet-4.5", 1000, 500)
        
        summary = self.tracker.get_usage_summary("today")
        
        # All should be logged as same model (sonnet-4.5)
        self.assertEqual(len(summary['models']), 1)
        self.assertEqual(summary['models'][0]['model'], "sonnet-4.5")
    
    def test_free_tier_models_cost(self):
        """Test free tier models (grok, gemini) have zero cost."""
        self.tracker.log_usage("BOLT", "grok", 1000000, 500000)
        self.tracker.log_usage("GEMINI", "gemini", 1000000, 500000)
        
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(cost_usd) FROM usage_log")
        total_cost = cursor.fetchone()[0]
        conn.close()
        
        self.assertEqual(total_cost, 0.0)
    
    def test_budget_over_threshold_flag(self):
        """Test on_track flag changes when over 80% budget."""
        # Set small budget for easier testing
        self.tracker.set_budget(datetime.now().strftime("%Y-%m"), 10.0)
        
        # Spend $9 (90% of budget)
        # sonnet-4.5: Need to calculate tokens for ~$9
        # (input/1M * $3) + (output/1M * $15) = $9
        # Let's use 1M input ($3) + 400k output ($6) = $9
        self.tracker.log_usage("ATLAS", "sonnet-4.5", 1000000, 400000)
        
        budget = self.tracker.get_budget_status()
        
        self.assertFalse(budget['on_track'])  # Over 80%
    
    def test_different_period_summaries(self):
        """Test different summary periods return appropriate data."""
        self.tracker.log_usage("ATLAS", "sonnet-4.5", 10000, 5000)
        
        # All periods should include today's data
        today = self.tracker.get_usage_summary("today")
        week = self.tracker.get_usage_summary("week")
        month = self.tracker.get_usage_summary("month")
        all_time = self.tracker.get_usage_summary("all")
        
        self.assertEqual(today['sessions'], 1)
        self.assertEqual(week['sessions'], 1)
        self.assertEqual(month['sessions'], 1)
        self.assertEqual(all_time['sessions'], 1)


class TestTokenTrackerCostCalculation(unittest.TestCase):
    """Test cost calculation accuracy for different models."""
    
    def setUp(self):
        """Set up test fixtures with isolated database."""
        self.test_dir = tempfile.mkdtemp()
        self.test_db = Path(self.test_dir) / "test_tokens.db"
        self.tracker = TokenTracker(db_path=self.test_db)
    
    def tearDown(self):
        """Clean up test directory."""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_opus_cost_calculation(self):
        """Test Opus 4.5 cost calculation ($15/$75 per 1M)."""
        cost = self.tracker._calculate_cost("opus-4.5", 1000000, 1000000)
        # (1M/1M * $15) + (1M/1M * $75) = $15 + $75 = $90
        self.assertAlmostEqual(cost, 90.0, places=2)
    
    def test_sonnet_cost_calculation(self):
        """Test Sonnet 4.5 cost calculation ($3/$15 per 1M)."""
        cost = self.tracker._calculate_cost("sonnet-4.5", 1000000, 1000000)
        # (1M/1M * $3) + (1M/1M * $15) = $3 + $15 = $18
        self.assertAlmostEqual(cost, 18.0, places=2)
    
    def test_haiku_cost_calculation(self):
        """Test Haiku 3.5 cost calculation ($0.80/$4 per 1M)."""
        cost = self.tracker._calculate_cost("haiku-3.5", 1000000, 1000000)
        # (1M/1M * $0.80) + (1M/1M * $4) = $0.80 + $4 = $4.80
        self.assertAlmostEqual(cost, 4.80, places=2)
    
    def test_grok_cost_calculation(self):
        """Test Grok cost calculation (free tier)."""
        cost = self.tracker._calculate_cost("grok", 1000000, 1000000)
        self.assertEqual(cost, 0.0)
    
    def test_gemini_cost_calculation(self):
        """Test Gemini cost calculation (extension, free)."""
        cost = self.tracker._calculate_cost("gemini", 1000000, 1000000)
        self.assertEqual(cost, 0.0)
    
    def test_partial_million_tokens(self):
        """Test cost calculation for partial million tokens."""
        # 500k input, 500k output for sonnet-4.5
        cost = self.tracker._calculate_cost("sonnet-4.5", 500000, 500000)
        # (500k/1M * $3) + (500k/1M * $15) = $1.50 + $7.50 = $9.00
        self.assertAlmostEqual(cost, 9.0, places=2)
    
    def test_small_token_counts(self):
        """Test cost calculation for small token counts."""
        # 10k input, 5k output for sonnet-4.5
        cost = self.tracker._calculate_cost("sonnet-4.5", 10000, 5000)
        # (10k/1M * $3) + (5k/1M * $15) = $0.03 + $0.075 = $0.105
        self.assertAlmostEqual(cost, 0.105, places=3)


def run_tests():
    """Run all tests with nice output."""
    print("=" * 70)
    print("TESTING: TokenTracker v1.0")
    print("=" * 70)
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestTokenTrackerCore))
    suite.addTests(loader.loadTestsFromTestCase(TestTokenTrackerValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestTokenTrackerEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestTokenTrackerCostCalculation))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print()
    print("=" * 70)
    print(f"RESULTS: {result.testsRun} tests")
    passed = result.testsRun - len(result.failures) - len(result.errors)
    print(f"[OK] Passed: {passed}")
    if result.failures:
        print(f"[X] Failed: {len(result.failures)}")
    if result.errors:
        print(f"[!] Errors: {len(result.errors)}")
    print("=" * 70)
    
    # Print pass rate
    if result.testsRun > 0:
        pass_rate = (passed / result.testsRun) * 100
        print(f"Pass Rate: {pass_rate:.1f}%")
    
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
