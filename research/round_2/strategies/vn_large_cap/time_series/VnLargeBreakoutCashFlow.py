"""
name:    VnLargeBreakoutCashFlow
summary: Long large caps breaking out on volume with positive annual cash flow.
idea:    Retail herding makes breakouts on real volume carry on for several
         sessions, so entering a large cap that clears its trend with
         above-average turnover captures the continuation. The annual CFO
         filter keeps the long on cash-generative names, and a trend break
         exits quickly.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual

        ema_fast = self.feat.ema(close, timeperiod=8)
        ema_slow = self.feat.ema(close, timeperiod=24)
        vol_base = self.feat.sma(volume, timeperiod=20)

        fundamentals_known = self.op.notna(operating_cash_flow)

        base_entry = (
            fundamentals_known
            & (operating_cash_flow > 0)
            & (close > ema_slow)
            & (ema_fast > ema_slow)
        )
        strong_entry = base_entry & (volume > vol_base * 1.5)
        exit_setup = (close < ema_slow)

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)
