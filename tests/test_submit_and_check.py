"""Unit tests for tools/submit_and_check.py — filtering, dry-run, HTTP workflow (mocked)."""

import os
import sys
import tempfile
import unittest
import csv
from unittest import mock

TOOLS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(TOOLS_DIR, "tools"))
import submit_and_check as sub

# Avoid hitting the network / requiring .env at import time
sub.session = mock.MagicMock()

CODE = """
class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        self.set_positions(close > 0, position=1)
"""


def make_tree():
    tmp = tempfile.mkdtemp()
    base = os.path.join(tmp, "output", "stage_2")
    files = {
        "vn_small_cap/time_series/A.py": CODE,
        "vn_small_cap/cross_sectional/B.py": CODE,
        "vn_mid_cap/time_series/C.py": CODE,
        "vn_large_cap/cross_sectional/D.py": CODE,
    }
    for rel, content in files.items():
        abspath = os.path.join(base, *rel.split("/"))
        os.makedirs(os.path.dirname(abspath), exist_ok=True)
        with open(abspath, "w", encoding="utf-8") as f:
            f.write(content)
    index = os.path.join(tmp, "output", "index.csv")
    header = "filepath,thesis_group,template,mode,universe,description,params"
    rows = []
    for rel in files:
        cap, mode, fname = rel.split("/")
        u = {"vn_small_cap": "VN-SMALL-CAP", "vn_mid_cap": "VN-MID-CAP", "vn_large_cap": "VN-LARGE-CAP"}[cap]
        rows.append(f"{rel},tg,tpl,{mode},{u},desc,params")
    with open(index, "w", encoding="utf-8") as f:
        f.write(header + "\n" + "\n".join(rows) + "\n")
    return tmp


class TestPathInference(unittest.TestCase):

    def test_infer_universe(self):
        cases = [
            (r"output\stage_2\vn_small_cap\time_series\A.py", "VN-SMALL-CAP"),
            ("output/stage_2/vn_mid_cap/time_series/C.py", "VN-MID-CAP"),
            ("output/stage_2/vn_large_cap/cross_sectional/D.py", "VN-LARGE-CAP"),
            ("/somewhere/else.py", ""),
        ]
        for path, expected in cases:
            self.assertEqual(sub.infer_universe_from_path(path), expected)

    def test_resolve_universe_ignores_explicit(self):
        # explicit --universe is a FILTER, never overrides the cap-derived value
        f = "output/stage_2/vn_small_cap/time_series/A.py"
        self.assertEqual(sub.resolve_universe(f, "VN-MID-CAP"), "VN-SMALL-CAP")


class TestFilterByUniverse(unittest.TestCase):

    def test_filter_small_cap(self):
        tmp = make_tree()
        files = [os.path.join(tmp, "output", "stage_2", "vn_small_cap", "time_series", "A.py"),
                 os.path.join(tmp, "output", "stage_2", "vn_mid_cap", "time_series", "C.py")]
        matching, skipped = sub.filter_files_by_universe(files, "VN-SMALL-CAP")
        self.assertEqual(len(matching), 1)
        self.assertIn("A.py", matching[0])
        self.assertEqual(len(skipped), 1)

    def test_invalid_universe_returns_empty(self):
        tmp = make_tree()
        files = [os.path.join(tmp, "output", "stage_2", "vn_small_cap", "time_series", "A.py")]
        matching, skipped = sub.filter_files_by_universe(files, "VN-NOPE")
        self.assertEqual(matching, [])
        self.assertEqual(skipped, files)


class TestDiscoverBatchFiles(unittest.TestCase):

    def test_discover_uses_manifest_not_raw_walk(self):
        tmp = make_tree()
        base = os.path.join(tmp, "output", "stage_2")
        # add an orphan file NOT in the manifest
        orphan = os.path.join(base, "vn_small_cap", "time_series", "Orphan.py")
        os.makedirs(os.path.dirname(orphan), exist_ok=True)
        with open(orphan, "w", encoding="utf-8") as f:
            f.write(CODE)

        with mock.patch.object(sub, "BASE_DIR", tmp):
            files = sub.discover_batch_files()
        names = [os.path.basename(f) for f in files]
        self.assertEqual(len(files), 4)
        self.assertNotIn("Orphan.py", names)


class TestRunBatchMode(unittest.TestCase):

    def _args(self, **kw):
        defaults = dict(batch=True, test=False, start=1, limit=None, files=None,
                        universe="", dry_run=True, yes=False, force=False)
        defaults.update(kw)
        return mock.Mock(**defaults)

    def test_dry_run_no_http(self):
        tmp = make_tree()
        with mock.patch.object(sub, "BASE_DIR", tmp), \
             mock.patch.object(sub, "discover_batch_files") as mdisc:
            mdisc.return_value = [os.path.join(tmp, "output", "stage_2", "vn_small_cap", "time_series", "A.py")]
            with mock.patch.object(sub, "run_http_sequence") as mrun:
                rc = sub.run_batch_mode(self._args(dry_run=True, universe="VN-SMALL-CAP"))
                self.assertEqual(rc, 0)
                mrun.assert_not_called()

    def test_multi_universe_without_flag_rejected(self):
        tmp = make_tree()
        with mock.patch.object(sub, "BASE_DIR", tmp):
            rc = sub.run_batch_mode(self._args(dry_run=True, universe=""))
            self.assertEqual(rc, 1)

    def test_invalid_universe_rejected(self):
        tmp = make_tree()
        with mock.patch.object(sub, "BASE_DIR", tmp):
            rc = sub.run_batch_mode(self._args(dry_run=True, universe="VN-NOPE"))
            self.assertEqual(rc, 1)


class TestHTTPSequence(unittest.TestCase):

    def _resp(self, code):
        r = mock.MagicMock()
        r.status_code = code
        r.text = "body"
        return r

    def test_update_failure_skips_verify_simulate(self):
        env = ("editor", "token", "http://base")
        session = mock.MagicMock()
        session.put.return_value = self._resp(500)
        with mock.patch.object(sub, "requests") as mreq:
            mreq.Session.return_value = session
            with mock.patch.object(sub, "save_to_csv") as msave:
                f = tempfile.NamedTemporaryFile("w", suffix=".py", delete=False)
                f.write(CODE); f.close()
                sub.run_http_sequence(env, f.name, "A.py", "VN-SMALL-CAP", 1, 1)
                msave.assert_called_once()
                saved = msave.call_args[0][0]
                self.assertEqual(saved["status"], "UPDATE_FAILED")
                # simulate must not be called after failed update
                session.post.assert_not_called()
                os.unlink(f.name)

    def test_verify_failure_skips_simulate(self):
        env = ("editor", "token", "http://base")
        session = mock.MagicMock()
        session.put.return_value = self._resp(200)
        session.post.return_value = self._resp(400)  # verify fails
        with mock.patch.object(sub, "requests") as mreq:
            mreq.Session.return_value = session
            with mock.patch.object(sub, "save_to_csv") as msave:
                f = tempfile.NamedTemporaryFile("w", suffix=".py", delete=False)
                f.write(CODE); f.close()
                sub.run_http_sequence(env, f.name, "A.py", "VN-SMALL-CAP", 1, 1)
                saved = msave.call_args[0][0]
                self.assertEqual(saved["status"], "VERIFY_FAILED")
                # put (1) + verify (1) — no simulate
                self.assertEqual(session.post.call_count, 1)
                os.unlink(f.name)

    def test_full_success_with_metrics(self):
        env = ("editor", "token", "http://base")
        session = mock.MagicMock()
        session.put.return_value = self._resp(200)
        session.post.return_value = self._resp(200)  # verify + simulate
        with mock.patch.object(sub, "requests") as mreq:
            mreq.Session.return_value = session
            with mock.patch.object(sub, "get_strategy_id", return_value="old-sid"), \
                 mock.patch.object(sub, "wait_for_new_strategy_id", return_value="sid"), \
                 mock.patch.object(sub, "wait_for_metrics",
                                    return_value={
                                        stage: {"sharpe": 1.5, "cagr": 0.3, "calmar": 1.2,
                                                "max_drawdown": -0.2, "profit_factor": 1.6}
                                        for stage in ("simulate", "train", "test")}), \
                 mock.patch.object(sub, "save_to_csv") as msave:
                f = tempfile.NamedTemporaryFile("w", suffix=".py", delete=False)
                f.write(CODE); f.close()
                sub.run_http_sequence(env, f.name, "A.py", "VN-SMALL-CAP", 1, 1)
                saved = msave.call_args[0][0]
                self.assertEqual(saved["status"], "SIMULATED")
                self.assertEqual(saved["strategy_id"], "sid")
                self.assertEqual(saved["train_sharpe"], 1.5)
                self.assertEqual(saved["test_sharpe"], 1.5)
                os.unlink(f.name)

    def test_wait_for_new_strategy_id_returns_changed_id(self):
        session = mock.MagicMock()
        # first /info returns old id, second returns new id
        r1, r2 = mock.MagicMock(), mock.MagicMock()
        r1.status_code = 200; r1.json.return_value = {"data": {"strategy_ids": ["old"]}}
        r2.status_code = 200; r2.json.return_value = {"data": {"strategy_ids": ["new"]}}
        session.get.side_effect = [r1, r2]
        with mock.patch.object(sub, "time") as mtime:
            sid = sub.wait_for_new_strategy_id(session, "http://base", "old", timeout=10)
            self.assertEqual(sid, "new")
            mtime.sleep.assert_called_once()

    def test_wait_for_new_strategy_id_times_out_to_latest(self):
        session = mock.MagicMock()
        r = mock.MagicMock()
        r.status_code = 200; r.json.return_value = {"data": {"strategy_ids": ["old"]}}
        session.get.return_value = r
        with mock.patch.object(sub, "time"):
            sid = sub.wait_for_new_strategy_id(session, "http://base", "old", timeout=5)
            self.assertEqual(sid, "old")


class TestStageMetrics(unittest.TestCase):

    def _response(self, data):
        response = mock.MagicMock()
        response.status_code = 200
        response.json.return_value = {"data": data}
        return response

    def test_wait_fetches_all_three_stage_urls(self):
        metrics = {"sharpe": 1.5, "cagr": 0.3, "calmar": 1.2,
                   "max_drawdown": -0.2, "profit_factor": 1.6}
        session = mock.MagicMock()
        session.get.side_effect = self._summary_or_perf(metrics)
        result = sub.wait_for_metrics(session, "sid", timeout=5)
        self.assertEqual(set(result), {"simulate", "train", "test"})
        urls = [call.args[0] for call in session.get.call_args_list]
        self.assertTrue(any("/stages/simulate/summary-aggregate" in url for url in urls))
        self.assertTrue(any("/stages/train/summary-aggregate" in url for url in urls))
        self.assertTrue(any("/stages/test/summary-aggregate" in url for url in urls))
        self.assertTrue(any("/stages/simulate/performance" in url for url in urls))

    def test_partial_stage_is_polled_again(self):
        full = {"sharpe": 1.5, "cagr": 0.3, "calmar": 1.2,
                "max_drawdown": -0.2, "profit_factor": 1.6}
        partial = dict(full)
        partial.pop("calmar")

        calls = []
        stage_count = {"simulate": 0, "train": 0, "test": 0}
        urls = {
            "simulate": 2, "train": 2, "test": 2,
        }

        def fake_get(url, **kwargs):
            calls.append(url)
            if "/performance" in url:
                return self._response({})
            for stage in ("simulate", "train", "test"):
                if f"/stages/{stage}/summary-aggregate" in url:
                    stage_count[stage] += 1
                    if stage == "train" and stage_count[stage] == 1:
                        return self._response(partial)
                    return self._response(full)
            return self._response({})

        session = mock.MagicMock()
        session.get.side_effect = fake_get
        with mock.patch.object(sub.time, "sleep"):
            result = sub.wait_for_metrics(session, "sid", timeout=10)
        self.assertEqual(result["train"], full)
        # First train summary is partial -> second poll refetches it.
        self.assertEqual(stage_count["train"], 2)
        self.assertEqual(stage_count["simulate"], 1)
        self.assertEqual(stage_count["test"], 1)

    def _summary_or_perf(self, metrics):
        """Return a callable that serves summary-aggregate (full) and performance (empty)."""
        def fake_get(url, **kwargs):
            if "/performance" in url:
                return self._response({})
            if "/summary-aggregate" in url:
                return self._response(metrics)
            return self._response({})
        return fake_get


class TestCsvSchemaMigration(unittest.TestCase):

    def test_old_header_is_atomically_migrated_before_append(self):
        old_fields = [field for field in sub.CSV_FIELDS
                      if not field.startswith("train_") and not field.startswith("test_")]
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "results.csv")
            old_row = {field: "" for field in old_fields}
            old_row.update({"timestamp": "old", "filepath": "a.py", "status": "SIMULATED",
                            "universe": "VN-SMALL-CAP", "sharpe": "1.5"})
            with open(path, "w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=old_fields)
                writer.writeheader()
                writer.writerow(old_row)

            sub.save_to_csv(sub.make_row("b.py", "VN-SMALL-CAP", "METRICS_TIMEOUT"), path)

            with open(path, newline="", encoding="utf-8") as handle:
                reader = csv.DictReader(handle)
                rows = list(reader)
                self.assertEqual(reader.fieldnames, sub.CSV_FIELDS)
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]["filepath"], "a.py")
            self.assertEqual(rows[0]["train_sharpe"], "")
            self.assertEqual(rows[0]["test_sharpe"], "")


if __name__ == "__main__":
    unittest.main()
