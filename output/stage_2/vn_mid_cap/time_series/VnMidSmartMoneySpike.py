"""
name:    VnMidSmartMoneySpike
summary: Long mid caps after a smart-money volume spike near the limit-up.
idea:    A volume spike above three times the 20-day average with a gain of at
         least 6.8% signals large money finishing accumulation and pushing the
         price. Mid-cap moves without liquidity support often reverse, so the
         spike is only taken inside an existing uptrend.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume

        vol_sma = self.feat.sma(volume, timeperiod=20)
        ema_slow = self.feat.ema(close, timeperiod=30)
        ret_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)

        known = (
            self.op.notna(vol_sma)
            & self.op.notna(ema_slow)
            & (close > 0)
            & (volume > 0)
            & (vol_sma > 0)
        )

        spike = known & (volume > vol_sma * 3.0) & (ret_1 >= 0.068)
        base_long = spike & (close > ema_slow)
        exit_setup = known & (close < ema_slow)

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_long, position=1)