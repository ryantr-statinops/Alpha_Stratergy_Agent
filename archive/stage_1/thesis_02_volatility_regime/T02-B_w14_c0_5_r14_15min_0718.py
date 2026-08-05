"""
name:    T02-B_w14_c0.5_r14
summary: Low Vol Mean Reversion
idea:    Trade mean reversion during volatility compression (ATR < SMA × 0.7) with RSI extremes.
"""
class CustomStrategy(SimpleAlgorithm):
    vol_window = 14


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        atr_val = self.feat.atr(high, low, close, timeperiod=self.vol_window)
        atr_sma = self.feat.sma(atr_val, timeperiod=self.vol_window)
        rsi = self.feat.rsi(close, timeperiod=14)

        vol_compression = atr_val < atr_sma * 0.5

        long_setup = vol_compression & (rsi < 30)
        short_setup = vol_compression & (rsi > 70)
        exit_setup = self.op.crossed_above(rsi, 50) | self.op.crossed_below(rsi, 50)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

