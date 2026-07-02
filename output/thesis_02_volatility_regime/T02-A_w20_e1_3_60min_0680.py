"""
name:    T02-A_w20_e1.3
summary: Volatility Breakout
idea:    Enter on volatility expansion (ATR > SMA × multiplier) confirmed by ROC and ADX direction.
"""
class CustomStrategy(SimpleAlgorithm):
    vol_window = 20
    thesis_group = "02"

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        atr_val = self.feat.atr(high, low, close, timeperiod=self.vol_window)
        atr_sma = self.feat.sma(atr_val, timeperiod=self.vol_window)
        adx_val = self.feat.adx(high, low, close, timeperiod=21)

        vol_expansion = atr_val > atr_sma * 1.3
        roc_val = self.feat.roc(close, timeperiod=14)

        long_setup = vol_expansion & (roc_val > 0) & (adx_val > 16)
        short_setup = vol_expansion & (roc_val < 0) & (adx_val > 16)
        exit_setup = (atr_val < atr_sma) | self.op.crossed_below(adx_val, 10)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

