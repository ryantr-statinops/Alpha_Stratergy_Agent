"""
name:    VnLargeAbnormalVolumeTrend
summary: Long large caps with abnormal volume confirming a positive return,
         in an uptrend.
idea:    Abnormal volume signals investor attention and recognition. When
         elevated participation confirms a positive price move, it suggests
         institutional accumulation rather than distribution. Requiring the
         volume spike to coincide with a positive return filters for
         accumulation-driven advances that tend to continue.
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
            & (return_1 > 0)
            & (close > ema_slow)
        )
        strong_entry = base_entry & (ema_fast > ema_slow)
        exit_setup = (return_1 < 0) | (close < ema_slow)

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)