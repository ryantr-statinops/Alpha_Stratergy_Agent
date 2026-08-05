"""
name:    VnLargeCapexDownFlatten
summary: CapexDisciplineTrend baseline plus a per-stock crash guard that
         flattens all positions whenever the stock's own 20-day return drops
         below -10%. The 12/36 EMA trend block is untouched so re-entry after a
         crash stays fast.
idea:    A broad crash (2022) shows up as sharp per-stock drawdowns before the
         slow 36-day EMA rolls over. A dedicated 20-day downside guard flattens
         fast on that crash, protecting the compounding base, while the
         unchanged capex/trend blocks re-enter quickly on recovery. Uses only
         the stock's own price, avoiding reliance on a constant index field.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual
        capex = self.data.fun_cf_purchases_of_fixed_assets_and_other_long_term_assets_annual

        ema_fast = self.feat.ema(close, timeperiod=12)
        ema_slow = self.feat.ema(close, timeperiod=36)

        fundamentals_known = self.op.notna(operating_cash_flow) & self.op.notna(capex)

        stock_return = self.op.fillna(self.op.pct_change(close, periods=20), value=0)
        crash_guard = stock_return < -0.10

        base_entry = (
            fundamentals_known
            & (operating_cash_flow > 0)
            & (capex < operating_cash_flow)
            & (close > ema_slow)
            & (~crash_guard)
        )
        strong_entry = base_entry & (ema_fast > ema_slow)
        exit_setup = (operating_cash_flow < 0) | (capex > operating_cash_flow) | (close < ema_slow) | crash_guard

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)