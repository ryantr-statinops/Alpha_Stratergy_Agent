"""
name:    VnLargeCfoImprovingTrend
summary: Long large caps where operating cash flow is positive and improving,
         in an uptrend.
idea:    Improving cash flow generation signals a business gaining momentum
         in its core operations. When annual CFO is both positive and rising
         year-over-year, it captures accelerating cash generation quality.
         Combined with price trend, this identifies companies where improving
         fundamentals are beginning to be reflected in price action. The 10/30
         EMA trend provides moderate-speed timing.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual
        total_assets = self.data.fun_bs_total_assets_annual

        ema_fast = self.feat.ema(close, timeperiod=10)
        ema_slow = self.feat.ema(close, timeperiod=30)

        cfo_improvement = self.op.pct_change(operating_cash_flow, periods=1)

        fundamentals_known = (
            self.op.notna(operating_cash_flow)
            & self.op.notna(total_assets)
            & self.op.notna(cfo_improvement)
            & (total_assets > 0)
        )

        base_entry = (
            fundamentals_known
            & (operating_cash_flow > 0)
            & (cfo_improvement > 0)
            & (close > ema_slow)
        )
        strong_entry = base_entry & (ema_fast > ema_slow)
        exit_setup = (
            (operating_cash_flow < 0)
            | (cfo_improvement < 0)
            | (close < ema_slow)
        )

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)
