"""
name:    VnLargePullbackQuality
summary: Long cash-generative large caps pulling back to the 24-day EMA within
         an uptrend.
idea:    In a strong large-cap trend, a pullback to the 24-day EMA offers a
         better entry than chasing strength. The position is opened when price
         holds the trend line, annual cash flow is positive and RSI is not
         overbought, and is exited if the trend line breaks.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual

        ema_fast = self.feat.ema(close, timeperiod=8)
        ema_slow = self.feat.ema(close, timeperiod=24)
        rsi = self.feat.rsi(close, timeperiod=7)

        fundamentals_known = self.op.notna(operating_cash_flow)

        base_entry = (
            fundamentals_known
            & (operating_cash_flow > 0)
            & (ema_fast > ema_slow)
            & (close >= ema_slow)
        )
        strong_entry = base_entry & (rsi < 70)
        exit_setup = (close < ema_slow)

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)
