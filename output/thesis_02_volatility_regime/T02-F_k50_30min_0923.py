"""
name:    T02-F_k50
summary: KAMA Trend
idea:    Adaptive trend following with Kaufman MA and ADX confirmation; exit on trend loss.
"""
class CustomStrategy(SimpleAlgorithm):
    kama_window = 50
    thesis_group = "02"

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        kama = self.feat.kama(close, timeperiod=self.kama_window)
        adx_val = self.feat.adx(high, low, close, timeperiod=14)

        long_setup = (close > kama) & (adx_val > 18)
        short_setup = (close < kama) & (adx_val > 18)
        exit_setup = self.op.crossed_below(close, kama) | self.op.crossed_above(close, kama) | (adx_val < 12)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

