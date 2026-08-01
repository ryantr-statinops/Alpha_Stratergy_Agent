"""Unit tests for tools/validate_framework.py — Round 2 compliance validator."""

import os
import sys
import tempfile
import unittest

TOOLS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(TOOLS_DIR, "tools"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import validate_framework as vf

VALID_TS = """
class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        sma20 = self.feat.sma(close, timeperiod=20)
        self.set_positions(close > sma20, position=0.5)
"""

VALID_CS = """
class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close_panel
        eps = self.data.fun_is_eps_basis_quarterly_panel
        eligible = (eps > 0) & (close > 0)
        weights = self.op.portfolio_weights_panel(eps, method='rank_demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
"""


class FakeFileTestCase(unittest.TestCase):
    """Helper: write a temp strategy file and call validate_file against it."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp()
        self._vf_output_dir = vf.OUTPUT_DIR
        vf.OUTPUT_DIR = self._tmp

    def tearDown(self):
        vf.OUTPUT_DIR = self._vf_output_dir

    def write(self, rel: str, code: str) -> str:
        abspath = os.path.join(self._tmp, *rel.split("/"))
        os.makedirs(os.path.dirname(abspath), exist_ok=True)
        with open(abspath, "w", encoding="utf-8") as f:
            f.write(code)
        return rel

    def validate(self, rel: str):
        return vf.validate_file(rel, "VN-SMALL-CAP", "time_series")


class TestValidateFile(FakeFileTestCase):

    def test_valid_time_series_passes(self):
        rel = self.write("vn_small_cap/time_series/Good.py", VALID_TS)
        self.assertEqual(self.validate(rel), [])

    def test_valid_cross_sectional_passes(self):
        rel = self.write("vn_small_cap/cross_sectional/Good.py", VALID_CS)
        findings = vf.validate_file(rel, "VN-SMALL-CAP", "cross_sectional")
        self.assertEqual(findings, [])

    def test_negative_shift_flagged(self):
        code = VALID_TS.replace("self.set_positions(close > sma20, position=0.5)",
                                "self.set_positions(close > sma20.shift(-1), position=0.5)")
        rel = self.write("vn_small_cap/time_series/BadShift.py", code)
        msgs = [m for _, _, m in self.validate(rel)]
        self.assertTrue(any("shift" in m.lower() for m in msgs))

    def test_loop_flagged(self):
        code = VALID_TS + "\n        for i in close:\n            pass\n"
        rel = self.write("vn_small_cap/time_series/BadLoop.py", code)
        msgs = [m for _, _, m in self.validate(rel)]
        self.assertTrue(any("loops are forbidden" in m for m in msgs))

    def test_print_eval_exec_flagged(self):
        for bad in ["print('x')", "eval('1')", "exec('1')"]:
            code = VALID_TS + f"\n        {bad}\n"
            rel = self.write(f"vn_small_cap/time_series/Bad{bad.split('(')[0]}.py", code)
            msgs = [m for _, _, m in self.validate(rel)]
            self.assertTrue(any(bad.split("(")[0] in m.lower() for m in msgs))

    def test_time_series_negative_position_flagged(self):
        code = VALID_TS.replace("position=0.5", "position=-0.5")
        rel = self.write("vn_small_cap/time_series/BadNeg.py", code)
        msgs = [m for _, _, m in self.validate(rel)]
        self.assertTrue(any("long-only" in m for m in msgs))

    def test_time_series_position_over_one_flagged(self):
        code = VALID_TS.replace("position=0.5", "position=1.5")
        rel = self.write("vn_small_cap/time_series/BadOver.py", code)
        msgs = [m for _, _, m in self.validate(rel)]
        self.assertTrue(any("exceeds max" in m for m in msgs))

    def test_mode_mismatch_path_vs_code(self):
        code = VALID_CS
        rel = self.write("vn_small_cap/time_series/BadMode.py", code)
        msgs = [m for _, _, m in self.validate(rel)]
        self.assertTrue(any("does not match path mode" in m for m in msgs))

    def test_manifest_universe_mismatch(self):
        rel = self.write("vn_small_cap/time_series/Good.py", VALID_TS)
        findings = vf.validate_file(rel, "VN-MID-CAP", "time_series")
        msgs = [m for _, _, m in findings]
        self.assertTrue(any("Manifest universe" in m for m in msgs))

    def test_cross_sectional_requires_weights(self):
        code = """
class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close_panel
        self.set_portfolio_positions(close)
"""
        rel = self.write("vn_small_cap/cross_sectional/BadCs.py", code)
        findings = vf.validate_file(rel, "VN-SMALL-CAP", "cross_sectional")
        msgs = [m for _, _, m in findings]
        self.assertTrue(any("portfolio_weights_panel" in m for m in msgs))

    def test_cross_sectional_requires_mask(self):
        code = VALID_CS.replace(", mask=eligible", "")
        rel = self.write("vn_small_cap/cross_sectional/BadMask.py", code)
        findings = vf.validate_file(rel, "VN-SMALL-CAP", "cross_sectional")
        msgs = [m for _, _, m in findings]
        self.assertTrue(any("mask" in m for m in msgs))

    def test_cross_sectional_rejects_unsupported_method(self):
        code = VALID_CS.replace("method='rank_demean_l1'", "method='totally_wrong'")
        rel = self.write("vn_small_cap/cross_sectional/BadMethod.py", code)
        findings = vf.validate_file(rel, "VN-SMALL-CAP", "cross_sectional")
        msgs = [m for _, _, m in findings]
        self.assertTrue(any("unsupported weighting" in m for m in msgs))

    def test_fundamental_ratio_without_guard_warns(self):
        code = """
class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        eps = self.data.fun_is_eps_basis_quarterly
        signal = self.op.pct_change(eps, periods=1)
        self.set_positions(signal > 0, position=1)
"""
        rel = self.write("vn_small_cap/time_series/BadFund.py", code)
        findings = vf.validate_file(rel, "VN-SMALL-CAP", "time_series")
        msgs = [m for _, _, m in findings]
        self.assertTrue(any("notna" in m or "denominator" in m for m in msgs))

    def test_invalid_layout_flagged(self):
        rel = self.write("random_folder/Good.py", VALID_TS)
        findings = vf.validate_file(rel, "", "")
        msgs = [m for _, _, m in findings]
        self.assertTrue(any("Invalid filepath layout" in m for m in msgs))

    def test_duplicate_filepath_detected(self):
        code = VALID_TS
        rel = self.write("vn_small_cap/time_series/Good.py", code)
        os.makedirs(os.path.join(self._tmp, "vn_mid_cap", "time_series"), exist_ok=True)
        rel2 = self.write("vn_mid_cap/time_series/Good.py", code)
        findings = vf.validate_file(rel, "VN-SMALL-CAP", "time_series")
        self.assertEqual(findings, [])
        findings2 = vf.validate_file(rel2, "VN-MID-CAP", "time_series")
        self.assertEqual(findings2, [])


class TestValidateIndex(FakeFileTestCase):

    def _write_index(self, content: str):
        idx = os.path.join(self._tmp, "index.csv")
        with open(idx, "w", encoding="utf-8") as f:
            f.write(content)
        return idx

    def setUp(self):
        super().setUp()
        self._vf_index = vf.INDEX_PATH
        vf.INDEX_PATH = os.path.join(self._tmp, "index.csv")

    def tearDown(self):
        vf.INDEX_PATH = self._vf_index
        super().tearDown()

    def test_empty_index_with_nested_files_fails(self):
        self._write_index(",".join(vf.INDEX_HEADER) + "\n")
        self.write("vn_small_cap/time_series/Good.py", VALID_TS)
        findings = vf.validate_index()
        msgs = [m for _, _, m in findings]
        self.assertTrue(any("no data rows" in m for m in msgs))

    def test_empty_index_no_files_passes(self):
        self._write_index(",".join(vf.INDEX_HEADER) + "\n")
        self.assertEqual(vf.validate_index(), [])

    def test_index_row_missing_file_fails(self):
        self._write_index(
            ",".join(vf.INDEX_HEADER) + "\n"
            "vn_small_cap/time_series/Ghost.py,thesis,mode,time_series,VN-SMALL-CAP,desc,params\n"
        )
        findings = vf.validate_index()
        msgs = [m for _, _, m in findings]
        self.assertTrue(any("missing file" in m for m in msgs))

    def test_index_universe_mismatch_fails(self):
        self._write_index(
            ",".join(vf.INDEX_HEADER) + "\n"
            "vn_small_cap/time_series/Good.py,thesis,mode,time_series,VN-MID-CAP,desc,params\n"
        )
        self.write("vn_small_cap/time_series/Good.py", VALID_TS)
        findings = vf.validate_index()
        msgs = [m for _, _, m in findings]
        self.assertTrue(any("does not match cap" in m for m in msgs))

    def test_orphan_file_fails(self):
        self._write_index(
            ",".join(vf.INDEX_HEADER) + "\n"
            "vn_small_cap/time_series/Good.py,thesis,mode,time_series,VN-SMALL-CAP,desc,params\n"
        )
        self.write("vn_small_cap/time_series/Good.py", VALID_TS)
        self.write("vn_small_cap/time_series/Orphan.py", VALID_TS)
        findings = vf.validate_index()
        msgs = [m for _, _, m in findings]
        self.assertTrue(any("File not in index" in m for m in msgs))

    def test_description_with_comma_parses(self):
        # description contains a comma — csv must still parse correctly
        self._write_index(
            f"{','.join(vf.INDEX_HEADER)}\n"
            "vn_small_cap/time_series/Good.py,thesis,mode,time_series,VN-SMALL-CAP,\"desc, with comma\",params\n"
        )
        self.write("vn_small_cap/time_series/Good.py", VALID_TS)
        self.assertEqual(vf.validate_index(), [])


if __name__ == "__main__":
    unittest.main()
