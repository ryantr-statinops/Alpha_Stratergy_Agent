"""
name:    VnLargeCashFlowVolume
summary: Long large caps with positive annual cash flow in a 12/36 EMA uptrend
         with stable volume participation.
idea:    Positive operating cash flow screens for quality, while the slower
         12/36 EMA pair filters for a durable trend. Doubling the position only
         when turnover clears its 20-day base ensures the rally has real
         participation behind it rather than a thin, speculative drift.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual

        ema_fast = self.feat.ema(close, timeperiod=12)
        ema_slow = self.feat.ema(close, timeperiod=36)
        vol_base = self.feat.sma(volume, timeperiod=20)

        fundamentals_known = self.op.notna(operating_cash_flow)

        base_entry = fundamentals_known & (operating_cash_flow > 0) & (ema_fast > ema_slow)
        strong_entry = base_entry & (volume > vol_base)
        exit_setup = (operating_cash_flow < 0) | (ema_fast < ema_slow)

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)
