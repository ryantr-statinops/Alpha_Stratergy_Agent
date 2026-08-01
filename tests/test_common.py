"""Unit tests for tools/common.py — result identity, pass logic, fail-closed universe."""

import os
import sys
import tempfile
import unittest

TOOLS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(TOOLS_DIR, "tools"))
import common


def sim_row(filepath, universe, metrics, status="SIMULATED"):
    row = {"status": status, "filepath": filepath, "universe": universe,
           "filename": os.path.basename(filepath)}
    row.update(metrics)
    return row


FULL_METRICS = {"sharpe": 1.5, "cagr": 0.30, "max_drawdown": -0.20,
                "profit_factor": 1.6, "calmar": 1.2}


class TestThresholds(unittest.TestCase):

    def test_known_universe(self):
        self.assertIn("sharpe", common.thresholds_for("VN-SMALL-CAP"))

    def test_unknown_universe_raises(self):
        with self.assertRaises(KeyError):
            common.thresholds_for("VN-NOPE")

    def test_empty_universe_raises(self):
        with self.assertRaises(KeyError):
            common.thresholds_for("")


class TestIsPass(unittest.TestCase):

    def test_full_metrics_simulated_passes(self):
        row = sim_row("vn_small_cap/time_series/A.py", "VN-SMALL-CAP", FULL_METRICS)
        self.assertTrue(common.is_pass(row))

    def test_low_metric_fails(self):
        bad = dict(FULL_METRICS, sharpe=0.5)
        row = sim_row("vn_small_cap/time_series/A.py", "VN-SMALL-CAP", bad)
        self.assertFalse(common.is_pass(row))

    def test_unknown_universe_fails_closed(self):
        row = sim_row("vn_small_cap/time_series/A.py", "VN-BOGUS", FULL_METRICS)
        with self.assertRaises(KeyError):
            common.is_pass(row)

    def test_non_simulated_never_passes(self):
        row = sim_row("vn_small_cap/time_series/A.py", "VN-SMALL-CAP", FULL_METRICS, status="METRICS_TIMEOUT")
        self.assertFalse(common.is_pass(row))

    def test_missing_metric_never_passes(self):
        missing = dict(FULL_METRICS); missing["calmar"] = ""
        row = sim_row("vn_small_cap/time_series/A.py", "VN-SMALL-CAP", missing)
        self.assertFalse(common.is_pass(row))

    def test_empty_status_never_passes(self):
        row = sim_row("vn_small_cap/time_series/A.py", "VN-SMALL-CAP", FULL_METRICS, status="")
        self.assertFalse(common.is_pass(row))


class TestRowKey(unittest.TestCase):

    def test_key_uses_filepath_and_universe(self):
        a = sim_row("vn_small_cap/time_series/A.py", "VN-SMALL-CAP", FULL_METRICS)
        b = sim_row("vn_mid_cap/time_series/A.py", "VN-MID-CAP", FULL_METRICS)
        self.assertNotEqual(common.row_key(a), common.row_key(b))
        self.assertEqual(common.row_key(a), common.row_key(dict(a)))


class TestBuildLatest(unittest.TestCase):

    def test_same_basename_different_cap_no_collision(self):
        rows = [
            sim_row("vn_small_cap/time_series/A.py", "VN-SMALL-CAP", FULL_METRICS),
            sim_row("vn_mid_cap/time_series/A.py", "VN-MID-CAP", FULL_METRICS),
        ]
        latest = common.build_latest(rows)
        self.assertEqual(len(latest), 2)

    def test_latest_wins_for_same_key(self):
        rows = [
            sim_row("vn_small_cap/time_series/A.py", "VN-SMALL-CAP", dict(FULL_METRICS, sharpe=1.0)),
            sim_row("vn_small_cap/time_series/A.py", "VN-SMALL-CAP", dict(FULL_METRICS, sharpe=2.0)),
        ]
        latest = common.build_latest(rows)
        self.assertEqual(len(latest), 1)
        self.assertAlmostEqual(common.getf(latest[common.row_key(rows[0])], "sharpe"), 2.0)


class TestLoadPrevious(unittest.TestCase):

    def test_only_simulated_passing_rows_returned(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "r.csv")
            with open(path, "w", encoding="utf-8") as f:
                f.write("timestamp,filepath,filename,universe,mode,status,strategy_id,cagr,sharpe,calmar,max_drawdown,profit_factor,error\n")
                f.write("t,vn_small_cap/time_series/A.py,A.py,VN-SMALL-CAP,time_series,SIMULATED,s1,0.30,1.50,1.20,-0.20,1.60,\n")
                f.write("t,vn_small_cap/time_series/B.py,B.py,VN-SMALL-CAP,time_series,SIMULATED,s2,0.30,0.50,1.20,-0.20,1.60,\n")
                f.write("t,vn_small_cap/time_series/C.py,C.py,VN-SMALL-CAP,time_series,METRICS_TIMEOUT,,,,\n")
            prev = common.load_previous_results(path)
            self.assertIn(("vn_small_cap/time_series/A.py", "VN-SMALL-CAP"), prev)
            self.assertNotIn(("vn_small_cap/time_series/B.py", "VN-SMALL-CAP"), prev)
            self.assertNotIn(("vn_small_cap/time_series/C.py", "VN-SMALL-CAP"), prev)


class TestStatusLabel(unittest.TestCase):

    def test_labels(self):
        cases = [
            (sim_row("a.py", "VN-SMALL-CAP", FULL_METRICS), "PASS"),
            (sim_row("a.py", "VN-SMALL-CAP", dict(FULL_METRICS, sharpe=0.1)), "FAIL"),
            (sim_row("a.py", "VN-SMALL-CAP", FULL_METRICS, status="METRICS_TIMEOUT"), "PENDING"),
            (sim_row("a.py", "VN-SMALL-CAP", FULL_METRICS, status="VERIFY_FAILED"), "API_ERROR"),
            (sim_row("a.py", "VN-SMALL-CAP", FULL_METRICS, status=""), "INVALID_METADATA"),
        ]
        for row, expected in cases:
            self.assertEqual(common.status_label(row), expected, row)


if __name__ == "__main__":
    unittest.main()
