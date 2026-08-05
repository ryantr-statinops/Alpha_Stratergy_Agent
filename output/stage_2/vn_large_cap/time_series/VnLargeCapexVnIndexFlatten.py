"""
name:    VnLargeCapexVnIndexFlatten
summary: CapexDisciplineTrend baseline plus a market-wide crash guard that
         flattens all positions whenever VN30 has turned down over the last
         20 sessions. Trend block (12/36 EMA) is untouched so re-entry after a
         crash stays fast.
idea:    Most large-cap strategies die in 2022 not because firm signals break,
         but because broad-market drawdown drags the full-sample Sharpe
         (volatility inflation + eroded compounding base). A dedicated index
         guard flatens during VN30 downtrends, preserving capital, then lets the
         unchanged trend block re-enter quickly on the recovery. Firm-level
         capex cash-flow discipline still times quality entries.
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

        vn30_return = self.op.fillna(self.op.pct_change(vn30_close, periods=20), value=0)
        index_guard = vn30_return < 0

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