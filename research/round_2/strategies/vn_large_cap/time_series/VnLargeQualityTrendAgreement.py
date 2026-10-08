"""
name:    VnLargeQualityTrendAgreement
summary: Long large caps with positive cash flow and profit confirmed by both
         8/24 and 12/36 EMA uptrends.
idea:    Multi-horizon trend agreement separates persistent large-cap uptrends
         from short-lived ripples. Requiring both an 8/24 and a 12/36 EMA stack
         to be bullish, on names with positive annual CFO and positive quarterly
         profit, couples business quality to two independent trend horizons;
         exit on the fast-horizon break while the slower regime still holds.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual
        net_profit = self.data.fun_is_net_profit_loss_after_tax_quarterly

        ema_fast_short = self.feat.ema(close, timeperiod=8)
        ema_slow_short = self.feat.ema(close, timeperiod=24)
        ema_fast_long = self.feat.ema(close, timeperiod=12)
        ema_slow_long = self.feat.ema(close, timeperiod=36)

        fundamentals_known = self.op.notna(operating_cash_flow) & self.op.notna(net_profit)

        base_entry = (
            fundamentals_known
            & (operating_cash_flow > 0)
            & (net_profit > 0)
            & (ema_fast_short > ema_slow_short)
            & (ema_fast_long > ema_slow_long)
        )
        strong_entry = base_entry & (close > ema_slow_long)
        exit_setup = (ema_fast_short < ema_slow_short)

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)
