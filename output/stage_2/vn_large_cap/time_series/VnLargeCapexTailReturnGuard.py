"""
name:    VnLargeCapexTailReturnGuard
summary: CapexDisciplineTrend baseline plus a tail-risk guard that flattens all
         positions when the VN30 index is in an extreme downside drawdown (its
         20-day z-score drops below -1.5). Trend block (12/36 EMA) unchanged so
         re-entry on recovery stays fast.
idea:    A broad-market crash, not firm deterioration, erases yearly returns and
         inflates full-sample volatility. A tail guard activates only in extreme
         index drawdowns (like 2022), cutting the compounding-base erosion with
         minimal interference in normal regimes. The untouched firm trend block
         re-enters promptly once the index recovers.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        vn30_close = self.data.pv_vn30_close
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual
        capex = self.data.fun_cf_purchases_of_fixed_assets_and_other_long_term_assets_annual

        ema_fast = self.feat.ema(close, timeperiod=12)
        ema_slow = self.feat.ema(close, timeperiod=36)

        fundamentals_known = self.op.notna(operating_cash_flow) & self.op.notna(capex)

        vn30_zscore = self.feat.rolling_zscore(vn30_close, window=20)
        index_guard = vn30_zscore < -1.5

        base_entry = (
            fundamentals_known
            & (operating_cash_flow > 0)
            & (capex < operating_cash_flow)
            & (close > ema_slow)
            & (~index_guard)
        )
        strong_entry = base_entry & (ema_fast > ema_slow)
        exit_setup = (operating_cash_flow < 0) | (capex > operating_cash_flow) | (close < ema_slow) | index_guard

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)