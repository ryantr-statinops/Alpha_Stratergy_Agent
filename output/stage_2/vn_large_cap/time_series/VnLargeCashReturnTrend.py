"""
name:    VnLargeCashReturnTrend
summary: Long large caps with healthy cash return on assets in an 8/24 EMA
         uptrend.
idea:    Cash return on assets (annual CFO over total assets) measures how
         efficiently the asset base turns into cash. Requiring a positive ratio
         and an intact 8/24 EMA uptrend keeps the position in cash-generative
         large caps whose price confirms the quality story.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual
        total_assets = self.data.fun_bs_total_assets_annual

        ema_fast = self.feat.ema(close, timeperiod=8)
        ema_slow = self.feat.ema(close, timeperiod=24)

        cash_return = operating_cash_flow / total_assets
        fundamentals_known = (
            self.op.notna(operating_cash_flow)
            & self.op.notna(total_assets)
            & (total_assets > 0)
            & self.op.notna(cash_return)
        )

        base_entry = fundamentals_known & (cash_return > 0.02) & (close > ema_slow)
        strong_entry = base_entry & (ema_fast > ema_slow)
        exit_setup = (cash_return < 0) | (close < ema_slow)

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)
