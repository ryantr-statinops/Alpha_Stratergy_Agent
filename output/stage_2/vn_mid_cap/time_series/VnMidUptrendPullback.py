"""
name:    VnMidUptrendPullback
summary: Long mid caps on a 10-15% pullback inside an uptrend.
idea:    Retail-driven mid-cap uptrends pull back sharply (10-15%) before
         resuming. Buying a dip of 10-15% from the 20-day peak while price stays
         above the slow average and RSI is below 45 enters the rebound rather
         than chasing the top. Exit when the uptrend itself breaks.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close

        ema_slow = self.feat.ema(close, timeperiod=30)
        peak_20 = self.feat.rolling_max(close, window=20)
        rsi_val = self.feat.rsi(close, timeperiod=9)

        known = (
            self.op.notna(ema_slow)
            & self.op.notna(peak_20)
            & self.op.notna(rsi_val)
            & (close > 0)
            & (peak_20 > 0)
        )
        drawdown = close / peak_20

        base_long = (
            known
            & (close > ema_slow)
            & (drawdown < 0.90)
            & (drawdown > 0.85)
            & (rsi_val < 45)
        )
        strong_long = base_long & self.op.rising(close, 3)
        exit_setup = known & (close < ema_slow)

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_long, position=0.5)
        self.set_positions(strong_long, position=1)