"""
name:    VnLargeVolumePullbackTrend
summary: Long large caps in an uptrend that pull back on abnormal volume,
         expecting the pressure to reverse.
idea:    A strong stock in an intact uptrend that experiences a sharp,
         volume-heavy decline often suffers temporary selling pressure rather
         than a fundamental deterioration. When volume spikes coincide with a
         negative return but the longer-term trend remains intact, the move
         may be flow-driven and mean to revert. Buying these dips within an
         uptrend exploits short-term oversold conditions.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume

        ema_fast = self.feat.ema(close, timeperiod=8)
        ema_slow = self.feat.ema(close, timeperiod=24)
        vol_base = self.feat.sma(volume, timeperiod=20)

        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)

        base_entry = (
            (volume > vol_base)
            & (return_1 < 0)
            & (close > ema_slow)
        )
        strong_entry = base_entry & (ema_fast > ema_slow)
        exit_setup = (close < ema_slow)

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)