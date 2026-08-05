"""
name:    VnLargeCfoSurpriseTrend
summary: Long large caps reporting positive year-over-year growth in
         quarterly operating cash flow, in an uptrend.
idea:    Operating cash flow surprises diffuse more slowly into prices than
         earnings surprises because they receive less analyst attention.
         A positive year-over-year CFO change signals improving underlying
         cash generation. Combined with an uptrend, this captures the
         delayed market reaction to cash flow news.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        operating_cash_flow_q = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_quarterly

        ema_fast = self.feat.ema(close, timeperiod=8)
        ema_slow = self.feat.ema(close, timeperiod=24)

        cfo_growth = self.op.pct_change(operating_cash_flow_q, periods=1)

        fundamentals_known = (
            self.op.notna(operating_cash_flow_q)
            & self.op.notna(cfo_growth)
            & (operating_cash_flow_q > 0)
        )

        base_entry = (
            fundamentals_known
            & (cfo_growth > 0)
            & (close > ema_slow)
        )
        strong_entry = base_entry & (ema_fast > ema_slow)
        exit_setup = (
            (operating_cash_flow_q < 0)
            | (cfo_growth < 0)
            | (close < ema_slow)
        )

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)