"""
name:    T02-D_at10_m3_e26
summary: ATR Trailing Stop + Trend
idea:    Trend following with ATR-based trailing stop and EMA/ADX directional filter.
"""
class CustomStrategy(SimpleAlgorithm):
    atr_window = 10
    atr_mult = 3


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        atr_val = self.feat.atr(high, low, close, timeperiod=self.atr_window)
        ema = self.feat.ema(close, timeperiod=26)
        adx_val = self.feat.adx(high, low, close, timeperiod=10)

        long_setup = (close > ema) & (adx_val > 22) & (close > (close - atr_val * self.atr_mult))
        short_setup = (close < ema) & (adx_val > 22) & (close < (close + atr_val * self.atr_mult))
        exit_setup = self.op.crossed_below(close, ema) | self.op.crossed_above(close, ema)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

